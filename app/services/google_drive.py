import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from fastapi import HTTPException
import logging

# Define your scopes b
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

# Setup logging
logger = logging.getLogger(__name__)

def get_credentials():
    """
    Retrieves Google service account credentials.
    """
    logger.info("Getting service account credentials")
    try:
        # Use the correct environment variable for the credentials file
        creds = service_account.Credentials.from_service_account_file(
            os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE"), scopes=SCOPES
        )
        return creds
    except Exception as e:
        logger.exception("Failed to get service account credentials")
        raise HTTPException(status_code=500, detail="Error retrieving Google credentials")


def get_folder_id(folder_path):
    """
    Resolves the folder ID from Google Drive using the given folder path.
    """
    logger.info(f"Resolving folder ID for path: {folder_path}")
    creds = get_credentials()

    if not folder_path:
        logger.error("Folder path is None or empty")
        raise HTTPException(status_code=400, detail="Folder path cannot be None or empty")

    try:
        service = build('drive', 'v3', credentials=creds)

        # Log all folders under root for debugging
        logger.info("Listing all folders under the root directory for debugging")
        query = "'root' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        root_folders = results.get('files', [])
        logger.info(f"Root folders: {[(folder['name'], folder['id']) for folder in root_folders]}")

        folder_names = folder_path.strip('/').split('/')
        parent_id = 'root'  # Start from the root folder

        for name in folder_names:
            logger.info(f"Looking for folder '{name}' under parent ID '{parent_id}'")
            query = f"'{parent_id}' in parents and name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = service.files().list(q=query, fields="files(id, name)").execute()
            items = results.get('files', [])

            if not items:
                logger.error(f"Folder '{name}' not found under parent ID '{parent_id}'")
                raise HTTPException(status_code=404, detail=f"Folder '{name}' not found")

            parent_id = items[0]['id']
            logger.info(f"Found folder '{name}' with ID '{parent_id}'")

        return parent_id
    except Exception as e:
        logger.exception("An error occurred while resolving the folder ID")
        raise HTTPException(status_code=500, detail=f"Error resolving folder ID: {str(e)}")


def list_files_in_folder():
    """
    Lists spreadsheet files in the specified folder.
    """
    logger.info("Listing files in the specified folder")
    creds = get_credentials()

    # Fetch the folder path from environment variables
    folder_path = os.getenv("GOOGLE_FOLDER_APP_ONLY_ACCESS")
    if not folder_path:
        logger.error("Environment variable 'GOOGLE_FOLDER_APP_ONLY_ACCESS' is not set")
        raise HTTPException(status_code=500, detail="Google folder path is not configured")

    try:
        service = build('drive', 'v3', credentials=creds)
        folder_id = get_folder_id(folder_path)
        logger.info(f"Folder ID resolved: {folder_id}")

        # Query for files in the resolved folder
        query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.spreadsheet' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])

        logger.info(f"Retrieved {len(items)} files from folder '{folder_path}'")
        return items
    except Exception as e:
        logger.exception("An error occurred while listing files in the folder")
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")
