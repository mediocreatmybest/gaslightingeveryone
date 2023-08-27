@echo off

if exist .\venv\Scripts\activate.bat (
    call .\venv\Scripts\activate.bat
    echo Using venv...
    streamlit run webui.py
) else (
    echo Virtual environment not found, trying to launch anyway...
    streamlit run webui.py
)
