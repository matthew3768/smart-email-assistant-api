from app.schemas import EmailSummaryRequest, EmailSummaryResponse
from app.services.ai_service import generate_ai_email_summary


def generate_fallback_summary(request: EmailSummaryRequest) -> str:
    body_preview = request.body.strip()

    if len(body_preview) > 120:
        body_preview = body_preview[:120].rstrip() + "..."

    return f"Email about '{request.subject}': {body_preview}"


def summarise_email(request: EmailSummaryRequest) -> EmailSummaryResponse:
    ai_summary = generate_ai_email_summary(request)

    if ai_summary:
        return EmailSummaryResponse(
            subject=request.subject,
            summary=ai_summary,
            used_ai=True,
        )

    return EmailSummaryResponse(
        subject=request.subject,
        summary=generate_fallback_summary(request),
        used_ai=False,
    )