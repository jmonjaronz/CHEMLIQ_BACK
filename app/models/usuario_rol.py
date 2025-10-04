#app/models/usuario_rol.py
from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class UsuarioRol(Base):
    __tablename__ = "usuario_roles"

    usuario_role_id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    assigned_at = Column(TIMESTAMP)

    usuario = relationship("Usuario", backref="roles_asignados")
    rol = relationship("Rol", backref="usuarios_asignados")