# app/main.py

from fastapi import FastAPI
from app.routers import auth, drive

app = FastAPI(
    title="My API",
    description="API para gestionar login y operaciones con Google Drive",
    version="1.0.0"
)

# Incluir routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(drive.router, prefix="/drive", tags=["drive"])

# Endpoint de ejemplo
@app.get("/hello")
async def read_root():
    return {"message": "Hello World"}
