# app/schemas/auth.py
from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(..., description="Nombre de usuario para iniciar sesión")
    password: str = Field(..., description="Contraseña del usuario")

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseModel):
    username: str = Field(..., description="Nombre de usuario único")
    nombre: str = Field(..., description="Nombre completo del usuario")
    password: str = Field(..., description="Contraseña segura del usuario (mínimo 8 caracteres)")