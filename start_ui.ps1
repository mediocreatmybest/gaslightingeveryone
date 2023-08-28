$venv_path = ".\venv\Scripts\Activate"
if (Test-Path -Path $venv_path) {
    & $venv_path
    streamlit run --server.address localhost webui.py
} else {
    Write-Output "Virtual environment not found, trying to launch anyway..."
    streamlit run --server.address localhost webui.py
}
