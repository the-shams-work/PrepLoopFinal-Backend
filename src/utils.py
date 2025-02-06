from __future__ import annotations

import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

with open("public.pem", "rb") as f:
    public_key = RSA.import_key(f.read())


def encrypt(data: str) -> str:
    cipher = PKCS1_OAEP.new(public_key)
    return base64.b64encode(cipher.encrypt(data.encode())).decode()


def decrypt(data: str) -> str:
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.decrypt(base64.b64decode(data)).decode()
