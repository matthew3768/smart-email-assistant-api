from fastapi import FastAPI
from app.schemas import EmailDraftRequest, EmailDraftResponse

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
    suggetsted_reply = (
        f"hi {request.sender},\n\n"
        f"Thank you for your email about '{request.subject}'."
        f"I'll review your message and get back to you shortly.\n\n"
        f"Best Regards"
    )

    return EmailDraftResponse(
        suggested_reply=suggetsted_reply,
        tone=request.tone,
    )   