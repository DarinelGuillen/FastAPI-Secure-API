# app/main.py

import logging
from fastapi import FastAPI
from app.routers import auth, drive

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="My API",
    description="API para gestionar login y operaciones con Google Drive",
    version="1.0.0"
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(drive.router, prefix="/drive", tags=["drive"])

# Example endpoint
@app.get("/hello")
async def read_root():
    logger.info("Hello endpoint was called")
    return {"message": "Hello World"}
