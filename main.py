# -*- coding: utf-8 -*-
import os
import json
from random import randint
from mnemonic import Mnemonic
from eth_account import Account
from DB_HANDLER import DATABASE

def generate_mnemonic():
    mnemo = Mnemonic("english")
    mnemonic_phrase = mnemo.generate(strength = 256)
    return mnemonic_phrase

def mnemonic_to_seed(mnemonic_phrase: list, passphrase = ""):
    mnemo = Mnemonic("english")
    seed = mnemo.to_seed(mnemonic_phrase, passphrase = passphrase)
    return seed

def generate_wallet(passphrase = ""):
    mnemonic_phrase = generate_mnemonic()
    
    seed = mnemonic_to_seed(mnemonic_phrase, passphrase = passphrase)
    
    Account.enable_unaudited_hdwallet_features()
    account = Account.from_key(seed[:32])
    
    wallet_address = account.address
    private_key = account.key.hex()

    public_key = account._key_obj.public_key.to_hex()
    
    return {
        "wallet_address": wallet_address,
        "private_key": private_key,
        "public_key": public_key,
        "mnemonic_phrase": mnemonic_phrase
    }

if __name__ == "__main__":
    passphrase = ""
    for i in range(100):
        wallet = generate_wallet(passphrase = passphrase)

        DB: str = database(
            filename = "WALLETS"
        ).get_connection()
        CURSOR: str = DB.cursor()

        CURSOR.execute(f"INSERT INTO WALLETS VALUES(?,?,?,?)", (wallet["wallet_address"], wallet["public_key"], wallet["private_key"], wallet["mnemonic_phrase"]));DB.commit()
