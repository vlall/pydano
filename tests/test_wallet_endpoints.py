from cardano_wrapper.wrappers.AddressWrap import AddressWrap
from cardano_wrapper.wrappers.WalletWrap import WalletWrap
import unittest
import requests
import json
import time


class TestWalletEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wallet_type = "byron"
        cls.wallet = WalletWrap()
        # Create wallet.
        cls.wallet_name = "Test Wallet May 6 2021"
        cls.passphrase = "Very important!!!"
        cls.mnemonic = [
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
        cls.wallet.create_wallet(
            cls.wallet_type, cls.wallet_name, cls.passphrase, cls.mnemonic
        )
        walletList = cls.wallet.list_wallets(cls.wallet_type)
        print(walletList)
        cls.wallet_id = walletList[0]["id"]

        # Make an address here.
        cls.wallet.create_address(
            cls.wallet_type, cls.wallet_id, cls.passphrase, 2147483648
        )
        cls.wallet.create_address(
            cls.wallet_type, cls.wallet_id, cls.passphrase, 2147483649
        )
        # Takes time for the wallet/address to sync if we want to be able to test transaction creation.
        time.sleep(240)
        print("addresses")
        cls.addresses = cls.wallet.list_addresses(cls.wallet_type, cls.wallet_id)
        from_address = cls.addresses[0]["id"]
        print(cls.addresses)
        print(from_address)
        to_address = cls.addresses[1]["id"]
        quantity = 1000000
        # Make a transaction.
        print(
            cls.wallet.create_transaction(
                cls.wallet_type, cls.wallet_id, to_address, quantity
            )
        )
        time.sleep(30)
        print("transactions")
        print(
            cls.wallet.list_transactions(
                cls.wallet_type,
                cls.wallet_id,
            )
        )

    @classmethod
    def tearDownClass(cls):
        # Delete wallet.
        cls.wallet.delete_wallet("byron", cls.wallet_id)
        print(cls.wallet.list_wallets(cls.wallet_type))

    def test_check_wallet_id(cls):
        """Check if the correct wallet id is generated."""
        cls.assertEqual(
            TestWalletEndpoints.wallet_id, "ccea052a3de2846b10693105a6a888571f7d985a"
        )

    def test_node_sync(cls):
        """Check if node is finished syncing and has the 'ready' status."""
        resp = cls.wallet.is_sync_ready()
        if resp == "syncing":
            print("Node is still syncing...")
        assert resp

    # def test_transaction(cls):
    #     # TODO: Make a transaction before calling this.ArithmeticError
    #     # v2/byron-wallets/{walletId}/transactions?start={start}&end={end}"
    #     resp = cls.wallet.list_transactions(cls.wallet_type, cls.wallet_id)
    #     print(resp)
    #     expected = ""
    #     cls.assertEqual(json.dumps(resp), json.dumps(expected))

    def test_inspect_wallet(cls):
        # /v2/byron-wallets/{_walletId}";
        resp = cls.wallet.inspect_wallet(cls.wallet_type, cls.wallet_id)
        expected = {
            "passphrase": {"last_updated_at": "2021-05-07T01:27:19.047684518Z"},
            "state": {
                "status": "syncing",
                "progress": {"quantity": 0.28, "unit": "percent"},
            },
            "discovery": "random",
            "balance": {
                "total": {"quantity": 0, "unit": "lovelace"},
                "available": {"quantity": 0, "unit": "lovelace"},
            },
            "name": "Test Wallet May 6 2021",
            "id": "ccea052a3de2846b10693105a6a888571f7d985a",
            "tip": {
                "height": {"quantity": 7000, "unit": "block"},
                "epoch_number": 0,
                "absolute_slot_number": 8030,
                "slot_number": 8030,
            },
        }
        print("@@")
        print(expected)
        print("@@")
        print(resp)
        cls.assertEqual(resp.keys(), expected.keys())

    def test_inspect_address(cls):
        # /v2/addresses/{address}
        resp = cls.addresses[0]["id"]
        print(resp)
        expected = "37btjrVyb4KFhBxHKZnZCYkHsJgSCNDqa2wjMHS41BqLrhUevSWtTBAQFcWbrPSGwgn4kYfJuEDwvJ5hi7xcVdbXkG3pFFGvkonPvxTVrtV4kCCU5A"
        cls.assertEqual(resp, expected)

    # def test_stakepool(self):
    #     # v2/stake-pools/{stakePoolId}/wallets/{walletId}"
    #     # TODO: Obtain stakepool id, wallet id, passphrase.
    #     stake_pool_id = ""
    #     wallet_id = ""
    #     passphrase = ""
    #     resp = self.wallet.join_stake_pool(
    #         stake_pool_id, self.wallet_id, self.passphrase
    #     )
    #     print(resp)
    #     expected = ""
    #     self.assertEqual(resp, expected)

    # def test_stakepools(self):
    #     # /v2/stake-pools/*/wallets/{walletId}"
    #     resp = self.wallet.join_stake_pools(self.wallet_id, self.passphrase)
    #     print(resp)
    #     expected = ""
    #     self.assertEqual(resp, expected)


if __name__ == "__main__":
    unittest.main(verbosity=1)
