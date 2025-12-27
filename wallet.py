# wallet.py
import os
import json
import secrets
import hashlib

WALLET_FILE = "wallet_atlas.json"


def generate_private_key():
    # Clave privada simple: 32 bytes aleatorios (no es estándar Bitcoin, pero sirve para aprender)
    return secrets.token_hex(32)


def private_to_public_key(private_key_hex: str) -> str:
    # Versión muy simplificada: derivar "clave pública" como hash de la privada
    # En un sistema real se usaría curva elíptica (secp256k1), aquí solo queremos un identificador reproducible
    pk_bytes = bytes.fromhex(private_key_hex)
    public_hash = hashlib.sha256(pk_bytes).hexdigest()
    return public_hash


def public_to_address(public_key_hex: str) -> str:
    # Dirección AtlasCoin simplificada: hash doble (SHA256 + RIPEMD160) con prefijo "ATC"
    sha = hashlib.sha256(bytes.fromhex(public_key_hex)).digest()
    ripe = hashlib.new("ripemd160", sha).hexdigest()
    address = "ATC" + ripe[:32]
    return address


def create_new_wallet():
    if os.path.exists(WALLET_FILE):
        print(f"Ya existe un wallet en {WALLET_FILE}.")
        return

    private_key = generate_private_key()
    public_key = private_to_public_key(private_key)
    address = public_to_address(public_key)

    wallet_data = {
        "private_key": private_key,
        "public_key": public_key,
        "address": address,
    }

    with open(WALLET_FILE, "w", encoding="utf-8") as f:
        json.dump(wallet_data, f, indent=2)

    print("Nuevo wallet AtlasCoin creado.")
    print("Archivo:", WALLET_FILE)
    print("Dirección:", address)


def load_wallet():
    if not os.path.exists(WALLET_FILE):
        print("No se encontró wallet. Crea uno nuevo con create_new_wallet().")
        return None
    with open(WALLET_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def sign_message(private_key_hex: str, message: str) -> str:
    """
    Firma simplificada: hash(message + private_key).
    NO es criptografía real segura, solo un esquema didáctico.
    """
    data = (message + private_key_hex).encode("utf-8")
    signature = hashlib.sha256(data).hexdigest()
    return signature


def verify_signature(private_key_hex: str, message: str, signature_hex: str) -> bool:
    """
    Verificación simplificada: volvemos a firmar el mensaje con la MISMA clave privada
    y comprobamos que coincide. En un sistema real se usaría solo la clave pública,
    aquí es solo para entender el flujo firma/verificación.
    """
    expected_sig = sign_message(private_key_hex, message)
    return expected_sig == signature_hex
if __name__ == "__main__":
    if not os.path.exists(WALLET_FILE):
        create_new_wallet()
    else:
        w = load_wallet()
        print("Wallet cargado desde archivo.")
        print("Dirección:", w["address"])

        # Prueba de firma
        test_msg = "Hola AtlasCoin"
        sig = sign_message(w["private_key"], test_msg)
        print("Mensaje de prueba:", test_msg)
        print("Firma:", sig)
        print("Verificación:",
              verify_signature(w["private_key"], test_msg, sig))
