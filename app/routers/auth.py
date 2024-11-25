# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth import create_access_token
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


router = APIRouter()

class Settings:
    # ... (other settings)
    TEST_USERNAME: str = os.getenv("TEST_USERNAME")
    TEST_PASSWORD: str = os.getenv("TEST_PASSWORD")

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Here you should verify the user's credentials
    # For simplicity, we assume the user is valid if username and password match
    if form_data.username != settings.TEST_USERNAME or form_data.password != settings.TEST_PASSWORD:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
