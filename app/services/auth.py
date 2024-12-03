

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings
import pickle
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import logging


logger = logging.getLogger(__name__)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crea un token JWT de acceso.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """
    Verifica y decodifica un token JWT.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Obtiene el usuario actual basado en el token.
    """
    user_id = verify_token(token)
    return user_id

def get_user_credentials(user_id: str):
    """
    Obtiene las credenciales de Google del usuario a partir del user_id.
    """
    try:
        with open(f"user_credentials_USERNAME.pkl", "rb") as token_file:
            creds_data = pickle.load(token_file)
        creds = Credentials(
            token=creds_data["token"],
            refresh_token=creds_data["refresh_token"],
            token_uri=creds_data["token_uri"],
            client_id=creds_data["client_id"],
            client_secret=creds_data["client_secret"],
            scopes=creds_data["scopes"]
        )
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        return creds
    except Exception as e:
        logger.exception("No se pudieron obtener las credenciales del usuario.")
        raise HTTPException(status_code=401, detail="No se pudieron obtener las credenciales del usuario.")
