from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Usuario
from security import hash_password

router = APIRouter(prefix="/admin")


# Benjamin Orellana - 2026/04/20 - Alta mínima de usuarios alineada al esquema real de tecnica_nro1.
@router.post("/usuarios")
def crear_usuario(
    username: str,
    password: str,
    rol: str,
    email: str = None,
    db: Session = Depends(get_db)
):
    existe = db.query(Usuario).filter(
        Usuario.username == username
    ).first()

    if existe:
        raise HTTPException(status_code=400, detail="El username ya existe")

    if rol not in ["alumno", "preceptor", "jefe_preceptor", "administrador"]:
        raise HTTPException(status_code=400, detail="Rol inválido")

    nuevo = Usuario(
        username=username,
        password=hash_password(password),
        rol=rol,
        email=email
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {
        "mensaje": "Usuario creado correctamente",
        "usuario": {
            "id": nuevo.id,
            "username": nuevo.username,
            "rol": nuevo.rol,
            "email": nuevo.email
        }
    }


# Benjamin Orellana - 2026/04/20 - Listado mínimo de usuarios alineado al esquema real.
@router.get("/usuarios")
def listar_usuarios(
    db: Session = Depends(get_db)
):
    return db.query(Usuario).all()

@router.put("/usuarios/{id}/estado")
def cambiar_estado(
    id: int,
    activo: bool,
    db: Session = Depends(get_db),
    user=Depends(require_role([1]))
):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no existe")

    usuario.activo = activo
    db.commit()

    return {"mensaje": "Estado actualizado correctamente"}


# =========================
# CURSOS
# =========================

@router.post("/cursos")
def crear_curso(
    nombre: str,
    anio: int,
    db: Session = Depends(get_db),
    user=Depends(require_role([1]))
):
    nuevo = Curso(nombre=nombre, anio=anio)

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {"mensaje": "Curso creado correctamente"}


@router.get("/cursos")
def listar_cursos(
    db: Session = Depends(get_db),
    user=Depends(require_role([1, 2]))
):
    return db.query(Curso).all()


# =========================
# MATERIAS
# =========================

@router.post("/materias")
def crear_materia(
    nombre: str,
    curso_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role([1]))
):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()

    if not curso:
        raise HTTPException(status_code=404, detail="Curso no existe")

    nueva = Materia(nombre=nombre, curso_id=curso_id)

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return {"mensaje": "Materia creada correctamente"}


@router.get("/materias/{curso_id}")
def listar_materias(
    curso_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role([1, 2]))
):
    return db.query(Materia).filter(Materia.curso_id == curso_id).all()


# =========================
# ALUMNOS
# =========================

@router.post("/alumnos")
def crear_alumno(
    usuario_id: int,
    curso_id: int,
    dni: str,
    db: Session = Depends(get_db),
    user=Depends(require_role([1]))
):
    # 🔍 Validar usuario
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no existe")

    # 🔍 Validar curso
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no existe")

    # 🔍 Validar DNI único
    existe = db.query(Alumno).filter(Alumno.dni == dni).first()
    if existe:
        raise HTTPException(status_code=400, detail="El DNI ya está registrado")

    nuevo = Alumno(
        usuario_id=usuario_id,
        curso_id=curso_id,
        dni=dni
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {"mensaje": "Alumno creado correctamente"}


@router.get("/alumnos")
def listar_alumnos(
    db: Session = Depends(get_db),
    user=Depends(require_role([1, 2]))
):
    return db.query(Alumno).all()


# =========================
# PRECEPTORES
# =========================

@router.post("/preceptores/asignar")
def asignar_preceptor(
    usuario_id: int,
    curso_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role([1]))
):
    # 🔍 Validar duplicado
    existe = db.query(PreceptorCurso).filter(
        PreceptorCurso.usuario_id == usuario_id,
        PreceptorCurso.curso_id == curso_id
    ).first()

    if existe:
        raise HTTPException(status_code=400, detail="El preceptor ya está asignado a este curso")

    asignacion = PreceptorCurso(
        usuario_id=usuario_id,
        curso_id=curso_id
    )

    db.add(asignacion)
    db.commit()

    return {"mensaje": "Preceptor asignado correctamente"}


@router.get("/preceptores")
def listar_preceptores(
    db: Session = Depends(get_db),
    user=Depends(require_role([1]))
):
    return db.query(PreceptorCurso).all()