@echo off

if exist .\venv\Scripts\activate.bat (
    call .\venv\Scripts\activate.bat
    python xyz_script.py
) else (
    echo Virtual environment not found, trying to launch anyway...
    python xyz_script.py
)
