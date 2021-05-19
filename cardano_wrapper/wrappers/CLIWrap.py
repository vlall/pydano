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
    conf_path = path.join(path.dirname(__file__), "../../conf.yaml")
    with open(conf_path, "r") as stream:
        conf = yaml.safe_load(stream)
    OS = conf.get("os")

    executable = (
        os.path.dirname(os.path.realpath(__file__)) + f"/../bin/{OS}/./cardano-cli"
    )

    def __init__(
        self,
        network_type=None,
        network_id=None,
    ):
        self.network_type = network_type
        self.network_id = network_id

    def get_protocol(self):
        cmd = (
            f"{CLIWrap.executable} query protocol-parameters "
            "--{self.network_type} {self.network_id} "
            "--out-file protocol.json"
        )
        output = subprocess.run(cmd.split(), capture_output=True)
        return output.stdout.rstrip()

    def query_utxo(self, address):
        cmd = (
            f"{CLIWrap.executable} query utxo "
            "--address {address} "
            "--{self.network_type} {self.network_id} "
        )
        output = subprocess.run(cmd.split(), capture_output=True)
        return output.stdout.rstrip()

    def calculate_min_fee(
        self,
        tx_in,
        tx_in_index,
        tx_out_list,
        tx_out_amount,
        invalid_hereafter,
        out_file,
        protocol_param_file,
    ):
        out_count = len(tx_out_list)
        cmd = f"{CLIWrap.executable} transaction calculate-min-fee "
        "--tx-body-file {out_file} "
        "--tx-in-count 1 "
        "--tx-out-count {out_count} "
        "--witness-count 1 "
        "--{self.network_type} {self.network_id} "
        "--protocol-params-file {protocol_param_file}"
        fee = subprocess.run(cmd.split())
        print(fee)
        tx_outs = ""
        # Handle multiple tx outputs using tx_out_list.
        for i, tx in enumerate(tx_out_list):
            tx_outs = tx_outs + " --tx-out {tx}+{tx_out_amount[i]}"

        cmd = (
            f"{CLIWrap.executable} transaction build-raw "
            "--tx-in {tx_in}#{tx_in_index}"
            "{tx_outs} "
            "--invalid-hereafter {invalid_hereafter} "
            "--fee {fee} "
            "--out-file {out_file} "
        )

        output = subprocess.run(cmd2.split(), capture_output=True)
        return output.stdout.rstrip()

    def build_transaction(self, tx_in, tx_out, invalid_hereafter, fee, out_file):
        cmd = (
            f"{CLIWrap.executable} transaction build-raw "
            "--tx-in {tx_in} "
            "--tx-out {tx_out} "
            "--invalid-hereafter {invalid_hereafter} "
            "--fee {fee} "
            "--out-file {out_file} "
        )
        output = subprocess.run(cmd.split(), capture_output=True)
        return output.stdout.rstrip()

    def query_tip(self):
        cmd = (
            f"{CLIWrap.executable} query tip "
            "--{self.network_type} {self.network_id} "
        )
        output = subprocess.run(cmd.split(), capture_output=True)
        return output.stdout.rstrip()

    def sign(self, tx_body_file, signing_key_file, out_file):
        cmd = (
            f"{CLIWrap.executable} transaction sign "
            " --tx-body-file {tx_body_file} "
            "--signing-key-file {signing_key_file} "
            "--{self.network_type} {self.network_id} "
            "--out-file {out_file} "
        )
        output = subprocess.run(cmd.split(), capture_output=True)
        return output.stdout.rstrip()

    def submit(self, tx_file):
        cmd = (
            f"{CLIWrap.executable} transaction submit "
            "--tx-file {tx_file} "
            "--{self.network_type} {self.network_id} "
        )
        output = subprocess.run(cmd.split(), capture_output=True)
        return output.stdout.rstrip()

    def convert_cardano_address_key(self, key_in, key_out):
        cmd = f"{CLIWrap.executable} key convert-cardano-address-key --shelley-payment-key --signing-key-file {key_in} --out-file {key_out}"
        subprocess.run(cmd.split())
        # Python program to read
        f = open(key_out)
        data = json.load(f)
        return data
