from algosdk import account, mnemonic
from algosdk.constants import microalgos_to_algos_ratio
from algosdk.v2client import algod, indexer
from fastapi import FastAPI

app = FastAPI()


def algod_client():
    algod_address = "http://localhost:4001"
    indexer_client = indexer.IndexerClient("", "http://localhost:8980")
    algod_token = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    headers = {
        "X-API-Key": algod_token,
    }
    return algod.AlgodClient(algod_token, algod_address, headers)


@app.get("/account")
def create_account():
    private_key, address = account.generate_account()
    passphrase = mnemonic.from_private_key(private_key)
    return {"address": address, "passphrase": passphrase}


@app.get("/account/{Address}")
def get_account_info(Address: str):
    info = algod_client.account_info(Address)
    return {"Address": info}


def get_balance(address):
    account_info = algod_client().account_info(address)
    balance = account_info.get('amount') / microalgos_to_algos_ratio
    return balance
