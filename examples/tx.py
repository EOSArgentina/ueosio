import sys
import json
import binascii
import requests as r
from getpass import getpass
from datetime import datetime, timedelta
from ueosio import sign_tx, DataStream, get_expiration, get_tapos_info, build_push_transaction_body

### example tx
tx = {"delay_sec":0,"max_cpu_usage_ms":0,"actions":[{"account":"eosio.token","name":"transfer","data":{"from":"youraccount1","to":"argentinaeos","quantity":"0.0001 EOS","memo":" This tx was sent using µEOSIO"},"authorization":[{"actor":"youraccount1","permission":"active"}]}]}

# Get chain info from a working api node
info = r.get('https://api.eosargentina.io/v1/chain/get_info').json()
ref_block_num, ref_block_prefix = get_tapos_info(info['last_irreversible_block_id'])
chain_id = info['chain_id']

# package transation
data = tx['actions'][0]['data']
ds = DataStream()
ds.pack_name(data['from'])
ds.pack_name(data['to'])
ds.pack_asset(data['quantity'])
ds.pack_string(data['memo'])

tx['actions'][0]['data'] = binascii.hexlify(ds.getvalue()).decode('utf-8')

tx.update({
    "expiration": get_expiration(datetime.utcnow(), timedelta(minutes=15).total_seconds()),
    "ref_block_num": ref_block_num,
    "ref_block_prefix": ref_block_prefix,
    "max_net_usage_words": 0,
    "max_cpu_usage_ms": 0,
    "delay_sec": 0,
    "context_free_actions": [],
    "transaction_extensions": [],
    "context_free_data": []
})

# enter private key of the account
auth = tx['actions'][0]['authorization'][0]
private_key = getpass("Enter private key for %s@%s: " % (auth['actor'], auth['permission']))

# Sign transaction
tx_id, tx = sign_tx(
   chain_id,
   tx,
   private_key
)
ds = DataStream()
ds.pack_transaction(tx)
packed_trx = binascii.hexlify(ds.getvalue()).decode('utf-8')
tx = build_push_transaction_body(tx['signatures'][0], packed_trx)

# Push transaction
res = r.post('https://api.eosargentina.io/v1/chain/push_transaction', json=tx).json()
print(res)
