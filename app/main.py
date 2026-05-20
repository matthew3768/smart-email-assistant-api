from fastapi import FastAPI
from app.schemas import EmailDraftRequest, EmailDraftResponse, EmailCategory, EmailClassificationRequest, EmailClassificationResponse

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
    if request.tone == "friendly":
        suggested_reply= (
            f"Hi {request.sender},\n\n"
            f"Thanks for reaching out about '{request.subject}'."
            f"I'll take a look and get back to you soon.\n\n"
            f"Best"

        )

    elif request.tone == "concise":
        suggested_reply = (
            f"Hi {request.sender},\n\n"
            f"Thanks for your email. I'll review this and respond shortly.\n\n"
            f"Best"
        )

    else:
        suggested_reply = (
            f"Hi {request.sender},\n\n"
            f"Thank you for your email about '{request.subject}'."
            f"I'll review and get back to you shortly.\n\n"
            f"Best regards"
        )
    

    return EmailDraftResponse(
        subject=request.subject,
        suggested_reply=suggested_reply,
        tone=request.tone,
    )   

@app.post("/classify-email", response_model=EmailClassificationResponse)
def classify_email(request: EmailClassificationRequest):
    email_text = f"{request.subject} {request.body}".lower()

    if any(word in email_text for word in ["complaint", "unhappy","issue","problem", "not working", "disappointed"]):
        category = EmailCategory.complaint
        confidence = 0.85
        explanation = "This email contains language hitting to a complaint or a problem."

    elif any(word in email_text for word in ["please", "could you", "can you", "would you"]):
         category = EmailCategory.request
         confidence = 0.80
         explanation = "This email appears to ask the recipient to take action."

    elif any(word in email_text for word in ["?", "how", "what", "when", "where", "why"]):
        category = EmailCategory.question
        confidence = 0.70
        explanation = "This email contains words hinting at a question."

    elif any(word in email_text for word in ["following up", "follow up", "checking in", "any update", "update on"]):
        category = EmailCategory.follow_up
        confidence =  0.85
        explanation = "This email appears to be hitting to be a follow up message"

    else:
        category = EmailCategory.general
        confidence = 0.60
        explanation = "This email dosen't seem to fit within any default category" 

    return EmailClassificationResponse(
        category=category,
        confidence=confidence,
        explanation=explanation
      
    )