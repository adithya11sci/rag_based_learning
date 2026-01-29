"""FastAPI Backend"""
import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

from .rag_engine import RAGEngine

app = FastAPI(title="RAG Learning Assistant")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

rag = RAGEngine()
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

class Question(BaseModel):
    question: str

@app.get("/")
async def root():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "index.html")
    return FileResponse(path) if os.path.exists(path) else {"message": "RAG API"}

@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(400, "Only PDF files allowed")
    path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        result = rag.process_pdf(path, file.filename)
        return result
    finally:
        if os.path.exists(path):
            os.remove(path)

@app.post("/api/ask")
async def ask(q: Question):
    return rag.ask(q.question)

@app.get("/api/status")
async def status():
    return rag.get_status()

@app.post("/api/clear")
async def clear():
    rag.clear()
    return {"success": True}

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

frontend = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend):
    app.mount("/static", StaticFiles(directory=frontend), name="static")
