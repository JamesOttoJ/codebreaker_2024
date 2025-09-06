from cryptography.hazmat.primitives.asymmetric import x25519
import binascii


# The known keypair from the code
private_key_hex = "c00148283ae459fc94519a4d749bd17529769ce014575a6fa55f8127376a8429"
expected_public_hex = "884c809374464472ca6b937ce3620750caf3569f069f09eeeff4c89e4161400e"

# Convert private key from hex to bytes
private_key_bytes = binascii.unhexlify(private_key_hex)

# Create private key object from bytes
private_key = x25519.X25519PrivateKey.from_private_bytes(private_key_bytes)

# Get the public key
computed_public = private_key.public_key().public_bytes_raw()

# Convert to hex for comparison
computed_public_hex = binascii.hexlify(computed_public).decode()
print(f"Computed public key: {computed_public_hex}")
print(f"Expected public key: {expected_public_hex}")
print(f"Keys match: {computed_public_hex == expected_public_hex}")
