# schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MemoryCreate(BaseModel):
    transcription: str
    paraphrase: str
    audio: bytes  # Il file audio sarà passato come base64 o raw data
    categories: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class Memory(BaseModel):
    id: int
    transcription: str
    paraphrase: str
    audio: bytes
    date: datetime
    categories: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

    class Config:
        from_attributes = True