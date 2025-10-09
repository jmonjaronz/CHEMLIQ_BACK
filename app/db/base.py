# app/db/base.py
from sqlalchemy.orm import declarative_base

# Base que usarán todos los modelos ORM
Base = declarative_base()