# app/schemas/empresa.py
from pydantic import BaseModel
from typing import Optional

class EmpresaBase(BaseModel):
    ruc: str
    nombre: str
    direccion: Optional[str] = None
    config_igv_porcent: Optional[float] = 18
    config_documento_elect: Optional[str] = None
    activo: Optional[str] = "Y"

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaUpdate(BaseModel):
    nombre: Optional[str]
    direccion: Optional[str]
    config_igv_porcent: Optional[float]
    config_documento_elect: Optional[str]
    activo: Optional[str]

class EmpresaResponse(EmpresaBase):
    empresa_id: int

    class Config:
        orm_mode = True