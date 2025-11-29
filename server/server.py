import os
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 

def load_client_public_key():
    """
    Carrega a chave pública do cliente a partir de um arquivo PEM.
    
    Returns:
        RSA key object: A chave pública do cliente.
    """
    path = "../keys/client_public.pem"
    with open(path, "rb") as f:
        key = RSA.import_key(f.read())
    return key

def generate_nonce():
    """
    Gera um nonce aleatório de 32 bytes.
    
    Returns:
        bytes: O nonce gerado.
    """
    return os.urandom(32)

def encrypt_challenge(nonce, public_key):
    """
    Criptografa o nonce usando a chave pública do cliente.
    
    Args:
        nonce (bytes): O nonce a ser criptografado.
        public_key (RSA key object): A chave pública do cliente.
    
    Returns:
        str: O nonce criptografado em Base64.
    """
    cipher = PKCS1_v1_5.new(public_key)
    encrypted = cipher.encrypt(nonce)
    return base64.b64encode(encrypted).decode()

def generate_challenge():
    """
    Gera um challenge criptografado para o cliente.
    
    Returns:
        bytes: O nonce original gerado.
    """
    public_key = load_client_public_key()
    nonce = generate_nonce()
    encrypted_nonce = encrypt_challenge(nonce, public_key)

    print("\n======== Challenge gerado e enviado ao cliente ========")
    print(encrypted_nonce)
    print("========================================================")

    return nonce

def get_client_response():
    """
    Obtém a resposta do cliente criptografada.
    
    Returns:
        bytes: A resposta do cliente decodificada.
    """
    print("Cole aqui a resposta do cliente (Base64):")
    response_b64 = input("> ")
    return base64.b64decode(response_b64.encode())

def validate_response(original_nonce, client_response):
    """
    Valida a resposta do cliente comparando com o nonce original.
    
    Args:
        original_nonce (bytes): O nonce original gerado.
        client_response (bytes): A resposta do cliente decodificada.
    """
    if original_nonce == client_response:
        print("\n AUTENTICADO!")
    else:
        print("\n FALHA: Resposta não corresponde ao nonce original.")

def main():
    """
    Função principal do servidor.
    """
    print("\n=== Servidor: Gerando challenge... ===\n")
    original_nonce = generate_challenge()

    print("\n=== Aguardando resposta do cliente... ===\n")
    client_response = get_client_response()

    print("\n=== Validando resposta do cliente... ===\n")
    validate_response(original_nonce, client_response)

if __name__ == "__main__":
    main()