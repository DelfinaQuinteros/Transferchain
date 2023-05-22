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


def contract(current_owner: User, new_owner: User, car: Cars):
    contract = pyteal.compileTeal(pyteal.App(
        pyteal.If(
            pyteal.And(
                pyteal.Txn.sender() == pyteal.Addr(current_owner.algorand_address),
                pyteal.Txn.asset_sender() == pyteal.Addr(current_owner.algorand_address),
                pyteal.Txn.asset_receiver() == pyteal.Addr(new_owner.algorand_address),
                pyteal.Txn.asset_amount() == pyteal.Int(1)
            ),
            pyteal.Seq(
                pyteal.Assert(
                    pyteal.Global.group_size() == pyteal.Int(1)
                ),
                pyteal.App.localPut(
                    pyteal.Bytes("sender"),
                    pyteal.App.optIn(
                        pyteal.Bytes("autos_" + str(current_owner.id)),
                        on_completion=pyteal.OnComplete.NoOp
                    ).asset_close_to()
                ),
                pyteal.App.localPut(
                    pyteal.Bytes("recipient"),
                    pyteal.App.optIn(
                        pyteal.Bytes("autos_" + str(new_owner.id)),
                        on_completion=pyteal.OnComplete.NoOp
                    ).asset_acceptance()
                ),
                pyteal.App.localPut(
                    pyteal.Bytes("timestamp"),
                    pyteal.Global.latest_timestamp()
                ),
                pyteal.Assert(
                    pyteal.App.localGet(pyteal.Bytes("sender"), pyteal.Bytes("count")) == pyteal.Int(0)
                ),
                pyteal.App.localPut(
                    pyteal.Bytes("sender"),
                    pyteal.Int(1)
                ),
                pyteal.Assert(
                    pyteal.App.globalGet(pyteal.Bytes("AssetID")) == pyteal.Int(car.asset_id)
                ),
                pyteal.Assert(
                    pyteal.App.globalGet(pyteal.Bytes("AppID")) == pyteal.Int(car.app_id)
                ),
                pyteal.App.localPut(
                    pyteal.Bytes("sender"),
                    pyteal.Global.latest_timestamp()
                ),
                pyteal.App.localPut(
                    pyteal.Bytes("recipient"),
                    pyteal.Global.latest_timestamp()
                ),
                pyteal.Return(pyteal.Int(1))
            )
        )
    ))
    return contract