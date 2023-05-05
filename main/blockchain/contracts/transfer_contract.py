from algosdk import account, encoding, transaction, mnemonic
from algosdk.transaction import PaymentTxn, wait_for_confirmation
from algosdk.v2client import algod
from solcx import compile_standard, install_solc
from pyteal import *

# Definir el código fuente del contrato
contract_source_code = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;


contract CarOwnership {
    struct Car {
        address owner;
        string brand;
        string model;
        uint256 year;
    }
    
    mapping(uint256 => Car) private cars;
    
    event Transfer(uint256 indexed carId, address indexed previousOwner, address indexed newOwner);
    
    function registerCar(uint256 carId, string memory brand, string memory model, uint256 year) public {
        require(cars[carId].owner == address(0), "Car already registered");
        cars[carId] = Car(msg.sender, brand, model, year);
    }
    
    function transferOwnership(uint256 carId, address newOwner) public {
        require(cars[carId].owner == msg.sender, "Only the owner can transfer ownership");
        cars[carId].owner = newOwner;
        emit Transfer(carId, msg.sender, newOwner);
    }
    
    function getCar(uint256 carId) public view returns (address owner, string memory brand, string memory model, uint256 year) {
        owner = cars[carId].owner;
        brand = cars[carId].brand;
        model = cars[carId].model;
        year = cars[carId].year;
    }
}
"""

# Compilar el contrato
install_solc("0.8.0")
compiled_contract = compile_standard(
    {
        "language": "Solidity",
        "sources": {"CarOwnership.sol": {"content": contract_source_code}},
        "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}},
    },
    solc_version="0.8.0",

)
print(compiled_contract)

# Obtener el ABI y el bytecode del contrato compilado
abi = compiled_contract["contracts"]["CarOwnership.sol"]["CarOwnership"]["abi"]
bytecode = compiled_contract["contracts"]["CarOwnership.sol"]["CarOwnership"]["evm"]["bytecode"]["object"]

# Conexion con la red algorand
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


def sign_transaction(txn_dict, private_key):
    txn = transaction.Transaction(**txn_dict)
    signed_txn = txn.sign(private_key)
    return signed_txn


def sign_algorand_txn(txn, sender_mnemonic):
    sender_private_key = mnemonic.to_private_key(sender_mnemonic)
    signed_txn = txn.sign(sender_private_key)
    return signed_txn


def create_algorand_txn(sender_address, recipient_address):
    params = algod_client.suggested_params()
    txn = transaction.PaymentTxn(sender_address, params, recipient_address, 0, None, params.fee)
    return txn


def send_algorand_txn(signed_txn):
    txid = algod_client.send_transaction(signed_txn)
    return txid


# Crear una transacción de transferencia de Algos

params = algod_client.suggested_params()
algo_txn = create_algorand_txn(sender_address, receiver_address)
signed_txn = sign_algorand_txn(algo_txn, sender_mnemonic)

# Enviar la transacción a la red Algorand
txid = send_algorand_txn(signed_txn)
print(txid)

# Escribir el código del contrato en lenguaje Algorand TEAL
teal_code = Cond(
    [Txn.application_id() == Int(0), Seq([
        App.localPut(Int(0), Bytes("sender"), Txn.sender()),
        App.localPut(Int(0), Bytes("receiver"), Btoi(Txn.application_args[0])),
        App.localPut(Int(0), Bytes("car_id"), Btoi(Txn.application_args[1])),
        App.localPut(Int(0), Bytes("approved"), Int(0)),
        Int(1)
    ])],
    [And(Txn.application_id() == Int(0),
         App.localGet(Int(0), Bytes("approved")) == Int(0),
         Txn.sender() == App.localGet(Int(0), Bytes("receiver")),
         App.localGet(Int(0), Bytes("car_id")) == Btoi(Txn.application_args[1])), Seq([
        App.localPut(Int(0), Bytes("approved"), Int(1)),
        Int(1)
    ])],
    [And(Txn.application_id() == Int(0),
         App.localGet(Int(0), Bytes("approved")) == Int(1),
         Txn.sender() == App.globalGet(Bytes("admin")),
         Txn.application_args[0] == Bytes("save_transfer")), Seq([
        App.globalPut(Bytes("last_transfer_id"), App.globalGet(Bytes("last_transfer_id")) + Int(1)),
        App.localPut(Int(0), Bytes("approved"), Int(0)),
        App.localPut(Int(0), Bytes("transfer_id"), App.globalGet(Bytes("last_transfer_id"))),
        App.localPut(Int(0), Bytes("timestamp"), Global.latest_timestamp()),
        App.localPut(Int(0), Bytes("hash"), Txn.application_args[1]),
        Int(1)
    ])],
    [And(Txn.application_id() == Int(0),
         Txn.application_args[0] == Bytes("set_admin")), Seq([
        App.globalPut(Bytes("admin"), Txn.application_args[1]),
        Int(1)
    ])],
    [Txn.application_id() == Int(0), Int(1)]
)

# Compilar el contrato TEAL
compiled_teal = compileTeal(teal_code, Mode.Application)
