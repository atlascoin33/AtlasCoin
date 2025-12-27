# block.py
import time
import hashlib
import json
from config import GENESIS_MESSAGE, INITIAL_DIFFICULTY_BITS

def calculate_hash(index, previous_hash, timestamp, transactions, nonce, difficulty_bits):
    block_data = {
        "index": index,
        "previous_hash": previous_hash,
        "timestamp": timestamp,
        "transactions": transactions,
        "nonce": nonce,
        "difficulty_bits": difficulty_bits,
    }
    value = json.dumps(block_data, sort_keys=True).encode("utf-8")
    return hashlib.sha256(value).hexdigest()

def hash_meets_difficulty(hash_hex, difficulty_bits):
    hash_int = int(hash_hex, 16)
    target = 2 ** (256 - difficulty_bits)
    return hash_int < target

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, nonce, difficulty_bits):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions  # lista de dicts
        self.nonce = nonce
        self.difficulty_bits = difficulty_bits
        self.hash = calculate_hash(index, previous_hash, timestamp, transactions, nonce, difficulty_bits)
    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "nonce": self.nonce,
            "difficulty_bits": self.difficulty_bits,
            "hash": self.hash,
        }

    @staticmethod
    def from_dict(data):
        return Block(
            index=data["index"],
            previous_hash=data["previous_hash"],
            timestamp=data["timestamp"],
            transactions=data["transactions"],
            nonce=data["nonce"],
            difficulty_bits=data["difficulty_bits"],
        )

    @staticmethod
    def mine_block(index, previous_hash, transactions, difficulty_bits):
        timestamp = int(time.time())
        nonce = 0
        while True:
            hash_hex = calculate_hash(index, previous_hash, timestamp, transactions, nonce, difficulty_bits)
            if hash_meets_difficulty(hash_hex, difficulty_bits):
                print(f"Bloque minado: index={index}, nonce={nonce}, hash={hash_hex}")
                return Block(index, previous_hash, timestamp, transactions, nonce, difficulty_bits)
            nonce += 1

    @staticmethod
    def genesis():
        index = 0
        previous_hash = "0" * 64

        # Distribución del génesis de AtlasCoin
        genesis_txs = [
            {
                "from": "GENESIS",
                "to": "ATLAS_TREASURY",
                "amount": 10,
                "note": GENESIS_MESSAGE,
            },
            {
                "from": "GENESIS",
                "to": "ATLAS_FOUNDATION",
                "amount": 10,
                "note": GENESIS_MESSAGE,
            },
            {
                "from": "GENESIS",
                "to": "ATLAS_DEV_WALLET",
                "amount": 5,
                "note": GENESIS_MESSAGE,
            },
        ]

        transactions = genesis_txs
        difficulty_bits = INITIAL_DIFFICULTY_BITS
        print("Minando bloque génesis de AtlasCoin (distribución oficial)...")
        return Block.mine_block(index, previous_hash, transactions, difficulty_bits)
