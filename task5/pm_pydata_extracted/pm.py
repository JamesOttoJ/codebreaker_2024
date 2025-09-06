# Source Generated with Decompyle++
# File: pm.pyc (Python 3.11)

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


def generate_password(length = None):
    character_list = string.ascii_letters + string.digits + string.punctuation
    password = []
# WARNING: Decompyle incomplete


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


def save_password(filename = None, password = None, spassword = None):
    encrypted_password = encrypt_password(spassword, password)
# WARNING: Decompyle incomplete


def load_password(filename = None, password = None):
    pass
# WARNING: Decompyle incomplete


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
        password = getpass(prompt = 'Enter your master password: ')
        passhash = hashlib.md5(password.encode('utf-8')).hexdigest()
        dirname = passdir + '/' + passhash
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
            return None
        None('directory already exists for that master password')
        return None
    if None == 'add':
        password = getpass(prompt = 'Enter your master password: ')
        passhash = hashlib.md5(password.encode('utf-8')).hexdigest()
        dirname = os.path.expanduser('~') + '/.passwords/' + passhash
        if not os.path.isdir(dirname):
            print('Unknown master password, please init first')
            return None
        service = None('Enter the service name:  ')
        filename = dirname + '/' + service
        if os.path.isfile(filename):
            print('A password was already stored for that service.')
            return None
        spassword = None(f'''Enter the password to store for {service}:  ''')
        save_password(filename, password, spassword)
        return None
    if None == 'read':
        password = getpass(prompt = 'Enter your master password: ')
        passhash = hashlib.md5(password.encode('utf-8')).hexdigest()
        dirname = os.path.expanduser('~') + '/.passwords/' + passhash
        if not os.path.isdir(dirname):
            print('Unknown master password')
            return None
        service = None('Enter the service name:  ')
        filename = dirname + '/' + service
        if not os.path.isfile(filename):
            print('No password stored for that service using that master password')
            return None
        spassword = None(filename, password)
        print(f'''Password for {service}: {spassword}''')
        return None
    if None == 'gen':
        password = getpass(prompt = 'Enter your master password: ')
        passhash = hashlib.md5(password.encode('utf-8')).hexdigest()
        dirname = os.path.expanduser('~') + '/.passwords/' + passhash
        if not os.path.isdir(dirname):
            print('Unknown master password, please init first')
            return None
        service = None('Enter the service name:  ')
        filename = dirname + '/' + service
        if os.path.isfile(filename):
            print('A password was already stored for that service.')
            return None
        if not input('Enter the password length (default 18):  '):
            pass_len = None('18')
            spassword = generate_password(pass_len)
            save_password(filename, password, spassword)
            return None
        if input('Enter the password length (default 18):  ') == 'help':
            usage()
            return None
        None('Unknown command')
        return None

if __name__ == '__main__':
    main()
    return None
