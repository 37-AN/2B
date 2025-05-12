FROM python:3.10-slim

WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p data/documents data/vector_db

# Set environment variable to avoid TOKENIZERS_PARALLELISM warning
ENV TOKENIZERS_PARALLELISM=false

# Expose the Streamlit port
EXPOSE 8501

# Set the entrypoint command to run the Streamlit app
CMD ["streamlit", "run", "app/ui/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"] 