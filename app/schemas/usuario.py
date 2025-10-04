# app/schemas/usuario.py
from pydantic import BaseModel
from typing import Optional, List

class UsuarioBase(BaseModel):
    usuario: str
    nombre: str
    activo: Optional[str] = "Y"

class UsuarioCreate(UsuarioBase):
    password: str  # necesario solo al crear

class UsuarioUpdate(BaseModel):
    nombre: Optional[str]
    activo: Optional[str]

class UsuarioResponse(UsuarioBase):
    usuario_id: int
    empresa_id: int
    roles: Optional[List[str]] = []

    class Config:
        orm_mode = True