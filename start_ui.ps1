$venv_path = ".\venv\Scripts\Activate"
if (Test-Path -Path $venv_path) {
    & $venv_path
    streamlit run webui.py
} else {
    Write-Output "Virtual environment not found, trying to launch anyway..."
    streamlit run webui.py
}
