# AtlasCoin (ATC)

AtlasCoin es una criptomoneda experimental de tipo Proof of Work inspirada en los principios de Bitcoin: reglas claras, emisión limitada y red descentralizada. Está diseñada como proyecto educativo y de investigación; no es un producto financiero ni una inversión.

Autor: **Uarag Legacy**

## Características básicas

- Nombre: AtlasCoin  
- Símbolo: ATC  
- Consenso: Proof of Work (PoW)  
- Tiempo objetivo de bloque: 5 minutos (ajustable en `config.py`)  
- Suministro máximo: 21.000.000 ATC  
- Recompensa inicial por bloque: 25 ATC  
- Fees: cada transacción puede incluir una comisión (fee) que se entrega al minero además de la recompensa fija.

## Distribución del bloque génesis

El bloque génesis de AtlasCoin reparte 25 ATC de la siguiente forma:

- `ATLAS_TREASURY`: 10 ATC  
- `ATLAS_FOUNDATION`: 10 ATC  
- `ATLAS_DEV_WALLET`: 5 ATC  

Esta distribución está codificada en `block.py`, dentro del método `Block.genesis()`.

## Estado actual del proyecto

AtlasCoin incluye actualmente:

- Nodo local escrito en Python que implementa:
  - Minería Proof of Work (PoW).
  - Transacciones con `amount` + `fee`.
  - Balances por dirección.
  - Persistencia de la cadena en el archivo `atlascoin_chain.json`.
- Interfaz de línea de comandos (`node.py`) con menú interactivo:
  - Ver balances.
  - Crear transacciones.
  - Ver transacciones pendientes.
  - Minar bloques.
  - Ver información de la cadena.

Es un prototipo funcional pensado para aprender cómo funciona una criptomoneda tipo Bitcoin a nivel básico.

## Requisitos

- Python 3.10 o superior.  
- (Opcional) Docker, si se desea ejecutar el nodo en un contenedor.

## Uso rápido (sin Docker)

1. Clonar el repositorio (o copiar los archivos del proyecto) en una carpeta:


2. Ejecutar el nodo:


3. Usar el menú interactivo:

- `1` – Ver balances  
- `2` – Crear transacción  
- `3` – Ver transacciones pendientes  
- `4` – Minar bloque  
- `5` – Ver información de la cadena  
- `0` – Salir  

Las direcciones “oficiales” usadas en el prototipo son:

- `ATLAS_TREASURY`  
- `ATLAS_FOUNDATION`  
- `ATLAS_DEV_WALLET`  
- `LOCAL_MINER` (minero por defecto en el nodo local)

## Uso con Docker (opcional)

Con Docker instalado, desde la carpeta del proyecto:


Esto lanzará el mismo menú interactivo dentro de un contenedor.

## Aviso

AtlasCoin es un proyecto experimental y educativo. No constituye una oferta de inversión ni un instrumento financiero.


