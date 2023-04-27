from pyteal import *

handle_creation = Seq(
    App.globalPut(Bytes("Creator"), Int(0),
                  Approve())
)

router = Router("Transferchain", BareCallActions(no_op=OnCompleteAction.create_only(handle_creation),
                                                 ),
                )
