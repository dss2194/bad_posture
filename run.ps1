$currentDirectory = Get-Location
set-location $currentDirectory\backend
venv\Scripts\Activate.ps1
uvicorn main:app --reload  --workers 8 --port 5555