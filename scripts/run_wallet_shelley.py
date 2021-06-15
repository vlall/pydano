import pydano.utils

# from cardano_wrapper.wrappers.AddressWrap import AddressWrap
from pydano.wrappers.WalletWrap import WalletWrap
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
wallet = WalletWrap("../conf.yaml")
wallet_type = "shelley"
# # start
# wallet_name = "Shelley 6/1/21"
# passphrase = "d7c7f3g3gx"
# mnemonic = (
#     "parade inmate track private stove leaf mystery letter detect drum galaxy party december unlock victory sponsor action buzz mention fade addict custom ring toilet"
# ).split()
# print(wallet.create_wallet(wallet_type, wallet_name, passphrase, mnemonic))
walletList = wallet.list_wallets(wallet_type)
pp.pprint(walletList)
wallet_id = walletList[0]["id"]
# print(wallet.create_address(wallet_type, wallet_id, passphrase, 2147483648))
# end

# print(wallet.create_address(wallet_type, wallet_id, passphrase, 2147483649))

# # Takes time for the wallet/address to sync if we want to be able to test transaction creation.
addresses = wallet.list_addresses(wallet_type, wallet_id)
# pp.pprint(addresses)
from_address = addresses[0]["id"]
to_address = addresses[1]["id"]
print(from_address)
print(to_address)
