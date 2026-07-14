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


def merge_mailbox(scenario: Scenario, generated_root: Path, output_path: Path, allow_incomplete: bool = False) -> dict[str, Any]:
    bodies: dict[str, str] = {}
    missing_threads: list[str] = []
    for thread in scenario.threads:
        thread_id = thread["thread_id"]
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
        if source["id"] not in bodies:
            if allow_incomplete:
                continue
            raise ValueError(f"Missing body for {source['id']}")
        cleaned = {key: value for key, value in source.items() if key not in {"body_status", "authoring_metadata"}}
        cleaned["body"] = bodies[source["id"]]
        mailbox.append(cleaned)

    mailbox.sort(key=lambda item: item["sent_at"], reverse=True)
    write_json(output_path, mailbox)
    return {"message_count": len(mailbox), "missing_threads": missing_threads, "output": str(output_path)}
