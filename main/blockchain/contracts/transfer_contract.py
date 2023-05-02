from pyteal import *


def transfer_title(approver, new_owner):
    on_creation = Seq([
        App.globalPut(Bytes("approver"), approver),
        App.globalPut(Bytes("new_owner"), new_owner),
        Return(Int(1))
    ])

    is_approver = Txn.sender() == App.globalGet(Bytes("approver"))
    is_new_owner = Txn.sender() == App.globalGet(Bytes("new_owner"))

    on_closeout = If(
        is_approver,
        Return(Int(1)),
        Return(Int(0))
    )

    on_transfer = Seq([
        Assert(is_approver),
        App.globalPut(Bytes("new_owner"), Txn.application_args[0]),
        Return(Int(1))
    ])

    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.DeleteApplication, on_closeout],
        [Txn.application_args.length() == Int(1), on_transfer]
    )

    return program