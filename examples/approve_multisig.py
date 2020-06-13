import sys
import json
import binascii
import requests as r
from getpass import getpass
from datetime import datetime, timedelta
from ueosio import sign_tx, DataStream, get_expiration, get_tapos_info, build_push_transaction_body

### example tx
tx = {"delay_sec":0,"max_cpu_usage_ms":0,"actions":[{"account":"eosio.msig","name":"approve","data":{"proposer":"5du5xkgkki5x","proposal_name":"updatesysf31","level":{"actor":"2v5kbsi1qr2n","permission":"active"},"max_fee":400000000},"authorization":[{"actor":"2v5kbsi1qr2n","permission":"active"}]}]}

info = r.get('https://fio.testnet.eosargentina.io/v1/chain/get_info').json()
ref_block_num, ref_block_prefix = get_tapos_info(info['last_irreversible_block_id'])

data = tx['actions'][0]['data']
ds = DataStream()
ds.pack_name(data['proposer'])
ds.pack_name(data['proposal_name'])
ds.pack_permission_level(data['level'])
ds.pack_uint64(data['max_fee'])

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

auth = tx['actions'][0]['authorization'][0]
private_key = getpass("Enter private key for %s@%s: " % (auth['actor'], auth['permission']))

tx_id, tx = sign_tx(
   "b20901380af44ef59c5918439a1f9a41d83669020319a80574b804a5f95cbd7e",
   tx,
   private_key
)
ds = DataStream()
ds.pack_transaction(tx)
packed_trx = binascii.hexlify(ds.getvalue()).decode('utf-8')
tx = build_push_transaction_body(tx['signatures'][0], packed_trx)

res = r.post('https://fio.testnet.eosargentina.io/v1/chain/push_transaction', json=tx).json()
print(res)
