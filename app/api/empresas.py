# app/api/empresas.py
from fastapi import APIRouter, Depends, HTTPException, status, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.empresa import EmpresaCreate, EmpresaUpdate, EmpresaResponse
from app.services import empresa_service

router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"]
)

# =========================
# ENDPOINTS EMPRESAS
# =========================

@router.get("/", response_model=List[EmpresaResponse])
def listar_empresas(
    incluir_inactivas: bool = Query(False, description="Incluir empresas inactivas (activo='N')"),
    db: Session = Depends(get_db)
):
    """
    Lista empresas activas por defecto.  
    Si `incluir_inactivas=true`, lista todas (activas e inactivas).
    """
    empresas = empresa_service.get_empresas(db, incluir_inactivas)
    return empresas


@router.get("/{empresa_id}", response_model=EmpresaResponse)
def obtener_empresa(empresa_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una empresa por su ID (activa o inactiva).
    """
    empresa = empresa_service.get_empresa_by_id(db, empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa


@router.post("/", response_model=EmpresaResponse, status_code=status.HTTP_201_CREATED)
def crear_empresa(
    ruc: str = Form(..., description="RUC de la empresa (11 dígitos, empieza con 10 o 20)"),
    nombre: str = Form(..., description="Nombre o razón social de la empresa"),
    direccion: Optional[str] = Form(None, description="Dirección fiscal de la empresa"),
    config_igv_porcent: Optional[float] = Form(18, description="Porcentaje de IGV configurado (por defecto 18%)"),
    config_documento_elect: Optional[str] = Form(None, description="Configuración del documento electrónico"),
    activo: Optional[str] = Form("Y", description="Estado de la empresa (Y/N)"),
    db: Session = Depends(get_db)
):
    """
    Crea una nueva empresa (el RUC debe ser único, tener 11 caracteres y comenzar con '10' o '20').
    """
    # Validaciones del RUC
    if len(ruc) != 11:
        raise HTTPException(status_code=400, detail="El RUC debe tener exactamente 11 caracteres.")
    if not (ruc.startswith("10") or ruc.startswith("20")):
        raise HTTPException(status_code=400, detail="El RUC debe comenzar con '10' o '20'.")

    # Validación de duplicado
    empresa_existente = empresa_service.get_empresa_by_ruc(db, ruc)
    if empresa_existente:
        raise HTTPException(status_code=400, detail="El RUC ya está registrado en otra empresa.")

    # Crear empresa
    empresa_in = EmpresaCreate(
        ruc=ruc,
        nombre=nombre,
        direccion=direccion,
        config_igv_porcent=config_igv_porcent,
        config_documento_elect=config_documento_elect,
        activo=activo
    )

    nueva_empresa = empresa_service.create_empresa(db, empresa_in)
    return nueva_empresa


@router.put("/{empresa_id}", response_model=EmpresaResponse)
def actualizar_empresa(
    empresa_id: int,
    nombre: Optional[str] = Form(None, description="Nuevo nombre o razón social"),
    direccion: Optional[str] = Form(None, description="Nueva dirección fiscal"),
    config_igv_porcent: Optional[float] = Form(None, description="Nuevo porcentaje de IGV"),
    config_documento_elect: Optional[str] = Form(None, description="Nueva configuración de documento electrónico"),
    activo: Optional[str] = Form(None, description="Actualizar estado (Y/N)"),
    db: Session = Depends(get_db)
):
    """
    Actualiza una empresa (activa o inactiva).
    Permite reactivar empresas estableciendo activo='Y'.
    """
    empresa_in = EmpresaUpdate(
        nombre=nombre,
        direccion=direccion,
        config_igv_porcent=config_igv_porcent,
        config_documento_elect=config_documento_elect,
        activo=activo
    )

    empresa_actualizada = empresa_service.update_empresa(db, empresa_id, empresa_in)
    if not empresa_actualizada:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa_actualizada


@router.delete("/{empresa_id}", response_model=EmpresaResponse)
def eliminar_empresa(empresa_id: int, db: Session = Depends(get_db)):
    """
    Realiza un borrado lógico (marca activo='N').
    """
    empresa = empresa_service.delete_empresa(db, empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa