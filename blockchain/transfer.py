from algosdk import account, encoding, algod, transaction
from pyteal import compileTeal, Mode


class Transfer:
    def __init__(self, algod_client, contract_path):
        self.algod_client = algod_client
        self.contract_path = contract_path
        self.contract_address = None

    def create_account(self):
        private_key, address = account.generate_account()
        return private_key, address

    def compile_contract(self):
        with open(self.contract_path) as f:
            contract_code = f.read()
        return compileTeal(contract_code, mode=Mode.Application)

    def deploy_contract(self, private_key):
        contract = self.compile_contract()
        params = self.algod_client.suggested_params()
        txn = transaction.ApplicationCreateTxn(
            account.address_from_private_key(private_key),
            params,
            on_complete=transaction.OnComplete.NoOpOC,
            approval_program=contract,
            clear_program=b"",
        )
        signed_txn = txn.sign(private_key)
        tx_id = self.algod_client.send_transaction(signed_txn)
        result = self.algod_client.status_after_block(txn.last_valid())
        self.contract_address = result["created_applications"][0]

    def send_transaction(self, sender_private_key, receiver_address, asset_id):
        params = self.algod_client.suggested_params()
        txn = transaction.ApplicationNoOpTxn(
            account.address_from_private_key(sender_private_key),
            params,
            self.contract_address,
            [bytes(receiver_address, "utf-8"), asset_id],
        )
        signed_txn = txn.sign(sender_private_key)
        tx_id = self.algod_client.send_transaction(signed_txn)
        result = self.algod_client.status_after_block(txn.last_valid())
        return result["application_results"][0]["result"] == "int 1"
