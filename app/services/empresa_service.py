# app/services/empresa_service.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.empresa import Empresa
from app.schemas.empresa import EmpresaCreate, EmpresaUpdate

# =========================
# CRUD EMPRESAS
# =========================

def get_empresas(db: Session):
    """
    Retorna todas las empresas activas.
    """
    return db.execute(select(Empresa).order_by(Empresa.empresa_id)).scalars().all()


def get_empresa_by_id(db: Session, empresa_id: int):
    """
    Retorna una empresa por su ID.
    """
    return db.get(Empresa, empresa_id)


def get_empresa_by_ruc(db: Session, ruc: str):
    """
    Retorna una empresa por su RUC (único).
    """
    return db.execute(select(Empresa).where(Empresa.ruc == ruc)).scalar_one_or_none()


def create_empresa(db: Session, empresa_in: EmpresaCreate):
    """
    Crea una nueva empresa.
    """
    nueva_empresa = Empresa(**empresa_in.dict())
    db.add(nueva_empresa)
    db.commit()
    db.refresh(nueva_empresa)
    return nueva_empresa


def update_empresa(db: Session, empresa_id: int, empresa_in: EmpresaUpdate):
    """
    Actualiza los datos de una empresa existente.
    """
    empresa = db.get(Empresa, empresa_id)
    if not empresa:
        return None

    update_data = empresa_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(empresa, key, value)

    db.commit()
    db.refresh(empresa)
    return empresa


def delete_empresa(db: Session, empresa_id: int):
    """
    Elimina una empresa (borrado lógico → marca activo='N').
    """
    empresa = db.get(Empresa, empresa_id)
    if not empresa:
        return None
    empresa.activo = "N"
    db.commit()
    db.refresh(empresa)
    return empresa