# app/db/test_connection.py
# python -m app.db.test_connection

from app.db.session import engine

def test_connection():
    try:
        with engine.connect() as connection:
            print("✅ Conexão com banco de dados bem-sucedida!")
    except Exception as e:
        print("❌ Erro ao conectar ao banco:", e)

if __name__ == "__main__":
    test_connection()
