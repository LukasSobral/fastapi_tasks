from app.db.base import Base
from app.db.session import engine
from app.db import models

def init_db():
    print("🧩 Criando tabelas no banco...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")

if __name__ == "__main__":
    init_db()
