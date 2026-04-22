from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DECIMAL, Text
from sqlalchemy.orm import relationship
from database import Base


# Benjamin Orellana - 2026/04/20 - Se adapta el modelo Usuario al esquema real de tecnica_nro1.
class PreguntaSeguridad(Base):
    __tablename__ = "preguntas_seguridad"

    id = Column(Integer, primary_key=True)
    pregunta = Column(String(255), nullable=False)


# Benjamin Orellana - 2026/04/20 - Se reemplaza el esquema viejo de usuarios por el esquema real con username y rol textual.
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    rol = Column(String(30), nullable=False)
    id_pregunta_seguridad = Column(Integer, ForeignKey("preguntas_seguridad.id"), nullable=True)
    respuesta_seguridad_hash = Column(String(255), nullable=True)
    email = Column(String(100), unique=True, nullable=True)

    pregunta_seguridad = relationship("PreguntaSeguridad")


class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    anio = Column(Integer)


class Alumno(Base):
    __tablename__ = "alumnos"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    curso_id = Column(Integer, ForeignKey("cursos.id"))

    usuario = relationship("Usuario")
    curso = relationship("Curso")


class Materia(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    curso_id = Column(Integer, ForeignKey("cursos.id"))

    curso = relationship("Curso")


class PreceptorCurso(Base):
    __tablename__ = "preceptor_curso"

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    curso_id = Column(Integer, ForeignKey("cursos.id"), primary_key=True)


class Nota(Base):
    __tablename__ = "notas"

    id = Column(Integer, primary_key=True)
    alumno_id = Column(Integer, ForeignKey("alumnos.id"))
    materia_id = Column(Integer, ForeignKey("materias.id"))
    trimestre = Column(Integer)
    anio = Column(Integer)
    nota = Column(DECIMAL(4, 2))
    observaciones = Column(Text)

    materia = relationship("Materia")