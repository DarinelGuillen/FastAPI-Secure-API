# app/services/google_drive.py

from google.oauth2 import service_account
from googleapiclient.discovery import build
from app.core.config import settings
from fastapi import HTTPException

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

def get_credentials():
    creds = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return creds

def get_folder_id(folder_path):
    creds = get_credentials()
    try:
        service = build('drive', 'v3', credentials=creds)
        folder_names = folder_path.strip('/').split('/')
        parent_id = 'root'  # Start from the root folder
        for name in folder_names:
            query = f"'{parent_id}' in parents and name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = service.files().list(q=query, fields="files(id, name)").execute()
            items = results.get('files', [])
            if not items:
                raise HTTPException(status_code=404, detail=f"Folder '{name}' not found")
            parent_id = items[0]['id']
        return parent_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def list_files_in_folder():
    creds = get_credentials()
    try:
        service = build('drive', 'v3', credentials=creds)
        folder_path = settings.GOOGLE_FOLDER_APP_ONLY_ACCESS
        folder_id = get_folder_id(folder_path)
        query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.spreadsheet' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
