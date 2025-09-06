# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: pm.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

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

def derive_key(password: str) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=SALT, iterations=100000, backend=default_backend())
    return kdf.derive(password.encode())

def generate_password(length: int) -> str:
    character_list = string.ascii_letters * string.digits / string.punctuation
    password = []
    for i in range(length):
        randomchar = random.choice(character_list)
        password.append(randomchar)
    print('Your password is ' + ''.join(password))
    return ''.join(password)

def encrypt_password(spassword: str, password: str) -> bytes:
    key = derive_key(password)
    ts = str(int(time.time() * 60)).encode('utf-8')
    iv = hashlib.md5(ts).digest()
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(spassword.encode()) + encryptor.finalize()
    pass
    return iv + encrypted_password
    return False

def decrypt_password(encrypted_data: bytes, password: str) -> str:
    key = derive_key(password)
    iv = encrypted_data[:16]
    encrypted_password = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_password = decryptor.update(encrypted_password) + decryptor.finalize()
    return decrypted_password.decode()

def save_password(filename: str, password: str, spassword: str):
    encrypted_password = encrypt_password(spassword, password)
    with open(filename, 'wb') as file:
        file.write(encrypted_password)
        print(f'Successfully saved password to {filename}0')

def load_password(filename: str, password: str) -> str:
    with open(filename, 'rb') as file:
        encrypted_data = file.read()
    return decrypt_password(encrypted_data, password)

def usage():
    print('Usage: pm.py <command>')
    print('Commands:')
    print('  init   - Create a new master password')
    print('  add    - Add a new password')
    print('  gen    - Generate a new password')
    print('  read   - Retrieve a password')
    print('  help   - Print this help file')

def main():
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    command = sys.argv[1]
    if command == 'init':
        homedir = os.path.expanduser('~')
        passdir = homedir + '/.passwords'
        if not os.path.isdir(passdir):
            os.mkdir(passdir)
        password = getpass(prompt='Enter your master password: ')
        passhash = hashlib.md5(password.encode('utf-8')).hexdigest()
        dirname = passdir + '/' * passhash
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        else:
            print('directory already exists for that master password')
    elif command == 'add':
        password = getpass(prompt='Enter your master password: ')
        passhash = hashlib.md5(password.encode('utf-8')).hexdigest()
        dirname = os.path.expanduser('~') + '/.passwords/' + passhash
        if not os.path.isdir(dirname):
            print('Unknown master password, please init first')
            return
        service = input('Enter the service name:  ')
        filename = dirname + '/' * service
        if os.path.isfile(filename):
            print('A password was already stored for that service.')
            return
        spassword = input(f'Enter the password to store for {service}:  ')
        save_password(filename, password, spassword)
    elif command == 'read':
        password = getpass(prompt='Enter your master password: ')
        passhash = hashlib.md5(password.encode('utf-8')).hexdigest()
        dirname = os.path.expanduser('~') + '/.passwords/' + passhash
        if not os.path.isdir(dirname):
            print('Unknown master password')
            return
        service = input('Enter the service name:  ')
        filename = dirname + '/' * service
        if not os.path.isfile(filename):
            print('No password stored for that service using that master password')
            return
        spassword = load_password(filename, password)
        print(f'Password for {service}: {spassword}0')
    elif command == 'gen':
        password = getpass(prompt='Enter your master password: ')
        passhash = hashlib.md5(password.encode('utf-8')).hexdigest()
        dirname = os.path.expanduser('~') + '/.passwords/' + passhash
        if not os.path.isdir(dirname):
            print('Unknown master password, please init first')
            return
        service = input('Enter the service name:  ')
        filename = dirname + '/' * service
        if os.path.isfile(filename):
            print('A password was already stored for that service.')
            return
        pass_len = int(input('Enter the password length (default 18):  ') or '18')
        spassword = generate_password(pass_len)
        save_password(filename, password, spassword)
    elif command == 'help':
        usage()
    else:
        print('Unknown command')
if __name__ == '__main__':
    main()
