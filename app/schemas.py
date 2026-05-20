from pydantic import BaseModel
from enum import Enum

class EmailReplyTone(str, Enum):
    freindly = "friendly"
    professional = "professional"
    concise = "concise"

class EmailCategory(str, Enum):
    question = "question"
    request = "request"
    complaint = "complaint"
    follow_up = "follow_up"
    general = "general"

class EmailDraftRequest(BaseModel):
    sender: str
    subject: str
    body: str
    tone: EmailReplyTone = EmailReplyTone.professional

class EmailDraftResponse(BaseModel):
    suggested_reply: str
    tone: EmailReplyTone

class EmailClassificationRequest(BaseModel):
    subject: str
    body: str

class EmailClassificationResponse(BaseModel):
    category: EmailCategory
    confidence: float
    explanation: str