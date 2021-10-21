import json
import time
from os import path
import requests
import yaml
import subprocess
from pydano.utils import bcolors
import pprint

pp = pprint.PrettyPrinter(indent=4)


class WalletWrap(object):
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
        self.server = conf.get("wallet_server")
        if not self.server:
            raise ValueError(
                f"{bcolors.WARNING}Define server in `{file}`.{bcolors.ENDC}"
            )
        self.version = conf.get("wallet_version")
        r = requests.get(f"{self.server}/{self.version}/network/information")
        return r.raise_for_status()

    def make_wallet_path(self, wallet_type):
        """[summary]

        Args:
            wallet_type (str): Either "shelley" or "byron".

        Raises:
            ValueError: Raised if the wallet is not "shelley" or "byron".

        Returns:
            str: Formatted `wallets` URL path.
        """
        if wallet_type == "shelley":
            return "wallets"
        elif wallet_type == "byron":
            print(
                f"{bcolors.WARNING}Warning:{bcolors.ENDC} Since you're using Byron, there might be some errors. "
                "The construction of random wallet in itself is deprecated, in particular "
                "the restoration from an encrypted root private key. These endpoints exist "
                "to ease migrations from legacy software such as cardano-sl but should be "
                "avoided by new applications."
            )
            return "byron-wallets"
        else:
            raise ValueError(
                f"{bcolors.FAIL}Empty or incorrect wallet type.{bcolors.ENDC}"
            )

    def network_information(self):
        print("*** Get network information. ***")
        r = requests.get(f"{self.server}/{self.version}/network/information")
        print(r.status_code)
        if r.status_code == 404:
            raise ConnectionError(
                f"{bcolors.WARNING}Please check your server URL in the config.{bcolors.ENDC}"
            )
        return r.json()

    def create_wallet(
        self,
        wallet_type,
        name,
        passphrase,
        mnemonic,
        style="random",
        address_pool_gap=20,
    ):
        wallets = self.make_wallet_path(wallet_type)
        print("*** Create Wallet. ***")
        endpoint = f"{self.server}/{self.version}/{wallets}/"
        r = requests.post(
            endpoint,
            json={
                "style": style,
                "name": name,
                "passphrase": passphrase,
                "mnemonic_sentence": mnemonic,
                "address_pool_gap": address_pool_gap,
            },
            headers=self.headers,
        )
        # print(json.dumps(mnemonic))
        return r.json()

    def construct_address(self, payment, stake, validation):
        endpoint = f"{self.server}/{self.version}/addresses"
        r = requests.post(
            endpoint,
            json={
                "payment": payment,
                "stake": stake,
                "validation": validation,  # Enum: "required" or "recommended"
            },
            headers=self.headers,
        )
        return r.json()

    def create_address(self, wallet_type, wallet_id, passphrase, address_index=0):
        wallets = self.make_wallet_path(wallet_type)
        if wallet_type == "shelley":
            raise (KeyError)
        else:
            endpoint = f"{self.server}/{self.version}/{wallets}/{wallet_id}/addresses"
            r = requests.post(
                endpoint,
                json={
                    "passphrase": passphrase,
                    "address_index": address_index,
                },
                headers=self.headers,
            )
        return r.json()

    def create_transaction(
        self, wallet_type, wallet_id, passphrase, to_addresses, quantities, assets=None
    ):
        if len(to_addresses) != len(quantities):
            raise ("List Error")
        wallets = self.make_wallet_path(wallet_type)
        endpoint = f"{self.server}/{self.version}/{wallets}/{wallet_id}/transactions"
        payments = []
        for idx in range(0, len(to_addresses)):
            payments.append(
                {
                    "address": to_addresses[idx],
                    "amount": {"quantity": quantities[idx], "unit": "lovelace"},
                },
            )
        # print(payments)
        payload = {
            "passphrase": passphrase,
            "payments": payments,
        }
        # print(payload)
        # if assets:
        #     payload["payments"][0]["asset"] = [assets]
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(json.dumps(payload))
        r = requests.post(
            endpoint,
            json=payload,
            headers=self.headers,
        )
        return r.json()

    def delete_wallet(self, wallet_type, wallet_id):
        wallets = self.make_wallet_path(wallet_type)
        print("*** Deleting Wallet. ***")
        r = requests.delete(
            f"{self.server}/{self.version}/{wallets}/{wallet_id}",
        )
        print(f"*** Wallet {wallet_id} deleted. ***")
        return True

    def inspect_wallet(self, wallet_type, wallet_id, start=None, stop=None):
        wallets = self.make_wallet_path(wallet_type)
        endpoint = f"{self.server}/{self.version}/{wallets}/{wallet_id}"
        print(endpoint)
        r = requests.get(endpoint)
        print("HERE")
        print(r.json())
        return r.json()

    def inspect_address(self, address):
        wallets = self.make_wallet_path(wallet_type)
        endpoint = f"{self.server}/{self.version}/addresses/{address}"
        print(endpoint)
        r = requests.get(endpoint)
        return r.json()

    def list_wallets(self, wallet_type):
        wallets = self.make_wallet_path(wallet_type)
        print("*** List Wallet Information. ***")
        endpoint = f"{self.server}/{self.version}/{wallets}"
        print(endpoint)
        r = requests.get(endpoint)
        return r.json()

    def list_addresses(self, wallet_type, wallet_id):
        wallets = self.make_wallet_path(wallet_type)
        print("*** List addresses. ***")
        endpoint = f"{self.server}/{self.version}/{wallets}/{wallet_id}/addresses"
        r = requests.get(endpoint)
        return r.json()

    def list_transactions(self, wallet_type, wallet_id, start=None, end=None):
        wallets = self.make_wallet_path(wallet_type)
        r = requests.get(
            f"{self.server}/{self.version}/{wallets}/{wallet_id}/transactions"
        )
        return r.json()

    def list_stakepools(self):
        print("*** List stakepools. ***")
        r = requests.get(f"{self.server}/{self.version}/stake-pools")
        return r.json()

    def join_stakepool(self, stake_pool_id, wallet_id, passphrase):
        endpoint = (
            f"{self.server}/{self.version}/stake-pools/{stakePoolId}/wallets/{walletId}"
        )
        r = requests.put(
            endpoint,
            json={
                "passphrase": passphrase,
            },
            headers=self.headers,
        )
        return r.json()

    def join_stakepools(self, wallet_id, passphrase):
        endpoint = f"{self.server}/{self.version}/stake-pools/*/wallets/{walletId}"
        r = requests.get(
            endpoint,
            json={
                "passphrase": passphrase,
            },
            headers=self.headers,
        )
        return r.json()

    def is_sync_ready(self):
        progress = self.network_information()["sync_progress"]["status"]
        print(progress)
        return progress == "ready"

    def smash_health(self):
        r = requests.get(f"{self.server}/{self.version}/smash/health")
        return r.json()

    def network_clock(self):
        print("*** Get network clock. ***")
        r = requests.get(f"{self.server}/{self.version}/network/clock")
        return r.json()

    def network_parameters(self):
        r = requests.get(f"{self.server}/{self.version}/network/parameters")
        return r.json()

    def settings(self):
        r = requests.get(f"{self.server}/{self.version}/settings")
        return r.json()

    def utxo_statistics(self, wallet_id):
        print("*** Get UTxO Statistics. ***")
        r = requests.get(
            f"{self.server}/{self.version}/wallets/{wallet_id}/statistics/utxos"
        )
        return r.json()

    def update_wallet_name(self, wallet_type, wallet_id, name):
        print("*** Update wallet name. ***")
        wallets = self.make_wallet_path(wallet_type)
        r = requests.put(
            f"{self.server}/{self.version}/{wallets}/{wallet_id}",
            json={
                "name": name,
            },
        )
        return r.json()

    def update_wallet_passphrase(
        self, wallet_type, wallet_id, old_passphrase, new_passphrase
    ):
        print("*** Update wallet passphrase. ***")
        wallets = self.make_wallet_path(wallet_type)

        r = requests.put(
            f"{self.server}/{self.version}/{wallets}/{wallet_id}/passphrase",
            json={
                "old_passphrase": old_passphrase,
                "new_passphrase": new_passphrase,
            },
        )
        return r.json()

    def list_wallet_assets(self, wallets, wallet_id):
        print("*** List assets. ***")
        r = requests.get(f"{self.server}/{self.version}/{wallets}/{wallet_id}/assets")
        return r.json()

    def maintenance_ations(self, wallet_id):
        print("*** List maintenance actions. ***")
        r = requests.get(
            f"{self.server}/{self.version}/stake-pools/maintenance-actions"
        )
        return r.json()

    def delegation_fees(self, wallets, wallet_id):
        print("*** List delegation fees. ***")
        r = requests.get(
            f"{self.server}/{self.version}/{wallets}/{wallet_id}/delegation-fees"
        )
        return r.json()

    def coin_selections(self, wallets, wallet_id):
        print("*** Select coins to cover the given set of payments. ***")
        r = requests.post(
            f"{self.server}/{self.version}/{wallets}/{wallet_id}/coin-selections/random"
        )
        print(r.json())

    def shared_wallets(self, wallets, wallet_id):
        print("*** Get share wallets. ***")
        r = requests.get(f"{self.server}/{self.version}/shared-wallets/{wallet_id}/")
        print(r.json())

    def import_addresses(self, wallet_id, addresses):
        print("*** Import addresses. ***")
        r = requests.put(
            f"{self.server}/{self.version}/{wallet_id}/addresses",
            json={
                "addresses": addresses,
            },
        )
        return r.json()


if __name__ == "__main__":
    wallet = WalletWrap()
    print(wallet.network_information())
    print(wallet.is_sync_ready())
    print(wallet.list_wallets())
    name = "Test Wallet May 6 2021"
    passphrase = "Very important!!!"
    # mnemonic = AddressWrapper.get_mnemonic(12)
    mnemonic = [
        "squirrel",
        "material",
        "silly",
        "twice",
        "direct",
        "slush",
        "pistol",
        "razor",
        "become",
        "junk",
        "kingdom",
        "flee",
    ]
    wallet.create_wallet(name, passphrase, mnemonic, wallet_type="byron")
    print("Should be created...")
    print(wallet.list_addresses())
    print(wallet.list_wallets())