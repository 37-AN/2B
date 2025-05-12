import streamlit as st
import os
import sys
import tempfile
from datetime import datetime
from typing import List, Dict, Any

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.core.agent import AssistantAgent
from app.core.ingestion import DocumentProcessor
from app.utils.helpers import get_document_path, format_sources, save_conversation
from app.config import LLM_MODEL, EMBEDDING_MODEL

# Set page config
st.set_page_config(
    page_title="Personal AI Assistant (Hugging Face)",
    page_icon="🤗",
    layout="wide"
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = AssistantAgent()

if "document_processor" not in st.session_state:
    st.session_state.document_processor = DocumentProcessor(st.session_state.agent.memory_manager)

# App title
st.title("🤗 Personal AI Assistant (Hugging Face)")

# Create a sidebar for uploading documents and settings
with st.sidebar:
    st.header("Upload Documents")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "csv"])
    
    if uploaded_file is not None:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        if st.button("Process Document"):
            with st.spinner("Processing document..."):
                try:
                    # Get a path to store the document
                    doc_path = get_document_path(uploaded_file.name)
                    
                    # Copy the file to the documents directory
                    with open(doc_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    
                    # Ingest the document
                    st.session_state.document_processor.ingest_file(tmp_path, {"original_name": uploaded_file.name})
                    
                    # Clean up the temporary file
                    os.unlink(tmp_path)
                    
                    st.success(f"Document {uploaded_file.name} processed successfully!")
                except Exception as e:
                    st.error(f"Error processing document: {str(e)}")
    
    st.header("Raw Text Input")
    text_input = st.text_area("Enter text to add to the knowledge base")
    
    if st.button("Add Text"):
        if text_input:
            with st.spinner("Adding text to knowledge base..."):
                try:
                    # Create metadata
                    metadata = {
                        "type": "manual_input",
                        "timestamp": str(datetime.now())
                    }
                    
                    # Ingest the text
                    st.session_state.document_processor.ingest_text(text_input, metadata)
                    
                    st.success("Text added to knowledge base successfully!")
                except Exception as e:
                    st.error(f"Error adding text: {str(e)}")
    
    # Display model information
    st.header("Models")
    st.write(f"**LLM**: [{LLM_MODEL}](https://huggingface.co/{LLM_MODEL})")
    st.write(f"**Embeddings**: [{EMBEDDING_MODEL}](https://huggingface.co/{EMBEDDING_MODEL})")
    
    # Add Hugging Face deployment info
    st.header("Deployment")
    st.write("This app can be easily deployed to [Hugging Face Spaces](https://huggingface.co/spaces) for free hosting.")
    
    # Link to Hugging Face
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <a href="https://huggingface.co" target="_blank">
            <img src="https://huggingface.co/front/assets/huggingface_logo.svg" width="200" alt="Hugging Face">
        </a>
    </div>
    """, unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
        # Display sources if available
        if message["role"] == "assistant" and "sources" in message:
            with st.expander("View Sources"):
                sources = message["sources"]
                if sources:
                    for i, source in enumerate(sources, 1):
                        st.write(f"{i}. {source['file_name']}" + (f" (Page {source['page']})" if source.get('page') else ""))
                        st.text(source['content'])
                else:
                    st.write("No specific sources used.")

# Chat input
if prompt := st.chat_input("Ask a question..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.agent.query(prompt)
            answer = response["answer"]
            sources = response["sources"]
            
            # Display the response
            st.write(answer)
            
            # Display sources in an expander
            with st.expander("View Sources"):
                if sources:
                    for i, source in enumerate(sources, 1):
                        st.write(f"{i}. {source['file_name']}" + (f" (Page {source['page']})" if source.get('page') else ""))
                        st.text(source['content'])
                else:
                    st.write("No specific sources used.")
            
            # Save conversation
            save_conversation(prompt, answer, sources)
            
            # Add assistant response to chat history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": answer,
                "sources": sources
            })
            
            # Update the agent's memory
            st.session_state.agent.add_conversation_to_memory(prompt, answer)

# Add a footer
st.markdown("---")
st.markdown("Built with LangChain, Hugging Face, and Qdrant")

if __name__ == "__main__":
    # This is used when running the file directly
    pass