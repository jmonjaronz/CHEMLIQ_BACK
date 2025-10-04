#app/models/audit_log.py
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text
from sqlalchemy.sql import func
from app.db.base import Base

class AuditLog(Base):
    __tablename__ = "audit_log"

    audit_id = Column(Integer, primary_key=True, autoincrement=True)
    tabla_name = Column(String(200), nullable=False)
    pk_value = Column(String(400), nullable=False)
    accion = Column(String(20), nullable=False)  # INSERT, UPDATE, DELETE
    old_value = Column(Text)
    new_value = Column(Text)
    usuario_id = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())