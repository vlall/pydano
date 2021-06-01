import cardano_wrapper.utils
from cardano_wrapper.wrappers.AddressWrap import AddressWrap
from cardano_wrapper.wrappers.WalletWrap import WalletWrap
import os
import requests
import json
import time

"""
This is a test script with implements the functionality of 
the Python WalletWrap object.
"""
wallet = WalletWrap()
wallet_type = "shelley"
wallet_name = "test wallet shelley"
passphrase = "test1234"
mnemonic = (
    "plunge rain hurry crash citizen fish frozen ginger tiny garlic pond diagram enough leaf subway maid toddler extend cry sure still horror pull brass"
).split()
print(wallet.create_wallet(wallet_type, wallet_name, passphrase, mnemonic))
walletList = wallet.list_wallets(wallet_type)
print(walletList)
wallet_id = walletList[0]["id"]
print(wallet.create_address(wallet_type, wallet_id, passphrase, 2147483648))

# print(wallet.create_address(wallet_type, wallet_id, passphrase, 2147483649))

# Takes time for the wallet/address to sync if we want to be able to test transaction creation.
addresses = wallet.list_addresses(wallet_type, wallet_id)
from_address = addresses[0]["id"]
# to_address = addresses[1]["id"]
print(from_address)
# print(to_address)
