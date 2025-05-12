# Personal AI Assistant with RAG (Hugging Face Edition)

A powerful personal AI assistant built with LangChain, integrating Retrieval-Augmented Generation (RAG) with a vector database (Qdrant) for improved contextual awareness and memory. This version uses Hugging Face models and can be deployed to Hugging Face Spaces for free hosting.

[![Open In Spaces](https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-spaces-sm.svg)](https://huggingface.co/spaces)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com)

## Features

- Large Language Model integration using Hugging Face's free models
- RAG-based memory system with vector database storage
- Document ingestion pipeline for various file types
- Simple web UI built with Streamlit
- Conversation history tracking and retrieval
- Free deployment on Hugging Face Spaces

## Project Structure

```
.
├── README.md
├── requirements.txt
├── .env.example
├── app.py                 # Main entry point for Hugging Face Spaces
├── space.py               # Hugging Face Spaces SDK integration
├── app/
│   ├── main.py            # FastAPI application entry point
│   ├── config.py          # Configuration settings
│   ├── ui/
│   │   └── streamlit_app.py # Streamlit web interface
│   ├── core/
│   │   ├── llm.py         # LLM integration (Hugging Face)
│   │   ├── memory.py      # RAG and vector store integration
│   │   ├── agent.py       # Agent orchestration
│   │   └── ingestion.py   # Document processing pipeline
│   └── utils/
│       └── helpers.py     # Utility functions
└── data/
    ├── documents/         # Store for uploaded documents
    └── vector_db/         # Local vector database storage
```

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your Hugging Face API keys (optional)
4. Start the Streamlit UI:
   ```
   streamlit run app/ui/streamlit_app.py
   ```

## Usage

1. Upload documents through the web interface
2. Chat with your assistant, which can now reference your documents
3. The assistant will automatically leverage your document knowledge to provide more personalized responses

## Deployment to Hugging Face Spaces

This app can be easily deployed to Hugging Face Spaces for free hosting:

1. Create a Hugging Face account at [huggingface.co](https://huggingface.co)
2. Set environment variables:
   ```
   export HF_USERNAME=your-username
   export HF_TOKEN=your-huggingface-token
   export SPACE_NAME=personal-rag-assistant  # optional
   ```
3. Run the deployment script:
   ```
   python space.py
   ```
4. Visit your deployed app at `https://huggingface.co/spaces/{your-username}/{space-name}`

Alternatively, you can manually create a new Space on Hugging Face and link it to your GitHub repository.

## Models Used

This implementation uses the following free models from Hugging Face:

- LLM: [google/flan-t5-large](https://huggingface.co/google/flan-t5-large) - A powerful instruction-tuned model
- Embeddings: [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) - Efficient embedding model

You can change these in the `.env` file.

## Extending

- Add more document loaders in `ingestion.py`
- Integrate additional tools in `agent.py`
- Customize the UI in `streamlit_app.py`
- Switch to a different LLM in `llm.py` and `.env` 