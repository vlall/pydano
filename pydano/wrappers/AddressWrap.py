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


class AddressWrap(object):
    """Cardano Python wrapper for the cardano-addresses executable."""

    conf_path = path.join(path.dirname(__file__), "../../conf.yaml")
    with open(conf_path, "r") as stream:
        conf = yaml.safe_load(stream)
    OS = conf.get("os")
    executable = (
        os.path.dirname(os.path.realpath(__file__)) + f"/../bin/{OS}/./cardano-address"
    )

    def __init__(self, wallet="shelley", os=None, write=False):
        """Initialize the root keys and open a data file to store the generated addresses.

        Args:
            wallet (str, optional): Wallet Type.
            Either "byron" or "shelley". Defaults to "shelley".

        Raises:
            ValueError: Raised if wallet is incorrect
        """
        if wallet.lower() == "shelley":
            self.phrase = self.cli_mnemonic(24)
        elif wallet.lower() == "byron":
            self.phrase = self.cli_mnemonic(12)
        else:
            raise ValueError("Incorrect wallet type.")

    def make_keys(self, write=False):
        self.root_private = self.root_private_key(self.phrase)
        keyDict = {
            "phrase": self.phrase.decode("utf8"),
            "root_private_key": self.root_private.decode("utf8"),
        }
        time_str = self.time_str()
        if write:
            with open(f"keys_{time_str}.json", "w") as keys:
                json.dump(keyDict, keys)
        return keyDict

    @staticmethod
    def trezor_mnenmoic(language="english"):
        mnemo = Mnemonic(language)
        words = mnemo.generate(strength=256)
        return words.split()

    @staticmethod
    def cli_mnemonic(n, to_list=False):
        #  ./cardano-address recovery-phrase generate --size 24 > phrase.prv
        cmd = f"{AddressWrap.executable} recovery-phrase generate --size {n}"
        output = subprocess.run(cmd.split(), capture_output=True)
        words = output.stdout.rstrip()
        if to_list:
            words = str(words, "UTF-8")
            return words.split()
        else:
            return words

    @staticmethod
    def root_private_key(phrase):
        #  cat phrase.prv \
        # | ./cardano-address key from-recovery-phrase Shelley > root.xs
        cmd = f"{AddressWrap.executable} key from-recovery-phrase Shelley"
        output = subprocess.run(cmd.split(), input=phrase, capture_output=True)
        return output.stdout.rstrip()

    @staticmethod
    def root_public_key(root_private):
        # cat root.xsk | ./cardano-address key public --with-chain-code
        cmd = f"{AddressWrap.executable}  key public --with-chain-code"
        output = subprocess.run(cmd.split(), input=root_private, capture_output=True)
        return output.stdout.rstrip()

    @staticmethod
    def private_key(root_private, index):
        """Indices are 2^32
            cat root.xsk \
                | ./cardano-address key child 852H/1815H/0H/0/0 \
                | tee acct.prv \
                | ./cardano-address key public --with-chain-code > acct.pub
        """
        # cmd = "./cardano-address key child 852H/1815H/0H/0/0"
        cmd = f"{AddressWrap.executable}  key child 1852H/1815H/0H/0/{index}"
        output = subprocess.run(cmd.split(), input=root_private, capture_output=True)
        return output.stdout.rstrip()

    @staticmethod
    def public_key(private_key):
        cmd = f"{AddressWrap.executable}  key public --with-chain-code"
        output = subprocess.run(cmd.split(), input=private_key, capture_output=True)
        return output.stdout.rstrip()

    @staticmethod
    def payment_address(public_key):
        cmd = f"{AddressWrap.executable}  address payment --network-tag testnet"
        output = subprocess.run(cmd.split(), input=public_key, capture_output=True)
        return output.stdout.rstrip()

    @staticmethod
    def time_str():
        timestr = datetime.utcnow().strftime("%m-%d-%Y_%H-%M-%S-%f")[:-3]
        return timestr

    def task(self, nth_address):
        """Given an nth address, return generated payment address.

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
    address = AddressWrap()
    with Timer() as timer:
        print(address.generate(10))
    print(str(timer.interval))
