#app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "CHEMLIQ API"
    VERSION: str = "0.1.0"

    # 🔐 Seguridad
    SECRET_KEY: str  # se cargará desde .env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hora

    # 🔗 Base de datos (se cargará desde .env)
    DATABASE_URL: str

    class Config:
        env_file = ".env"  # Indica que lea variables desde .env

settings = Settings()