#!/bin/bash

venv_path="./venv/bin/activate"

if [ -f "$venv_path" ]; then
  source $venv_path
  streamlit run --server.address localhost webui.py
else
  echo "Virtual environment not found, trying to launch anyway..."
  streamlit run --server.address localhost webui.py
fi
