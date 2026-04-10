from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import Alumno, Nota
from security import require_role
from utils.pdf_generator import generar_boleta_pdf

router = APIRouter(prefix="/alumnos")


# =========================
# 🔁 FUNCIÓN INTERNA REUTILIZABLE
# =========================
def obtener_boleta_data(user, db):

    alumno = db.query(Alumno).filter(
        Alumno.usuario_id == user["id"]
    ).first()

    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    notas = db.query(Nota).options(
        joinedload(Nota.materia)
    ).filter(
        Nota.alumno_id == alumno.id
    ).all()

    materias = {}

    for n in notas:
        nombre = n.materia.nombre

        if nombre not in materias:
            materias[nombre] = []

        materias[nombre].append(float(n.nota))

    resultado = []
    suma_general = 0
    total_materias = 0

    for materia, lista_notas in materias.items():
        promedio = sum(lista_notas) / len(lista_notas)

        resultado.append({
            "materia": materia,
            "notas": lista_notas,
            "promedio": round(promedio, 2),
            "estado": "Aprobado" if promedio >= 6 else "Desaprobado"
        })

        suma_general += promedio
        total_materias += 1

    promedio_general = round(suma_general / total_materias, 2) if total_materias > 0 else 0

    return {
        "alumno": alumno.usuario.nombre,
        "materias": resultado,
        "promedio_general": promedio_general
    }


# =========================
# 👨‍🎓 VER BOLETA
# =========================
@router.get("/mi-boleta")
def mi_boleta(
    user=Depends(require_role([3])),
    db: Session = Depends(get_db)
):
    return obtener_boleta_data(user, db)


# =========================
# DESCARGAR PDF
# =========================

@router.get("/mi-boleta/pdf")
def descargar_boleta(
    user=Depends(require_role([3])),
    db: Session = Depends(get_db)
):

    data = obtener_boleta_data(user, db)

    archivo = generar_boleta_pdf(
        nombre_alumno=data["alumno"],
        datos=data
    )

    return FileResponse(
        path=archivo,
        filename="boleta.pdf",
        media_type="application/pdf"
    )
