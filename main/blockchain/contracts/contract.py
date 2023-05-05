import pyteal
from algosdk import account, encoding, transaction, algod
from algosdk.v2client import algod as algod2
from main.models import User, Cars, Transfer, Certificate
from datetime import datetime
from main import db

from main.resources.cars import algod_client


def transfer_car(current_owner: User, new_owner: User, car: Cars):
    # Crear instancia de la clase Transaction
    txn = transaction.Transaction(
        sender=current_owner.algorand_address,
        receiver=new_owner.algorand_address,
        amt=0,
        note="Transferencia de propiedad de automóvil",
        fee=1000,
        flat_fee=True
    )

    # Crear contrato inteligente utilizando la biblioteca pyteal
    contract = pyteal.compileTeal(pyteal.Program(
        pyteal.If(
            pyteal.And(
                pyteal.Txn.sender() == pyteal.Addr(current_owner.algorand_address),
                pyteal.Txna.asset_sender() == pyteal.Addr(current_owner.algorand_address),
                pyteal.Txna.asset_receiver() == pyteal.Addr(new_owner.algorand_address),
                pyteal.Txna.asset_amount() == pyteal.Int(1)
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
                    pyteal.Int(1),
                    action=pyteal.App.localPutAction.Add
                ),
                pyteal.Assert(
                    pyteal.App.globalGet(pyteal.Bytes("AssetID")) == pyteal.Int(car.asset_id)
                ),
                pyteal.Assert(
                    pyteal.App.globalGet(pyteal.Bytes("AppID")) == pyteal.Int(car.app_id)
                ),
                pyteal.App.localPut(
                    pyteal.Bytes("sender"),
                    pyteal.Global.latest_timestamp(),
                    action=pyteal.App.localPutAction.Replace
                ),
                pyteal.App.localPut(
                    pyteal.Bytes("recipient"),
                    pyteal.Global.latest_timestamp(),
                    action=pyteal.App.localPutAction.Replace
                ),
                pyteal.Return(pyteal.Int(1))
            )
        )
    ))

    # Obtener el id del app
    app_info = algod_client.application_info(car.app_id)
    app_id = app_info["params"]["application-id"]

    # Obtener el id del activo
    asset_id = car.asset_id

    # Firmar la transacción
    signed_txn = txn.sign(current_owner.private_key)

    # Enviar la transacción y el contrato inteligente
    tx_confirm = algod_client.send_transactions([signed_txn], [contract], app_id=app_id, asset_id=asset_id)

    # Guardar la transferencia en la base de datos
    new_transfer = Transfer(
        sender=current_owner,
        recipient=new_owner,
        car=car,
        timestamp=datetime.now()
    )
    db.session.add(new_transfer)
    db.session.commit()

    return tx_confirm