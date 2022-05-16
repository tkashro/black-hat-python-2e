#!/usr/bin/env python3
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from io import BytesIO

import base64
import zlib


def generate():
    new_key = RSA.generate(2048)
    private_key = new_key.exportKey()
    public_key = new_key.public_key().exportKey()

    with open('key.pri', 'wb') as f:
        f.write(private_key)

    with open('key.pub', 'wb') as f:
        f.write(public_key)


def get_rsa_cipher(key_type):
    with open(f'key.{key_type}') as f:
        key = f.read()
    rsa_key = RSA.importKey(key)
    return PKCS1_OAEP.new(rsa_key), rsa_key.size_in_bytes()


def encrypt(plain_text):
    compressed_text = zlib.compress(plain_text)

    session_key = get_random_bytes(16)
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(compressed_text)

    cipher_rsa, _ = get_rsa_cipher('pub')
    encrypted_session_key = cipher_rsa.encrypt(session_key)

    msg_payload = encrypted_session_key + cipher_aes.nonce + tag + ciphertext
    encrypted = base64.encodebytes(msg_payload)
    return encrypted


def decrypt(encrypted):
    encrypted_bytes = BytesIO(base64.decodebytes(encrypted))
    cipher_rsa, key_size_in_bytes = get_rsa_cipher('pri')

    encrypted_session_key = encrypted_bytes.read(key_size_in_bytes)
    nonce = encrypted_bytes.read(16)
    tag = encrypted_bytes.read(16)
    ciphertext = encrypted_bytes.read()

    session_key = cipher_rsa.decrypt(encrypted_session_key)
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    decrypted = cipher_aes.decrypt_and_verify(ciphertext, tag)

    plain_text = zlib.decompress(decrypted)
    return plain_text


if __name__ == '__main__':
    # generate() # run this first.

    # comment this lines when uncomment generate()
    plaintext = b'hey there you.'
    print(decrypt(encrypt(plaintext)))
