# cardano-wrapper

**Under-development: Some features are incomplete.**

This is a Cardano wrapper package using Python that allows for quick development using the Cardano executables and the Rest APIs used in the Cardano ecosystem. It works with the official cardano executables, currently supporting `cardano-cli` and `cardano-addresses`. It also allows for Rest API interaction using Cardano Wallet and Cardano Rosetta. Wrapping code in a general purpose object-oriented language like Python is useful for quickly automating, monitoring, deploying, testing, and building complex interactions with Cardano components on the fly.

In the future, the plan is to run continuous integration testing using Docker containers with Github Actions.

## Installation

- With Python 3.7+ installed, run `python setup.py install`
- Check to make sure the executables in `/bin` work with your environment. If they do not, place the appropiate version of the cardano executables in the `cardano_wrapper/bin` directory that corresponds to your operating system.

## Running scripts

- Make sure your `config.yaml` is pointing to the correct servers. Then run the appropiate script in python from the `scripts/` directory
- 
## Running tests

To run tests, use the command `python -m nose2 tests` from the root directory. In the future, the tests can be run in different modes depending on the level of replication a user wishes to achieve (ie: running/syncing node in a compatiablity matrix with cardano wallet).
