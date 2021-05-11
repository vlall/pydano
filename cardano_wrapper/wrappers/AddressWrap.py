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

class AddressWrap(object):

    def __init__(self, path="../bin/cardano-address", wallet="shelley"):
        self.path = path
        if wallet.lower() == "shelley":
            phrase = self.get_mnemonic(24)
        elif wallet.lower() == "byron":
            phrase = self.get_mnemonic(12)
        else:
            raise ValueError("test")
        self.root_private = self.get_root_private_key(phrase)
        keyDict = {
            "phrase": phrase.decode("utf8"),
            "root_private_key": self.root_private.decode("utf8"),
        }
        time_str = self.get_time_str()
        with open(f"keys_{time_str}.json", "w") as keys:
            json.dump(keyDict, keys)
    
    @staticmethod
    def trezor_mnenmoic(language="english"):
        mnemo = Mnemonic(language)
        words = mnemo.generate(strength=256)
        return words.split()

    @staticmethod
    def get_mnemonic(n):
        #  ./cardano-address recovery-phrase generate --size 24 > phrase.prv
        cmd = f"./cardano-address recovery-phrase generate --size {n}"
        output = subprocess.run(cmd.split(), capture_output=True)
        return output.stdout.rstrip()
    
    @staticmethod 
    def get_root_private_key(phrase):
        #  cat phrase.prv \
        # | ./cardano-address key from-recovery-phrase Shelley > root.xs
        cmd = "./cardano-address key from-recovery-phrase Shelley"
        output = subprocess.run(cmd.split(), input=phrase, capture_output=True)
        return output.stdout.rstrip()
    
    @staticmethod
    def get_root_public_key(root_private):
        # cat root.xsk | ./cardano-address key public --with-chain-code
        cmd = "./cardano-address key public --with-chain-code"
        output = subprocess.run(cmd.split(), input=root_private, capture_output=True)
        return output.stdout.rstrip()

    @staticmethod
    def get_private_key(root_private, index):
        """cat root.xsk \
                | ./cardano-address key child 852H/1815H/0H/0/0 \
                | tee acct.prv \
                | ./cardano-address key public --with-chain-code > acct.pub
        """
        # cmd = "./cardano-address key child 852H/1815H/0H/0/0"
        cmd = f"./cardano-address key child 1852H/1815H/0H/0/{index}"
        output = subprocess.run(cmd.split(), input=root_private, capture_output=True)
        return output.stdout.rstrip()

    @staticmethod
    def get_public_key(private_key):
        cmd = " ./cardano-address key public --with-chain-code"
        output = subprocess.run(cmd.split(), input=private_key, capture_output=True)
        return output.stdout.rstrip()

    @staticmethod
    def get_payment_address(public_key):
        cmd = "./cardano-address address payment --network-tag testnet"
        output = subprocess.run(cmd.split(), input=public_key, capture_output=True)
        return output.stdout.rstrip()

    @staticmethod
    def get_time_str():
        timestr = datetime.utcnow().strftime("%m-%d-%Y_%H-%M-%S-%f")[:-3]
        return timestr
    
    def task(self, address):
        # Indices are random 2^32.
        private_key = self.get_private_key(self.root_private, address)
        public_key = self.get_public_key(private_key)
        return self.get_payment_address(public_key).decode("utf8")

    def run(
        self,
        addresses,
        threading=False,
        multiprocessing=False,
        batch=None,
    ):
        start_time = time.time()
        list_of_addresses = []
        if threading:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.task, i) for i in range(0, addresses)]
            list_of_addresses.append([f.result() for f in futures])
        # if thread_custom_pool:
        #     p = mp.Pool(batch)
        #     x = p.map(self.task, range(addresses))
        #     p.close()
        #     p.join()
        #     return x
        elif multiprocessing:
            pass
        else:
            for address in range(0, addresses):
                if address % 100:
                    print(address)
                list_of_addresses.append(self.task(address))
        keyDict = {
            "list_of_addresses": list_of_addresses,
            "time": time.time() - start_time,
        }
        time_str = self.get_time_str()
        with open(f"addresses_{time_str}.json", "w") as keys:
            json.dump(keyDict, keys)
        return list_of_addresses


class Timer:
    def warn(self, s):
        print(s, file=sys.stderr)

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.interval = self.end - self.start
        self.warn("timer (sec): " + str(self.interval))


if __name__ == "__main__":
    gen = AddressWrapper()
    with Timer() as timer:
        print(gen.run(400000))
    print(str(timer.interval))
