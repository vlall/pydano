import json
import os
import subprocess
import sys
import multiprocessing.dummy as mp
import multiprocessing
import time
import random
import concurrent.futures
import json
from datetime import datetime


class CLIWrap(object):
    # TODO: Complete Wrapping.

    PATH = path.join(path.dirname(__file__), "../bin/")

    def __init__(
        self,
        network_type,
        network_id,
    ):
        self.path = path
        self.network_type = network_type
        self.network_id = network_id

    def get_protocol(self):
        cmd = (
            f"{CLIWrap.PATH}./cardano-cli query protocol-parameters "
            "{self.network_type} {self.network_id} "
            "--out-file protocol.json"
        )
        output = subprocess.run(cmd.split(), capture_output=True)
        return output.stdout.rstrip()

    def query_utxo(self):
        """ 
        Example:
            ./cardano-cli query utxo \
            --address $(cat pay.addr) \
            --testnet-magic 1097911063
        """
        pass

    def build_transaction(self, txin, txout, invalid_hereafter, fee, out_file):
        """
        Example:
            ./cardano-cli transaction build-raw \
            --tx-in 53cc31d5575b7096f11b9830da1efea485c887f37cc5743bf4673686cad2f36d#0 \
            --tx-out addr_test1vpkhrv7856jekfshnf5v0ymjjsd5w7nyuxfn73e9h4xkfgqcfynk4+10000000 \
            --tx-out addr_test1vzy3kc8ja0wyhwtjsm0q90g5pryq25gshjzt4r24gkzkzvcw5uc3c+989825743 \
            --invalid-hereafter 25820928 \
            --fee 174257 \
            --out-file tx2.raw
        """

    def send_transaction(self):
        pass

    def query_tip(self):
        """
        Example:
            ./cardano-cli query tip --testnet-magic 1097911063
        """
        pass

    def sign(self):
        """
        Example: 
            ./cardano-cli transaction sign \
            --tx-body-file tx2.raw \
            --signing-key-file pay.skey \
            --testnet-magic 1097911063 \
            --out-file tx2.signed
        """
        pass

    def submit(self):
        """
        Example:
            ./cardano-cli transaction submit \
            --tx-file tx2.signed \
            --testnet-magic 1097911063 
        """
        pass
