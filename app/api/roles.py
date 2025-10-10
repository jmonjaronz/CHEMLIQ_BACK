# app/api/roles.py
from fastapi import APIRouter, Depends, HTTPException, status, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.rol import RolCreate, RolUpdate, RolResponse
from app.services import rol_service

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

# =========================
# ENDPOINTS ROLES
# =========================

@router.get("/", response_model=List[RolResponse])
def listar_roles(
    empresa_id: Optional[int] = Query(None, description="ID de empresa (opcional)"),
    incluir_globales: bool = Query(True, description="Incluir roles globales"),
    db: Session = Depends(get_db)
):
    """
    Lista todos los roles (globales y/o por empresa).
    """
    roles = rol_service.get_roles(db, empresa_id, incluir_globales)
    return roles


@router.get("/{role_id}", response_model=RolResponse)
def obtener_rol(role_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un rol por su ID.
    """
    rol = rol_service.get_rol_by_id(db, role_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol


@router.post("/", response_model=RolResponse, status_code=status.HTTP_201_CREATED)
def crear_rol(
    nombre: str = Form(..., description="Nombre del rol"),
    descripcion: Optional[str] = Form(None, description="Descripción del rol"),
    es_predefinido: Optional[str] = Form("N", description="Indica si el rol es predefinido (Y/N)"),
    empresa_id: Optional[str] = Form(None, description="ID de la empresa (nulo si es global)"),
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo rol (global o empresarial).
    """

    # Manejo de empresa_id vacío o nulo
    empresa_id_int = int(empresa_id) if empresa_id not in (None, "", "null") else None

    rol_in = RolCreate(
        nombre=nombre,
        descripcion=descripcion,
        es_predefinido=es_predefinido,
        empresa_id=empresa_id_int
    )

    nuevo_rol = rol_service.create_rol(db, rol_in)
    if not nuevo_rol:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un rol con ese nombre en la empresa o a nivel global."
        )
    return nuevo_rol


@router.put("/{role_id}", response_model=RolResponse)
def actualizar_rol(
    role_id: int,
    nombre: Optional[str] = Form(None, description="Nuevo nombre del rol"),
    descripcion: Optional[str] = Form(None, description="Nueva descripción del rol"),
    es_predefinido: Optional[str] = Form(None, description="Indica si el rol es predefinido (Y/N)"),
    empresa_id: Optional[str] = Form(None, description="ID de la empresa (nulo si es global)"),
    db: Session = Depends(get_db)
):
    """
    Actualiza un rol existente (global o empresarial).
    """

    # Manejar el caso de empresa_id vacío
    empresa_id_int = int(empresa_id) if empresa_id not in (None, "", "null") else None

    rol_in = RolUpdate(
        nombre=nombre,
        descripcion=descripcion,
        es_predefinido=es_predefinido,
        empresa_id=empresa_id_int
    )

    rol_actualizado = rol_service.update_rol(db, role_id, rol_in)
    if not rol_actualizado:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    return rol_actualizado


@router.delete("/{role_id}", response_model=RolResponse)
def eliminar_rol(role_id: int, db: Session = Depends(get_db)):
    """
    Elimina un rol (borrado físico por ahora).
    """
    rol = rol_service.delete_rol(db, role_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol