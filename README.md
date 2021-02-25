# µEOSIO
**General purpose library for the EOSIO blockchains**

Micro EOSIO allows you to interact with any EOSio chain using Python, it consists of 3 modules: 

* **DS:** Is the Data Stream module and it contains functions for serialization and deserialization of data streams in the eosio format.
* **UTILS:** General functions that are useful for eosio.
* **RPC:** Module for making API interactions.
* **ABI:** Module to work with eosio ABI files

# Install

    pip3 install ueosio

# Build from source

    git clone https://github.com/EOSArgentina/ueosio
    cd ueosio
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r examples/requirements.txt

### Examples:

[tx.py](/examples/tx.py): Send a transaction on any given chain.

[keys.py](/examples/keys.py): Generate a key pair or get the public key of any given private key.

[approve_multisig.py](/examples/approve_multisig.py): Approve a multisig transaction.

[create_account.py](/examples/create_account.py): Create an account, buy ram and delegate bandwidth and CPU. 

[get_top_10_bps.py](/examples/get_top_10_bps.py): Use the rpc module to get list of BPs on any eosio blockchain. 

[abi_hash.py](/examples/abi_hash.py): Get serialized abi hash. 

[extract_pubkey_from_tx.py](/examples/extract_pubkey_from_tx.py): Extract pubkeys used to sign a transaction. 
_____


[MIT License](LICENSE) \
Copyright (c) 2020 EOS Argentina
