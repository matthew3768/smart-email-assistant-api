from app.config import OPENAI_API_KEY, USE_AI
from app.schemas import EmailDraftRequest


def is_ai_available() -> bool:
    return USE_AI and bool(OPENAI_API_KEY)


def generate_ai_draft_reply(request: EmailDraftRequest) -> str:
    """
    Placeholder for AI-generated email replies.

    This will later call an AI model when USE_AI=true and an API key is available.
    For now, it returns a safe placeholder response.
    """
    if not is_ai_available():
        return ""

    return (
        f"Hi {request.sender},\n\n"
        f"This is where an AI-generated reply about '{request.subject}' would be created.\n\n"
        f"Best regards"
    )