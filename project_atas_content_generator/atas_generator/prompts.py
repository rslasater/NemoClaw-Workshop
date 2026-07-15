from __future__ import annotations

import json
from typing import Any

from .scenario import Scenario

SYSTEM_PROMPT = """You are the senior scenario author for Project ATaS, a fictional, unclassified military staff-training simulation.

Write realistic professional email conversations while obeying these rules:
- The scenario is fictional and all domains ending in .example are synthetic.
- Preserve every supplied message ID, subject, sender, recipient, timestamp, classification, and attachment reference exactly.
- Generate only the body text for each supplied message.
- Maintain continuity across replies. Later messages may quote or briefly reference earlier messages, but avoid repeating full chains.
- Match each persona's voice and what that person knows at that point in time.
- Do not reveal instructor metadata, truth IDs, grading language, or that this is a simulation.
- Do not mention raw message IDs, thread IDs, conversation IDs, blueprint labels, or category prefixes such as ATAS-001, CONG-004, NEWS-010, SPAM-002, or PHISH-003. The project name "Project ATaS" may be referenced normally when relevant.
- No email may itself be classified. Mailbox labels may only be UNCLASSIFIED or CUI.
- A single presentation attachment may contain an erroneously embedded fictional slide marked SECRET//NOFORN. Do not invent operational details, real collection capabilities, real targeting data, or actionable classified content.
- The security thread should describe the marking and the need to report suspected spillage, not reproduce sensitive slide contents.
- Use plausible military and government-office tone without imitating any real person's private communications.
- Vary length naturally: terse replies, short coordination notes, and occasional detailed technical messages.
- Return strict JSON only, with this shape: {\"emails\": [{\"id\": \"...\", \"body\": \"...\"}]}.
"""


def build_thread_prompt(scenario: Scenario, thread_id: str) -> str:
    thread = scenario.thread_definition(thread_id)
    messages = scenario.thread_messages(thread_id)
    allows_spillage_marking = thread_id in {"SEC-004", "SEC-005"}

    participants = sorted({m["from"]["name"] for m in messages} | {
        recipient["name"] for m in messages for recipient in (m.get("to", []) + m.get("cc", []))
    })
    relevant_knowledge: dict[str, Any] = {
        name: states for name, states in scenario.knowledge.items() if name in participants
    }

    authoring_messages = []
    for message in messages:
        authoring_messages.append({
            "id": message["id"],
            "thread_index": message["thread_index"],
            "sent_at": message["sent_at"],
            "from": message["from"],
            "to": message.get("to", []),
            "cc": message.get("cc", []),
            "subject": message["subject"],
            "classification": message["classification"],
            "importance": message["importance"],
            "attachments": message.get("attachments", []),
            "in_reply_to": message.get("in_reply_to"),
            "purpose": message.get("authoring_metadata", {}).get("thread_purpose"),
            "facts_to_support": message.get("authoring_metadata", {}).get("truth_ids", []),
        })

    payload = {
        "thread": thread,
        "character_knowledge_states": relevant_knowledge,
        "messages_to_author": authoring_messages,
        "quality_requirements": [
            "The conversation must have a clear beginning, progression, and ending.",
            "Do not make every message equally long or polished.",
            "Technical concerns should emerge incrementally rather than through one smoking-gun email.",
            "Do not put instructor truth IDs into email bodies.",
            "Do not put message IDs, thread IDs, conversation IDs, or raw scenario category labels into email bodies.",
            "Do not fabricate attachment contents beyond what the scenario requires.",
            (
                "This is an approved security-spillage thread; references to the embedded slide marking may appear only as needed."
                if allows_spillage_marking
                else "Do not include the string SECRET//NOFORN or any classified-document marking in this thread."
            ),
        ],
    }
    return "Author this thread using the following structured brief:\n\n" + json.dumps(payload, indent=2)
