$currentDirectory = Get-Location
set-location $currentDirectory\backend
venv\Scripts\Activate.ps1
uvicorn main:app --reload --port 5555