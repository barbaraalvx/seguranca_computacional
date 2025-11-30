import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

def load_client_private_key():
    """
    Carrega a chave privada do cliente a partir de um arquivo PEM.
    
    Returns:
        RSA key object: A chave privada do cliente.
    """
    path = "keys/client_private.pem"
    with open(path, "rb") as f:
        key = RSA.import_key(f.read())
    return key

def decrypt_challenge(encrypted_b64, private_key):
    # Remove quebras de linha e espaços extras
    encrypted_b64 = "".join(encrypted_b64.split())
    encrypted_bytes = base64.b64decode(encrypted_b64)
    
    from Crypto.Cipher import PKCS1_v1_5
    cipher = PKCS1_v1_5.new(private_key)
    sentinel = None
    decrypted = cipher.decrypt(encrypted_bytes, sentinel)
    return decrypted

def main():
    print("=== Cliente RSA ===\n")

    # 1. Carregar chave privada do cliente
    private_key = load_client_private_key()
    print("Chave privada carregada com sucesso.\n")

    # 2. Receber challenge do servidor (copiar e colar)
    print("Cole aqui o challenge que o servidor gerou (Base64):")
    encrypted_challenge = input("> ")

    # 3. Decifrar o challenge
    nonce = decrypt_challenge(encrypted_challenge, private_key)
    print("\nNonce decifrado com sucesso!")

    # 4. Converter para Base64 e mostrar (resposta para o servidor)
    response_b64 = base64.b64encode(nonce).decode()
    print("\nResposta (Base64) para enviar de volta ao servidor:")
    print(response_b64)

if __name__ == "__main__":
    main()
