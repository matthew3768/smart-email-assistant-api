from sqlalchemy.orm import Session

from app.models import DraftReply
from app.schemas import EmailDraftRequest, EmailDraftResponse

def generate_draft_reply(request: EmailDraftRequest) -> EmailDraftResponse:
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

def save_draft_reply(
        db: Session,
        request: EmailDraftRequest,
        response: EmailDraftResponse,
) -> DraftReply: 
    draft = DraftReply(
        sender=request.sender,
        subject=request.subject,
        body=request.body,
        tone=request.tone.value,
        suggested_reply=response.suggested_reply,
    )

    db.add(draft)
    db.commit()
    db.refresh(draft)

    return draft