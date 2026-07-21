#!/bin/bash
# Run the FastAPI backend server

cd "$(dirname "$0")" || exit

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from .env.example - please configure it"
fi

# Install dependencies (optional)
# pip install -r ../requirements.txt

# Run the server
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
