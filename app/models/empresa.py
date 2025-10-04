#app/models/empresa.py
from sqlalchemy import Column, Integer, String, Numeric, CLOB, TIMESTAMP, CheckConstraint
from app.db.base import Base

class Empresa(Base):
    __tablename__ = "empresas"

    empresa_id = Column(Integer, primary_key=True, autoincrement=True)
    ruc = Column(String(11), nullable=False, unique=True)
    nombre = Column(String(250), nullable=False)
    direccion = Column(String(400))
    config_igv_porcent = Column(Numeric(5, 2), default=18)
    config_documento_elect = Column(CLOB)
    creado_en = Column(TIMESTAMP)
    activo = Column(String(1), default="Y")

    __table_args__ = (
        CheckConstraint("activo IN ('Y','N')", name="ck_empresas_activo"),
    )