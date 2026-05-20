from app.schemas import EmailCategory, EmailClassificationRequest, EmailClassificationResponse

def classify_email_meessage(request: EmailClassificationRequest):
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