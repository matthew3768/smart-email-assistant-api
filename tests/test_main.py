from fastapi.testclient import TestClient

from app.main import app
from app.models import DraftReply,  EmailClassification
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
    assert data["category"] == "question"
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

def test_get_drafts_returns_saved_drafts():
    client.post(
        "/draft-reply",
        json={
            "sender": "Taylor",
            "subject": "Draft history test",
            "body": "can you check this appears in the history",
            "tone": "friendly",
        }
    )

    response = client.get("/drafts")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    matching_drafts = [
        draft for draft in data
        if draft["subject"] == "Draft history test"
    ]

    assert len(matching_drafts) > 0
    assert matching_drafts[0]["sender"] == "Taylor"
    assert matching_drafts[0]["tone"] == "friendly"
    assert "suggested_reply" in matching_drafts[0]

def test_classify_email_saves_to_database():
    response = client.post(
        "/classify-email",
        json={
             "subject": "Issue with my account",
             "body": "Hi, I am unhappy because my account is not working properly.",
        },
    )

    assert response.status_code == 200

    db = SessionLocal()
    saved_classification = (
        db.query(EmailClassification)
        .filter(EmailClassification.subject == "Issue with my account")
        .first()
    )
    db.close()

    assert saved_classification is not None
    assert saved_classification.category == "complaint"
    assert saved_classification.confidence == 0.85

def test_get_classifications_gets_saved_classifications():
    client.post(
        "/classify-email",
        json={
             "subject": "Document Classification test",
             "body": "Could you check this appears in the history?",
        },
    )

    response = client.get("/classifications")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    matching_classification = [
        classification for classification in data
        if classification["subject"] == "Document Classification test"
    ]

    assert len(matching_classification) > 0
    assert matching_classification[0]["subject"] == "Document Classification test"
    assert matching_classification[0]["body"] == "Could you check this appears in the history?"
    assert matching_classification[0]["category"] == "request"
    assert matching_classification[0]["confidence"] == 0.80
    assert "action" in matching_classification[0]["explanation"].lower()
    assert "created_at" in matching_classification[0]


def test_delete_existing_draft():
    create_response = client.post(
        "/draft-reply",
        json={
            "sender": "Morgan",
            "subject": "Delete draft test",
            "body": "Please create this draft so it can be deleted.",
            "tone": "professional",
        },
    )

    assert create_response.status_code == 200

    db = SessionLocal()
    saved_draft = (
        db.query(DraftReply)
        .filter(DraftReply.subject == "Delete draft test")
        .first()
    )

    db.close()

    assert saved_draft is not None

    delete_response = client.delete(f"/drafts/{saved_draft.id}")

    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "Draft reply successfully deleted."
    }
  
    db = SessionLocal()
    deleted_draft = (
        db.query(DraftReply)
        .filter(DraftReply.id == saved_draft.id)
        .first()
    )
    
    db.close()

    assert deleted_draft is None

def test_delete_missing_draft():
    response = client.delete("/drafts/9999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Draft reply not found"
    }

def test_delete_existing_classification():
    create_response = client.post(
        "/classify-email",
        json={
            "subject": "Delete Classification test",
            "body": "Classification deletion test"
        },  
    )
        
    assert create_response.status_code == 200

    db = SessionLocal()
    saved_classification = (
        db.query(EmailClassification)
        .filter(EmailClassification.body == "Classification deletion test")
        .first()
    )

    db.close()

    assert saved_classification is not None

    delete_response = client.delete(f"/classifications/{saved_classification.id}")

    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "Email classification successfully deleted"
    }

    db = SessionLocal()
    deleted_classification = (
        db.query(EmailClassification)
        .filter(EmailClassification.id == saved_classification.id)
        .first()
    )
    db.close()

    assert deleted_classification is  None

def test_delete_missing_classification():
    response = client.delete("/classifications/99999999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Email classification not found"
    }

def test_draft_reply_uses_complaint_category():
    response = client.post(
        "/draft-reply",
        json={
            "sender": "Alex",
            "subject": "Issue with account",
            "body": "I am unhappy because my account is not working.",
            "tone": "professional",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["category"] == "complaint"
    assert "sorry" in data["suggested_reply"].lower()
    assert data["tone"] == "professional"

def test_priority_urgent():
    response = client.post(
        "/detect-priority",
        json={
            "subject": "Urgent account issue",
            "body": "Please fix this immediately, this is critical.",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["priority"] == "urgent"
    assert data["confidence"] == 0.90
    assert "urgent" in data["explanation"].lower()

def test_priority_high():
    response = client.post(
        "/detect-priority",
        json={
            "subject": "Deadline today",
            "body": "This is important and needs to be completed by end of day.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["priority"] == "high"
    assert data["confidence"] == 0.80
    assert "high" in data["explanation"].lower()

def test_detect_priority_low():
    response = client.post(
        "/detect-priority",
        json={
            "subject": "Small update",
            "body": "No rush, please check this whenever you have time.",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["priority"] == "low"
    assert data["confidence"] == 0.75


def test_detect_priority_normal():
    response = client.post(
        "/detect-priority",
        json={
            "subject": "Weekly notes",
            "body": "Here are the notes from this week.",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["priority"] == "normal"
    assert data["confidence"] == 0.60


def test_detect_priority_rejects_empty_body():
    response = client.post(
        "/detect-priority",
        json={
            "subject": "Urgent account issue",
            "body": "",
        },
    )

    assert response.status_code == 422

def test_get_drafts_can_filter_by_sender():
    client.post(
        "/draft-reply",
        json={
            "sender": "FilterSenderTest",
            "subject": "Sender filter test",
            "body": "Can you check this sender filter?",
            "tone": "friendly",
        },
    )

    response = client.get("/drafts?sender=FilterSenderTest")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all("FilterSenderTest" in draft["sender"] for draft in data)


def test_get_drafts_can_filter_by_tone():
    client.post(
        "/draft-reply",
        json={
            "sender": "Tone Filter User",
            "subject": "Tone filter test",
            "body": "Can you check this tone filter?",
            "tone": "concise",
        },
    )

    response = client.get("/drafts?tone=concise")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(draft["tone"] == "concise" for draft in data)


def test_get_classifications_can_filter_by_category():
    client.post(
        "/classify-email",
        json={
            "subject": "Filter complaint test",
            "body": "I am unhappy because there is a problem with my account.",
        },
    )

    response = client.get("/classifications?category=complaint")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(classification["category"] == "complaint" for classification in data)


def test_get_classifications_can_filter_by_min_confidence():
    client.post(
        "/classify-email",
        json={
            "subject": "Filter confidence test",
            "body": "I am unhappy because there is a problem with my account.",
        },
    )

    response = client.get("/classifications?min_confidence=0.8")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(classification["confidence"] >= 0.8 for classification in data)