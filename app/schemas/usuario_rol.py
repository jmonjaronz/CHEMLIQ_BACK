# app/schemas/usuario_rol.py
from pydantic import BaseModel

class UsuarioRolBase(BaseModel):
    pass

class UsuarioRolCreate(BaseModel):
    usuario_id: int
    role_id: int

class UsuarioRolResponse(UsuarioRolBase):
    usuario_role_id: int
    usuario_id: int
    role_id: int

    class Config:
        orm_mode = True