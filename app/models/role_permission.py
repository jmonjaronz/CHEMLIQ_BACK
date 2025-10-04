#app/models/role_permission.py
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_perm_id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    perm_code = Column(String(80), nullable=False)
    creado_en = Column(TIMESTAMP)

    rol = relationship("Rol", backref="permissions")