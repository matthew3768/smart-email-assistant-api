from fastapi.testclient import TestClient

from app.main import app
from app.models import DraftReply
from app.database import SessionLocal

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()== {
        "message": "Smart Email Assistant API is running"
    }

def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok"
    }
def test_draft_reply_endpoint():
    response = client.post(
        "/draft-reply",
        json={
            "sender": "Alex",
            "subject": "Project meeting",
            "body": "Hi are we still okay to meet tomorrow?",
            "tone": "professional",
        },

    )

    assert response.status_code == 200

    data = response.json()
    assert data["subject"] == "Project meeting"
    assert data["tone"] == "professional"
    assert "suggested_reply" in data
    assert "Hi Alex" in data["suggested_reply"]

def test_classify_email_endpoint():
    response = client.post(
        "/classify-email",
        json={
           "subject": "Issue with my account",
           "body": "Hi, I am unhappy because my account is not working properly."
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["category"] == "complaint"
    assert data["confidence"] == 0.85
    assert "complaint" in data["explanation"].lower()


def test_invalid_tone_returns_validation_error():
     response = client.post(
        "/draft-reply",
        json={
            "sender": "Alex",
            "subject": "Project meeting",
            "body": "Hi, are we still okay to meet tomorrow?",
            "tone": "angry",
        },
    )
     
     assert response.status_code == 422

def test_draft_reply_rejects_empty_sender():
    response = client.post(
        "/draft-reply",
        json={
            "sender": "",
            "subject": "Project meeting",
            "body": "Hi, are we still meeting tomorrow",
            "tone": "professional",
        },
    )    

    assert response.status_code == 422   

def test_draft_reply_rejects_empty_subject():
    response = client.post(
        "/draft-reply",
        json={
            "sender": "Alex",
            "subject": "",
            "body": "Hi, are we still meeting tomorrow?",
            "tone": "professional",
        },
    )

    assert response.status_code == 422


def test_draft_reply_rejects_empty_body():
    response = client.post(
        "/draft-reply",
        json={
            "sender": "Alex",
            "subject": "Project meeting",
            "body": "",
            "tone": "professional",
        },
    )

    assert response.status_code == 422


def test_classify_email_rejects_empty_subject():
    response = client.post(
        "/classify-email",
        json={
            "subject": "",
            "body": "Hi, I am unhappy because my account is not working properly.",
        },
    )

    assert response.status_code == 422


def test_classify_email_rejects_empty_body():
    response = client.post(
        "/classify-email",
        json={
            "subject": "Issue with my account",
            "body": "",
        },
    )

    assert response.status_code == 422

def test_draft_reply_is_saved_to_database():
    response = client.post(
        "/draft-reply",
        json={
            "sender":"Jamie",
            "subject": "Database test",
            "body": "Can you confirm that this is saving?",
            "tone": "concise",
        },
    )

    assert response.status_code == 200

    db = SessionLocal()
    saved_draft = (
        db.query(DraftReply)
        .filter(DraftReply.subject == "Database test")
        .first()
    )
    db.close()

    assert saved_draft is not None
    assert saved_draft.sender == "Jamie"
    assert saved_draft.tone == "concise"
    assert "Thanks for your email" in saved_draft.suggested_reply
