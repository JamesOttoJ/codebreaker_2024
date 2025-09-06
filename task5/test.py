import string
import random
from Crypto.PublicKey import RSA
from rsa import core
import math
import base64
from functools import reduce

# character_list = string.ascii_letters + string.digits + string.punctuation
# print(character_list)
# print(len(character_list))

# random.seed(a='None')
# for i in range(10):
#     print(random.randrange(1, 255))
def nth_root(x, n):
    # Start with some reasonable bounds around the nth root.
    upper_bound = 1
    while upper_bound ** n <= x:
        upper_bound *= 2
    lower_bound = upper_bound // 2
    # Keep searching for a better result as long as the bounds make sense.
    while lower_bound < upper_bound:
        mid = (lower_bound + upper_bound) // 2
        mid_nth = mid ** n
        if lower_bound < mid and mid_nth < x:
            lower_bound = mid
        elif upper_bound > mid and mid_nth > x:
            upper_bound = mid
        else:
            # Found perfect nth root.
            return mid
    return mid + 1

def chinese_remainder(m, a):
    sum = 0
    prod = reduce(lambda acc, b: acc*b, m)
    for n_i, a_i in zip(m, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod

def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

mods = []

with open("./files/.keys/570RM_public_key.pem", "rb") as f:
    public_key = RSA.import_key(f.read())
    print("570RM:")
    print("\tn: " + str(public_key.n))
    print(math.ceil(public_key.n.bit_length()) / 8)
#    print("\te: " + str(public_key.e))
with open("./files/.keys/4C1D_public_key.pem", "rb") as f:
    public_key = RSA.import_key(f.read())
    print("4C1D:")
    print("\tn: " + str(public_key.n))
    mods.append(public_key.n)
    print(math.ceil(public_key.n.bit_length()) / 8)
#    print("\te: " + str(public_key.e))
with open("./files/.keys/PL46U3_public_key.pem", "rb") as f:
    public_key = RSA.import_key(f.read())
    print("PL46U3:")
    print("\tn: " + str(public_key.n))
    mods.append(public_key.n)
    print(math.ceil(public_key.n.bit_length()) / 8)
#    print("\te: " + str(public_key.e))
with open("./files/.keys/V3RM1N_public_key.pem", "rb") as f:
    public_key = RSA.import_key(f.read())
    print("V3RM1N:")
    print("\tn: " + str(public_key.n))
    mods.append(public_key.n)
    print(math.ceil(public_key.n.bit_length()) / 8)
#   print("\te: " + str(public_key.e))

remainders = []
remainders.append(int.from_bytes(base64.b64decode("Xe7bFwXKYIyAh5Cd9d0cvHuqfPvX9180fQI8/q/hKe+y+zndg4yaP63Iq8xZtm8qucChx7AS1s7k8GqG9ZuyWVL/VPo9vRmJInmb/pEaEHlhFW4skWKPpNvLCPmZ6mfLiDaQpymqTLsAGeVgmbnR+WMWqaf9D6pO/vEQi3Mq6jQHLHaEsXEgf4hGtgilUWtw5wdqp9zxMMHnaOG8d5iJYzgC5FqmCpF7/ZW8Rp87OPnq2CF3AZdCGPKZM40bY+7SFVjs5PibV8NzKqWQJ4eFsE7Hwl838Dqy7nuVN0lLxMkgQ95FHzukDnC9Gy9Mh+wDdxg6ciFzZku05Svj+rCJQQ=="), byteorder="big"))
remainders.append(int.from_bytes(base64.b64decode("Xe7bFwXKYIyAh5Cd9d0cvHuqfPvX9180fQI8/q/hKe+y+zndg4yaP63Iq8xZtm8qucChx7AS1s7k8GqG9ZuyWVL/VPo9vRmJInmb/pEaEHlhFW4skWKPpNvLCPmZ6mfLiDaQpymqTLsAGeVgmbnR+WMWqaf9D6pO/vEQi3Mq6jQHLHaEsXEgf4hGtgilUWtw5wdqp9zxMMHnaOG8d5iJYzgC5FqmCpF7/ZW8Rp87OPnq2CF3AZdCGPKZM40bY+7SFVjs5PibV8NzKqWQJ4eFsE7Hwl838Dqy7nuVN0lLxMkgQ95FHzukDnC9Gy9Mh+wDdxg6ciFzZku05Svj+rCJQQ=="), byteorder="big"))
remainders.append(int.from_bytes(base64.b64decode("Xe7bFwXKYIyAh5Cd9d0cvHuqfPvX9180fQI8/q/hKe+y+zndg4yaP63Iq8xZtm8qucChx7AS1s7k8GqG9ZuyWVL/VPo9vRmJInmb/pEaEHlhFW4skWKPpNvLCPmZ6mfLiDaQpymqTLsAGeVgmbnR+WMWqaf9D6pO/vEQi3Mq6jQHLHaEsXEgf4hGtgilUWtw5wdqp9zxMMHnaOG8d5iJYzgC5FqmCpF7/ZW8Rp87OPnq2CF3AZdCGPKZM40bY+7SFVjs5PibV8NzKqWQJ4eFsE7Hwl838Dqy7nuVN0lLxMkgQ95FHzukDnC9Gy9Mh+wDdxg6ciFzZku05Svj+rCJQQ=="), byteorder="big"))

print("\nChinese: " + nth_root(chinese_remainder(mods, remainders), 3).to_bytes(256, byteorder="big").hex())

with open("./files/.keys/570RM_public_key.pem", "rb") as f:
    public_key = RSA.import_key(f.read())
    random.seed(a='None')
    padding = bytes([random.randrange(1, 255) for i in range(253)])
    padding = b'\x00\x02' + padding + b'\x00'
    padding = int.from_bytes(padding, byteorder='big')
    print("\npadding: " + padding.to_bytes(256, byteorder="big").hex())
    power_padding = padding * padding * padding
    print ("\nPower padding: " + power_padding.to_bytes(1024, byteorder="big").hex())
    
    test = int.from_bytes(base64.b64decode("dR6UPSE09Z9lRllcmBZWprmm0LFzjlIBmUq6MuLzIjOZWUmIaMuVHFs3BP9MwmLmbPWIpU7hlW6axPYu5SXt9x2fsYvWH8rz7fnJjea4XTruUC3Fp294daKONPF5g/8B9k6mQFQatQzXzMYvz2hd6pO05uDbKI7BUIMNDv+99sKwch09IINNPcwx14spGlBaU+9qPULm0Enqx559Ek7PmUNB20etckX/0yl2HXfEbcPbpw0HLcEzCqyZQ54ug3RSFfAbVbCsTCmmjh/cRV080CU4MZ2Q5YRsEMsljv3t3uKrMRJObqNgjJPD8twB/HMuQgLbg4kNkMJE8yRVgiHhXA=="), byteorder="big")
    
    base_multiple = power_padding // public_key.n
    test = test + (public_key.n * base_multiple)

    for i in range(1):
        # print("\ntest: " + test.to_bytes(1024, byteorder="big").hex())
        # print("\ntest: " + str(test))
        root_test = nth_root(test, 3).to_bytes(256, byteorder="big")
        if (root_test[:2] == b'\x00\x02'):
            # print("\ntest root: " + root_test.hex())
            # print("\ntest root: " + str(nth_root(test, 3)))
            result = root_test[2:]
            start = result.find(b'\x00')
            result = result[start + 1:]
            if (result.hex() != ""):
                # print("\ntest root: " + root_test.hex())
                print("\nResult: " + result.hex())
            # break
        test = test + public_key.n
    # test = -1 * nth_root(core.encrypt_int(input_nr, public_key.e, public_key.n), 3) + nth_root(core.encrypt_int(input_nr+2, public_key.e, public_key.n), 3)
    # print("difference: " + test.to_bytes(256, byteorder="big").hex())
    # print("input^3: " + (input_nr * input_nr * input_nr).to_bytes(1024, byteorder="big").hex())
    # crypted_nr = core.encrypt_int(input_nr, public_key.e, public_key.n)
    # print("crypted: " + crypted_nr.to_bytes(256, byteorder="big").hex())

#print(nth_root(int.from_bytes(base64.b64decode("Xe7bFwXKYIyAh5Cd9d0cvHuqfPvX9180fQI8/q/hKe+y+zndg4yaP63Iq8xZtm8qucChx7AS1s7k8GqG9ZuyWVL/VPo9vRmJInmb/pEaEHlhFW4skWKPpNvLCPmZ6mfLiDaQpymqTLsAGeVgmbnR+WMWqaf9D6pO/vEQi3Mq6jQHLHaEsXEgf4hGtgilUWtw5wdqp9zxMMHnaOG8d5iJYzgC5FqmCpF7/ZW8Rp87OPnq2CF3AZdCGPKZM40bY+7SFVjs5PibV8NzKqWQJ4eFsE7Hwl838Dqy7nuVN0lLxMkgQ95FHzukDnC9Gy9Mh+wDdxg6ciFzZku05Svj+rCJQQ=="), byteorder="big"), 3).to_bytes(256, byteorder="big").hex())
#print(nth_root(int.from_bytes(base64.b64decode("dR6UPSE09Z9lRllcmBZWprmm0LFzjlIBmUq6MuLzIjOZWUmIaMuVHFs3BP9MwmLmbPWIpU7hlW6axPYu5SXt9x2fsYvWH8rz7fnJjea4XTruUC3Fp294daKONPF5g/8B9k6mQFQatQzXzMYvz2hd6pO05uDbKI7BUIMNDv+99sKwch09IINNPcwx14spGlBaU+9qPULm0Enqx559Ek7PmUNB20etckX/0yl2HXfEbcPbpw0HLcEzCqyZQ54ug3RSFfAbVbCsTCmmjh/cRV080CU4MZ2Q5YRsEMsljv3t3uKrMRJObqNgjJPD8twB/HMuQgLbg4kNkMJE8yRVgiHhXA=="), byteorder="big"), 3).to_bytes(256, byteorder="big").hex())
#print(nth_root(int.from_bytes(base64.b64decode("VqpzVBxjmQ5/+trKindpobyE+Z1arWOMxSn8Njl5hBMX0OJ+5neh5yvN9MCE4kb/qEGzlYOjVuRX9oG/Mzv3xpp9lOk8kz8Ds8sAMWQ9Bs1qnUipT1LMBRd50uDhAXwysEtY+J3dP74uEeWnuKfgx1yUi378rheOCBwoTluN+ytRLrbi9Tzfb02gpuXQRTVB/SPRWbhZ7oLdZTxaoAhqBipvUnKcOwbkXlmQcac8kio2271MLlO9b+QeT8Tp7tLAj18sPt2N8Vs8VWkT1dLzE2MhUF7PON3wEH85qlj7b3cFNPm2rG1U0in8NoPdrRWbM7SucKiKHSeZ7Tum/JjE9g=="), byteorder="big"), 3).to_bytes(256, byteorder="big").hex())
#print(nth_root(int.from_bytes(base64.b64decode("TrdkBHkRLGxxNJLAOSeJiDq0Alyr9EoXc2FnxZjDpgJLfkPjCSU/Mu2ub6BerVRMISMDBMTG0d0PiA2ZSwwAHtWTetPfKl9+J21ZHrNMWt6Qjmtgna3Y0BpM2OxClWzwcejbiiOstmbMSuU1LbHUglRmCoMr33WOvjXDVK3mDHwIHiLCGCnStRDko4Id/QjdTn39JQ88aEGv1ttnOCGwjxU2pCQWSAhSuc9oGkgxuYQiKCrz2q082zoV8AUCb6x+i8niyuky6QlHMtzCS34y/SYJ11Eaa3o9aETO3cZb/+bTQTMbPI5NKSkAkaFJNT8tOcu64F3oTg2kAfvpubUZwQ=="), byteorder="big"), 3).to_bytes(256, byteorder="big").hex())
