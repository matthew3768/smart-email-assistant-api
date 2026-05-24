from sqlalchemy.orm import Session

from app.models import DraftReply
from app.schemas import EmailDraftRequest, EmailDraftResponse, EmailCategory, EmailClassificationRequest
from app.services.classification_service import classify_email_message

def generate_draft_reply(request: EmailDraftRequest) -> EmailDraftResponse:
    classification_request = EmailClassificationRequest(
        subject=request.subject,
        body=request.body,
    )
    classification_response = classify_email_message(classification_request)
    category = classification_response.category

    if category == EmailCategory.complaint:
        if request.tone == "concise":
            suggested_reply = (
                f"Hi {request.sender},\n\n"
                f"Thanks for letting me know. I’ll look into this issue and get back to you shortly.\n\n"
                f"Best"
            )
        elif request.tone == "friendly":
            suggested_reply = (
                f"Hi {request.sender},\n\n"
                f"Thanks for reaching out, and I’m sorry to hear there’s been an issue. "
                f"I’ll take a closer look and get back to you as soon as I can.\n\n"
                f"Best"
            )
        else:
            suggested_reply = (
                f"Hi {request.sender},\n\n"
                f"Thank you for your email. I’m sorry to hear about the issue you’ve experienced. "
                f"I’ll review this carefully and get back to you with an update shortly.\n\n"
                f"Best regards"
            )

    elif category == EmailCategory.question:
        if request.tone == "concise":
            suggested_reply = (
                f"Hi {request.sender},\n\n"
                f"Thanks for your question. I’ll check this and respond shortly.\n\n"
                f"Best"
            )
        elif request.tone == "friendly":
            suggested_reply = (
                f"Hi {request.sender},\n\n"
                f"Thanks for your message. I’ll look into your question about '{request.subject}' "
                f"and get back to you soon.\n\n"
                f"Best"
            )
        else:
            suggested_reply = (
                f"Hi {request.sender},\n\n"
                f"Thank you for your question about '{request.subject}'. "
                f"I’ll review this and respond with the relevant information shortly.\n\n"
                f"Best regards"
            )

    elif category == EmailCategory.request:
        if request.tone == "concise":
            suggested_reply = (
                f"Hi {request.sender},\n\n"
                f"Thanks. I’ll review this request and get back to you shortly.\n\n"
                f"Best"
            )
        elif request.tone == "friendly":
            suggested_reply = (
                f"Hi {request.sender},\n\n"
                f"Thanks for reaching out. I’ll take a look at your request and get back to you soon.\n\n"
                f"Best"
            )
        else:
            suggested_reply = (
                f"Hi {request.sender},\n\n"
                f"Thank you for your email. I’ll review your request and get back to you shortly.\n\n"
                f"Best regards"
            )

    elif category == EmailCategory.follow_up:
        if request.tone == "concise":
            suggested_reply = (
                f"Hi {request.sender},\n\n"
                f"Thanks for following up. I’ll check on this and update you shortly.\n\n"
                f"Best"
            )
        elif request.tone == "friendly":
            suggested_reply = (
                f"Hi {request.sender},\n\n"
                f"Thanks for checking in. I’ll look into this and send you an update soon.\n\n"
                f"Best"
            )
        else:
            suggested_reply = (
                f"Hi {request.sender},\n\n"
                f"Thank you for following up. I’ll review the current status and provide an update shortly.\n\n"
                f"Best regards"
            )

    else:
        if request.tone == "concise":
            suggested_reply = (
                f"Hi {request.sender},\n\n"
                f"Thanks for your email. I’ll review this and respond shortly.\n\n"
                f"Best"
            )
        elif request.tone == "friendly":
            suggested_reply = (
                f"Hi {request.sender},\n\n"
                f"Thanks for reaching out about '{request.subject}'. "
                f"I’ll take a look and get back to you soon.\n\n"
                f"Best"
            )
        else:
            suggested_reply = (
                f"Hi {request.sender},\n\n"
                f"Thank you for your email about '{request.subject}'. "
                f"I’ll review your message and get back to you shortly.\n\n"
                f"Best regards"
            )

    return EmailDraftResponse(
        subject=request.subject,
        category=category,
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

def get_draft_replies(db: Session, sender: str | None = None, tone: str | None = None) -> list[DraftReply]:
   
   query = db.query(DraftReply)

   if sender:
       query = query.filter(DraftReply.sender.ilike(f"%{sender}%"))
   
   if tone:
       query = query.filter(DraftReply.tone == tone)

   return query.order_by(DraftReply.created_at.desc()).all()



def delete_draft_reply(db:Session, draft_id: int) -> bool:
    draft = db.query(DraftReply).filter(DraftReply.id == draft_id).first()

    if draft is None:
        return False
    
    db.delete(draft)
    db.commit()

    return True

