# models.py
from sqlalchemy import Column, Integer, String, Text, LargeBinary, Float, TIMESTAMP
from database import Base

class Memory(Base):
    __tablename__ = "memories"
    
    id = Column(Integer, primary_key=True, index=True)
    transcription = Column(Text)
    paraphrase = Column(Text)
    audio = Column(LargeBinary)  # Per i file audio
    date = Column(TIMESTAMP)
    categories = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)