from Crypto.PublicKey import RSA
from sympy import gcd

public_key1 = RSA.import_key(open("./files/.keys/570RM_public_key.pem", "rb").read())
public_key2 = RSA.import_key(open("./files/.keys/4C1D_public_key.pem", "rb").read())
public_key3 = RSA.import_key(open("./files/.keys/PL46U3_public_key.pem", "rb").read())
public_key4 = RSA.import_key(open("./files/.keys/V3RM1N_public_key.pem", "rb").read())

print("GCD 1,2: " + str(gcd(public_key1.n, public_key2.n)))
print("GCD 1,3: " + str(gcd(public_key1.n, public_key3.n)))
print("GCD 1,4: " + str(gcd(public_key1.n, public_key4.n)))
print("GCD 2,3: " + str(gcd(public_key2.n, public_key3.n)))
print("GCD 2,4: " + str(gcd(public_key2.n, public_key4.n)))
print("GCD 3,4: " + str(gcd(public_key3.n, public_key4.n)))
