from sqlalchemy.orm import Session

from app.schemas import EmailCategory, EmailClassificationRequest, EmailClassificationResponse
from app.models import EmailClassification

def classify_email_message(request: EmailClassificationRequest) -> EmailClassificationResponse:
    email_text = f"{request.subject} {request.body}".lower()

    if any(word in email_text for word in ["complaint", "unhappy","issue","problem", "not working", "disappointed"]):
        category = EmailCategory.complaint
        confidence = 0.85
        explanation = "This email contains language hinting at a complaint or a problem."

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
        explanation = "This email appears to be a follow-up message."

    else:
        category = EmailCategory.general
        confidence = 0.60
        explanation = "This email doesn't seem to fit within any default category." 

    return EmailClassificationResponse(
        category=category,
        confidence=confidence,
        explanation=explanation
      
    )


def save_email_classification(
    db: Session,
    request: EmailClassificationRequest,
    response: EmailClassificationResponse,
) -> EmailClassification:
    classification = EmailClassification(
        subject=request.subject,
        body=request.body,
        category=response.category.value,
        confidence=response.confidence,
        explanation=response.explanation,
    )

    db.add(classification)
    db.commit()
    db.refresh(classification)

    return classification

def get_classification_responses(db: Session, category: str | None = None, min_confidence: float | None = None) -> list[EmailClassification]:
    query = db.query(EmailClassification)

    if category:
        query = query.filter(EmailClassification.category == category)

    if min_confidence:
        query = query.filter(EmailClassification.confidence >= min_confidence)
   
    return query.order_by(EmailClassification.created_at.desc()).all()

def delete_email_classifications(db: Session, classification_id: int) -> bool:
    classification = db.query(EmailClassification).filter(EmailClassification.id == classification_id).first()

    if classification is None:
        return False
    
    db.delete(classification)
    db.commit()

    return True
