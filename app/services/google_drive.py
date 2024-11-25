# app/services/google_drive.py

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from app.core.config import settings
from fastapi import HTTPException
import os

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_flow():
    return Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost:8000/drive/oauth2callback"]
            }
        },
        scopes=SCOPES
    )

def get_credentials(token: str):
    # En un caso real, debes almacenar y recuperar el token de acceso del usuario
    # Aquí, asumimos que el token es válido y lo usamos directamente
    creds = Credentials(token)
    return creds

def list_files(token: str):
    creds = get_credentials(token)
    try:
        service = build('drive', 'v3', credentials=creds)
        results = service.files().list(pageSize=10, fields="files(id, name)").execute()
        items = results.get('files', [])
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
