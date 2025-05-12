import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# API Keys
HF_API_KEY = os.getenv('HF_API_KEY', '')

# LLM Configuration
LLM_MODEL = os.getenv('LLM_MODEL', 'google/flan-t5-large')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')

# Vector Database
VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', './data/vector_db')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'personal_assistant')

# Application Settings
DEFAULT_TEMPERATURE = float(os.getenv('DEFAULT_TEMPERATURE', 0.7))
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 1000))
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 200))
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 512))

# Create a template .env file if it doesn't exist
def create_env_example():
    if not os.path.exists('.env.example'):
        with open('.env.example', 'w') as f:
            f.write("""# API Keys
HF_API_KEY=your_huggingface_api_key_here

# LLM Configuration
LLM_MODEL=google/flan-t5-large  # Free model with good performance
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Vector Database
VECTOR_DB_PATH=./data/vector_db
COLLECTION_NAME=personal_assistant

# Application Settings
DEFAULT_TEMPERATURE=0.7
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_TOKENS=512
""") 