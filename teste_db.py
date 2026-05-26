from database.database import engine

try:
    connection = engine.connect()
    print("Banco conectado com sucesso 🚀")
except Exception as e:
    print("Erro:", e)