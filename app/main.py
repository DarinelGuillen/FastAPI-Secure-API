from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, drive
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="My API",
    description="API para gestionar login y operaciones con Google Drive",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to allowed origins, for example, ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(drive.router, prefix="/drive", tags=["drive"])

@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}

@app.get("/hello", tags=["general"])
async def read_root():
    logger.info("Hello endpoint fue llamado")
    return {"message": "Hello World"}
