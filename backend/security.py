from passlib.context import CryptContext
from jose import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

security = HTTPBearer()

# =========================
# PASSWORD
# =========================

def hash_password(password: str):
    return pwd_context.hash(password)


# Benjamin Orellana - 10/04/2026 - Verifica password hasheado con fallback para usuarios legacy en texto plano
def verify_password(password, hashed):
    try:
        return pwd_context.verify(password, hashed)
    except:
        return password == hashed


# =========================
# TOKEN
# =========================

def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(status_code=401, detail="Token inválido")


# =========================
# ROLES
# =========================

def require_role(roles: list):

    def role_checker(request: Request):

        user = request.session.get("user")

        if not user:
            raise HTTPException(status_code=401, detail="No autenticado")

        if user["rol"] not in roles:
            raise HTTPException(status_code=403, detail="Sin permisos")

        return user

    return role_checker