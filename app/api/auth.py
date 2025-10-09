# app/api/auth.py
from fastapi import APIRouter, Depends, status, Form
from sqlalchemy.orm import Session
from app.services.auth_service import register_user, authenticate_user
from app.db.session import get_db
from app.schemas.auth import LoginResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
def register(
    username: str = Form(..., description="Nombre de usuario"),
    nombre: str = Form(..., description="Nombre completo"),
    password: str = Form(..., description="Contraseña"),
    db: Session = Depends(get_db)
):
    empresa_id = 1
    user_data = {"username": username, "nombre": nombre, "password": password}
    new_user = register_user(db=db, user_data=user_data, empresa_id=empresa_id)
    login_response = authenticate_user(db=db, username=username, password=password)
    return login_response


@router.post("/login", response_model=LoginResponse)
def login(
    username: str = Form(..., description="Nombre de usuario"),
    password: str = Form(..., description="Contraseña"),
    db: Session = Depends(get_db)
):
    login_response = authenticate_user(db=db, username=username, password=password)
    return login_response