from Crypto.PublicKey import RSA

key = RSA.generate(2048)  # chave segura para demo

private_key = key.export_key()
with open("keys/client_private.pem", "wb") as f:
    f.write(private_key)

public_key = key.publickey().export_key()
with open("keys/client_public.pem", "wb") as f:
    f.write(public_key)

print("Chaves geradas em keys/")
