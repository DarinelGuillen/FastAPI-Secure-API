# app/routers/drive.py

from fastapi import APIRouter, Depends, HTTPException
from app.services.google_drive import get_flow, list_files
from fastapi.responses import RedirectResponse
from app.services.auth import oauth2_scheme, verify_token

router = APIRouter()

@router.get("/authorize")
async def authorize():
    flow = get_flow()
    auth_url, _ = flow.authorization_url(prompt='consent')
    return RedirectResponse(auth_url)

@router.get("/oauth2callback")
async def oauth2callback(code: str):
    flow = get_flow()
    flow.fetch_token(code=code)
    credentials = flow.credentials
    # Aquí debes almacenar las credenciales del usuario de forma segura
    # Retornar un token o establecer una sesión
    return {"access_token": credentials.token}

@router.get("/files")
async def get_files(token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    # Recuperar el token de acceso de Google Drive del usuario
    google_token = "google-drive-access-token"
    files = list_files(google_token)
    return files
