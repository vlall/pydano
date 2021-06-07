import cardano_wrapper.utils

# from cardano_wrapper.wrappers.AddressWrap import AddressWrap
from cardano_wrapper.wrappers.WalletWrap import WalletWrap
import os
import requests
import json
import time
import pprint

"""
This is a test script with implements the functionality of 
the Python WalletWrap object.
"""
pp = pprint.PrettyPrinter(indent=4)
wallet = WalletWrap()
wallet_type = "shelley"

walletList = wallet.list_wallets(wallet_type)
pp.pprint(walletList)
wallet_id = walletList[0]["id"]

# # Takes time for the wallet/address to sync if we want to be able to test transaction creation.
addresses = wallet.list_addresses(wallet_type, wallet_id)
# pp.pprint(addresses)
from_address = addresses[0]["id"]
to_address = addresses[1]["id"]
print(from_address)
print(to_address)
