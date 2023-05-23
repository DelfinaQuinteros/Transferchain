from algosdk import transaction, mnemonic
from algosdk.v2client import algod
import pyteal
from pyteal import Seq, Txn, Int
from pyteal.ast import abi

from main.models import User, Cars

algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "TnqYtzsJKK1DS3TLNWDJ29wZEex8Y3iy5kNjhrx6"
headers = {
    "X-API-Key": algod_token,
}
algod_client = algod.AlgodClient(algod_token, algod_address, headers)


def create_algorand_txn(sender_address, recipient_address):
    params = algod_client.suggested_params()
    txn = transaction.PaymentTxn(sender_address, params, recipient_address, 0, None, params.fee)
    return txn


def sign_algorand_txn(txn, sender_mnemonic):
    sender_private_key = mnemonic.to_private_key(sender_mnemonic)
    signed_txn = txn.sign(sender_private_key)
    return signed_txn


def send_algorand_txn(signed_txn):
    txid = algod_client.send_transaction(signed_txn)
    return txid


def contract():
    contract_teal_code = ("""
     // Definir las variables del contrato
     bytes user.id
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