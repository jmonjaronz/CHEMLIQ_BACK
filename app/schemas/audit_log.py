# app/schemas/audit_log.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AuditLogResponse(BaseModel):
    audit_id: int
    tabla_name: str
    pk_value: str
    accion: str
    old_value: Optional[str]
    new_value: Optional[str]
    usuario_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True