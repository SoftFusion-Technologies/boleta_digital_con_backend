from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DECIMAL, Text
from sqlalchemy.orm import relationship
from database import Base


class Rol(Base):
    __tablename__ = "rol"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True)


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))

    usuario = Column(String(50), unique=True)
    dni = Column(String(20), unique=True)

    password = Column(String(255))
    rol_id = Column(Integer, ForeignKey("rol.id"))
    activo = Column(Boolean, default=True)

    rol = relationship("Rol")


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