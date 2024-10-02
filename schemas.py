# schemas.py
from pydantic import BaseModel
from typing import List, Optional
import uuid

class Memory(BaseModel):
    transcription: Optional[str] = None
    paraphrase: Optional[str] = None
    categories: Optional[List[str]] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    audio_url: Optional[str] = None
    photo_url: Optional[str] = None
    video_url: Optional[str] = None
    user_id: Optional[uuid.UUID] = None
    title: Optional[str] = None

    class Config:
        from_attributes = True