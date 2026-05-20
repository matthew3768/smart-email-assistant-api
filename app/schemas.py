from pydantic import BaseModel

class EmailDraftRequest(BaseModel):
    sender: str
    subject: str
    body: str
    tone: str = "professional"

class EmailDraftResponse(BaseModel):
    suggested_reply: str
    tone: str