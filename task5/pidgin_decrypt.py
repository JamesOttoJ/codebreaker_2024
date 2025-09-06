import sys
import math
import base64
import random
import threading
import os
from Crypto.PublicKey import RSA
from rsa import core

def encrypt_chunk(chunk, public_key, padding, goal):
    k = math.ceil(public_key.n.bit_length() / 8)
    #print(k)
    pad_len = k - len(chunk)
    padding = b'\x00\x02' + padding[:pad_len-3] + b'\x00'
    try:
        padded_chunk = padding + chunk.encode()
    except:
        print("Could not encode chunk")
        return None
    # print(len(padded_chunk))
    input_nr = int.from_bytes(padded_chunk, byteorder='big')
    #print(input_nr.to_bytes(k, byteorder="big").hex())
    try:
        crypted_nr = core.encrypt_int(input_nr, public_key.e, public_key.n)
    except:
        print("Could not encrypt message: " + chunk.hex())
        print("Input: " + str(input_nr.to_bytes(512, byteorder='big')))
        return None
    encrypted_chunk = crypted_nr.to_bytes(k, byteorder='big')
    #print(encrypted_chunk.hex())
    if (base64.b64encode(encrypted_chunk).decode() == goal):
        print(chunk.decode())
        #print("True")
        return True
    #print("False")
    return False

#public_key = RSA.import_key(open("./files/.keys/4C1D_public_key.pem", "rb").read())
#ciphertext = "dR6UPSE09Z9lRllcmBZWprmm0LFzjlIBmUq6MuLzIjOZWUmIaMuVHFs3BP9MwmLmbPWIpU7hlW6axPYu5SXt9x2fsYvWH8rz7fnJjea4XTruUC3Fp294daKONPF5g/8B9k6mQFQatQzXzMYvz2hd6pO05uDbKI7BUIMNDv+99sKwch09IINNPcwx14spGlBaU+9qPULm0Enqx559Ek7PmUNB20etckX/0yl2HXfEbcPbpw0HLcEzCqyZQ54ug3RSFfAbVbCsTCmmjh/cRV080CU4MZ2Q5YRsEMsljv3t3uKrMRJObqNgjJPD8twB/HMuQgLbg4kNkMJE8yRVgiHhXA=="
#ciphertext = "Xe7bFwXKYIyAh5Cd9d0cvHuqfPvX9180fQI8/q/hKe+y+zndg4yaP63Iq8xZtm8qucChx7AS1s7k8GqG9ZuyWVL/VPo9vRmJInmb/pEaEHlhFW4skWKPpNvLCPmZ6mfLiDaQpymqTLsAGeVgmbnR+WMWqaf9D6pO/vEQi3Mq6jQHLHaEsXEgf4hGtgilUWtw5wdqp9zxMMHnaOG8d5iJYzgC5FqmCpF7/ZW8Rp87OPnq2CF3AZdCGPKZM40bY+7SFVjs5PibV8NzKqWQJ4eFsE7Hwl838Dqy7nuVN0lLxMkgQ95FHzukDnC9Gy9Mh+wDdxg6ciFzZku05Svj+rCJQQ=="

#random.seed(a='None')
#padding = bytes([random.randrange(1, 255) for i in range(256)])
#encrypt_chunk(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', public_key, padding, ciphertext)
#encrypt_chunk(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01', public_key, padding, ciphertext)
#encrypt_chunk(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02', public_key, padding, ciphertext)
# print(encrypt_chunk("a", public_key, padding))
#with open("wordlist.txt", "rb") as wordlist_file:
#    threads = []
#    for line in wordlist_file:
        # print(line)
        # print(encrypt_chunk(line, public_key, padding))
#        line = line[:-1]
#        try:
#            line = line.decode('utf-8')
#        except:
#            print("Could not decode line: " + line.hex())
#            continue
        #while len(threads) > 30:
        #    for thread in threads:
        #        if not thread.is_alive():
        #            threads.remove(thread)
                    #print("Thread removed")
        
        #new_thread = threading.Thread(target=encrypt_chunk, args=[line, public_key, padding, ciphertext])
        #threads.append(new_thread)
        #print("Thread created")
#        if len(line) == 18:
#            encrypt_chunk(line, public_key, padding, ciphertext)
#print("not found!")
