# cardano-wrapper

**Under-development: Some features are incomplete.**

This is a Cardano exectuable wrapper package using Python. It allows for quickly running scripts using the official cardano released executables using `cardano-cli`, `cardano-addresses`, Rest API calls for using Cardano Wallet and, later, integration Rosetta. Finally, we can run continuous integration tests once everything is wrapped using Docker containers with Github Actions.

## Installation

- With Python 3.6+ installed, run `python setup.py install`
- Check to make sure the executables in `/bin` work with your environment. If they do not, place the appropiate version of the cardano executables in the `cardano_wrapper/bin` directory

## Running scripts

- In the /scripts folder, make sure your config is pointing to the correct server if you're running the carrdano wallet wrapper. Then run `python script_name.py`

## Running tests

To run tests, use the command `python -m nose2 tests` from the root directory.

In the future, the tests can be run in different modes depending on the level of replication a user wishes to achieve. If you want a full replication of the integration, the tests will take hours to sync a running node to cardano-wallet. Make sure to check the `config.yaml` file and change to the apporpiate `server` key.
