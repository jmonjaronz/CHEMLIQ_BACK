#app/models/role_permission.py
from pydantic import BaseModel, Field
from typing import Optional

class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    es_predefinido: Optional[str] = Field(
        "N",
        pattern="^(Y|N)$",
        description="Indica si el rol es predefinido"
    )

class RolCreate(RolBase):
    empresa_id: Optional[int] = Field(
        None,
        description="ID de la empresa (nulo si el rol es global)"
    )

class RolUpdate(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]
    es_predefinido: Optional[str]
    empresa_id: Optional[int]  # 🔸 Por si se quiere mover un rol global a una empresa

class RolResponse(RolBase):
    role_id: int
    empresa_id: Optional[int]
    creado_en: Optional[str]

    class Config:
        orm_mode = True