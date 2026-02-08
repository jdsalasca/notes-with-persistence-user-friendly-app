from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Dict, Any
import datetime
import uuid

# Import DummyLocal adapter
from database import DummyLocalDatabase

# Initialize app
app = FastAPI()
app.mount("/public", StaticFiles(directory="public"), name="public")

# Initialize DummyLocal Database
db = DummyLocalDatabase()

# --- API Endpoints ---

@app.post("/notes", response_model=Dict[str, Any])
async def create_note(request: Request):
    data = await request.json()
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        raise HTTPException(status_code=400, detail="Title and content are required")

    note_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    new_note = {
        "id": note_id,
        "title": title,
        "content": content,
        "created_at": timestamp,
        "updated_at": timestamp,
    }
    db.create_note(new_note)
    return new_note

@app.get("/notes", response_model=List[Dict[str, Any]])
async def get_notes():
    return db.get_all_notes()

@app.get("/notes/{note_id}", response_model=Dict[str, Any])
async def get_note(note_id: str):
    note = db.get_note(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.put("/notes/{note_id}", response_model=Dict[str, Any])
async def update_note(note_id: str, request: Request):
    data = await request.json()
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        raise HTTPException(status_code=400, detail="Title and content are required")

    updated_note_data = {
        "title": title,
        "content": content,
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    updated_note = db.update_note(note_id, updated_note_data)
    if updated_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note

@app.delete("/notes/{note_id}", response_model=Dict[str, Any])
async def delete_note(note_id: str):
    deleted_note = db.delete_note(note_id)
    if deleted_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return deleted_note

# Serve the index.html for the root path
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return FileResponse('public/index.html')
