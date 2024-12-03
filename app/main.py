

import logging
from fastapi import FastAPI
from app.routers import auth, drive


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="My API",
    description="API para gestionar login y operaciones con Google Drive",
    version="1.0.0"
)


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(drive.router, prefix="/drive", tags=["drive"])


@app.get("/hello", tags=["general"])
async def read_root():
    logger.info("Hello endpoint fue llamado")
    return {"message": "Hello World"}
