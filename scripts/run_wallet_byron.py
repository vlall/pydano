import cardano_wrapper.utils
from pydano.wrappers.AddressWrap import AddressWrap
from pydano.wrappers.WalletWrap import WalletWrap
import os
import requests
import json
import time

"""
This is a test script with implements the functionality of 
the Python WalletWrap object.
"""
wallet = WalletWrap()
wallet_type = "byron"
wallet_name = "This is a wallet that will test the defrag script"
passphrase = "d9c9f9g9g9125"
mnemonic = (
    "waste child document prosper law wink push fortune material bleak rough actor"
).split()
print(wallet.create_wallet(wallet_type, wallet_name, passphrase, mnemonic))
walletList = wallet.list_wallets(wallet_type)
print(walletList)
wallet_id = walletList[0]["id"]
print(wallet.create_address(wallet_type, wallet_id, passphrase, 2147483648))
# Creates 37btjrVyb4KBLpM7L1vGf1cxhoKN4qTTYBHeAPKDsk2SeHqgmsqetncbu63bCB71UPsGeHLQXazyLUrfn926p5TQmH2eoKXinyGV43ubsriU4iGWvn

print(wallet.create_address(wallet_type, wallet_id, passphrase, 2147483649))
# Creates 37btjrVyb4KE6VsJRGRjiGNzuX3jr68AGLtjg8zKsspVh27yFqzKQ9Pwa36EJZoCvwnDWbRJq1NSBwwTDmMT8NnXVnFt8FiiNXrXkoE79W1e2rrfzZ

# Takes time for the wallet/address to sync if we want to be able to test transaction creation.
addresses = wallet.list_addresses(wallet_type, wallet_id)
from_address = addresses[0]["id"]
to_address = addresses[1]["id"]
print(from_address)
print(to_address)
