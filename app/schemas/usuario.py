# app/schemas/usuario.py
from pydantic import BaseModel
from typing import Optional, List

class UsuarioBase(BaseModel):
    usuario: str
    nombre: str
    activo: Optional[str] = "Y"

class UsuarioCreate(UsuarioBase):
    password: str  # ← no se devuelve nunca
    empresa_id: int  # ← obligatorio

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    activo: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    usuario_id: int
    empresa_id: int
    roles: Optional[List[str]] = []  # luego puede cambiar a List[RolResponse]

    class Config:
        orm_mode = True