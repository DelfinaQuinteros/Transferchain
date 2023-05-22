from datetime import datetime
from hashlib import sha256
import bcrypt as bcrypt
from algosdk import account, mnemonic, encoding
from flask import request, jsonify, Blueprint
import jwt
from pyteal import Mode, compileTeal

from main.blockchain.algorand import send_algorand_txn, sign_algorand_txn, create_algorand_txn
from main.models import User, Transfer, Certificate, Cars
from main.repositories import UserRepository, TransferRepository, CertificateRepository, CarsRepository
from main import db
from algosdk import transaction, mnemonic
from algosdk.v2client import algod

transfer = Blueprint('transfer', __name__)

transfer_repo = TransferRepository()
car_repo = CarsRepository()

algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "TnqYtzsJKK1DS3TLNWDJ29wZEex8Y3iy5kNjhrx6"
headers = {
    "X-API-Key": algod_token,
}
algod_client = algod.AlgodClient(algod_token, algod_address, headers)

sender_address = 'U3HODHJAAG5O42JSBEU3BR65DVMIWRAQXBDEAAB7AC5G2CFCLO6DBCEEJM'
sender_mnemonic = 'boy sword kiwi wasp federal puzzle flash add bargain just traffic glass whale garment any timber plunge reveal govern flavor spend release under abstract thrive'
sender_sk = 'FF7tCzpzXBZWno4x45XNUrGMjitQS8h0pKTGKJOfBqrZzjubA0L6EsCzd638s2u5Sod0oZ14yOkSPZ1LVrGlhw=='
receiver_address = "WGJ6RVG3TLWQ7L3K233A7HJT7ZYN34G2Y7KVTJIGANIBARJJSV7CNG4E4E"

# Realiza un POST al contrato inteligente
car_owner = "WGJ6RVG3TLWQ7L3K233A7HJT7ZYN34G2Y7KVTJIGANIBARJJSV7CNG4E4E"
car_brand = "Tesla"
car_model = "Model 3"
car_year = 2022


# Compila el contrato y obtén su código TEAL
def compile_contract():
    contract_teal_code = ("""
    // Definir las variables del contrato
    bytes owner
    bytes brand
    bytes model
    int year
    
    // Verificar los datos
    // Compara los datos recibidos con los almacenados en el contrato
    int verifyData:
        owner = Txn.application_args[0]
        brand = Txn.application_args[1]
        model = Txn.application_args[2]
        year = Txn.application_args[3]
        
        // Verificar que los datos sean correctos
        return Cond(
            // Comparar los datos con los almacenados en el contrato
            And(
                BytesEq(owner, App.localGet(Int(0))),
                BytesEq(brand, App.localGet(Int(1))),
                BytesEq(model, App.localGet(Int(2))),
                Eq(year, App.localGet(Int(3)))
            ),
            // Si los datos coinciden, devuelve 1 (verificación exitosa)
            Int(1),
            // Si los datos no coinciden, devuelve 0 (verificación fallida)
            Int(0)
        )
        
    // Lógica de ejecución del contrato
    // El contrato solo acepta transacciones con la operación "ApplicationCall"
    // y verifica los datos utilizando la función "verifyData"
    txn_accept:
        // Verificar que la operación sea "ApplicationCall"
        is_app_call = Txn.application_id != Int(0)
        // Verificar los datos llamando a la función "verifyData"
        data_verified = App.localPut(Int(0), App.localGetEx(Int(0)), Txn.application_args[0]) &&
                        App.localPut(Int(1), App.localGetEx(Int(1)), Txn.application_args[1]) &&
                        App.localPut(Int(2), App.localGetEx(Int(2)), Txn.application_args[2]) &&
                        App.localPut(Int(3), App.localGetEx(Int(3)), Txn.application_args[3]) &&
                        App.localPut(Int(4), App.localGetEx(Int(4)), App.localGet(Int(4)) + Int(1))
        
        // Aceptar la transacción solo si la operación es "ApplicationCall"
        // y los datos son verificados correctamente
        return And(is_app_call, data_verified)
        
    // Programa principal del contrato
    main:
        // Ejecutar la lógica de ejecución del contrato
        return txn_accept
    """)
    contract_teal_bytes = contract_teal_code.encode()
    return contract_teal_bytes


# Crea una transacción de despliegue del contrato
txn = transaction.ApplicationCreateTxn(
    sender=sender_address,
    sp=transaction.SuggestedParams(
        fee=1000,
        first=algod_client.status().get('last-round') + 1,
        last=algod_client.status().get('last-round') + 1000,
        gen='testnet-v1.0',
        flat_fee=True,
        gh='SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI='
    ),
    on_complete=transaction.OnComplete.NoOpOC,
    approval_program=compile_contract(),
    clear_program=b'ASABASI=',
    global_schema=transaction.StateSchema(0, 0),
    local_schema=transaction.StateSchema(5, 5),
)

# Firmar la transacción con la clave privada de la cuenta
signed_txn = txn.sign(sender_sk)

# Enviar la transacción a la red de Algorand
txid = algod_client.send_transaction(signed_txn)
print(f"Contract deployment transaction ID: {txid}")

# Esperar a que la transacción se confirme en la cadena de bloques
confirmed_txn = algod_client.pending_transaction_info(txid)
while not confirmed_txn.get('confirmed-round'):
    confirmed_txn = algod_client.pending_transaction_info(txid)
print("Contract deployed successfully!")


# Crea una transacción de aplicación para el POST
txn = transaction.ApplicationCallTxn(
    sender=car_owner,
    sp=transaction.SuggestedParams(
        fee=1000,
        first=algod_client.status().get('last-round') + 1,
        last=algod_client.status().get('last-round') + 1000,
        gen='testnet-v1.0',
        flat_fee=True
    ),
    index=1,  # Índice del contrato desplegado
    on_complete=transaction.OnComplete.NoOpOC,
    app_args=[
        encoding.decode_address(car_owner),
        car_brand.encode(),
        car_model.encode(),
        car_year.to_bytes(8, 'big')
    ],
)

signed_txn = txn.sign(sender_sk)
txid = algod_client.send_transaction(signed_txn)
confirmed_txn = algod_client.pending_transaction_info(txid)
while not confirmed_txn.get('confirmed-round'):
    confirmed_txn = algod_client.pending_transaction_info(txid)
print("POST transaction executed successfully!")
