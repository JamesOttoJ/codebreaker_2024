from datetime import datetime
import hashlib

start = int(datetime(2024, 8, 10, 22, 53).timestamp() / 60)
end = int(datetime(2024, 8, 13, 18, 22).timestamp() / 60)
goal = b'\x7c\x30\x03\x7e\xec\x00\xb2\xe1\xf4\x09\xea\x92\x27\x2d\x1e\x80'

for i in range(end - start):
    digest = hashlib.md5(str(start + i).encode('utf-8')).digest()
    #print(digest)
    if digest == goal:
        print("Found:" + str((start + i) * 60))

