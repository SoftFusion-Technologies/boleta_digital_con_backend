from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db
from models import Usuario
from schemas import LoginSchema
from fastapi import Request

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(data: LoginSchema, request: Request, db: Session = Depends(get_db)):

    user = db.query(Usuario).filter(
        or_(
            Usuario.usuario == data.dni,
            Usuario.dni == data.dni
        )
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if data.password != user.password:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # 🔥 GUARDAR SESIÓN
    request.session["user"] = {
        "id": user.id,
        "nombre": user.nombre,
        "rol": user.rol_id
    }

    return {
        "mensaje": "Login exitoso"
    }