FROM ubuntu:20.04 AS cardano-wrapper

LABEL version="0.1-beta" \
    author="vlall" \
    release-date="2021-05-10" \
    description="Run cardano tests for integration testing."

ENV HOME=/home
WORKDIR /home

RUN apt-get update -y && apt-get install -y wget \
    python3-pip \ 
    python3 \
    tmux \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# ARG NODE_URL="https://hydra.iohk.io/build/5550453/download/1/cardano-node-1.25.1-linux.tar.gz"
# ARG WALLET_URL="https://github.com/input-output-hk/cardano-wallet/releases/download/v2021-04-28/cardano-wallet-v2021-04-28-linux64.tar.gz"
# RUN wget $NODE_URL \
#     $WALLET_URL
# RUN for f in *.tar; do tar xf "$f"; done

# RUN wget https://hydra.iohk.io/build/6198010/download/1/testnet-config.json \
#     https://hydra.iohk.io/build/6198010/download/1/testnet-byron-genesis.json \
#     https://hydra.iohk.io/build/6198010/download/1/testnet-shelley-genesis.json \
#     https://hydra.iohk.io/build/6198010/download/1/testnet-topology.json

# # This will eventually be serperated into two different services once a docker-compose is made.
# RUN ./cardano-node run --topology ./testnet-topology.json --database-path ./state-lp --port 3001 --config ./testnet-config.json --socket-path ./node.socket & \
#     ./cardano-wallet serve --node-socket ./node.socket --database ./wallet-db --listen-address 0.0.0.0 --port 8090 --testnet testnet-byron-genesis.json &

# # Clone the cardano-wrappers test with authentication.
# RUN git clone $REPO
# TODO: Answer:
# 1. How long does it take for the node to sync on docker?
# 2. Is it useful to sync these components for this test? 
# 3. How do we prevent the build from timing out? 
# 4. How do we detect failure early?
