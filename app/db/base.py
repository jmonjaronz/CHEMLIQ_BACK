# app/db/base.py
from sqlalchemy.orm import declarative_base

# Base que usarán todos los modelos ORM
Base = declarative_base()

# Aquí importaremos los modelos para que Alembic o SQLAlchemy
# puedan reconocerlos automáticamente al hacer migraciones
# (se irán agregando conforme crees tus modelos)
from app.models.empresa import Empresa
from app.models.usuario import Usuario
from app.models.rol import Rol