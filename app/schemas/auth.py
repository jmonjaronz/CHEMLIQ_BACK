# app/schemas/auth.py
from pydantic import BaseModel

class LoginRequest(BaseModel):
    usuario: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseModel):
    usuario: str
    nombre: str
    password: str