from app.schemas import EmailPriority, EmailPriorityRequest,EmailPriorityResponse

def detect_email_priority(request: EmailPriorityRequest) -> EmailPriorityResponse:
    email_text = f"{request.subject} {request.body}".lower()

    if any(
        word in email_text
        for word in [
            "urgent",
            "asap",
            "immediately",
            "emergency",
            "critical",
            "right away",
        ]
    ):
        priority = EmailPriority.urgent
        confidence = 0.90
        explanation = "The email contains urgent language requiring immediate attention."

    elif any(
        word in email_text
        for word in [
            "important",
            "deadline",
            "today",
            "by end of day",
            "eod",
            "soon",
        ]
    ):
        priority = EmailPriority.high
        confidence = 0.80
        explanation = "The email contains high priority, time-sensitive or important wording."

    elif any(
        word in email_text
        for word in [
            "whenever",
            "no rush",
            "when you have time",
            "not urgent",
            "low priority",
        ]
    ):
        priority = EmailPriority.low
        confidence = 0.75
        explanation = "The email suggests the request is not time-sensitive."

    else:
        priority = EmailPriority.normal
        confidence = 0.60
        explanation = "The email does not contain strong priority signals."

    return EmailPriorityResponse(
        priority=priority,
        confidence=confidence,
        explanation=explanation,
    )
