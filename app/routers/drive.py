# app/routers/drive.py

from fastapi import APIRouter, Depends
from app.services.google_drive import list_files_in_folder
from app.services.auth import oauth2_scheme, verify_token
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/files")
async def get_files(token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    logger.info(f"User {user_id} is accessing /drive/files")
    files = list_files_in_folder()
    logger.info(f"Retrieved {len(files)} files from Google Drive")
    for file in files:
        logger.info(f"File ID: {file['id']}, Name: {file['name']}")
    return files
