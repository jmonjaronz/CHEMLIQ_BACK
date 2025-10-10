# app/services/rol_service.py

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from sqlalchemy.exc import IntegrityError
from app.models.rol import Rol
from app.schemas.rol import RolCreate, RolUpdate
from datetime import datetime

# =========================
# CONSULTAS
# =========================

def get_roles(db: Session, empresa_id: int = None, incluir_globales: bool = True):
    """
    Lista los roles. Si se especifica empresa_id, lista los roles de esa empresa
    y opcionalmente también los globales.
    """
    query = db.query(Rol)
    if empresa_id:
        if incluir_globales:
            query = query.filter(or_(Rol.empresa_id == empresa_id, Rol.empresa_id == None))
        else:
            query = query.filter(Rol.empresa_id == empresa_id)
    return query.order_by(Rol.nombre.asc()).all()


def get_rol_by_id(db: Session, role_id: int):
    """
    Obtiene un rol por su ID.
    """
    return db.query(Rol).filter(Rol.role_id == role_id).first()


def get_rol_by_nombre(db: Session, nombre: str, empresa_id: int = None):
    """
    Verifica si ya existe un rol con ese nombre dentro de la empresa o globalmente.
    """
    return db.query(Rol).filter(
        Rol.nombre == nombre,
        Rol.empresa_id == empresa_id
    ).first()

# =========================
# CRUD
# =========================

def create_rol(db: Session, rol_in: RolCreate):
    """
    Crea un nuevo rol (global o asociado a empresa).
    """
    # Normalizar: si llega string vacío, dejar como None
    if rol_in.empresa_id == "" or rol_in.empresa_id is None:
        rol_in.empresa_id = None

    # Validar duplicado
    rol_existente = get_rol_by_nombre(db, rol_in.nombre, rol_in.empresa_id)
    if rol_existente:
        return None  # ⚠️ Se maneja el error en el router

    nuevo_rol = Rol(
        nombre=rol_in.nombre.strip(),
        descripcion=rol_in.descripcion,
        es_predefinido=rol_in.es_predefinido or "N",
        empresa_id=rol_in.empresa_id,
        creado_en=datetime.now()
    )

    try:
        db.add(nuevo_rol)
        db.commit()
        db.refresh(nuevo_rol)
        return nuevo_rol
    except IntegrityError:
        db.rollback()
        return None


def update_rol(db: Session, role_id: int, rol_in: RolUpdate):
    """
    Actualiza un rol existente (global o empresarial).
    """
    rol = get_rol_by_id(db, role_id)
    if not rol:
        return None

    # Manejar empresa_id vacío o "null"
    if hasattr(rol_in, "empresa_id") and rol_in.empresa_id in ("", "null"):
        rol_in.empresa_id = None

    # Validar duplicado si se cambia el nombre o empresa_id
    campos = rol_in.dict(exclude_unset=True)
    nuevo_nombre = campos.get("nombre", rol.nombre)
    nueva_empresa_id = campos.get("empresa_id", rol.empresa_id)

    duplicado = db.query(Rol).filter(
        Rol.role_id != role_id,
        Rol.nombre == nuevo_nombre,
        Rol.empresa_id == nueva_empresa_id
    ).first()

    if duplicado:
        return None  # ⚠️ Ya existe un rol igual

    for campo, valor in campos.items():
        setattr(rol, campo, valor)

    db.commit()
    db.refresh(rol)
    return rol


def delete_rol(db: Session, role_id: int):
    """
    Elimina un rol (borrado físico por ahora).
    Más adelante se puede cambiar a borrado lógico si se asocia con usuarios.
    """
    rol = get_rol_by_id(db, role_id)
    if not rol:
        return None

    db.delete(rol)
    db.commit()
    return rol