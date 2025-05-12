from langchain.llms import HuggingFaceHub
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.config import HF_API_KEY, LLM_MODEL, EMBEDDING_MODEL, DEFAULT_TEMPERATURE, MAX_TOKENS

def get_llm():
    """Initialize and return the language model."""
    if not HF_API_KEY:
        # Can still work without API key but with rate limits
        print("Warning: Hugging Face API key not set. Using models without authentication.")
    
    llm = HuggingFaceHub(
        huggingfacehub_api_token=HF_API_KEY,
        repo_id=LLM_MODEL,
        model_kwargs={
            "temperature": DEFAULT_TEMPERATURE,
            "max_length": MAX_TOKENS
        }
    )
    
    return llm

def get_embeddings():
    """Initialize and return the embeddings model."""
    # SentenceTransformers can be used locally without an API key
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

def get_chat_model():
    """
    Create a chat-like interface using a regular LLM.
    This is necessary because many free HF models don't have chat interfaces.
    """
    llm = get_llm()
    
    # Create a chat-like prompt template
    chat_template = """
    Context: {context}
    
    Chat History:
    {chat_history}
    
    User: {question}
    AI Assistant:
    """
    
    prompt = PromptTemplate(
        input_variables=["context", "chat_history", "question"],
        template=chat_template
    )
    
    # Create a chain
    return LLMChain(llm=llm, prompt=prompt) 