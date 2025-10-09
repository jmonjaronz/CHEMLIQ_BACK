# app/schemas/empresa.py
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from datetime import datetime

# =============================
# Schemas para Empresa
# =============================

class EmpresaBase(BaseModel):
    ruc: Annotated[str, Field(min_length=11, max_length=11, description="RUC de la empresa (11 dígitos)")]
    nombre: str
    direccion: Optional[str] = None
    config_igv_porcent: Optional[float] = Field(default=18, description="Porcentaje de IGV aplicado")
    config_documento_elect: Optional[str] = Field(default=None, description="Configuración de facturación electrónica (JSON/XML)")
    activo: Optional[str] = Field(default="Y", description="Estado de la empresa (Y/N)")


class EmpresaCreate(EmpresaBase):
    """
    Esquema para crear una nueva empresa.
    Hereda todos los campos de EmpresaBase.
    """
    pass


class EmpresaUpdate(BaseModel):
    """
    Esquema para actualizar datos de una empresa.
    Los campos son opcionales.
    """
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    config_igv_porcent: Optional[float] = None
    config_documento_elect: Optional[str] = None
    activo: Optional[str] = None


class EmpresaResponse(EmpresaBase):
    """
    Esquema de respuesta que incluye el ID y fecha de creación.
    """
    empresa_id: int
    creado_en: Optional[datetime] = None

    class Config:
        orm_mode = True