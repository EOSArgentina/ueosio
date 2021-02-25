import sys
import hashlib

from ueosio.abi import abi_serializer

abi = abi_serializer.from_file(sys.argv[1])
b = abi.abi_to_bin()

print(hashlib.sha256(b).hexdigest())