# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from schemas import Memory, MemoryInput, MemoryParaphrased
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import requests
from io import BytesIO

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

client = OpenAI()
transcription_model = "whisper-1"
chat_model = "gpt-4o-mini"

categorie_predefinite = ["Lavoro", "Personale", "Famiglia", "Viaggio", "Salute", "Finanza", "Istruzione", "Intrattenimento", "Tecnologia", "Altro"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify which domains should have access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def transcribe_audio(audio_url):
    # Download the audio file from the URL
    response = requests.get(audio_url)
    
    # Check if the request was successful
    if response.status_code != 200:
        raise Exception("Failed to download audio file")
    
    # Use the content of the response as the audio file
    audio_file = BytesIO(response.content)
    audio_file.name = "audio.mp3"  # Set a name with the correct extension

    transcript = client.audio.transcriptions.create(
        model=transcription_model, 
        file=audio_file
    )
    return transcript.text


def paraphrase_memory(transcription: str):
    llm = ChatOpenAI(model=chat_model, temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Sei un assistente utile che aggiunge la punteggiatura corretta al testo, categorizza il testo in categorie predefinite e genera un titolo."),
        ("user", "Queste sono le categorie predefinite: {categories}. \nTesto:{input}")
    ])
    chain = prompt | llm.with_structured_output(MemoryParaphrased)
    return chain.invoke({"input": transcription, "categories": categorie_predefinite})


@app.post("/memories/", response_model=Memory)
def create_memory(memory_input: MemoryInput):
    # Transcribe audio
    transcription = transcribe_audio(memory_input.audio_url)
    memory_paraphrased = paraphrase_memory(transcription)
    
    # Create Memory object
    memory = Memory(
        transcription=transcription,
        paraphrase=memory_paraphrased.paraphrase,
        categories=memory_paraphrased.categories,
        latitude=memory_input.latitude,
        longitude=memory_input.longitude,
        audio_url=memory_input.audio_url,
        photo_url=memory_input.photo_url,
        video_url=memory_input.video_url,
        user_id=memory_input.user_id,
        title=memory_paraphrased.title
    )
    
    # Insert into Supabase
    data = memory.model_dump()
    data['user_id'] = str(data['user_id'])
    result = supabase.table("memories").insert(data).execute()
    
    return Memory(**result.data[0])