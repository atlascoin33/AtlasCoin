
# node.py
from blockchain import Blockchain

MINER_ADDRESS = "LOCAL_MINER"
def mostrar_menu():
    print("\n===== AtlasCoin Node =====")
    print("1. Ver balances")
    print("2. Crear transacción")
    print("3. Ver transacciones pendientes")
    print("4. Minar bloque")
    print("5. Ver información de la cadena")
    print("0. Salir")

def mostrar_balances(bc: Blockchain):
    print("\n--- Balances ---")
    if not bc.balances:
        print("No hay balances aún.")
        return
    for addr, bal in bc.balances.items():
        print(f"  {addr}: {bal} ATC")

def crear_transaccion(bc: Blockchain):
    print("\n--- Nueva transacción ---")
    sender = input("Dirección remitente (FROM): ").strip()
    receiver = input("Dirección destinataria (TO): ").strip()
    amount_str = input("Cantidad de ATC (amount): ").strip()
    fee_str = input("Fee (comisión) en ATC: ").strip()

    try:
        amount = float(amount_str)
        fee = float(fee_str)
    except ValueError:
        print("Cantidad o fee inválidas.")
        return

    try:
        tx = bc.create_transaction(sender, receiver, amount, fee)
        bc.add_pending_transaction(tx)
        print("Transacción añadida a la pool pendiente.")
    except ValueError as e:
        print(f"Error al crear transacción: {e}")

def ver_pendientes(bc: Blockchain):
    print("\n--- Transacciones pendientes ---")
    if not bc.pending_transactions:
        print("No hay transacciones pendientes.")
        return
    for i, tx in enumerate(bc.pending_transactions, start=1):
        fee = tx.get("fee", 0)
        print(f"{i}. {tx['from']} -> {tx['to']} : {tx['amount']} ATC (fee: {fee} ATC)")

def minar_bloque(bc: Blockchain):
    print("\n--- Minado de bloque ---")
    print(f"Minero: {MINER_ADDRESS}")
    bc.mine_block_with_pending(MINER_ADDRESS)

def info_cadena(bc: Blockchain):
    print("\n--- Información de la cadena ---")
    print("Número de bloques:", len(bc.chain))
    print("Supply total:", bc.total_supply)
    print("Cadena válida:", bc.is_chain_valid())
    print("Hash del último bloque:", bc.get_latest_block().hash)

def main():
    atlas_blockchain = Blockchain()
    print("AtlasCoin blockchain iniciada.")

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            mostrar_balances(atlas_blockchain)
        elif opcion == "2":
            crear_transaccion(atlas_blockchain)
        elif opcion == "3":
            ver_pendientes(atlas_blockchain)
        elif opcion == "4":
            minar_bloque(atlas_blockchain)
        elif opcion == "5":
            info_cadena(atlas_blockchain)
        elif opcion == "0":
            print("Saliendo del nodo AtlasCoin...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
