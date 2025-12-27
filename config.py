# config.py

# Nombre y símbolo
COIN_NAME = "AtlasCoin"
COIN_TICKER = "ATC"

# Política monetaria
MAX_SUPPLY = 21_000_000   # 21 millones de ATC
BLOCK_REWARD_INITIAL = 25  # 25 ATC por bloque al inicio
HALVING_INTERVAL = 210_000  # cada 210.000 bloques

# Tiempo de bloque objetivo en segundos (5 minutos)
BLOCK_TIME_TARGET = 5 * 60

# Dificultad inicial de la prueba de trabajo (ajustable)
INITIAL_DIFFICULTY_BITS = 18
# Frase oficial del bloque génesis
GENESIS_MESSAGE = "AtlasCoin Genesis Block — A neutral foundation for the future"
