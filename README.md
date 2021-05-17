# cardano-wrapper

**Under-development: Some features are incomplete.**

This is a Cardano wrapper package using Python that allows for quick interaction with Cardano executables and the Rest APIs used in the Cardano ecosystem. It works with the official cardano executables, currently supporting `cardano-cli` and `cardano-addresses`. It also allows for Rest API interaction using `Cardano Wallet` and `Cardano Rosetta`.

Wrapping code in a general purpose object-oriented language like Python is useful for quickly automating, monitoring, deploying, testing, and building complex interactions with Cardano components on the fly.

In the future, the plan is to run continuous integration testing using Docker containers with Github Actions.

## Installation

- With Python 3.7+ installed, run `python setup.py install`
- Check to make sure the executables in `/bin` are the versions you want to run. If they do not, download the appropriate versions (see [cardano-wallet](https://github.com/input-output-hk/cardano-wallet/releases)), then place the executables in the `cardano_wrapper/bin/{your_operating_system}` directory

## Running scripts

- Make sure your `config.yaml` is pointing to the correct servers. Then run the appropriate script in python from the `scripts/` directory

## Running tests

To run tests, use the command `python -m nose2 tests` from the root directory. In the future, the tests can be run in different modes depending on the level of replication a user wishes to achieve (ie: running/syncing node in a compatibility matrix with cardano-wallet).
