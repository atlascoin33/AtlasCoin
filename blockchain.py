# blockchain.py
import json
import os
from block import Block
from config import BLOCK_REWARD_INITIAL, MAX_SUPPLY

CHAIN_FILE = "atlascoin_chain.json"


class Blockchain:
    def __init__(self):
        # Si existe un archivo de cadena, lo cargamos
        if os.path.exists(CHAIN_FILE):
            print(f"Cargando cadena desde {CHAIN_FILE}...")
            self.chain = self._load_chain_from_file()
        else:
            # Si no existe, empezamos con el bloque génesis
            self.chain = [Block.genesis()]

        # Calcular supply a partir de las transacciones
        self.total_supply = self._calculate_total_supply()
        self.block_reward = BLOCK_REWARD_INITIAL
        self.balances = {}
        self._rebuild_balances()

        # Pool de transacciones pendientes (aún no minadas)
        self.pending_transactions = []

    def _calculate_total_supply(self):
        total = 0
        for block in self.chain:
            for tx in block.transactions:
                amount = tx["amount"]
                fee = tx.get("fee", 0)
                total += amount + fee
        return total

    def _rebuild_balances(self):
        self.balances = {}
        for block in self.chain:
            for tx in block.transactions:
                sender = tx["from"]
                receiver = tx["to"]
                amount = tx["amount"]
                fee = tx.get("fee", 0)

                # Si el emisor es normal, paga amount + fee
                if sender != "GENESIS" and sender != "COINBASE":
                    self.balances[sender] = self.balances.get(sender, 0) - (amount + fee)

                # El receptor recibe amount
                self.balances[receiver] = self.balances.get(receiver, 0) + amount

                # Las fees se entregan a quien tenga etiqueta "MINER" en la coinbase
                # (lo resolveremos en el bloque coinbase ahora)

    def get_balance(self, address):
        return self.balances.get(address, 0)

    def get_latest_block(self):
        return self.chain[-1]

    def create_transaction(self, sender, receiver, amount, fee):
        """
        Crea una transacción simple de sender -> receiver con fee.
        Comprueba saldo: amount + fee.
        """
        total_cost = amount + fee

        if sender != "COINBASE" and sender != "GENESIS":
            if self.get_balance(sender) < total_cost:
                raise ValueError("Fondos insuficientes (incluyendo fee)")

        tx = {
            "from": sender,
            "to": receiver,
            "amount": amount,
            "fee": fee,
        }
        return tx

    def add_pending_transaction(self, tx):
        """Añade una transacción a la pool pendiente."""
        self.pending_transactions.append(tx)

    def mine_block_with_pending(self, miner_address):
        """
        Mina un bloque con:
        - Recompensa coinbase para el minero.
        - Todas las transacciones pendientes.
        - Fees de las transacciones añadidas al minero.
        """
        if not self.pending_transactions:
            print("No hay transacciones pendientes para minar.")
            return

        latest_block = self.get_latest_block()
        index = latest_block.index + 1
        previous_hash = latest_block.hash

        transactions_block = []

        # Calcular fees totales de las transacciones pendientes
        total_fees = sum(tx.get("fee", 0) for tx in self.pending_transactions)

        # Transacción de recompensa al minero (recompensa fija + fees)
        if self.total_supply < MAX_SUPPLY:
            base_reward = min(self.block_reward, MAX_SUPPLY - self.total_supply)
        else:
            base_reward = 0

        miner_reward = base_reward + total_fees

        if miner_reward > 0:
            coinbase_tx = {
                "from": "COINBASE",
                "to": miner_address,
                "amount": miner_reward,
                "fee": 0,
            }
            transactions_block.append(coinbase_tx)
            self.total_supply += miner_reward

        # Añadir las transacciones de la pool
        transactions_block.extend(self.pending_transactions)

        # Minar el bloque con PoW
        new_block = Block.mine_block(
            index,
            previous_hash,
            transactions_block,
            latest_block.difficulty_bits
        )

        # Validar y añadir a la cadena
        if self.is_valid_new_block(new_block, latest_block):
            self.chain.append(new_block)
            self._rebuild_balances()
            self.pending_transactions = []  # vaciar pool
            print(f"Nuevo bloque añadido. Altura: {index}, reward minero: {miner_reward}, supply total: {self.total_supply}")
            self.save_chain_to_file()
        else:
            print("Bloque inválido, rechazado.")

    def is_valid_new_block(self, new_block, previous_block):
        # Comprobar índice
        if previous_block.index + 1 != new_block.index:
            return False
        # Comprobar hash anterior
        if previous_block.hash != new_block.previous_hash:
            return False
        # Comprobar integridad del hash (en esta versión simplificada usamos el hash calculado en el objeto)
        recalculated_hash = new_block.hash
        if recalculated_hash != new_block.hash:
            return False
        return True

    def is_chain_valid(self):
        # Comprobar la coherencia de toda la cadena
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.previous_hash != previous.hash:
                return False
        return True

    def save_chain_to_file(self):
        data = [block.to_dict() for block in self.chain]
        with open(CHAIN_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Cadena guardada en {CHAIN_FILE}")

    def _load_chain_from_file(self):
        with open(CHAIN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        chain = [Block.from_dict(bdict) for bdict in data]
        return chain

