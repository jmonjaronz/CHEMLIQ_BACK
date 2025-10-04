# app/schemas/rol_permission.py
from pydantic import BaseModel

class RolPermissionBase(BaseModel):
    perm_code: str

class RolPermissionCreate(RolPermissionBase):
    role_id: int

class RolPermissionResponse(RolPermissionBase):
    role_perm_id: int
    role_id: int

    class Config:
        orm_mode = True