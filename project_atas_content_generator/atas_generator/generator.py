from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .io import read_json, write_json
from .prompts import SYSTEM_PROMPT, build_thread_prompt
from .providers import Provider
from .scenario import Scenario
from .validation import validate_generation


def generate_thread(scenario: Scenario, thread_id: str, provider: Provider, output_root: Path) -> Path:
    messages = scenario.thread_messages(thread_id)
    prompt = build_thread_prompt(scenario, thread_id)
    raw = provider.generate(SYSTEM_PROMPT, prompt)
    try:
        generated = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Provider returned invalid JSON: {exc}") from exc

    errors = validate_generation(messages, generated)
    if errors:
        raise ValueError("Generation failed validation:\n- " + "\n- ".join(errors))

    thread_dir = output_root / "threads" / thread_id
    thread_dir.mkdir(parents=True, exist_ok=True)
    (thread_dir / "prompt.md").write_text(
        "# System Prompt\n\n" + SYSTEM_PROMPT + "\n\n# Thread Prompt\n\n" + prompt + "\n",
        encoding="utf-8",
    )
    write_json(thread_dir / "emails.json", generated)
    write_json(thread_dir / "generation.json", {
        "thread_id": thread_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "message_count": len(messages),
        "status": "generated_pending_human_review",
    })
    return thread_dir


def _build_mailbox(
    scenario: Scenario,
    generated_root: Path,
    allow_incomplete: bool,
    thread_ids: set[str] | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    bodies: dict[str, str] = {}
    missing_threads: list[str] = []
    for thread in scenario.threads:
        thread_id = thread["thread_id"]
        if thread_ids is not None and thread_id not in thread_ids:
            continue
        path = generated_root / "threads" / thread_id / "emails.json"
        if not path.exists():
            missing_threads.append(thread_id)
            continue
        generated = read_json(path)
        errors = validate_generation(scenario.thread_messages(thread_id), generated)
        if errors:
            raise ValueError(f"{thread_id} failed validation:\n- " + "\n- ".join(errors))
        bodies.update({item["id"]: item["body"] for item in generated["emails"]})

    if missing_threads and not allow_incomplete:
        raise ValueError("Missing generated threads: " + ", ".join(missing_threads))

    mailbox = []
    for source in scenario.emails:
        if thread_ids is not None and source["conversation_id"] not in thread_ids:
            continue
        if source["id"] not in bodies:
            if allow_incomplete:
                continue
            raise ValueError(f"Missing body for {source['id']}")
        cleaned = {key: value for key, value in source.items() if key not in {"body_status", "authoring_metadata"}}
        cleaned["body"] = bodies[source["id"]]
        mailbox.append(cleaned)

    mailbox.sort(key=lambda item: item["sent_at"], reverse=True)
    return mailbox, missing_threads


def merge_mailbox(scenario: Scenario, generated_root: Path, output_path: Path, allow_incomplete: bool = False) -> dict[str, Any]:
    mailbox, missing_threads = _build_mailbox(scenario, generated_root, allow_incomplete)
    write_json(output_path, mailbox)
    return {"message_count": len(mailbox), "missing_threads": missing_threads, "output": str(output_path)}


def _format_person(person: Any) -> str:
    if isinstance(person, str):
        return person
    if isinstance(person, dict):
        name = str(person.get("name", "")).strip()
        email = str(person.get("email", "")).strip()
        if name and email:
            return f"{name} <{email}>"
        return name or email
    return str(person)


def _format_people(people: Any) -> str:
    if not people:
        return ""
    if isinstance(people, list):
        return "; ".join(_format_person(person) for person in people)
    return _format_person(people)


def _attachment_for_api(attachment: Any) -> dict[str, str]:
    if isinstance(attachment, str):
        return {
            "id": attachment,
            "filename": attachment,
            "mime_type": "application/octet-stream",
            "path": f"attachments/{attachment}",
        }
    filename = str(attachment.get("filename", attachment.get("id", "attachment"))).strip()
    return {
        "id": str(attachment.get("id", filename)),
        "filename": filename,
        "mime_type": str(attachment.get("mime_type", "application/octet-stream")),
        "path": str(attachment.get("path", f"attachments/{filename}")),
    }


def export_api_seed(
    scenario: Scenario,
    generated_root: Path,
    output_path: Path,
    allow_incomplete: bool = False,
    thread_ids: list[str] | None = None,
) -> dict[str, Any]:
    selected_thread_ids = set(thread_ids) if thread_ids else None
    mailbox, missing_threads = _build_mailbox(scenario, generated_root, allow_incomplete, selected_thread_ids)
    api_seed = []
    for source in mailbox:
        api_seed.append({
            "id": source["id"],
            "from": _format_person(source.get("from")),
            "to": _format_people(source.get("to")),
            "cc": [_format_person(person) for person in source.get("cc", [])],
            "subject": source["subject"],
            "body": source["body"],
            "received_at": source["sent_at"],
            "read": bool(source.get("is_read", False)),
            "labels": source.get("labels", []),
            "attachments": [_attachment_for_api(item) for item in source.get("attachments", [])],
            "metadata": {
                "conversation_id": source.get("conversation_id"),
                "thread_index": source.get("thread_index"),
                "classification": source.get("classification"),
                "importance": source.get("importance"),
                "in_reply_to": source.get("in_reply_to"),
                "references": source.get("references", []),
                "sent_at": source.get("sent_at"),
            },
        })

    write_json(output_path, api_seed)
    return {"message_count": len(api_seed), "missing_threads": missing_threads, "output": str(output_path)}
