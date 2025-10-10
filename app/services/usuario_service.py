#app/services/usuario_Service.py
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import get_password_hash
from datetime import datetime

# =========================
# CONSULTAS
# =========================

def get_usuarios(db: Session, empresa_id: int, nombre: str = None, usuario: str = None, incluir_inactivos: bool = False):
    """
    Lista los usuarios de una empresa específica.
    Puede filtrar por nombre o usuario.
    """
    query = db.query(Usuario).filter(Usuario.empresa_id == empresa_id)

    if not incluir_inactivos:
        query = query.filter(Usuario.activo == "Y")

    if nombre:
        query = query.filter(Usuario.nombre.ilike(f"%{nombre}%"))

    if usuario:
        query = query.filter(Usuario.usuario.ilike(f"%{usuario}%"))

    return query.order_by(Usuario.nombre.asc()).all()


def get_usuario(db: Session, empresa_id: int, usuario_id: int):
    """
    Obtiene un usuario por ID dentro de una empresa específica.
    """
    return db.query(Usuario).filter(
        Usuario.empresa_id == empresa_id,
        Usuario.usuario_id == usuario_id
    ).first()

# =========================
# CRUD
# =========================

def create_usuario(db: Session, usuario_in: UsuarioCreate, empresa_id: int):
    """
    Crea un nuevo usuario asociado a una empresa.
    El nombre de usuario debe ser único dentro de esa empresa.
    """
    # Validar duplicado
    usuario_existente = db.query(Usuario).filter(
        Usuario.usuario == usuario_in.usuario,
        Usuario.empresa_id == empresa_id
    ).first()
    if usuario_existente:
        return None  # ⚠️ Se manejará en el router

    hashed_password = get_password_hash(usuario_in.password)

    nuevo_usuario = Usuario(
        empresa_id=empresa_id,
        usuario=usuario_in.usuario,
        nombre=usuario_in.nombre,
        email=f"{usuario_in.usuario}@empresa{empresa_id}.com",  # Temporal
        password_hash=hashed_password,
        creado_en=datetime.utcnow(),
        activo=usuario_in.activo or "Y"
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def update_usuario(db: Session, empresa_id: int, usuario_id: int, usuario_in: UsuarioUpdate):
    """
    Actualiza un usuario existente dentro de una empresa.
    """
    usuario = get_usuario(db, empresa_id, usuario_id)
    if not usuario:
        return None

    for campo, valor in usuario_in.dict(exclude_unset=True).items():
        setattr(usuario, campo, valor)
    db.commit()
    db.refresh(usuario)
    return usuario


def delete_usuario(db: Session, empresa_id: int, usuario_id: int):
    """
    Realiza un borrado lógico (activo='N') dentro de una empresa.
    """
    usuario = get_usuario(db, empresa_id, usuario_id)
    if not usuario:
        return None

    usuario.activo = "N"
    db.commit()
    db.refresh(usuario)
    return usuario