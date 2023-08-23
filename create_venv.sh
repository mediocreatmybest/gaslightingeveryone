#!/bin/bash

# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install packages from the requirements file
pip install -r ui-requirements.txt

# Deactivate the virtual environment when done
deactivate
