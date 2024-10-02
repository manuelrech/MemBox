# schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

class MemoryInput(BaseModel):
    audio_url: str
    latitude: float
    longitude: float
    user_id: uuid.UUID
    photo_url: Optional[str] = None
    video_url: Optional[str] = None

class Memory(BaseModel):
    transcription: str
    paraphrase: str
    categories: List[str]
    latitude: float
    longitude: float
    audio_url: str
    photo_url: Optional[str] = None
    video_url: Optional[str] = None
    user_id: uuid.UUID
    title: str

    class Config:
        from_attributes = True

class MemoryParaphrased(BaseModel):
    paraphrase: str = Field(..., description="The transcription of the audio with punctuation and capitalization")
    categories: list[str] = Field(..., description="The categories that the memory belongs to")
    title: str = Field(..., description="The title of the memory")
