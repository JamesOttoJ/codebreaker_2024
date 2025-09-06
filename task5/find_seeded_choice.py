import random
import string
from datetime import datetime
import hashlib
from Crypto.PublicKey import RSA
from pidgin_decrypt import encrypt_chunk

def generate_password(seed):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = []
    random.seed(a=seed)
    for i in range(18):
        rand_char = random.choice(characters)
        password.append(rand_char)
    return ''.join(password)

# start_time = int(datetime(2024, 8, 10, 22, 53).timestamp())
# end_time = int(datetime(2024, 8, 13, 18, 22).timestamp())

start_time = 1723417200 * 256
end_time = 1723417380 * 256
goal = b'\x7d\x10\x48\x3b\x27\x53\x6f\x1d\x52\x72\x3d\x51\x3d\x20\x14\x42'
passwords = []

public_key = RSA.import_key(open("./files/.keys/4C1D_public_key.pem", "rb").read())
ciphertext = "dR6UPSE09Z9lRllcmBZWprmm0LFzjlIBmUq6MuLzIjOZWUmIaMuVHFs3BP9MwmLmbPWIpU7hlW6axPYu5SXt9x2fsYvWH8rz7fnJjea4XTruUC3Fp294daKONPF5g/8B9k6mQFQatQzXzMYvz2hd6pO05uDbKI7BUIMNDv+99sKwch09IINNPcwx14spGlBaU+9qPULm0Enqx559Ek7PmUNB20etckX/0yl2HXfEbcPbpw0HLcEzCqyZQ54ug3RSFfAbVbCsTCmmjh/cRV080CU4MZ2Q5YRsEMsljv3t3uKrMRJObqNgjJPD8twB/HMuQgLbg4kNkMJE8yRVgiHhXA=="
#ciphertext = "Xe7bFwXKYIyAh5Cd9d0cvHuqfPvX9180fQI8/q/hKe+y+zndg4yaP63Iq8xZtm8qucChx7AS1s7k8GqG9ZuyWVL/VPo9vRmJInmb/pEaEHlhFW4skWKPpNvLCPmZ6mfLiDaQpymqTLsAGeVgmbnR+WMWqaf9D6pO/vEQi3Mq6jQHLHaEsXEgf4hGtgilUWtw5wdqp9zxMMHnaOG8d5iJYzgC5FqmCpF7/ZW8Rp87OPnq2CF3AZdCGPKZM40bY+7SFVjs5PibV8NzKqWQJ4eFsE7Hwl838Dqy7nuVN0lLxMkgQ95FHzukDnC9Gy9Mh+wDdxg6ciFzZku05Svj+rCJQQ=="

random.seed(a='None')
padding = bytes([random.randrange(1, 255) for i in range(256)])

with open("wordlist.txt", "w") as wordlist_file:
    for i in range(100000000):
        if i % 100000 == 0: 
            print(i)
        result = generate_password(start_time + i)
        #passwords.append(result)
        #wordlist_file.write(result + "\n")
        encrypt_chunk(result, public_key, padding, ciphertext)
        result = generate_password(end_time - i)
        #passwords.append(result)
        #wordlist_file.write(result + "\n")
        encrypt_chunk(result, public_key, padding, ciphertext)

print("Done generating passwords")

#for i in range(len(passwords)):
#    for j in range(len(passwords) - i - 1):
#        int_password1 = int.from_bytes(passwords[i][:18].encode('utf-8'), byteorder='little')
#        int_password2 = int.from_bytes(passwords[i+j+1][:18].encode('utf-8'), byteorder='little')
#        # print((int_password1 ^ int_password2).to_bytes(18, byteorder='little').hex())
#        if goal.hex() in (int_password1 ^ int_password2).to_bytes(18, byteorder='little').hex():
#            print(passwords[i])
#            print(passwords[i+j+1])
