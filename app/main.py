import os
import sys
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Request, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import tempfile

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.core.agent import AssistantAgent
from app.core.ingestion import DocumentProcessor
from app.utils.helpers import get_document_path
from app.config import create_env_example

# Create .env.example file if it doesn't exist
create_env_example()

# Create FastAPI app
app = FastAPI(
    title="Personal AI Assistant API",
    description="API for a personal AI assistant with RAG capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent and document processor
agent = AssistantAgent()
document_processor = DocumentProcessor(agent.memory_manager)

# Define request and response models
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]

class TextIngestionRequest(BaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = None

# Define API endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to the Personal AI Assistant API"}

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Query the assistant with a question."""
    try:
        response = agent.query(request.query)
        
        # Add the conversation to memory
        agent.add_conversation_to_memory(request.query, response["answer"])
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest/text")
async def ingest_text(request: TextIngestionRequest):
    """Ingest text into the knowledge base."""
    try:
        metadata = request.metadata or {}
        
        # Add the text to the knowledge base
        ids = document_processor.ingest_text(request.text, metadata)
        
        return {"message": "Text ingested successfully", "ids": ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest/file")
async def ingest_file(file: UploadFile = File(...)):
    """Ingest a file into the knowledge base."""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Get a path to store the document
        doc_path = get_document_path(file.filename)
        
        # Copy the file to the documents directory
        with open(doc_path, "wb") as f:
            # Seek to the beginning of the file
            await file.seek(0)
            content = await file.read()
            f.write(content)
        
        # Ingest the document
        metadata = {"original_name": file.filename}
        ids = document_processor.ingest_file(tmp_path, metadata)
        
        # Clean up the temporary file
        os.unlink(tmp_path)
        
        return {"message": f"File {file.filename} ingested successfully", "ids": ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the application
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 