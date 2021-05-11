import cardano_wrapper.utils
from cardano_wrapper.wrappers.AddressWrap import AddressWrap
from cardano_wrapper.wrappers.WalletWrap import WalletWrap
import os
import requests
import json
import time


wallet = WalletWrap()
wallet_type = "byron"
wallet_name = "This is a wallet that will test the defrag script"
passphrase = "d9c9f9g9"
mnemonic = AddressWrap().mnemonic(12)
w = wallet.create_wallet(wallet_type, wallet_name, passphrase, mnemonic)
print(w)