import json
import time
from os import path
import requests
import yaml
import subprocess
from pydano.utils import Timer
from pydano.utils import bcolors
import asyncio
import websockets


class OgmiosWrap(object):
    PAYLOAD = {
        "type": "jsonwsp/request",
        "version": "1.0",
        "servicename": "ogmios",
    }

    def __init__(self, conf_path):
        """This object wraps Ogmios so that we can use Python functionality
        to recieve and send socket requests.
        """
        self.setup(conf_path)

    def setup(self, conf_path):
        with open(conf_path, "r") as stream:
            conf = yaml.safe_load(stream)
        self.ws_server = "ws://%s" % conf.get("ogmios_server")
        self.http_server = "http://%s" % conf.get("ogmios_server")
        if not self.ws_server:
            raise ValueError(
                f"{bcolors.WARNING}Define server in `{file}`.{bcolors.ENDC}"
            )
        else:
            print(f"Sending requests to {self.ws_server}")

    def health(self):
        resp = requests.get(
            f"{self.http_server}/health", headers={"Accept": "application/json"}
        ).text
        return json.loads(resp)

    async def run_query(self, uri, payload):
        payload_test = {
            "type": "jsonwsp/request",
            "version": "1.0",
            "servicename": "ogmios",
            "methodname": "RequestNext",
            "args": {},
        }
        websocket = await websockets.connect(uri)
        # async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(payload))
        print(await websocket.recv())
        await websocket.send(json.dumps(payload_test))
        return await websocket.recv()

    def query(self, s):
        payload = OgmiosWrap.PAYLOAD
        payload.update(
            {
                "methodname": "Query",
                "args": {"query": s},
            }
        )
        print(payload)
        resp = asyncio.get_event_loop().run_until_complete(
            self.run_query(self.ws_server, payload)
        )
        return json.loads(resp)

    def request_next(self):
        payload = OgmiosWrap.PAYLOAD
        payload.update(
            {
                "methodname": "RequestNext",
                "args": {},
            }
        )
        resp = asyncio.get_event_loop().run_until_complete(
            self.run_query(self.ws_server, payload)
        )
        return json.loads(resp)

    def find_intersect(self, slot_in, hash_in):
        points = [
            {
                "slot": slot_in,
                "hash": hash_in,
            },
            "origin",
        ]
        payload = OgmiosWrap.PAYLOAD
        payload.update(
            {
                "methodname": "FindIntersect",
                "args": {"points": points},
            }
        )
        resp = asyncio.get_event_loop().run_until_complete(
            self.run_query(self.ws_server, payload)
        )
        return json.loads(resp)

    def acquire(self, slot_in, hash_in):
        payload = OgmiosWrap.PAYLOAD
        payload.update(
            {
                "methodname": "Acquire",
                "args": {
                    "point": {
                        "slot": slot_in,
                        "hash": hash_in,
                    },
                },
            }
        )
        resp = asyncio.get_event_loop().run_until_complete(
            self.run_query(self.ws_server, payload)
        )
        return json.loads(resp)

    def sequential(self, n):
        for i in range(0, n):
            print(i)
            resp = self.request_next()
            print(resp)
        return resp


if __name__ == "__main__":
    with Timer() as timer:
        og = OgmiosWrap()
        tip = og.query("ledgerTip")
        rnext = og.request_next()
        # currSlot = rnext["result"]["slot"]
        # currHash = rnext["result"]["hash"]
        getSlot = 31474792
        getHash = "31ca464b162ce9d8793d99fc30ca563773631c61a1fc3cdbeb39f4c444551434"
        # print(og.health())
        # print(og.find_intersect(getSlot, getHash))
        print(f"{bcolors.WARNING}*** Request next before. ***{bcolors.ENDC}")
        print(rnext)
        print(f"{bcolors.WARNING}*** Current tip. ***{bcolors.ENDC}")
        print(tip)
        print(f"{bcolors.WARNING}*** Finding intersect. ***{bcolors.ENDC}")
        print(
            og.find_intersect(
                4492799,
                "f8084c61b6a238acec985b59310b6ecec49c0ab8352249afd7268da5cff2a457",
            )
        )
        # print(f"{bcolors.WARNING}*** Current tip. ***{bcolors.ENDC}")
        # print(tip)
        # print(f"{bcolors.WARNING}*** Acquired point. ***{bcolors.ENDC}")
        # print(og.acquire(getSlot, getHash))
        print(f"{bcolors.WARNING}*** Request next after. ***{bcolors.ENDC}")
        print(og.sequential(3))
        # with Timer() as timer:
        #    resp = og.sequential(100)
        print(f"{bcolors.WARNING}*** Current tip. ***{bcolors.ENDC}")
        print(tip)
