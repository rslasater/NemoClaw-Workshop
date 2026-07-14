from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


class Attachment(BaseModel):
    id: str
    filename: str
    mime_type: str = "application/octet-stream"
    url: Optional[str] = None


class EmailSummary(BaseModel):
    id: str
    sender: str
    to: str
    subject: str
    received_at: str
    read: bool
    labels: List[str] = Field(default_factory=list)
    has_attachments: bool = False
    attachment_count: int = 0
    conversation_id: Optional[str] = None
    thread_index: Optional[int] = None
    classification: str = "UNCLASSIFIED"
    importance: str = "normal"


class Email(EmailSummary):
    body: str
    cc: List[str] = Field(default_factory=list)
    attachments: List[Attachment] = Field(default_factory=list)


class DraftCreate(BaseModel):
    to: str
    subject: str
    body: str
    in_reply_to: Optional[str] = None


class Draft(BaseModel):
    id: str
    to: str
    subject: str
    body: str
    in_reply_to: Optional[str] = None
    status: str = "draft"
    created_at: str


class SummarySend(BaseModel):
    subject: str
    body: str


class SentEmail(BaseModel):
    id: str
    sender: str = ""
    to: str
    subject: str
    body: str
    sent_at: str
    cc: List[str] = Field(default_factory=list)
    attachments: List[Attachment] = Field(default_factory=list)
    has_attachments: bool = False
    attachment_count: int = 0
    conversation_id: Optional[str] = None
    thread_index: Optional[int] = None
    classification: str = "UNCLASSIFIED"
    importance: str = "normal"


class Activity(BaseModel):
    timestamp: str
    actor: str
    action: str
    target: str
    details: dict = Field(default_factory=dict)


class Me(BaseModel):
    student_id: str
    email: str
    permissions: List[str]
