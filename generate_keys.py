from Crypto.PublicKey import RSA

print("[*] Generating RSA keys...")
key = RSA.generate(2048)

with open("keys/private.pem", "wb") as f:
    f.write(key.export_key())
    print("[*] Private key saved to keys/private.pem")

with open("keys/public.pem", "wb") as f:
    f.write(key.publickey().export_key())
    print("[*] Public key saved to keys/public.pem")

print("[*] Done")
