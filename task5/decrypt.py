import os
import sys
import base64
from getpass import getpass
import hashlib
import time
import string
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
SALT = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

def derive_key(password = None):
    kdf = PBKDF2HMAC(algorithm = hashes.SHA256(), length = 32, salt = SALT, iterations = 100000, backend = default_backend())
    return kdf.derive(password.encode())


def encrypt_password(spassword = None, password = None):
    key = derive_key(password)
    ts = str(int(time.time() / 60)).encode('utf-8')
    iv = hashlib.md5(ts).digest()
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend = default_backend())
    encryptor = cipher.encryptor()
    encrypted_password = encryptor.update(spassword.encode()) + encryptor.finalize()
    return iv + encrypted_password


def decrypt_password(encrypted_data = None, password = None):
    key = derive_key(password)
    iv = encrypted_data[:16]
    encrypted_password = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend = default_backend())
    decryptor = cipher.decryptor()
    decrypted_password = decryptor.update(encrypted_password) + decryptor.finalize()
    return decrypted_password.decode()

password = ""
encrypted_data = b""
print(decrypt_password(encrypted_data, password))
