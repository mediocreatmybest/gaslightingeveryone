@echo off

:: Create a virtual environment named 'venv'
python -m venv venv

:: Activate the virtual environment
call venv\Scripts\activate.bat

:: Install packages from the requirements file
pip install -r ui-requirements.txt

:: Deactivate the virtual environment when done
call venv\Scripts\deactivate.bat
