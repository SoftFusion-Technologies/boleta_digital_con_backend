from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Benjamin Orellana - 10/04/2026 - Ajusta credenciales reales de MySQL y base activa del proyecto
DATABASE_URL = "mysql+pymysql://root:123456@localhost/tecnica_nro1"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()