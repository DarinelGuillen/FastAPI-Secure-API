

import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from fastapi import HTTPException
import logging
from app.services.auth import get_user_credentials

logger = logging.getLogger(__name__)

def ensure_drive_setup(user_id: str):
    """
    Asegura que la carpeta y las hojas de cálculo existan en Google Drive del usuario.
    """
    logger.info("Asegurando configuración inicial de Google Drive para el usuario.")
    creds = get_user_credentials(user_id)

    folder_name = "Carpeta_Prueba_Mas_Descriptiva"

    try:
        folder_id = get_or_create_folder(creds, folder_name)
        logger.info(f"ID de la carpeta resuelta o creada: {folder_id}")

        sheet_names_with_data = {
            "Sheet1": [
                ["Nombre", "Edad", "Correo Electrónico"],
                ["Juan Pérez", "30", "juan.perez@example.com"],
                ["María López", "25", "maria.lopez@example.com"]
            ],
            "Sheet2": [
                ["Producto", "Cantidad", "Precio"],
                ["Laptop", "5", "$800"],
                ["Mouse", "15", "$20"]
            ],
            "Sheet3": [
                ["Proyecto", "Estado", "Fecha de Inicio"],
                ["API Development", "En progreso", "01/01/2024"],
                ["Website Redesign", "Completado", "15/02/2024"]
            ]
        }

        get_or_create_sheets(creds, folder_id, sheet_names_with_data)

        logger.info("Configuración inicial de Google Drive completada para el usuario.")
    except Exception as e:
        logger.exception("Error en ensure_drive_setup")
        raise HTTPException(status_code=500, detail=f"Error en la configuración de Google Drive: {str(e)}")

def get_or_create_folder(creds, folder_name):
    """
    Crea una carpeta en el directorio raíz del usuario si no existe.
    """
    try:
        service = build('drive', 'v3', credentials=creds)

        query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])

        if items:
            folder_id = items[0]['id']
            logger.info(f"Carpeta existente encontrada: {folder_name} (ID: {folder_id})")
        else:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = service.files().create(body=file_metadata, fields='id').execute()
            folder_id = folder.get('id')
            logger.info(f"Carpeta creada: {folder_name} (ID: {folder_id})")

        return folder_id
    except Exception as e:
        logger.exception("Error al crear o recuperar la carpeta")
        raise HTTPException(status_code=500, detail=f"Error al crear o recuperar la carpeta: {str(e)}")

def get_or_create_sheets(creds, folder_id, sheet_names_with_data):
    """
    Crea hojas de cálculo dentro de una carpeta con estructuras básicas si no existen.
    """
    try:
        drive_service = build('drive', 'v3', credentials=creds)

        for sheet_name, data in sheet_names_with_data.items():
            query = (
                f"mimeType='application/vnd.google-apps.spreadsheet' and "
                f"name='{sheet_name}' and trashed=false and '{folder_id}' in parents"
            )
            results = drive_service.files().list(q=query, fields="files(id, name)").execute()
            items = results.get('files', [])

            if items:
                spreadsheet_id = items[0]['id']
                logger.info(f"Hoja existente encontrada: {sheet_name} (ID: {spreadsheet_id})")
            else:
                file_metadata = {
                    'name': sheet_name,
                    'mimeType': 'application/vnd.google-apps.spreadsheet',
                    'parents': [folder_id]
                }
                sheet = drive_service.files().create(body=file_metadata, fields='id').execute()
                spreadsheet_id = sheet.get('id')
                logger.info(f"Hoja creada: {sheet_name} (ID: {spreadsheet_id})")

                create_sheet_with_structure(creds, spreadsheet_id, sheet_name, data)

    except Exception as e:
        logger.exception("Error al crear o recuperar las hojas de cálculo")
        raise HTTPException(status_code=500, detail=f"Error al crear o recuperar las hojas de cálculo: {str(e)}")

def create_sheet_with_structure(creds, spreadsheet_id, sheet_name, data):
    """
    Crea una nueva hoja dentro del Spreadsheet y añade una estructura básica.
    """
    try:
        sheets_service = build('sheets', 'v4', credentials=creds)

        add_sheet_request = {
            "requests": [{
                "addSheet": {
                    "properties": {
                        "title": sheet_name
                    }
                }
            }]
        }
        response = sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=add_sheet_request
        ).execute()

        sheet_id = response['replies'][0]['addSheet']['properties']['sheetId']
        logger.info(f"Hoja creada: {sheet_name} (ID: {sheet_id})")

        range_name = f"{sheet_name}!A1"
        body = {
            'values': data
        }
        sheets_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()

        logger.info(f"Estructura básica añadida a la hoja: {sheet_name}")
    except Exception as e:
        logger.exception(f"Error al crear o estructurar la hoja {sheet_name}")
        raise HTTPException(status_code=500, detail=f"Error al crear o estructurar la hoja {sheet_name}: {str(e)}")

def read_sheets(user_id: str):
    """
    Lee y lista las hojas de cálculo existentes en la carpeta del usuario.
    """
    logger.info("Leyendo hojas de cálculo existentes en la carpeta")
    creds = get_user_credentials(user_id)

    folder_name = "Carpeta_Prueba_Mas_Descriptiva"

    try:
        service = build('drive', 'v3', credentials=creds)

        query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            logger.warning(f"La carpeta '{folder_name}' no existe.")
            return {"message": f"La carpeta '{folder_name}' no existe."}

        folder_id = items[0]['id']
        logger.info(f"Carpeta encontrada: {folder_name} (ID: {folder_id})")

        drive_service = build('drive', 'v3', credentials=creds)
        query = (
            f"'{folder_id}' in parents and "
            f"mimeType='application/vnd.google-apps.spreadsheet' and trashed=false"
        )
        results = drive_service.files().list(q=query, fields="files(id, name)").execute()
        sheets = results.get('files', [])

        logger.info(f"Se encontraron {len(sheets)} hojas de cálculo en la carpeta '{folder_name}'")
        return sheets
    except Exception as e:
        logger.exception("Error al leer las hojas de cálculo")
        raise HTTPException(status_code=500, detail=f"Error al leer las hojas de cálculo: {str(e)}")

def get_sheet_content(user_id: str, spreadsheet_id: str):
    """
    Obtiene el contenido de la hoja de cálculo especificada.
    """
    creds = get_user_credentials(user_id)
    try:
        sheets_service = build('sheets', 'v4', credentials=creds)
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range="A1:Z1000"
        ).execute()
        values = result.get('values', [])
        return values
    except Exception as e:
        logger.exception("Error al obtener el contenido de la hoja de cálculo")
        raise HTTPException(status_code=500, detail=f"Error al obtener el contenido de la hoja de cálculo: {str(e)}")
