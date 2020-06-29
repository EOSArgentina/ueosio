from ueosio.rpc import Api

kilin = Api("https://eos.greymass.com")
for r in kilin.v1.chain.get_table_rows( code="eosio", scope="eosio", table="producers",
  key_type="float64", index_position="2", limit=10, json=True)["rows"]:
  print(r['owner'])
