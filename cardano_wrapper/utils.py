import sys
import hashlib
import os
import base64
import time

# import ed25519
class bcolors:
    OKGREEN = "\033[92m"
    WARNING = "\033[91m"
    ENDC = "\033[0m"


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


def get_sha256(file):
    """Returns SHA256 hash using a buffer."""
    size = 65536
    sha256 = hashlib.sha256()
    with open(file, "rb") as f:
        while True:
            data = f.read()
            if not data:
                break
            sha256.update(data)
    return sha256