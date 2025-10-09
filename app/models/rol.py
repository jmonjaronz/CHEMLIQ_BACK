#app/models/rol.py
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, CheckConstraint, UniqueConstraint, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Rol(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("empresas.empresa_id"), nullable=True)  # 🔸 Puede ser global
    nombre = Column(String(120), nullable=False)
    descripcion = Column(String(400))
    es_predefinido = Column(String(1), default="N")
    creado_en = Column(TIMESTAMP, server_default=func.now())  # 🔸 Fecha automática

    empresa = relationship("Empresa", backref="roles")

    __table_args__ = (
        UniqueConstraint("empresa_id", "nombre", name="ux_roles_empresa_nombre"),
        CheckConstraint("es_predefinido IN ('Y','N')", name="ck_roles_es_predefinido"),
    )