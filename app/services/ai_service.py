import logging

from google import genai
from openai import OpenAI
from app.schemas import EmailDraftRequest, EmailSummaryRequest

from app.config import (
    AI_PROVIDER,
    GEMINI_API_KEY,
    GROK_API_KEY,
    GROK_BASE_URL,
    GROK_MODEL,
    GROQ_API_KEY,
    GROQ_BASE_URL,
    GROQ_MODEL,
    USE_AI,
)



logger = logging.getLogger(__name__)


def is_ai_available() -> bool:
    if not USE_AI:
        return False

    if AI_PROVIDER == "gemini":
        return bool(GEMINI_API_KEY)

    if AI_PROVIDER == "groq":
        return bool(GROQ_API_KEY)

    if AI_PROVIDER == "grok":
        return bool(GROK_API_KEY)

    return False


def generate_ai_draft_reply(request: EmailDraftRequest) -> str:
    if not is_ai_available():
        return ""

    prompt = f"""
You are an email assistant.

Write a helpful email reply using the requested tone.

Sender: {request.sender}
Subject: {request.subject}
Original email:
{request.body}

Tone: {request.tone.value}

Rules:
- Keep the reply concise.
- Do not invent facts.
- Do not promise actions that are not stated.
- Do not include a subject line.
- Start with a greeting.
- End with a suitable sign-off.
"""

    try:
        if AI_PROVIDER == "gemini":
            client = genai.Client(api_key=GEMINI_API_KEY)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )

            return response.text.strip()

        if AI_PROVIDER == "grok":
            client = OpenAI(
                api_key=GROK_API_KEY,
                base_url=GROK_BASE_URL,
            )
            response = client.chat.completions.create(
                model=GROK_MODEL,
                messages=[
                    {"role": "user", "content": prompt},
                ],
            )

            return response.choices[0].message.content.strip()

        if AI_PROVIDER == "groq":
            client = OpenAI(
                api_key=GROQ_API_KEY,
                base_url=GROQ_BASE_URL,
            )
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "user", "content": prompt},
                ],
            )

            return response.choices[0].message.content.strip()

    except Exception as exc:
        logger.warning("%s draft generation failed; using fallback reply: %s", AI_PROVIDER, exc)
        return ""

    return ""

def generate_ai_email_summary(request: EmailSummaryRequest) -> str:
    if not is_ai_available():
        return ""

    prompt = f"""
You are an email assistant.

Summarise the email clearly and concisely.

Subject: {request.subject}

Email body:
{request.body}

Rules:
- Use 1 to 2 sentences.
- Focus on the main point of the email.
- Do not invent details.
- Do not include a greeting or sign-off.
"""

    try:
        client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url=GROQ_BASE_URL,
        )
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You summarise emails clearly and accurately.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
            max_tokens=120,
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return ""

    
