#!/bin/bash

# Startup script for Todo API Backend

# Activate virtual environment
source venv/bin/activate

# Install dependencies if not already installed
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the FastAPI application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

deactivate