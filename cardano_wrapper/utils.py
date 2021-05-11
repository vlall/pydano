import sys
import hashlib
import os
import ed25519 # pip install ed25519
import base64

class bcolors:
    OKGREEN = "\033[92m"
    WARNING = "\033[91m"
    ENDC = "\033[0m"
    
def get_sha256(file):
    """Returns SHA256 hash using a buffer.
    """
    size = 65536
    sha256 = hashlib.sha256()
    with open(file, 'rb') as f:
        while True:
            data = f.read()
            if not data:
                break
            sha256.update(data)
    return sha256