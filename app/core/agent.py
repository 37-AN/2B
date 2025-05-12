import sys
import os
from typing import List, Dict, Any
from langchain.prompts import PromptTemplate

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.core.memory import MemoryManager
from app.core.llm import get_llm

class AssistantAgent:
    """Orchestrates the assistant's functionality, managing RAG and tools."""
    
    def __init__(self):
        self.memory_manager = MemoryManager()
        self.rag_chain = self.memory_manager.create_rag_chain()
        self.llm = get_llm()
        
        # Define a system prompt template
        self.system_template = """You are a personal AI assistant that helps the user with their tasks and questions.
You have access to the user's documents and notes through a retrieval system.
When answering questions, leverage this knowledge base to provide specific, factual information.
If the answer is not in the provided context, acknowledge that and give the best general answer you can.

Context from the user's documents:
{context}

Chat History:
{chat_history}

User: {question}
Assistant:"""
        
        self.rag_prompt = PromptTemplate(
            input_variables=["context", "chat_history", "question"],
            template=self.system_template
        )
    
    def query(self, question: str) -> Dict[str, Any]:
        """Process a user query and return a response."""
        # Use the RAG chain to get an answer
        response = self.rag_chain({"question": question})
        
        # Extract the answer and source documents
        answer = response["answer"]
        source_docs = response["source_documents"] if "source_documents" in response else []
        
        # Format source documents for display
        sources = []
        for doc in source_docs:
            metadata = doc.metadata
            sources.append({
                "content": doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content,
                "source": metadata.get("source", "Unknown"),
                "file_name": metadata.get("file_name", "Unknown"),
                "page": metadata.get("page", "N/A") if "page" in metadata else None
            })
        
        return {
            "answer": answer,
            "sources": sources
        }
    
    def add_conversation_to_memory(self, question: str, answer: str):
        """Add a conversation exchange to the memory for future context."""
        # Create metadata for the conversation
        metadata = {
            "type": "conversation",
            "question": question
        }
        
        # Add the exchange to the vector store
        self.memory_manager.add_texts([answer], [metadata]) 