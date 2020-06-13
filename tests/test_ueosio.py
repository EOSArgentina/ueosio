from ueosio import __version__
from ueosio import DataStream
import json
def test_version():
    assert __version__ == '0.1.0'

def test_pack_authority():
    
    authority = json.loads('''
    { 
        "threshold":1,
        "keys":[
            {
                "key":"EOS6wDfFCJqNYD3mteMZ4nEaYzx6s4TKKXeU4aQu35vyvexMWSdi5",
                "weight":1
            }
        ],
        "accounts":[{
            "permission" : {
                "actor" : "menem",
                "permission" : "active"
            },
            "weight" : 1
        }],
        "waits":[]
    }
    ''')

    ds = DataStream()
    ds.pack_authority(authority)
    
    ds = DataStream(ds.getvalue())
    r = ds.unpack_authority()

    assert( r['threshold'] == 1 )
    assert( len(r['keys']) == 1 )
    assert( r['keys'][0]['key'] == 'EOS6wDfFCJqNYD3mteMZ4nEaYzx6s4TKKXeU4aQu35vyvexMWSdi5' )
    assert( r['keys'][0]['weight'] == 1 )
    assert( len(r['accounts']) == 1 )
    assert( r['accounts'][0]['permission']['actor']  == 'menem' )
    assert( r['accounts'][0]['permission']['permission']  == 'active' )
    assert( r['accounts'][0]['weight'] == 1 )
    assert( len(r['waits']) == 0 )


