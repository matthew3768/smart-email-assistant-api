from pydantic import BaseModel
from enum import Enum

class EmailReplyTone(str, Enum):
    freindly = "friendly"
    professional = "professional"
    concise = "concise"

class EmailDraftRequest(BaseModel):
    sender: str
    subject: str
    body: str
    tone: EmailReplyTone = EmailReplyTone.professional

class EmailDraftResponse(BaseModel):
    suggested_reply: str
    tone: EmailReplyTone