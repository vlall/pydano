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
from mnemonic import Mnemonic
from pydano.utils import Timer
import os
from os import path
import yaml
import pathlib


class AddressWrap(object):
    """Cardano Python wrapper for the cardano-addresses executable."""

    def __init__(self, conf_path, write=False):
        """Initialize the root keys and open a data file to store the generated addresses.

        Args:
            wallet (str, optional): Wallet Type.
            Either "byron" or "shelley". Defaults to "shelley".

        Raises:
            ValueError: Raised if wallet is incorrect
        """
        with open(conf_path, "r") as stream:
            conf = yaml.safe_load(stream)
        address_path = conf.get("cardano_address_path")
        self.executable = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            f"../../{address_path}",
        )

    def wallet_setup(self, wallet="shelley"):
        if wallet.lower() == "shelley":
            phrase = self.cli_mnemonic(24)
        elif wallet.lower() == "byron":
            phrase = self.cli_mnemonic(12)
        else:
            raise ValueError("Incorrect wallet type.")
        return phrase

    def make_keys(self, phrase, write=False):
        self.root_private = self.root_private_key(phrase)
        keyDict = {
            "phrase": phrase.decode("utf8"),
            "root_private_key": self.root_private.decode("utf8"),
        }
        time_str = self.time_str()
        if write:
            with open(f"keys_{time_str}.json", "w") as keys:
                json.dump(keyDict, keys)
        return keyDict

    def trezor_mnenmoic(language="english"):
        mnemo = Mnemonic(language)
        words = mnemo.generate(strength=256)
        return words.split()

    def cli_mnemonic(self, n, to_list=False):
        #  ./cardano-address recovery-phrase generate --size 24 > phrase.prv
        cmd = f"{self.executable} recovery-phrase generate --size {n}"
        output = subprocess.run(cmd.split(), capture_output=True)
        words = output.stdout.rstrip()
        if to_list:
            words = str(words, "UTF-8")
            return words.split()
        else:
            return words

    def root_private_key(self, phrase):
        #  cat phrase.prv \
        # | ./cardano-address key from-recovery-phrase Shelley > root.xs
        cmd = f"{self.executable} key from-recovery-phrase Shelley"
        output = subprocess.run(cmd.split(), input=phrase, capture_output=True)
        return output.stdout.rstrip()

    def root_public_key(self, root_private):
        # cat root.xsk | ./cardano-address key public --with-chain-code
        cmd = f"{self.executable} key public --with-chain-code"
        output = subprocess.run(cmd.split(), input=root_private, capture_output=True)
        return output.stdout.rstrip()

    def private_key(self, root_private, index):
        """Indices are 2^32
            cat root.xsk \
                | ./cardano-address key child 852H/1815H/0H/0/0 \
                | tee acct.prv \
                | ./cardano-address key public --with-chain-code > acct.pub
        """
        # cmd = "./cardano-address key child 852H/1815H/0H/0/0"
        cmd = f"{self.executable} key child 1852H/1815H/0H/0/{index}"
        output = subprocess.run(cmd.split(), input=root_private, capture_output=True)
        return output.stdout.rstrip()

    def public_key(self, private_key):
        cmd = f"{self.executable} key public --with-chain-code"
        output = subprocess.run(cmd.split(), input=private_key, capture_output=True)
        return output.stdout.rstrip()

    def payment_address(self, public_key):
        cmd = f"{self.executable} address payment --network-tag testnet"
        output = subprocess.run(cmd.split(), input=public_key, capture_output=True)
        return output.stdout.rstrip()

    def time_str(self):
        timestr = datetime.utcnow().strftime("%m-%d-%Y_%H-%M-%S-%f")[:-3]
        return timestr

    def task(self, address):
        """Given an nth address, s generated payment address.

        Args:
            address (int): Address number.

        Returns:
            str: Payment address.
        """
        private_key = self.private_key(self.root_private, address)
        public_key = self.public_key(private_key)
        return self.payment_address(public_key).decode("utf8")

    def generate(self, addresses, mode=None, batch=None, write=False):
        """Generate Cardano Addresses.

        Args:
            addresses ([type]): N Addresses to create.
            mode ([type], optional): "auto_thread", "custom_thread", or "multiprocessing". Defaults to None.
            batch ([type], optional): Processes to split threads into.

        Returns:
            list: List of addresses generated.
        """
        phrase = self.wallet_setup("shelley")
        print(self.make_keys(phrase))
        start_time = time.time()
        list_of_addresses = []
        if mode == "threading":
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.task, i) for i in range(0, addresses)]
            list_of_addresses.append([f.result() for f in futures])
        if mode == "custom_thread" and batch:
            p = mp.Pool(batch)
            resp = p.map(self.task, range(addresses))
            p.close()
            p.join()
            return resp
        elif mode == "multiprocessing":
            pass
        else:
            for nth_address in range(0, addresses):
                if nth_address % 100:
                    print(nth_address)
                list_of_addresses.append(self.task(nth_address))
        keyDict = {
            "list_of_addresses": list_of_addresses,
            "time": time.time() - start_time,
        }
        time_str = self.time_str()
        if write:
            with open(f"addresses_{time_str}.json", "w") as keys:
                json.dump(keyDict, keys)
        return list_of_addresses


if __name__ == "__main__":
    address = AddressWrap("../../config.yaml")
    with Timer() as timer:
        print(address.generate(10))
    print(str(timer.interval))
