# app/routers/drive.py

from fastapi import APIRouter, Depends
from app.services.google_drive import list_files_in_folder
from app.services.auth import oauth2_scheme, verify_token

router = APIRouter()

@router.get("/files")
async def get_files(token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    files = list_files_in_folder()
    return files
