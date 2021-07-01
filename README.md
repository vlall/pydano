# Pydano

This is a Cardano wrapper library implemented using Python that allows for quick interaction with the services used within the Cardano ecosystem. It works with official cardano executables, REST API interactions, and websocket requests. Here's a list of currently wrapped services:

- [Cardano Addresses](https://github.com/input-output-hk/cardano-addresses) :green_circle:
- [Cardano Wallet](https://github.com/input-output-hk/cardano-wallet) :green_circle:
- [Cardano Rosetta](https://github.com/input-output-hk/cardano-rosetta) :green_circle:
- [Cardano Db-sync](https://github.com/input-output-hk/cardano-db-sync) :green_circle:
- [Cardano Node CLI](https://github.com/input-output-hk/cardano-node/tree/master/cardano-cli) :red_circle:
- [Ogmios](https://github.com/CardanoSolutions/ogmios) :red_circle:

Wrapping code in a general purpose object-oriented language like Python is useful for quickly automating, monitoring, deploying, testing, and building complex interactions with Cardano components on the fly.

## Installation

- With `pip3` installed, install the dependencies using `pip install -r requirements.txt`
- With Python 3.7+ installed, run `python setup.py install`

## Running scripts

- Change the `config.yaml` to contain the correct URLs or paths for the services you are using. For the CLI config items, these values can be absolute paths or paths relative from the project's root directory.

## Running tests

To run tests, use the command `python -m nose2 tests` from the root directory.
