import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from .models import Draft, DraftCreate, Email, EmailSummary, Me, SentEmail, SummarySend, Activity
from .policy import PolicyError, ensure_summary_recipient_only
from pathlib import Path

from .storage import (
    attachment_file_path,
    create_draft as storage_create_draft,
    get_attachment,
    get_email,
    init_db,
    list_activity,
    list_drafts,
    list_emails,
    list_sent,
    reset_db,
    seed_emails,
    send_email,
)

STUDENT_ID = os.getenv("STUDENT_ID", "student-01")
STUDENT_EMAIL = os.getenv("STUDENT_EMAIL", f"{STUDENT_ID}@workshop.example")

STATIC_DIR = Path(__file__).resolve().parent / "static"


app = FastAPI(
    title="Workshop Fake Email API",
    description="A local training email provider for agentic AI labs.",
    version="0.1.0",
)


@app.on_event("startup")
def startup() -> None:
    init_db()
    seed_emails(STUDENT_EMAIL)


@app.exception_handler(PolicyError)
def policy_error_handler(_, exc: PolicyError):
    return JSONResponse(status_code=403, content={"error": "Policy violation", "reason": str(exc)})


@app.get("/", include_in_schema=False)
def webmail_ui() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/me", response_model=Me)
def me() -> Me:
    return Me(
        student_id=STUDENT_ID,
        email=STUDENT_EMAIL,
        permissions=[
            "read_email",
            "create_draft",
            "send_summary_to_self",
            "view_audit_log",
            "reset_inbox",
        ],
    )


@app.get("/emails", response_model=list[EmailSummary])
def emails() -> list[EmailSummary]:
    return [EmailSummary(**item) for item in list_emails(STUDENT_ID)]


@app.get("/emails/{email_id}", response_model=Email)
def email(email_id: str) -> Email:
    item = get_email(email_id, STUDENT_ID)
    if item is None:
        raise HTTPException(status_code=404, detail="Email not found")
    return Email(**item)


@app.get("/emails/{email_id}/attachments/{attachment_id}", include_in_schema=True)
def attachment(email_id: str, attachment_id: str) -> FileResponse:
    item = get_attachment(email_id, attachment_id, STUDENT_ID)
    if item is None:
        raise HTTPException(status_code=404, detail="Attachment not found")
    path = attachment_file_path(item)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Attachment file not found")
    return FileResponse(path, media_type=item["mime_type"], filename=item["filename"])


@app.post("/drafts", response_model=Draft)
def drafts(payload: DraftCreate) -> Draft:
    item = storage_create_draft(
        recipient=payload.to,
        subject=payload.subject,
        body=payload.body,
        in_reply_to=payload.in_reply_to,
        actor=STUDENT_ID,
    )
    return Draft(**item)


@app.get("/drafts", response_model=list[Draft])
def get_drafts() -> list[Draft]:
    return [Draft(**item) for item in list_drafts(STUDENT_ID)]


@app.post("/send-summary", response_model=SentEmail)
def send_summary(payload: SummarySend) -> SentEmail:
    ensure_summary_recipient_only(STUDENT_EMAIL, STUDENT_EMAIL)
    item = send_email(
        recipient=STUDENT_EMAIL,
        subject=payload.subject,
        body=payload.body,
        actor=STUDENT_ID,
    )
    return SentEmail(**item)


@app.post("/send", response_model=SentEmail)
def send_blocked(payload: DraftCreate) -> SentEmail:
    # Intentional teaching endpoint. It exists so students can see policy enforcement.
    ensure_summary_recipient_only(payload.to, STUDENT_EMAIL)
    item = send_email(payload.to, payload.subject, payload.body, STUDENT_ID)
    return SentEmail(**item)


@app.get("/sent", response_model=list[SentEmail])
def sent() -> list[SentEmail]:
    return [SentEmail(**item) for item in list_sent(STUDENT_ID)]


@app.get("/activity", response_model=list[Activity])
def activity() -> list[Activity]:
    return [Activity(**item) for item in list_activity()]


@app.post("/reset")
def reset() -> dict:
    reset_db(STUDENT_EMAIL, STUDENT_ID)
    return {"status": "reset", "student_id": STUDENT_ID, "email": STUDENT_EMAIL}
