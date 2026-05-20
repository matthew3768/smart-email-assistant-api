# Smart Email Assistant API

A FastAPI-based API for drafting, classifying, and eventually automating email replies.

## Features

- Health check endpoint
- Suggested email replies
- Email classification
- Request validation for required fields and allowed reply tones

## Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- Pytest

## Project Structure

```text
app/
  main.py
  schemas.py
  services/
    classification_service.py
    draft_service.py
tests/
  test_main.py
```

## Run Locally

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## Run Tests

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

## Common Issues

If PowerShell blocks virtual environment activation, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the virtual environment again:

```powershell
.\venv\Scripts\Activate.ps1
```
