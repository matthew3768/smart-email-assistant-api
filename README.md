# Smart Email Assistant API

A FastAPI-based API for drafting, classifying, storing, and managing email replies.

## Features

- Health check endpoint
- Suggested email replies
- Email classification
- Email priority detection
- SQLite database persistence
- Draft reply history, filtering, updates, and deletion
- Email classification history, filtering, and deletion
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
    priority_service.py
tests/
  test_main.py
```

## API Endpoints

```text
GET     /                         Health message
GET     /health                   Health status
POST    /draft-reply              Generate and save a draft reply
GET     /drafts                   List saved draft replies, optionally filtered by sender or tone
PUT     /drafts/{draft_id}        Update a saved draft reply
DELETE  /drafts/{draft_id}        Delete a saved draft reply
POST    /classify-email           Classify and save an email
GET     /classifications          List saved classifications, optionally filtered by category or minimum confidence
DELETE  /classifications/{id}     Delete a saved email classification
POST    /detect-priority          Detect email priority without saving it
```

## Query Filters

```text
GET /drafts?sender=Alex
GET /drafts?tone=concise
GET /classifications?category=complaint
GET /classifications?min_confidence=0.8
```

Allowed draft tones are `friendly`, `professional`, and `concise`.

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
