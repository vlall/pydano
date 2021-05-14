import json
import time
from os import path
import requests
import yaml
import subprocess
from cardano_wrapper.wrappers.AddressWrap import AddressWrap
from cardano_wrapper.utils import bcolors


class RosettaWrap(object):
    def __init__(self):
        """This object wraps the Cardano Wallet API so that we can use Python functionality
        to recieve and send API endpoint requests.
        """
        self.headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
        }
        self.setup()

    def setup(self, file="conf.yaml"):
        conf_path = path.join(path.dirname(__file__), "../../conf.yaml")
        with open(conf_path, "r") as stream:
            conf = yaml.safe_load(stream)
        self.server = conf.get("rosetta_server")
        if not self.server:
            raise ValueError(
                f"{bcolors.WARNING}Define server in `{file}`.{bcolors.ENDC}"
            )
        else:
            print(f"Sending requests to {self.server}")

    def network_status(self, network_id):
        payload = {
            "network_identifier": {"blockchain": "cardano", "network": network_id},
            "metadata": {},
        }
        print("*** Network status. ***")
        r = requests.post(
            f"{self.server}/network/status", json=payload, headers=self.headers
        )
        print(r.status_code)
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
            #    "index": current_block_index,
            #    "hash": current_block_hash,
            # },
        }
        r = requests.post(
            f"{self.server}/account/balance", json=payload, headers=self.headers
        )
        print(r.status_code)
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
        print(r.status_code)
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
    print(
        rosetta.account_balance(
            network_id, emptyAddress, current_block_index, current_block_hash
        )
    )
    exit()
    print(rosetta.block(network_id, current_block_index, current_block_hash))
    print(rosetta.events_blocks(network_id, 5, 5))
