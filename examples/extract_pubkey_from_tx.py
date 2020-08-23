stx = """
{
  "expiration": "2020-06-24T23:04:03",
  "ref_block_num": 50971,
  "ref_block_prefix": 2411618883,
  "max_net_usage_words": 0,
  "max_cpu_usage_ms": 0,
  "delay_sec": 0,
  "context_free_actions": [],
  "actions": [{
      "account": "evolutiondex",
      "name": "nop",
      "authorization": [{
          "actor": "evolutiondex",
          "permission": "active"
        }
      ],
      "data": ""
    }
  ],
  "transaction_extensions": [],
  "signatures": [
    "SIG_K1_JveJGJxRvsCGamQpugco2JrZwC2HVM7rkdCkhrZeytPgb8qHyk9nEQEsWuwJej23hUUUttTWTpKsKDZ29exgSWyyHZxVzK"
  ],
  "context_free_data": []
}
"""

import json
tx = json.loads(stx)

from ueosio.ds import DataStream
from cryptos import ecdsa_raw_recover, decode_sig
from cryptos import from_byte_to_int, decode, encode_pubkey

import hashlib
import binascii

dsp = DataStream()
dsp.pack_transaction(tx)
packed_trx = dsp.getvalue()

# m = hashlib.sha256()
# m.update(packed_trx)
# tx_id = binascii.hexlify(m.digest()).decode('utf-8')
#print(tx_id)

def get_sig_hash(chain_id):
  zeros = '0000000000000000000000000000000000000000000000000000000000000000'
  ds = DataStream()
  ds.pack_checksum256(chain_id)
  ds.write(packed_trx)
  ds.pack_checksum256(zeros)
  m = hashlib.sha256()
  m.update(ds.getvalue())
  return binascii.hexlify(m.digest()).decode('utf-8')

sig_hash = get_sig_hash("aca376f206b8fc25a6ed44dbdc66547c36c6c33e3a119ffbeaef943642f0e906")
#print(sig_hash)


def print_pub(sig_hash, sig):
    ds = DataStream()
    print("Signature => %s" % sig)
    ds.pack_signature(sig)
    sig0 = ds.getvalue()[1:]

    #print(len(sig0))
    #print(sig0)

    v,r,s = from_byte_to_int(sig0[0]), decode(sig0[1:33], 256), decode(sig0[33:], 256)
    # v,r,s = decode_sig(sig0[1:])
    #print(v,r,s)
    Q = ecdsa_raw_recover(sig_hash, (v,r,s))
    pub = encode_pubkey(Q, 'hex_compressed') if v >= 31 else encode_pubkey(Q, 'hex')
    #print(pub)

    ds = DataStream(bytes.fromhex("00"+pub))
    pub0 = ds.unpack_public_key()

    print(" |----> ", pub0)    

print_pub(sig_hash, tx['signatures'][0])
