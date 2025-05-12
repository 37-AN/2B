import os
import sys
from datetime import datetime
from typing import List, Dict, Any

def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing invalid characters."""
    # Replace invalid characters with underscores
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def get_document_path(filename: str) -> str:
    """Get the path to store a document."""
    # Get the documents directory
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'documents')
    
    # Create the directory if it doesn't exist
    os.makedirs(docs_dir, exist_ok=True)
    
    # Sanitize the filename
    filename = sanitize_filename(filename)
    
    # Add a timestamp to make the filename unique
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    base, ext = os.path.splitext(filename)
    unique_filename = f"{base}_{timestamp}{ext}"
    
    return os.path.join(docs_dir, unique_filename)

def format_sources(sources: List[Dict[str, Any]]) -> str:
    """Format source documents for display."""
    if not sources:
        return "No sources found."
    
    formatted = []
    for i, source in enumerate(sources, 1):
        source_str = f"{i}. {source['file_name']} "
        if source.get('page'):
            source_str += f"(Page {source['page']}) "
        formatted.append(source_str)
    
    return "\n".join(formatted)

def save_conversation(question: str, answer: str, sources: List[Dict[str, Any]]) -> str:
    """Save a conversation to a file."""
    # Create a directory for conversations
    conv_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'conversations')
    os.makedirs(conv_dir, exist_ok=True)
    
    # Create a filename based on the timestamp and first few words of the question
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    question_slug = "_".join(question.split()[:5]).lower()
    question_slug = sanitize_filename(question_slug)
    filename = f"{timestamp}_{question_slug}.txt"
    
    # Format the conversation
    formatted_sources = format_sources(sources)
    content = f"Question: {question}\n\nAnswer: {answer}\n\nSources:\n{formatted_sources}\n"
    
    # Save the conversation
    filepath = os.path.join(conv_dir, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath 