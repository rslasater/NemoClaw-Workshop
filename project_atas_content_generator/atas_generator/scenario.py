from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .io import read_json


@dataclass(frozen=True)
class Scenario:
    root: Path
    emails: list[dict[str, Any]]
    threads: list[dict[str, Any]]
    knowledge: dict[str, Any]

    @classmethod
    def load(cls, root: Path) -> "Scenario":
        return cls(
            root=root,
            emails=read_json(root / "emails_blueprint.json"),
            threads=read_json(root / "thread_catalog.json"),
            knowledge=read_json(root / "character_knowledge_states.json"),
        )

    def thread_definition(self, thread_id: str) -> dict[str, Any]:
        for thread in self.threads:
            if thread["thread_id"] == thread_id:
                return thread
        raise KeyError(f"Unknown thread: {thread_id}")

    def thread_messages(self, thread_id: str) -> list[dict[str, Any]]:
        messages = [m for m in self.emails if m["conversation_id"] == thread_id]
        if not messages:
            raise KeyError(f"Unknown thread: {thread_id}")
        return sorted(messages, key=lambda item: item["thread_index"])
