# app/core/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Crear el motor de conexión
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,   # Verifica conexión antes de usarla
    pool_size=10,         # Máx. conexiones en el pool
    max_overflow=20       # Conexiones extra si se llena el pool
)

# SessionLocal será usado en los endpoints para crear sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia de FastAPI: obtener sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()