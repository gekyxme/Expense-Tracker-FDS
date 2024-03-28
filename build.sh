#!/bin/bash

# Create a virtual environment with Python 3.9
python3.9.9 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Since there's no manage.py, you can just start your Flask app directly
python app.py
