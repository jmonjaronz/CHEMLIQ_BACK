# app/schemas/rol.py
from pydantic import BaseModel
from typing import Optional

class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    es_predefinido: Optional[str] = "N"

class RolCreate(RolBase):
    empresa_id: Optional[int] = None

class RolUpdate(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]
    es_predefinido: Optional[str]

class RolResponse(RolBase):
    role_id: int
    empresa_id: Optional[int]

    class Config:
        orm_mode = True