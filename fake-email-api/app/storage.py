import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

DB_PATH = os.getenv("EMAIL_API_DB", "/app/data/email_lab.sqlite")
SEED_PATH = Path(__file__).resolve().parent.parent / "data" / "seed_emails.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


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
                attachments TEXT NOT NULL DEFAULT '[]'
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
                recipient TEXT NOT NULL,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                sent_at TEXT NOT NULL
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


def reset_db(student_email: str, actor: str) -> None:
    with connect() as conn:
        conn.execute("DELETE FROM emails")
        conn.execute("DELETE FROM drafts")
        conn.execute("DELETE FROM sent")
        conn.execute("DELETE FROM activity")

    seed_emails(student_email)
    log_activity(actor, "reset", "inbox", {"student_email": student_email})


def seed_emails(student_email: str) -> None:
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        emails = json.load(f)

    with connect() as conn:
        existing = conn.execute("SELECT COUNT(*) AS count FROM emails").fetchone()["count"]
        if existing:
            return
        for email in emails:
            conn.execute(
                """
                INSERT INTO emails
                (id, sender, recipient, subject, body, received_at, read, labels, attachments)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    email["id"],
                    email["from"],
                    student_email,
                    email["subject"],
                    email["body"],
                    email["received_at"],
                    0,
                    json.dumps(email.get("labels", [])),
                    json.dumps(email.get("attachments", [])),
                ),
            )


def row_to_email(row: sqlite3.Row, include_body: bool = False) -> Dict[str, Any]:
    data = {
        "id": row["id"],
        "sender": row["sender"],
        "to": row["recipient"],
        "subject": row["subject"],
        "received_at": row["received_at"],
        "read": bool(row["read"]),
        "labels": json.loads(row["labels"]),
        "has_attachments": len(json.loads(row["attachments"])) > 0,
    }
    if include_body:
        data["body"] = row["body"]
        data["attachments"] = json.loads(row["attachments"])
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


def list_sent(actor: str) -> List[Dict[str, Any]]:
    with connect() as conn:
        rows = conn.execute("SELECT * FROM sent ORDER BY sent_at DESC").fetchall()
    log_activity(actor, "list_sent", "sent", {"count": len(rows)})
    return [
        {"id": r["id"], "to": r["recipient"], "subject": r["subject"], "body": r["body"], "sent_at": r["sent_at"]}
        for r in rows
    ]


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
