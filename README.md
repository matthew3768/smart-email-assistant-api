# smart-email-assistant-api
A FastAPI-based email assistant API for drafting, classifying, and automating email replies.

## Features explained 
- Email classification
- suggested email replies 
- Auto-drafting responses
- Gmail/Outlook integration
- User approval before sending

## tech stack
- Python
- FastAPI
- Uvicorm

## run locally
- bash
- python -m venv venv
- source venv/Scripts/Activate.ps1
- pip install -r requirements.txt
- uvicorn app.main:app --reload

## Common issues
- If PowerShell blocks the virtual environment activation, run:

- powershell
- Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

### Then activate again:

- powershell
- .\venv\Scripts\Activate.ps1

## run tests
-powershell
-pytest