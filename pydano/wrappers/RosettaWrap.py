import json
import time
from os import path
import requests
import yaml
import subprocess
from pydano.wrappers.AddressWrap import AddressWrap
from pydano.utils import bcolors


class RosettaWrap(object):
    def __init__(self, conf_path):
        """This object wraps the Cardano Wallet API so that we can use Python functionality
        to recieve and send API endpoint requests.
        """
        self.headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
        }
        self.setup(conf_path)

    def setup(self, conf_path):
        with open(conf_path, "r") as stream:
            conf = yaml.safe_load(stream)
        self.server = conf.get("rosetta_server")
        if not self.server:
            raise ValueError(
                f"{bcolors.WARNING}Define server in `{file}`.{bcolors.ENDC}"
            )

    def network_status(self, network_id):
        payload = {
            "network_identifier": {"blockchain": "cardano", "network": network_id},
            "metadata": {},
        }
        r = requests.post(
            f"{self.server}/network/status", json=payload, headers=self.headers
        )
        if r.status_code == 404:
            raise ConnectionError(
                f"{bcolors.WARNING}Please check your server URL in the config.{bcolors.ENDC}"
            )
        return r.json()

    def account_balance(
        self,
        network_id,
        sender_address,
        current_block_index=None,
        current_block_hash=None,
    ):
        payload = {
            "network_identifier": {
                "blockchain": "cardano",
                "network": network_id,
            },
            "account_identifier": {"address": sender_address, "metadata": {}},
            # "block_identifier": {
            #     "index": current_block_index,
            #     "hash": current_block_hash,
            # },
        }
        r = requests.post(
            f"{self.server}/account/balance", json=payload, headers=self.headers
        )
        return r.json()

    def account_coins(
        self,
        network_id,
        sender_address,
        current_block_index=None,
        current_block_hash=None,
    ):
        payload = {
            "network_identifier": {
                "blockchain": "cardano",
                "network": network_id,
            },
            "account_identifier": {"address": sender_address, "metadata": {}},
            # "block_identifier": {
            #    "index": current_block_index,
            #    "hash": current_block_hash,
            # },
            "include_mempool": True,
            "currencies": [
                {"symbol": "ADA", "decimals": 8, "metadata": {"Issuer": "Cardano"}}
            ],
        }
        r = requests.post(
            f"{self.server}/account/coins", json=payload, headers=self.headers
        )
        return r.json()

    def block(
        self,
        network_id,
        current_block_index,
        current_block_hash,
    ):
        payload = {
            "network_identifier": {
                "blockchain": "cardano",
                "network": network_id,
            },
            "block_identifier": {
                "index": current_block_index,
                "hash": current_block_hash,
            },
        }
        r = requests.post(f"{self.server}/block", json=payload, headers=self.headers)
        return r.json()


if __name__ == "__main__":
    rosetta = RosettaWrap()
    network_id = "testnet"
    print(rosetta.network_status(network_id))
    address = "37btjrVyb4KFFSX8cu1fLc9LmA33sC5TEakbjJtePEHiLf6Uk23fJY5T5dQAJQqM2PLR3A8FofNjnxMwFawPeDVS7ZhLVNdAVUHLTQ84uU8VJQWARG"
    emptyAddress = "addr_test1vrz3pgwnjxwk8cr7gue8rctqzq4mzwfuz29jgrztxcxk49qep4c79"
    current_block_index = "2580246"
    current_block_hash = (
        "e4659b6668a7f2333794f1c2b0b1a6a445e5598bbd3692fe35eae93cca4cd886"
    )
    print(rosetta.account_balance(network_id, emptyAddress))
    print(rosetta.account_coins(network_id, emptyAddress))
    # print(rosetta.block(network_id, current_block_index, current_block_hash))
    # print(rosetta.events_blocks(network_id, 5, 5))
