from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth import create_access_token
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

class Settings:

    TEST_USERNAME: str = os.getenv("TEST_USERNAME")
    TEST_PASSWORD: str = os.getenv("TEST_PASSWORD")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


settings = Settings()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    if form_data.username != settings.TEST_USERNAME or form_data.password != settings.TEST_PASSWORD:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
