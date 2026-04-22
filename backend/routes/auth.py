from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from database import get_db
from models import Usuario
from schemas import LoginSchema
from security import verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


# Benjamin Orellana - 2026/04/20 - Se corrige el login para autenticar contra username del esquema real y validar hash bcrypt.
@router.post("/login")
def login(data: LoginSchema, request: Request, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(
        Usuario.username == data.dni
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    request.session["user"] = {
        "id": user.id,
        "username": user.username,
        "rol": user.rol
    }

    return {
        "mensaje": "Login exitoso",
        "usuario": {
            "id": user.id,
            "username": user.username,
            "rol": user.rol,
            "email": user.email
        }
    }