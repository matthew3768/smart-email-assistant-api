# Smart Email Assistant API

A FastAPI-based API for drafting, classifying, storing, and managing email replies.

## Features

- Health check endpoint
- Suggested email replies
- Email classification
- SQLite database persistence
- Draft reply history and deletion
- Email classification history and deletion
- Request validation for required fields and allowed reply tones

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Uvicorn
- Pytest

## Project Structure

```text
app/
  database.py
  main.py
  models.py
  schemas.py
  services/
    classification_service.py
    draft_service.py
tests/
  test_main.py
```

## API Endpoints

```text
GET     /                         Health message
GET     /health                   Health status
POST    /draft-reply              Generate and save a draft reply
GET     /drafts                   List saved draft replies
DELETE  /drafts/{draft_id}        Delete a saved draft reply
POST    /classify-email           Classify and save an email
GET     /classifications          List saved email classifications
DELETE  /classifications/{id}     Delete a saved email classification
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
