# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Cria engine de conexão
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Cria sessão de banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
