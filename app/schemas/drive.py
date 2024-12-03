# app/schemas/drive.py

from pydantic import BaseModel

class Sheet(BaseModel):
    id: str
    name: str

class SheetsResponse(BaseModel):
    sheets: list[Sheet]
