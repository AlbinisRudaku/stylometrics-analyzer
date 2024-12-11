#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Start the application
uvicorn src.app:app --host 0.0.0.0 --port $PORT 