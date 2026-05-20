from pydantic import BaseModel, Field
from enum import Enum

class EmailReplyTone(str, Enum):
    friendly = "friendly"
    professional = "professional"
    concise = "concise"

class EmailCategory(str, Enum):
    question = "question"
    request = "request"
    complaint = "complaint"
    follow_up = "follow_up"
    general = "general"

class EmailDraftRequest(BaseModel):
    sender: str = Field(..., min_length=1)
    subject: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)
    tone: EmailReplyTone = EmailReplyTone.professional

class EmailDraftResponse(BaseModel):
    subject: str
    suggested_reply: str
    tone: EmailReplyTone

class EmailClassificationRequest(BaseModel):
    subject: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)

class EmailClassificationResponse(BaseModel):
    category: EmailCategory
    confidence: float = Field(..., ge=0, le=1)
    explanation: str
