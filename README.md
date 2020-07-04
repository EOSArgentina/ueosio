# µEOSIO
**General purpose library for the EOSIO blockchains**

Micro EOSIO allows you to interact with any EOSio chain using Python.

# Install

    pip3 install ueosio

# Build from source

    git clone https://github.com/AntarticaLabs/ueosio
    cd ueosio
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r examples/requirements.txt

### Examples:

[tx.py](/examples/tx.py): Send a transaction on any given chain.

[keys.py](/examples/keys.py): Generate a key pair or get the public key of any given private key.

[approve_multisig.py](/examples/approve_multisig.py): Approve a multisig transaction.

[create_account.py](/examples/create_account.py): Create an account, buy ram and delegate bandwidth and CPU. 

_____


[MIT License](LICENSE) \
Copyright (c) 2020 AntarticaLabs
