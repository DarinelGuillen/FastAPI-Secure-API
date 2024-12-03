from fastapi import APIRouter, Depends, HTTPException
from app.services.google_drive import ensure_drive_setup, read_sheets, get_sheet_content
from app.services.auth import get_current_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/first", tags=["drive"])
async def drive_first(user_id: str = Depends(get_current_user)):
    """
    Endpoint para crear las carpetas y hojas de cálculo si no existen.
    """
    logger.info(f"Usuario {user_id} está accediendo a /drive/first")
    try:
        ensure_drive_setup(user_id)
        return {"message": "Carpetas y hojas de cálculo aseguradas correctamente."}
    except Exception as e:
        logger.error(f"Error en /drive/first: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al asegurar configuración de Drive.")

@router.get("/read", tags=["drive"])
async def drive_read(user_id: str = Depends(get_current_user)):
    """
    Endpoint para leer y listar las hojas de cálculo existentes.
    """
    logger.info(f"Usuario {user_id} está accediendo a /drive/read")
    try:
        sheets = read_sheets(user_id)
        return {"sheets": sheets}
    except Exception as e:
        logger.error(f"Error en /drive/read: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al leer las hojas de cálculo.")

@router.get("/sheet/{sheet_id}", tags=["drive"])
async def drive_sheet(sheet_id: str, user_id: str = Depends(get_current_user)):
    """
    Endpoint para obtener el contenido de una hoja de cálculo.
    """
    logger.info(f"Usuario {user_id} está accediendo a /drive/sheet/{sheet_id}")
    try:
        content = get_sheet_content(user_id, sheet_id)
        return {"values": content}
    except Exception as e:
        logger.error(f"Error en /drive/sheet/{sheet_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener el contenido de la hoja de cálculo.")
