# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db
from datetime import date, datetime

# Crea le tabelle nel database (se non esistono)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Rotta per creare una nuova registrazione
@app.post("/memories/", response_model=schemas.Memory)
def create_memory(memory: schemas.MemoryCreate, db: Session = Depends(get_db)):
    db_memory = models.Memory(
        transcription=memory.transcription,
        paraphrase=memory.paraphrase,
        audio=memory.audio,
        categories=memory.categories,
        latitude=memory.latitude,
        longitude=memory.longitude,
        date=datetime.now()  # Imposta la data come datetime corrente
    )
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)
    return db_memory

# Rotta per ottenere tutte le registrazioni
@app.get("/memories/", response_model=list[schemas.Memory])
def read_memories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    memories = db.query(models.Memory).offset(skip).limit(limit).all()
    return memories

# Rotta per ottenere una registrazione specifica
@app.get("/memories/{memory_id}", response_model=schemas.Memory)
def read_memory(memory_id: int, db: Session = Depends(get_db)):
    memory = db.query(models.Memory).filter(models.Memory.id == memory_id).first()
    if memory is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    return memory