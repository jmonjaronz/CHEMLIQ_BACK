from sqlalchemy import (
    Column, Integer, String, TIMESTAMP, ForeignKey, CheckConstraint,
    UniqueConstraint, func
)
from sqlalchemy.orm import relationship
from app.db.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(Integer, primary_key=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("empresas.empresa_id"), nullable=False)
    usuario = Column(String(120), nullable=False)  # ← usado para login
    nombre = Column(String(200), nullable=False)
    password_hash = Column(String(200), nullable=False)
    salt = Column(String(100))
    ultimo_login = Column(TIMESTAMP)
    activo = Column(String(1), default="Y")
    row_version = Column(Integer, default=1)
    creado_en = Column(TIMESTAMP, server_default=func.now())

    empresa = relationship("Empresa", backref="usuarios")
    roles = relationship("UsuarioRol", back_populates="usuario")  # ← relación con roles

    __table_args__ = (
        UniqueConstraint("empresa_id", "usuario", name="ux_usuarios_empresa_usuario"),
        CheckConstraint("activo IN ('Y','N')", name="ck_usuarios_activo"),
    )