from fastapi import FastAPI
from app.schemas import EmailDraftRequest, EmailDraftResponse, EmailCategory, EmailClassificationRequest, EmailClassificationResponse
from app.services.classification_service import classify_email_message
from app.services.draft_service import generate_draft_reply

app = FastAPI(
    title="Smart Email Assistant API",
    description="An API for drafting, classifying, and automating email replies.",
    version="0.1.0",
)

@app.get("/")
def root():
    return {"message": "Smart Email Assistant API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/draft-reply", response_model=EmailDraftResponse)
def draft_reply(request: EmailDraftRequest):
    return generate_draft_reply(request)

@app.post("/classify-email", response_model=EmailClassificationResponse)
def classify_email(request:EmailClassificationRequest):
    return classify_email_message(request)

