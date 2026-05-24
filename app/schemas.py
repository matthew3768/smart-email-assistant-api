from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import datetime

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
    category: EmailCategory
    suggested_reply: str
    tone: EmailReplyTone

class EmailClassificationRequest(BaseModel):
    subject: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)

class EmailClassificationResponse(BaseModel):
    category: EmailCategory
    confidence: float = Field(..., ge=0, le=1)
    explanation: str

class DraftReplyHistoryResponse(BaseModel):

    model_config=ConfigDict(from_attributes=True)

    id: int
    sender: str
    subject: str
    body: str
    tone: str
    suggested_reply: str
    created_at: datetime

   

class EmailClassificationHistoryResponse(BaseModel):

    model_config=ConfigDict(from_attributes=True)

    id: int
    subject: str
    body: str
    category: str
    confidence: float
    explanation: str
    created_at: datetime

    
class EmailPriority(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"
    urgent = "urgent"

class EmailPriorityRequest(BaseModel):
    subject: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)

class EmailPriorityResponse(BaseModel):
    priority: EmailPriority
    confidence: float = Field(..., ge=0, le=1)
    explanation: str