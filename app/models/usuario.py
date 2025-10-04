#app/models/usuario.py
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, CheckConstraint, UniqueConstraint, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(Integer, primary_key=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("empresas.empresa_id"), nullable=False)
    email = Column(String(250), nullable=False)
    nombre = Column(String(200), nullable=False)
    password_hash = Column(String(200), nullable=False)
    salt = Column(String(100))
    ultimo_login = Column(TIMESTAMP)
    activo = Column(String(1), default="Y")
    row_version = Column(Integer, default=1)
    creado_en = Column(TIMESTAMP)

    empresa = relationship("Empresa", backref="usuarios")

    __table_args__ = (
        UniqueConstraint("empresa_id", "email", name="ux_usuarios_empresa_email"),
        CheckConstraint("activo IN ('Y','N')", name="ck_usuarios_activo"),
    )