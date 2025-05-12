#!/usr/bin/env python
"""
Main entry point for Hugging Face Spaces deployment.
This file starts the Streamlit UI when deployed to Hugging Face Spaces.
"""
import subprocess
import os
import sys

# Make sure the app directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Create necessary directories
os.makedirs('data/documents', exist_ok=True)
os.makedirs('data/vector_db', exist_ok=True)

# Run the Streamlit app
subprocess.run(["streamlit", "run", "app/ui/streamlit_app.py"]) 