import json
import time
from os import path
import requests
import yaml
import subprocess
from cardano_wrapper.utils import Timer
from cardano_wrapper.utils import bcolors
import asyncio
import websockets


class OgmiosWrap(object):
    SOCKET_HEADER = {
        "type": "jsonwsp/request",
        "version": "1.0",
        "servicename": "ogmios",
    }

    def __init__(self):
        """This object wraps Ogmios so that we can use Python functionality
        to recieve and send socket requests.
        """
        self.setup()

    def setup(self, file="conf.yaml"):
        conf_path = path.join(path.dirname(__file__), "../../conf.yaml")
        with open(conf_path, "r") as stream:
            conf = yaml.safe_load(stream)
        self.server = conf.get("ogmios_server")
        if not self.server:
            raise ValueError(
                f"{bcolors.WARNING}Define server in `{file}`.{bcolors.ENDC}"
            )
        else:
            print(f"Sending requests to {self.server}")

    async def run_query(self, uri, payload):
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps(payload))
            return await websocket.recv()

    def query(self, s):
        payload = {
            "methodname": "Query",
            "args": {"query": s},
        }.update(OgmiosWrap.SOCKET_HEADER)
        return asyncio.get_event_loop().run_until_complete(
            self.run_query(self.server, payload)
        )

    def request_next(self):
        payload = {
            "methodname": "RequestNext",
            "args": {},
        }.update(OgmiosWrap.SOCKET_HEADER)
        return asyncio.get_event_loop().run_until_complete(
            self.run_query(self.server, payload)
        )

    def find_intersect(self):
        # last Byron Block
        points = [
            {
                "slot": 4492799,
                "hash": "f8084c61b6a238acec985b59310b6ecec49c0ab8352249afd7268da5cff2a457",
            }
        ]
        payload = {
            "methodname": "FindIntersect",
            "args": {"points": points},
        }.update(OgmiosWrap.SOCKET_HEADER)
        return asyncio.get_event_loop().run_until_complete(
            self.run_query(self.server, payload)
        )

    def acquire(self, slot, hash):
        # Last Byron block
        payload = {
            "methodname": "Acquire",
            "args": {
                "point": {
                    "slot": 4492799,
                    "hash": "f8084c61b6a238acec985b59310b6ecec49c0ab8352249afd7268da5cff2a457",
                },
            },
        }.update(OgmiosWrap.SOCKET_HEADER)
        return asyncio.get_event_loop().run_until_complete(
            self.run_query(self.server, payload)
        )

    def sequential(self, n):
        for i in range(0, n):
            print(i)
            resp = og.request_next()
            print(resp)
        return resp


if __name__ == "__main__":
    og = OgmiosWrap()
    # print(og.find_intersect())
    # print(og.acquire())
    with Timer() as timer:
        resp = og.sequential(100000)
