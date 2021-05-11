# cardano-wrapper

_Under-development_ : Some features are incomplete.

This is a Cardano exectuable wrapper package using Python. It allows for quickly running scripts using the official cardano released executables using `cardano-cli` from `cardano-node` and `cardano-addresses`. We also wrap Rest API calls for using Wallet and Rosetta functionality within Python. Finally, we can run integration tests once everything is wrapped using Docker containers with Github Actions.

## Installation

- With Python 3.6+ installed, run `python setup.py install`
- If running manually, place the appropiate version of the cardano executables in the `cardano_wrapper/bin` directory

## Running tests

The tests can be run in different modes depending on the level of replication a user wishes to achieve. If you want a full replication of the integration, the tests will take hours to sync a running node to cardano-wallet. Otherwise, you can point to an already deployed cardano-wallet server in the `config.yaml` file using the `server` key.

To run tests, use the command `python -m nose2 tests` from the root directory.
