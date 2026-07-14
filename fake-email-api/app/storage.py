import json
import os
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

DB_PATH = os.getenv("EMAIL_API_DB", "/app/data/email_lab.sqlite")
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DEFAULT_SEED_PATH = DATA_DIR / "atas_seed_emails.json"
FALLBACK_SEED_PATH = DATA_DIR / "seed_emails.json"
DEFAULT_MAILBOX_OWNER_EMAIL = "james.maddox@jiaitf.example"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def seed_path() -> Path:
    configured = os.getenv("EMAIL_API_SEED_PATH")
    if configured:
        return Path(configured)
    return DEFAULT_SEED_PATH if DEFAULT_SEED_PATH.exists() else FALLBACK_SEED_PATH


def format_person(person: Any) -> str:
    if isinstance(person, str):
        return person
    if isinstance(person, dict):
        name = str(person.get("name", "")).strip()
        email = str(person.get("email", "")).strip()
        if name and email:
            return f"{name} <{email}>"
        return name or email
    return str(person)


def format_people(people: Any) -> str:
    if not people:
        return ""
    if isinstance(people, list):
        return "; ".join(format_person(person) for person in people)
    return format_person(people)


def extract_email(value: Any) -> str:
    text = format_person(value).strip()
    match = re.search(r"<([^>]+)>", text)
    return (match.group(1) if match else text).strip().lower()


def mailbox_owner_emails(student_email: str) -> set[str]:
    configured = os.getenv("MAILBOX_OWNER_EMAIL", DEFAULT_MAILBOX_OWNER_EMAIL)
    return {email.strip().lower() for email in (student_email, configured) if email.strip()}


def people_emails(people: Any) -> set[str]:
    if not people:
        return set()
    if isinstance(people, list):
        return {extract_email(person) for person in people if extract_email(person)}
    text = format_person(people)
    formatted = {match.strip().lower() for match in re.findall(r"<([^>]+)>", text)}
    if formatted:
        return formatted
    return {part.strip().lower() for part in re.split(r"[;,]", text) if part.strip()}


def normalize_attachment(attachment: Any) -> Dict[str, str]:
    if isinstance(attachment, str):
        filename = attachment
        return {
            "id": filename,
            "filename": filename,
            "mime_type": "application/octet-stream",
            "path": f"attachments/{filename}",
        }

    filename = str(attachment.get("filename", attachment.get("id", "attachment"))).strip()
    return {
        "id": str(attachment.get("id", filename)),
        "filename": filename,
        "mime_type": str(attachment.get("mime_type", "application/octet-stream")),
        "path": str(attachment.get("path", f"attachments/{filename}")),
    }


def attachment_with_url(email_id: str, attachment: Any) -> Dict[str, str]:
    normalized = normalize_attachment(attachment)
    return {
        "id": normalized["id"],
        "filename": normalized["filename"],
        "mime_type": normalized["mime_type"],
        "url": f"/emails/{email_id}/attachments/{normalized['id']}",
    }


def sent_attachment_with_url(sent_id: str, attachment: Any) -> Dict[str, str]:
    normalized = normalize_attachment(attachment)
    return {
        "id": normalized["id"],
        "filename": normalized["filename"],
        "mime_type": normalized["mime_type"],
        "url": f"/sent/{sent_id}/attachments/{normalized['id']}",
    }


def normalize_seed_email(email: Dict[str, Any], student_email: str) -> Dict[str, Any]:
    metadata = dict(email.get("metadata", {}))
    if "conversation_id" in email:
        metadata["conversation_id"] = email.get("conversation_id")
    if "thread_index" in email:
        metadata["thread_index"] = email.get("thread_index")
    if "classification" in email:
        metadata["classification"] = email.get("classification")
    if "importance" in email:
        metadata["importance"] = email.get("importance")
    if "in_reply_to" in email:
        metadata["in_reply_to"] = email.get("in_reply_to")
    if "references" in email:
        metadata["references"] = email.get("references", [])
    if "sent_at" in email:
        metadata["sent_at"] = email.get("sent_at")
    cc_value = email.get("cc", metadata.get("cc", []))
    if isinstance(cc_value, list):
        metadata["cc"] = [format_person(person) for person in cc_value]
    elif cc_value:
        metadata["cc"] = [format_person(cc_value)]
    else:
        metadata["cc"] = []

    return {
        "id": email["id"],
        "sender": format_person(email["from"]),
        "recipient": format_people(email.get("to")) or student_email,
        "subject": email["subject"],
        "body": email["body"],
        "received_at": email.get("received_at") or email.get("sent_at"),
        "read": int(bool(email.get("read", email.get("is_read", False)))),
        "labels": email.get("labels", []),
        "attachments": [normalize_attachment(item) for item in email.get("attachments", [])],
        "metadata": metadata,
    }


