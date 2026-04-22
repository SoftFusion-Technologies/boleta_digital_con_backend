from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import Nota, Alumno, Materia, PreceptorCurso
from schemas import NotaCreate
from security import require_role
from typing import List
router = APIRouter(prefix="/notas")

@router.post("/")
def cargar_notas(
    alumno_id: int,
    notas: List[NotaCreate],
        user=Depends(require_role([2])),
    db: Session = Depends(get_db)
):

    alumno = db.query(Alumno).filter(Alumno.id == alumno_id).first()

    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no existe")

    # VALIDAR CURSO DEL PRECEPTOR
    permiso = db.query(PreceptorCurso).filter(
        PreceptorCurso.usuario_id == user["id"],
        PreceptorCurso.curso_id == alumno.curso_id
    ).first()

    if not permiso:
        raise HTTPException(status_code=403, detail="No puedes cargar notas a este curso")

    for n in notas:

        existente = db.query(Nota).filter(
            Nota.alumno_id == alumno_id,
            Nota.materia_id == n.materia_id,
            Nota.trimestre == n.trimestre,
            Nota.anio == datetime.now().year
        ).first()

        if existente:
            existente.nota = n.nota
            existente.observaciones = n.observaciones
        else:
            nueva = Nota(
                alumno_id=alumno_id,
                materia_id=n.materia_id,
                trimestre=n.trimestre,
                anio=datetime.now().year,
                nota=n.nota,
                observaciones=n.observaciones,
                created_by=user["id"]
            )
            db.add(nueva)

    db.commit()

    return {"mensaje": "Notas guardadas correctamente"}