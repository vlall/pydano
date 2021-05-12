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
    def __init__(
        self,
        network_type,
        network_id,
        path=path.join(path.dirname(__file__), "../bin/./cardano-cli"),
    ):
        self.path = path
        self.network_type = network_type
        self.network_id = network_id

    def get_protocol(self):
        cmd = (
            f"{path} query protocol-parameters "
            "{self.network_type} {self.network_id} "
            "--out-file protocol.json"
        )
        output = subprocess.run(cmd.split(), capture_output=True)
        return output.stdout.rstrip()

    def query_utxo(self):
        pass

    def send_transaction(self):
        pass