from pyteal import *


def token_transfer(receiver):
    on_creation = Seq([
        App.localPut(Int(0), Bytes("receiver"), Addr(receiver)),
        App.localPut(Int(0), Bytes("balance"), Int(0))
    ])

    is_sender = Txn.sender() == App.localGet(Int(0), Bytes("sender"))
    has_balance = App.localGet(Int(0), Bytes("balance")) >= Int(1)

    on_closeout = Return(Int(1))

    on_transfer = Seq([
        Assert(is_sender),
        App.localPut(Int(0), Bytes("balance"), App.localGet(Int(0), Bytes("balance")) - Int(1)),
        App.localPut(Int(0), Bytes("balance"), App.localGet(Int(0), Bytes("balance"), Txn.receiver()) + Int(1))
    ])

    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.DeleteApplication, on_closeout],
        [Txn.application_args[0] == Bytes("transfer"), on_transfer]
    )

    return program
