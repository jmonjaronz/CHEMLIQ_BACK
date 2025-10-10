#app/api/usuarios.py
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.services.usuario_service import (
    get_usuarios,
    get_usuario,
    create_usuario,
    update_usuario,
    delete_usuario
)

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

# =========================
# ENDPOINTS
# =========================

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(
    empresa_id: int = Query(..., description="ID de la empresa (obligatorio)"),
    nombre: Optional[str] = Query(None, description="Filtrar por nombre"),
    usuario: Optional[str] = Query(None, description="Filtrar por usuario"),
    incluir_inactivos: bool = Query(False, description="Incluir usuarios inactivos"),
    db: Session = Depends(get_db)
):
    """
    Lista los usuarios de una empresa con opción de filtrar por nombre o usuario.
    """
    usuarios = get_usuarios(db, empresa_id, nombre, usuario, incluir_inactivos)
    return usuarios


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(
    usuario_id: int = Path(..., description="ID del usuario"),
    empresa_id: int = Query(..., description="ID de la empresa (obligatorio)"),
    db: Session = Depends(get_db)
):
    """
    Obtiene un usuario específico dentro de una empresa.
    """
    usuario = get_usuario(db, empresa_id, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en la empresa especificada.")
    return usuario


@router.post("/", response_model=UsuarioResponse, status_code=201)
def crear_usuario(
    usuario_in: UsuarioCreate,
    empresa_id: int = Query(..., description="ID de la empresa a la que pertenece el usuario"),
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo usuario asociado a una empresa.
    """
    usuario = create_usuario(db, usuario_in, empresa_id)
    if usuario is None:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese nombre en esta empresa.")
    return usuario


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(
    usuario_id: int,
    usuario_in: UsuarioUpdate,
    empresa_id: int = Query(..., description="ID de la empresa (obligatorio)"),
    db: Session = Depends(get_db)
):
    """
    Actualiza los datos de un usuario dentro de una empresa.
    """
    usuario_actualizado = update_usuario(db, empresa_id, usuario_id, usuario_in)
    if not usuario_actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no pertenece a esta empresa.")
    return usuario_actualizado


@router.delete("/{usuario_id}", response_model=UsuarioResponse)
def eliminar_usuario(
    usuario_id: int,
    empresa_id: int = Query(..., description="ID de la empresa (obligatorio)"),
    db: Session = Depends(get_db)
):
    """
    Desactiva (borrado lógico) un usuario dentro de una empresa.
    """
    usuario_eliminado = delete_usuario(db, empresa_id, usuario_id)
    if not usuario_eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no pertenece a esta empresa.")
    return usuario_eliminado