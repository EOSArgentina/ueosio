import sys
import json
import binascii
import requests as r
from getpass import getpass
from datetime import datetime, timedelta
from ueosio import sign_tx, DataStream, get_expiration, get_tapos_info, build_push_transaction_body

tx='{"delay_sec":0,"max_cpu_usage_ms":0,"actions":[{"account":"eosio","name":"newaccount","data":{"creator":"argentinatls","name":"chittychitty","owner":{"threshold":1,"keys":[{"key":"EOS6wDfFCJqNYD3mteMZ4nEaYzx6s4TKKXeU4aQu35vyvexMWSdi5","weight":1}],"accounts":[],"waits":[]},"active":{"threshold":1,"keys":[{"key":"EOS6wDfFCJqNYD3mteMZ4nEaYzx6s4TKKXeU4aQu35vyvexMWSdi5","weight":1}],"accounts":[],"waits":[]}},"authorization":[{"actor":"argentinatls","permission":"active"}]},{"account":"eosio","name":"buyram","data":{"payer":"argentinatls","receiver":"chittychitty","quant":"5.0000 TLOS"},"authorization":[{"actor":"argentinatls","permission":"active"}]},{"account":"eosio","name":"delegatebw","data":{"from":"argentinatls","receiver":"chittychitty","stake_net_quantity":"2.1234 TLOS","stake_cpu_quantity":"2.1234 TLOS","transfer":true},"authorization":[{"actor":"argentinatls","permission":"active"}]}]}'
tx = json.loads(tx)

# Get chain info
info = r.get('https://api.testnet.telos.eosargentina/v1/chain/get_info').json()
ref_block_num, ref_block_prefix = get_tapos_info(info['last_irreversible_block_id'])

# Wrap tx 1
data = tx['actions'][0]['data']
ds = DataStream()
ds.pack_name(data['creator'])
ds.pack_name(data['name'])
ds.pack_authority(data['owner'])
ds.pack_authority(data['active'])
# Wrap tx 2
ds2 = DataStream()
data = tx['actions'][1]['data']
ds2.pack_name(data['payer'])
ds2.pack_name(data['receiver'])
ds2.pack_asset(data['quant'])
# Wrap tx 3
ds3 = DataStream()
data = tx['actions'][2]['data']
ds3.pack_name(data['from'])
ds3.pack_name(data['receiver'])
ds3.pack_asset(data['stake_net_quantity'])
ds3.pack_asset(data['stake_cpu_quantity'])
ds3.pack_bool(data['transfer'])

tx['actions'][0]['data'] = binascii.hexlify(ds.getvalue()).decode('utf-8')
tx['actions'][1]['data'] = binascii.hexlify(ds2.getvalue()).decode('utf-8')
tx['actions'][2]['data'] = binascii.hexlify(ds3.getvalue()).decode('utf-8')

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

# Sign tx, make sure to have correct chain id
auth = tx['actions'][0]['authorization'][0]
private_key = getpass("Enter private key for %s@%s: " % (auth['actor'], auth['permission']))
tx_id, tx = sign_tx(
   "1eaa0824707c8c16bd25145493bf062aecddfeb56c736f6ba6397f3195f33c9f",
   tx,
   private_key
)
ds = DataStream()
ds.pack_transaction(tx)
packed_trx = binascii.hexlify(ds.getvalue()).decode('utf-8')
tx = build_push_transaction_body(tx['signatures'][0], packed_trx)

# Push tx
res = r.post('https://api.testnet.telos.eosargentina/v1/chain/push_transaction', json=tx).json()
print(res)
