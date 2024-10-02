# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from schemas import Memory
import uuid

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify which domains should have access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route to create a new memory
@app.post("/memories/", response_model=Memory)
def create_memory(memory: Memory):
    data = memory.model_dump(exclude_unset=True)
    if data.get('user_id'):
        data['user_id'] = str(data['user_id'])
    result = supabase.table("memories").insert(data).execute()
    return result.data[0]