import os
import sys
from typing import List, Dict, Any
from langchain.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.config import CHUNK_SIZE, CHUNK_OVERLAP
from app.core.memory import MemoryManager

class DocumentProcessor:
    """Processes documents for ingestion into the vector database."""
    
    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
    
    def process_file(self, file_path: str) -> List[str]:
        """Process a file and return a list of document chunks."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Get the file extension
        _, extension = os.path.splitext(file_path)
        extension = extension.lower()
        
        # Load the file using the appropriate loader
        if extension == '.pdf':
            loader = PyPDFLoader(file_path)
        elif extension == '.txt':
            loader = TextLoader(file_path)
        elif extension == '.csv':
            loader = CSVLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {extension}")
        
        # Load and split the documents
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)
        
        return chunks
    
    def ingest_file(self, file_path: str, metadata: Dict[str, Any] = None) -> List[str]:
        """Ingest a file into the vector database."""
        # Process the file
        chunks = self.process_file(file_path)
        
        # Add metadata to each chunk
        if metadata is None:
            metadata = {}
        
        # Add file path to metadata
        base_metadata = {
            "source": file_path,
            "file_name": os.path.basename(file_path)
        }
        base_metadata.update(metadata)
        
        # Prepare chunks and metadatas
        texts = [chunk.page_content for chunk in chunks]
        metadatas = []
        
        for i, chunk in enumerate(chunks):
            chunk_metadata = base_metadata.copy()
            if hasattr(chunk, 'metadata'):
                chunk_metadata.update(chunk.metadata)
            chunk_metadata["chunk_id"] = i
            metadatas.append(chunk_metadata)
        
        # Store in vector database
        ids = self.memory_manager.add_texts(texts, metadatas)
        
        return ids
    
    def ingest_text(self, text: str, metadata: Dict[str, Any] = None) -> List[str]:
        """Ingest raw text into the vector database."""
        if metadata is None:
            metadata = {}
        
        # Split the text
        chunks = self.text_splitter.split_text(text)
        
        # Prepare metadatas
        metadatas = []
        for i in range(len(chunks)):
            chunk_metadata = metadata.copy()
            chunk_metadata["chunk_id"] = i
            chunk_metadata["source"] = "direct_input"
            metadatas.append(chunk_metadata)
        
        # Store in vector database
        ids = self.memory_manager.add_texts(chunks, metadatas)
        
        return ids 