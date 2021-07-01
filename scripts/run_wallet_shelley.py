import pydano.utils
from pydano.wrappers.WalletWrap import WalletWrap
import os
import time
import pprint

"""
This is a test script with implements the functionality of 
the Python WalletWrap object.
"""
pp = pprint.PrettyPrinter(indent=4)
wallet = WalletWrap("../config.yaml")
wallet_type = "shelley"
wallet_name = "My Favorite Wallet- 6/15/21"
passphrase = "phrase1234$$$$$"
mnemonic = (
    "drink quality cage chunk field air govern wash sunny monster answer quick unaware flip believe suspect brave response syrup night tape crime various utility"
).split()
print(wallet.create_wallet(wallet_type, wallet_name, passphrase, mnemonic))
walletList = wallet.list_wallets(wallet_type)
pp.pprint(walletList)
wallet_id = walletList[0]["id"]
# TODO: Construct Address
addresses = wallet.list_addresses(wallet_type, wallet_id)
pp.pprint(addresses)
from_address = addresses[0]["id"]
to_address = addresses[1]["id"]
print(from_address)
print(to_address)