def is_outgoing_seed_email(normalized: Dict[str, Any], owner_emails: set[str]) -> bool:
    return extract_email(normalized["sender"]) in owner_emails


def is_inbound_seed_email(normalized: Dict[str, Any], owner_emails: set[str]) -> bool:
    metadata = normalized.get("metadata", {})
    recipients = people_emails(normalized.get("recipient"))
    recipients.update(people_emails(metadata.get("cc", [])))
    return bool(recipients & owner_emails)


def ensure_email_schema(conn: sqlite3.Connection) -> None:
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(emails)").fetchall()}
    if "metadata" not in columns:
        conn.execute("ALTER TABLE emails ADD COLUMN metadata TEXT NOT NULL DEFAULT '{}'")


def ensure_sent_schema(conn: sqlite3.Connection) -> None:
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(sent)").fetchall()}
    additions = {
        "sender": "TEXT NOT NULL DEFAULT ''",
        "cc": "TEXT NOT NULL DEFAULT '[]'",
        "attachments": "TEXT NOT NULL DEFAULT '[]'",
        "metadata": "TEXT NOT NULL DEFAULT '{}'",
    }
    for column, definition in additions.items():
        if column not in columns:
            conn.execute(f"ALTER TABLE sent ADD COLUMN {column} {definition}")


