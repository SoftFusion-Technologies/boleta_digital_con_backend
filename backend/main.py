import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from routes import auth, alumnos, notas, admin

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="clave_super_secreta_123"
)

#  rutas
app.include_router(auth.router)
app.include_router(alumnos.router)
app.include_router(notas.router)
app.include_router(admin.router)

# AL FINAL el frontend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_path = os.path.join(BASE_DIR, "frontend")

app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")