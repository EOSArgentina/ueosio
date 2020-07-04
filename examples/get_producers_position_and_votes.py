import time
import math
import datetime
from ueosio.rpc import Api

def get_producers(amount,api):
    endpoint = Api(api)
    producers = endpoint.v1.chain.get_table_rows(code="eosio",scope="eosio", table="producers", key_type="float64", index_position="2", limit=amount,json=True)["rows"]
    eosio_globals = endpoint.v1.chain.get_table_rows(code="eosio",scope="eosio", table="global", index_position="1", json=True)["rows"]
    for r in producers:
        position = list(producers).index(r)+1
        current_votes = get_votes(float(r['total_votes']))
        print("{} \t  {} \t {:,}".format(position,r['owner'],current_votes))
    
def get_votes(total_votes):
    epoch_2000=946684800
    seconds_per_week=604800 
    epoch_now = datetime.datetime.now().timestamp()
    weight= math.e**(((int(epoch_now-epoch_2000)/(seconds_per_week))/52)*math.log(2))
    return int(total_votes/weight/10000)


get_producers(50,"https://eos.greymass.com")
