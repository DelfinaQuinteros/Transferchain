from algosdk import transaction, mnemonic
from algosdk.v2client import algod

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
