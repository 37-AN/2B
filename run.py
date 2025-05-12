#!/usr/bin/env python
import os
import sys
import argparse
import subprocess

def setup_environment():
    """Check if the environment is set up correctly."""
    # Check if .env file exists
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            print("Warning: .env file not found. Creating from .env.example...")
            with open('.env.example', 'r') as example, open('.env', 'w') as env:
                env.write(example.read())
            print("Created .env file. Please edit it with your API keys and settings.")
            sys.exit(1)
        else:
            print("Error: Neither .env nor .env.example file found.")
            sys.exit(1)
    
    # Create necessary directories
    os.makedirs('data/documents', exist_ok=True)
    os.makedirs('data/vector_db', exist_ok=True)

def run_api():
    """Run the FastAPI server."""
    print("Starting API server...")
    subprocess.run(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

def run_ui():
    """Run the Streamlit UI."""
    print("Starting Streamlit UI...")
    subprocess.run(["streamlit", "run", "app/ui/streamlit_app.py"])

def main():
    parser = argparse.ArgumentParser(description="Run the Personal AI Assistant")
    parser.add_argument('--api', action='store_true', help='Run the FastAPI server')
    parser.add_argument('--ui', action='store_true', help='Run the Streamlit UI')
    args = parser.parse_args()
    
    setup_environment()
    
    if args.api:
        run_api()
    elif args.ui:
        run_ui()
    else:
        print("Please specify either --api or --ui")
        print("Examples:")
        print("  python run.py --api   # Run the API server")
        print("  python run.py --ui    # Run the Streamlit UI")

if __name__ == "__main__":
    main() 