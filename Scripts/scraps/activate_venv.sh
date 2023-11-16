#!/bin/bash

venv_path="./venv/bin/activate"

if [ -f "$venv_path" ]; then
  source $venv_path
  python xyz_script.py
else
  echo "Virtual environment not found, trying to launch anyway..."
  python xyz_script.py
fi
