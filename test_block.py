from block import Block

b = Block.genesis()
print("Atributos de Block:", dir(b))
print("Transactions:", getattr(b, "transactions", None))
