# Smart Email Assistant API

A FastAPI-based API for drafting, classifying, prioritising, storing, and managing email replies.

## Features

- Health check endpoint
- Suggested email replies
- Email classification
- Email priority detection
- SQLite database persistence
- Draft reply history, filtering, updates, and deletion
- Email classification history, filtering, and deletion
- Optional AI-generated draft replies with deterministic fallback replies
- Request validation for required fields and allowed reply tones

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Uvicorn
- Pytest
- python-dotenv
- OpenAI-compatible clients, Groq, and Google GenAI for optional AI draft generation

## Project Structure

```text
app/
  config.py
  database.py
  main.py
  models.py
  schemas.py
  services/
    ai_service.py
    classification_service.py
    draft_service.py
    priority_service.py
tests/
  test_main.py
```

Runtime data is stored in `email_assistant.db`, which is created automatically when the app starts.

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

## Optional AI Drafts

Draft replies work without external AI services by using local fallback logic. To enable AI-generated replies, create a `.env` file and set `USE_AI=true` with a supported provider.

```text
USE_AI=true
AI_PROVIDER=groq
GROQ_API_KEY=your_api_key_here
```

Supported `AI_PROVIDER` values are `groq`, `grok`, `xai`, `x.ai`, and `gemini`.

Provider-specific options:

```text
AI_API_KEY=shared_fallback_key
GROQ_API_KEY=your_groq_key
GROQ_BASE_URL=https://api.groq.com/openai/v1
GROQ_MODEL=llama-3.3-70b-versatile

GROK_API_KEY=your_xai_key
GROK_BASE_URL=https://api.x.ai/v1
GROK_MODEL=grok-4

GEMINI_API_KEY=your_gemini_key
```

If AI is disabled, missing a key, or the provider call fails, the API falls back to the built-in reply generator.

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

Interactive API docs are available at:

```text
http://127.0.0.1:8000/docs
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
