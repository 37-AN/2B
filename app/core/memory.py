import os
import sys
from langchain.vectorstores import Qdrant
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.config import VECTOR_DB_PATH, COLLECTION_NAME
from app.core.llm import get_llm, get_embeddings, get_chat_model

class MemoryManager:
    """Manages the RAG memory system using a vector database."""
    
    def __init__(self):
        self.embeddings = get_embeddings()
        self.llm = get_llm()
        self.chat_model = get_chat_model()
        self.client = self._init_qdrant_client()
        self.vectorstore = self._init_vector_store()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
    def _init_qdrant_client(self):
        """Initialize the Qdrant client."""
        os.makedirs(VECTOR_DB_PATH, exist_ok=True)
        return QdrantClient(path=VECTOR_DB_PATH)
    
    def _init_vector_store(self):
        """Initialize the vector store."""
        collections = self.client.get_collections().collections
        collection_names = [collection.name for collection in collections]
        
        # Get vector dimension from the embedding model
        vector_size = len(self.embeddings.embed_query("test"))
        
        if COLLECTION_NAME not in collection_names:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
            
        return Qdrant(
            client=self.client, 
            collection_name=COLLECTION_NAME,
            embeddings=self.embeddings
        )
    
    def get_retriever(self):
        """Get the retriever for RAG."""
        return self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
    
    def create_rag_chain(self):
        """Create a RAG chain for question answering."""
        # Using the chat model created with the regular LLM
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.get_retriever(),
            memory=self.memory,
            return_source_documents=True
        )
    
    def add_texts(self, texts, metadatas=None):
        """Add texts to the vector store."""
        return self.vectorstore.add_texts(texts=texts, metadatas=metadatas)
    
    def similarity_search(self, query, k=5):
        """Perform a similarity search."""
        return self.vectorstore.similarity_search(query, k=k) 