def init_db() -> None:
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    with connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS emails (
                id TEXT PRIMARY KEY,
                sender TEXT NOT NULL,
                recipient TEXT NOT NULL,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                received_at TEXT NOT NULL,
                read INTEGER NOT NULL DEFAULT 0,
                labels TEXT NOT NULL DEFAULT '[]',
                attachments TEXT NOT NULL DEFAULT '[]',
                metadata TEXT NOT NULL DEFAULT '{}'
            );

            CREATE TABLE IF NOT EXISTS drafts (
                id TEXT PRIMARY KEY,
                recipient TEXT NOT NULL,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                in_reply_to TEXT,
                status TEXT NOT NULL DEFAULT 'draft',
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS sent (
                id TEXT PRIMARY KEY,
                sender TEXT NOT NULL DEFAULT '',
                recipient TEXT NOT NULL,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                sent_at TEXT NOT NULL,
                cc TEXT NOT NULL DEFAULT '[]',
                attachments TEXT NOT NULL DEFAULT '[]',
                metadata TEXT NOT NULL DEFAULT '{}'
            );

            CREATE TABLE IF NOT EXISTS activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                actor TEXT NOT NULL,
                action TEXT NOT NULL,
                target TEXT NOT NULL,
                details TEXT NOT NULL DEFAULT '{}'
            );
            """
        )
        ensure_email_schema(conn)
        ensure_sent_schema(conn)


def reset_db(student_email: str, actor: str) -> None:
    with connect() as conn:
        conn.execute("DELETE FROM emails")
        conn.execute("DELETE FROM drafts")
        conn.execute("DELETE FROM sent")
        conn.execute("DELETE FROM activity")

    seed_emails(student_email)
    log_activity(actor, "reset", "inbox", {"student_email": student_email})


def seed_emails(student_email: str) -> None:
    with open(seed_path(), "r", encoding="utf-8") as f:
        emails = json.load(f)

    with connect() as conn:
        existing_inbox = conn.execute("SELECT COUNT(*) AS count FROM emails").fetchone()["count"]
        existing_sent = conn.execute("SELECT COUNT(*) AS count FROM sent").fetchone()["count"]
        existing = existing_inbox + existing_sent
        if existing:
            return
        owner_emails = mailbox_owner_emails(student_email)
        for email in emails:
            normalized = normalize_seed_email(email, student_email)
            if is_outgoing_seed_email(normalized, owner_emails):
                conn.execute(
                    """
                    INSERT INTO sent
                    (id, sender, recipient, subject, body, sent_at, cc, attachments, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        normalized["id"],
                        normalized["sender"],
                        normalized["recipient"],
                        normalized["subject"],
                        normalized["body"],
                        normalized["received_at"],
                        json.dumps(normalized["metadata"].get("cc", [])),
                        json.dumps(normalized["attachments"]),
                        json.dumps(normalized["metadata"]),
                    ),
                )
            elif is_inbound_seed_email(normalized, owner_emails):
                conn.execute(
                    """
                    INSERT INTO emails
                    (id, sender, recipient, subject, body, received_at, read, labels, attachments, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        normalized["id"],
                        normalized["sender"],
                        normalized["recipient"],
                        normalized["subject"],
                        normalized["body"],
                        normalized["received_at"],
                        normalized["read"],
                        json.dumps(normalized["labels"]),
                        json.dumps(normalized["attachments"]),
                        json.dumps(normalized["metadata"]),
                    ),
                )


def row_to_email(row: sqlite3.Row, include_body: bool = False) -> Dict[str, Any]:
    attachments = json.loads(row["attachments"])
    metadata = json.loads(row["metadata"])
    data = {
        "id": row["id"],
        "sender": row["sender"],
        "to": row["recipient"],
        "subject": row["subject"],
        "received_at": row["received_at"],
        "read": bool(row["read"]),
        "labels": json.loads(row["labels"]),
        "has_attachments": len(attachments) > 0,
        "attachment_count": len(attachments),
        "conversation_id": metadata.get("conversation_id"),
        "thread_index": metadata.get("thread_index"),
        "classification": metadata.get("classification", "UNCLASSIFIED"),
        "importance": metadata.get("importance", "normal"),
    }
    if include_body:
        data["body"] = row["body"]
        data["cc"] = metadata.get("cc", [])
        data["attachments"] = [attachment_with_url(row["id"], item) for item in attachments]
    return data


def list_emails(actor: str) -> List[Dict[str, Any]]:
    with connect() as conn:
        rows = conn.execute("SELECT * FROM emails ORDER BY received_at DESC").fetchall()
    log_activity(actor, "list_emails", "inbox", {"count": len(rows)})
    return [row_to_email(r) for r in rows]


def get_email(email_id: str, actor: str) -> Optional[Dict[str, Any]]:
    with connect() as conn:
        row = conn.execute("SELECT * FROM emails WHERE id = ?", (email_id,)).fetchone()
        if row:
            conn.execute("UPDATE emails SET read = 1 WHERE id = ?", (email_id,))
    if not row:
        return None
    log_activity(actor, "read_email", email_id)
    return row_to_email(row, include_body=True)


def get_attachment(email_id: str, attachment_id: str, actor: str) -> Optional[Dict[str, Any]]:
    with connect() as conn:
        row = conn.execute("SELECT attachments FROM emails WHERE id = ?", (email_id,)).fetchone()
    if not row:
        return None

    for item in json.loads(row["attachments"]):
        attachment = normalize_attachment(item)
        if attachment["id"] == attachment_id:
            log_activity(actor, "download_attachment", attachment_id, {"email_id": email_id})
            return attachment
    return None


def get_sent_attachment(sent_id: str, attachment_id: str, actor: str) -> Optional[Dict[str, Any]]:
    with connect() as conn:
        row = conn.execute("SELECT attachments FROM sent WHERE id = ?", (sent_id,)).fetchone()
    if not row:
        return None

    for item in json.loads(row["attachments"]):
        attachment = normalize_attachment(item)
        if attachment["id"] == attachment_id:
            log_activity(actor, "download_sent_attachment", attachment_id, {"sent_id": sent_id})
            return attachment
    return None


def attachment_file_path(attachment: Dict[str, str]) -> Path:
    configured_path = Path(attachment["path"])
    path = configured_path if configured_path.is_absolute() else DATA_DIR / configured_path
    resolved = path.resolve()
    data_root = DATA_DIR.resolve()
    if not resolved.is_relative_to(data_root):
        raise ValueError(f"Attachment path is outside the data directory: {attachment['path']}")
    return resolved


def create_draft(recipient: str, subject: str, body: str, in_reply_to: Optional[str], actor: str) -> Dict[str, Any]:
    draft_id = f"draft_{uuid4().hex[:8]}"
    created_at = now_iso()
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO drafts (id, recipient, subject, body, in_reply_to, status, created_at)
            VALUES (?, ?, ?, ?, ?, 'draft', ?)
            """,
            (draft_id, recipient, subject, body, in_reply_to, created_at),
        )
    log_activity(actor, "create_draft", draft_id, {"to": recipient, "in_reply_to": in_reply_to})
    return {
        "id": draft_id,
        "to": recipient,
        "subject": subject,
        "body": body,
        "in_reply_to": in_reply_to,
        "status": "draft",
        "created_at": created_at,
    }


