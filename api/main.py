from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MusicFile(BaseModel):
    file_name: str
    file_type: str
    bpm: int
    vocal_type: str
    file_upload: str
    waveform: str
    waveform_image: str

class Author(BaseModel):
    legal_name: str
    pseudonym: Optional[str]

class Track(BaseModel):
    id: str
    title: str
    music_store_musicfiles: List[MusicFile]
    music_store_author: Author
    thumbnail: Optional[str]
    mainFile: Optional[MusicFile]
    stems: List[MusicFile]

# Load samples data
with open('./samples.json', 'r') as f:
    samples = json.load(f)

@app.get("/api/tracks")
async def get_tracks():
    return samples