# app/services/auth_service.py
from sqlalchemy.orm import Session
from datetime import timedelta

from app.models.usuario import Usuario
from app.core.security import create_access_token, verify_user_password, get_password_hash
from app.schemas.auth import LoginResponse, RegisterRequest
from app.core.config import settings
from fastapi import HTTPException, status

def register_user(db: Session, user_data: RegisterRequest, empresa_id: int) -> Usuario:
    """
    Registra un nuevo usuario.
    """
    # Verificar si el username ya existe en la empresa
    existing_user = db.query(Usuario).filter(
        Usuario.username == user_data.username,
        Usuario.empresa_id == empresa_id
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe"
        )

    # Crear usuario con password hasheado
    new_user = Usuario(
        username=user_data.username,
        nombre=user_data.nombre,
        password_hash=get_password_hash(user_data.password),
        empresa_id=empresa_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, username: str, password: str) -> LoginResponse:
    """
    Verifica usuario y genera token JWT.
    """
    user = db.query(Usuario).filter(
        Usuario.username == username,
        Usuario.activo == "Y"
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrecta"
        )

    if not verify_user_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrecta"
        )

    # Generar token JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": str(user.usuario_id)}
    token = create_access_token(data=token_data, expires_delta=access_token_expires)

    return LoginResponse(access_token=token)