def list_drafts(actor: str) -> List[Dict[str, Any]]:
    with connect() as conn:
        rows = conn.execute("SELECT * FROM drafts ORDER BY created_at DESC").fetchall()
    log_activity(actor, "list_drafts", "drafts", {"count": len(rows)})
    return [
        {
            "id": r["id"],
            "to": r["recipient"],
            "subject": r["subject"],
            "body": r["body"],
            "in_reply_to": r["in_reply_to"],
            "status": r["status"],
            "created_at": r["created_at"],
        }
        for r in rows
    ]


def send_email(recipient: str, subject: str, body: str, actor: str) -> Dict[str, Any]:
    sent_id = f"sent_{uuid4().hex[:8]}"
    sent_at = now_iso()
    with connect() as conn:
        conn.execute(
            "INSERT INTO sent (id, recipient, subject, body, sent_at) VALUES (?, ?, ?, ?, ?)",
            (sent_id, recipient, subject, body, sent_at),
        )
    log_activity(actor, "send_email", sent_id, {"to": recipient})
    return {"id": sent_id, "to": recipient, "subject": subject, "body": body, "sent_at": sent_at}


def row_to_sent(row: sqlite3.Row) -> Dict[str, Any]:
    attachments = json.loads(row["attachments"])
    metadata = json.loads(row["metadata"])
    return {
        "id": row["id"],
        "sender": row["sender"],
        "to": row["recipient"],
        "subject": row["subject"],
        "body": row["body"],
        "sent_at": row["sent_at"],
        "cc": json.loads(row["cc"]),
        "attachments": [sent_attachment_with_url(row["id"], item) for item in attachments],
        "has_attachments": len(attachments) > 0,
        "attachment_count": len(attachments),
        "conversation_id": metadata.get("conversation_id"),
        "thread_index": metadata.get("thread_index"),
        "classification": metadata.get("classification", "UNCLASSIFIED"),
        "importance": metadata.get("importance", "normal"),
    }


def list_sent(actor: str) -> List[Dict[str, Any]]:
    with connect() as conn:
        rows = conn.execute("SELECT * FROM sent ORDER BY sent_at DESC").fetchall()
    log_activity(actor, "list_sent", "sent", {"count": len(rows)})
    return [row_to_sent(row) for row in rows]


def get_sent(sent_id: str, actor: str) -> Optional[Dict[str, Any]]:
    with connect() as conn:
        row = conn.execute("SELECT * FROM sent WHERE id = ?", (sent_id,)).fetchone()
    if not row:
        return None
    log_activity(actor, "read_sent", sent_id)
    return row_to_sent(row)


def log_activity(actor: str, action: str, target: str, details: Optional[Dict[str, Any]] = None) -> None:
    with connect() as conn:
        conn.execute(
            "INSERT INTO activity (timestamp, actor, action, target, details) VALUES (?, ?, ?, ?, ?)",
            (now_iso(), actor, action, target, json.dumps(details or {})),
        )


def list_activity() -> List[Dict[str, Any]]:
    with connect() as conn:
        rows = conn.execute("SELECT * FROM activity ORDER BY id ASC").fetchall()
    return [
        {
            "timestamp": r["timestamp"],
            "actor": r["actor"],
            "action": r["action"],
            "target": r["target"],
            "details": json.loads(r["details"]),
        }
        for r in rows
    ]
