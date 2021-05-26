import json
import time
from os import path
import requests
import yaml
import subprocess
from cardano_wrapper.utils import Timer
from cardano_wrapper.utils import bcolors
import psycopg2
from concurrent.futures import ThreadPoolExecutor


class DbSyncWrap(object):
    def __init__(self):
        """This object wraps Db-sync so that we can use Python functionality
        to make Postgres queries on the tables/do testing.
        """
        self.setup()

    def setup(self, file="conf.yaml"):
        conf_path = path.join(path.dirname(__file__), "../../conf.yaml")
        with open(conf_path, "r") as stream:
            conf = yaml.safe_load(stream)
        self.server = conf.get("db_sync_server")
        if not self.server:
            raise ValueError(
                f"{bcolors.WARNING}Define server in `{file}`.{bcolors.ENDC}"
            )
        else:
            print(f"Sending requests to {self.server}")
        self.conn = self.connect()

    def connect(self):
        conn = psycopg2.connect(
            host="localhost",
            database="cexplorer",
            user="postgres",
            password="v8hlDV0yMAHHlIurYupj",
        )
        return conn

    def run_block_query(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT id, hash, epoch_no, slot_no 
            FROM block
            ORDER BY time DESC 
            LIMIT 1
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        rows = rows[0]
        return rows[0], rows[1].hex(), rows[2], rows[3]

    def run_meta_query(self):
        self.conn = self.connect()
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT id, key, json, tx_id
            FROM tx_metadata
            ORDER BY id DESC 
            LIMIT 10
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        self.close()
        return rows

    def sequential(self, n):
        for i in range(0, n):
            print(i)
            resp = self.run_meta_query()
        return resp

    def threaded(self, n=1000):
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.run_meta_query(), i) for i in range(0, n)]
        # list_of_addresses.append([f.result() for f in futures])

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    sync = DbSyncWrap()
    with Timer() as timer:
        # xsresp1 = sync.run_block_query()
        resp2 = sync.sequential(
            1
        )  # 23 seconds sequential with new 23.872774021, 1.104003173......100k timer (sec): 112.075871908

    # with Timer() as timer:
    #     # xsresp1 = sync.run_block_query()
    #     resp2 = sync.threaded(
    #         100000
    #     )  # 26, 1.080929722.......... 100k 115.09937476900001
    # print(resp1, resp2)
    sync.close()