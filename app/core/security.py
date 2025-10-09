# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.core.config import settings
from app.utils.hashing import verify_password, hash_password

# =========================
# JWT
# =========================
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crea un JWT token con los datos proporcionados.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    """
    Verifica un JWT y devuelve el payload si es válido.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

# =========================
# Passwords
# =========================
def get_password_hash(password: str) -> str:
    """
    Hashea un password usando bcrypt (reutilizando utils/hashing.py).
    """
    return hash_password(password)

def verify_user_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica un password plano contra su hash.
    """
    return verify_password(plain_password, hashed_password)