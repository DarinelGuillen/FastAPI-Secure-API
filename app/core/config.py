# app/core/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_CLIENT_SECRET_JSON: str = os.getenv("GOOGLE_CLIENT_SECRET_JSON")
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_SERVICE_ACCOUNT_FILE: str = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
    GOOGLE_FOLDER_APP_ONLY_ACCESS: str = os.getenv("GOOGLE_FOLDER_APP_ONLY_ACCESS")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()
