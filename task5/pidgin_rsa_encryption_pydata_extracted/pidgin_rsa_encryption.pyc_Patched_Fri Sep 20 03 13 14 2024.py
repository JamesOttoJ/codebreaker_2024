# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: pidgin_rsa_encryption.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import sys
import math
import base64
import random
from Crypto.PublicKey import RSA
from rsa import core

def load_public_key(pub_key):
    try:
        with open(pub_key, 'rb') as f:
            public_key = RSA.import_key(f.read())
            return public_key
    except:
        pass
    print('public key not found')
    sys.exit(1)

def load_private_key(password, priv_key):
    try:
        with open(priv_key, 'rb') as f:
            try:
                private_key = RSA.import_key(f.read(), password)
            except:
                print('Incorrect password')
                sys.exit(1)
            return private_key
    except:
        pass
    print('private key not found or password incorrect')
    sys.exit(1)

def encrypt_chunk(chunk, public_key):
    k = math.ceil(public_key.n.bit_length() / 8)
    pad_len = k - len(chunk)
    random.seed(a='None')
    padding = bytes([random.randrange(1, 255) for i in range(pad_len - 3)])
    padding = b'\x00\x02' + padding + b'\x00'
    padded_chunk = padding + chunk.encode()
    input_nr = int.from_bytes(padded_chunk, byteorder='big')
    crypted_nr = core.encrypt_int(input_nr, public_key.e, public_key.n)
    encrypted_chunk = crypted_nr.to_bytes(k, byteorder='big')
    return base64.b64encode(encrypted_chunk).decode()

def decrypt_chunk(encrypted_chunk, private_key):
    try:
        decoded_chunk = base64.b64decode(encrypted_chunk)
    except:
        print('Invalid message')
        sys.exit(1)
    input_nr = int.from_bytes(decoded_chunk, byteorder='big')
    decrypted_nr = core.decrypt_int(input_nr, private_key.d, private_key.n)
    decrypted_chunk = decrypted_nr.to_bytes(256, byteorder='big')
    unpadded_chunk = decrypted_chunk[2:]
    end_of_pad = unpadded_chunk.find(b'\x00')
    unpadded_chunk = unpadded_chunk[end_of_pad + 1:]
    return unpadded_chunk.decode()

def encrypt_message(message, public_key):
    chunk_size = 245
    encrypted_chunks = []
    for i in range(0, len(message), chunk_size):
        chunk = message[i:i + chunk_size]
        encrypted_chunk = encrypt_chunk(chunk, public_key)
        encrypted_chunks.append(encrypted_chunk)
    return ' '.join(encrypted_chunks)

def decrypt_message(encrypted_message, private_key):
    encrypted_chunks = encrypted_message.split(' ')
    decrypted_message = ''.join((decrypt_chunk(chunk, private_key) for chunk in encrypted_chunks))
    return decrypted_message

def send_message_to_pidgin(message, recipient):
    import dbus
    bus = dbus.SessionBus()
    try:
        purple = bus.get_object('im.pidgin.purple.PurpleService', '/im/pidgin/purple/PurpleObject')
    except:
        print('Could not send message to pidgin - not connected')
        sys.exit(1)
    iface = dbus.Interface(purple, 'im.pidgin.purple.PurpleInterface')
    accounts = iface.PurpleAccountsGetAllActive()
    if not accounts:
        print('No active Pidgin accounts found.')
        return
    account = accounts[0]
    conv = iface.PurpleConversationNew(1, account, recipient)
    im = iface.PurpleConvIm(conv)
    iface.PurpleConvImSend(im, message)

def main():
    if len(sys.argv) < 2:
        print('Usage: python pidgin_rsa_encryption.py <mode> [<recipient> <message> <public_key> | <encrypted_message> <password>]')
        print('Modes:')
        print('  send <recipient> <message> <public_key> - Send an encrypted message')
        print('  receive <encrypted_message> <password> <private_key> - Decrypt the given encrypted message')
        sys.exit(1)
    mode = sys.argv[1]
    if mode == 'send' and len(sys.argv) != 5:
        print('Usage: python pidgin_rsa_encryption.py send <recipient> <message> <public_key>')
        sys.exit(1)
        recipient = sys.argv[2]
        message = sys.argv[3]
        pub_key = sys.argv[4]
        public_key = load_public_key(pub_key)
        encrypted_message = encrypt_message(message, public_key)
        send_message_to_pidgin(encrypted_message, recipient)
        print('Encrypted message sent to Pidgin.')
    elif mode == 'receive' and len(sys.argv) != 5:
        print('Usage: python pidgin_rsa_encryption.py receive <encrypted_message> <password> <private_key>')
        sys.exit(1)
        encrypted_message = sys.argv[2]
        password = sys.argv[3]
        priv_key = sys.argv[4]
        private_key = load_private_key(password, priv_key)
        decrypted_message = decrypt_message(encrypted_message, private_key)
        print('Decrypted message:', decrypted_message)
    else:
        print("Invalid mode. Use 'send' or 'receive'.")
if __name__ == '__main__':
    main()
