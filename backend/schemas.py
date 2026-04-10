from pydantic import BaseModel

class LoginSchema(BaseModel):
    dni: str
    password: str

class NotaCreate(BaseModel):
    alumno_id: int
    materia_id: int
    nota: float

