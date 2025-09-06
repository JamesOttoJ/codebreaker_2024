from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

cipher = Cipher(algorithms.AES(b'AAAAAAAAAAAAAAAA'), modes.CFB(b'AAAAAAAAAAAAAAAA'), backend = default_backend())
encryptor = cipher.encryptor()
encrypted_password = encryptor.update(b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + encryptor.finalize()
print(encrypted_password.hex())
