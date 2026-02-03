from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL no está definida. Revisá el archivo .env")

# Remover parámetros SSL de la URL si existen
if "?" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?")[0]

# Crear engine con SSL habilitado en connect_args
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl_disabled": False  # Habilita SSL para Aiven
    },
    pool_pre_ping=True,
    pool_recycle=3600  # Recicla conexiones cada hora
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()