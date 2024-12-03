# app/routers/auth.py

import os  # Importa os
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from app.services.auth import (
    create_access_token,
    verify_token,
    oauth2_scheme,
    get_user_credentials,
)
from app.schemas.user import User
from app.core.config import settings
from google_auth_oauthlib.flow import Flow
import pickle
from datetime import timedelta
import logging

from google.oauth2 import id_token
from google.auth.transport.requests import Request as GoogleRequest


# Ignorar la validación estricta de los scopes
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

# Permitir transporte inseguro
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

router = APIRouter()

# Configurar logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)  # Nivel de depuración

# Ruta para iniciar el login
@router.get("/login", tags=["auth"])
async def login():
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRET_JSON,
        scopes=[
            "openid",
            "email",
            "profile",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/spreadsheets"
        ],
        redirect_uri="http://localhost:8000/auth/callback",
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return RedirectResponse(authorization_url)

# Ruta para manejar el callback de OAuth2
@router.get("/callback", tags=["auth"])
async def callback(request: Request):
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRET_JSON,
        scopes=[
            "openid",
            "email",
            "profile",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/spreadsheets"
        ],
        redirect_uri="http://localhost:8000/auth/callback",
    )

    try:
        flow.fetch_token(authorization_response=str(request.url))
    except Exception as e:
        logger.error(f"Error al obtener el token: {e}")
        logger.error(f"Respuesta completa: {e.response.text if hasattr(e, 'response') else 'No hay respuesta'}")
        raise HTTPException(status_code=500, detail="Error al obtener el token.")

    if not flow.credentials:
        raise HTTPException(status_code=400, detail="Credenciales no obtenidas.")

    credentials = flow.credentials

    # Obtener información del usuario
    try:
        id_info = id_token.verify_oauth2_token(
            credentials.id_token,
            GoogleRequest(),
            settings.GOOGLE_CLIENT_ID
        )
        user_email = id_info.get('email')
        if not user_email:
            raise HTTPException(status_code=400, detail="No se pudo obtener el correo electrónico del usuario.")
    except ValueError as ve:
        logger.error(f"Error al verificar el token de ID: {ve}")
        raise HTTPException(status_code=400, detail="Token de ID inválido.")

    # Serializa las credenciales y guárdalas
    creds_data = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes
    }

    # En un entorno de producción, almacena estas credenciales de manera segura en una base de datos
    try:
        with open(f"user_credentials_USERNAME.pkl", "wb") as token:
            pickle.dump(creds_data, token)
    except Exception as e:
        logger.error(f"Error al guardar las credenciales: {e}")
        raise HTTPException(status_code=500, detail="Error al guardar las credenciales.")

    # Genera un token JWT para la sesión
    try:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_email}, expires_delta=access_token_expires
        )
    except Exception as e:
        logger.error(f"Error al generar el token JWT: {e}")
        raise HTTPException(status_code=500, detail="Error al generar el token de acceso.")

    # Redirige de vuelta al front-end con el token en el fragmento de la URL
    return RedirectResponse(f"http://localhost:3000/#access_token={access_token}")
