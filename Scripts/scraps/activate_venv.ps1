$venv_path = ".\venv\Scripts\Activate"
if (Test-Path -Path $venv_path) {
    & $venv_path
    python xyz_script.py
} else {
    Write-Output "Virtual environment not found, trying to launch anyway..."
    python xyz_script.py
}
