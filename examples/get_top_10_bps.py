from ueosio.rpc import Api
  ## Change api endpoints for different eosio blockchains
  
# EOS Mainnnet
node = Api("https://eos.greymass.com")
for r in node.v1.chain.get_table_rows( code="eosio", scope="eosio", table="producers",
  key_type="float64", index_position="2", limit=10, json=True)["rows"]:
  print(r['owner'])
  
# WAX
node = Api("https://api.wax.eosargentina.io")
for r in node.v1.chain.get_table_rows( code="eosio", scope="eosio", table="producers",
  key_type="float64", index_position="2", limit=10, json=True)["rows"]:
  print(r['owner'])
