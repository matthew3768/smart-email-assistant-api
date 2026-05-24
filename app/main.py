from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import EmailDraftRequest, EmailDraftResponse, EmailClassificationRequest, EmailClassificationResponse, DraftReplyHistoryResponse, EmailClassificationHistoryResponse,EmailPriorityRequest, EmailPriorityResponse
from app.services.classification_service import classify_email_message, save_email_classification, get_classification_responses,delete_email_classifications
from app.services.draft_service import generate_draft_reply, save_draft_reply, get_draft_replies, delete_draft_reply
from app.services.priority_service import detect_email_priority
from app.database import engine, get_db
from app.models import Base


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Email Assistant API",
    description="An API for drafting, classifying, and automating email replies.",
    version="0.11.0",
)

@app.get("/")
def root():
    return {"message": "Smart Email Assistant API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/draft-reply", response_model=EmailDraftResponse)
def draft_reply(
    request: EmailDraftRequest,
    db: Session = Depends(get_db)
):
    response = generate_draft_reply(request)
    save_draft_reply(db, request, response)

    return response

@app.get("/drafts", response_model=list[DraftReplyHistoryResponse])
def list_draft_replies(db: Session = Depends(get_db)):
    return get_draft_replies(db)

@app.delete("/drafts/{draft_id}")
def delete_draft(draft_id: int, db:Session = Depends(get_db)):
    deleted = delete_draft_reply(db, draft_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Draft reply not found")
    
    return {"message": "Draft reply successfully deleted."}


@app.post("/classify-email", response_model=EmailClassificationResponse)
def classify_email(
    request: EmailClassificationRequest,
    db: Session = Depends(get_db),
):
    response = classify_email_message(request)
    save_email_classification(db, request, response)
    
    return response

@app.get("/classifications", response_model=list[EmailClassificationHistoryResponse])
def list_classification_responses(db: Session = Depends(get_db)):
    return get_classification_responses(db)

@app.delete("/classifications/{classification_id}")
def delete_classification(classification_id: int, db: Session = Depends(get_db)):
    deleted = delete_email_classifications(db, classification_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Email classification not found")
    
    return {"message": "Email classification successfully deleted"}

@app.post("/detect-priority", response_model=EmailPriorityResponse)
def detect_priority(request: EmailPriorityRequest):
    return detect_email_priority(request)
