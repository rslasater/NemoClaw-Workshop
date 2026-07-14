from __future__ import annotations

from typing import Any

FORBIDDEN_BODY_TOKENS = (
    "T-001", "T-002", "T-003", "truth id", "grading rubric",
    "instructor guide", "student should discover",
)


def validate_generation(expected: list[dict[str, Any]], generated: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(generated, dict) or not isinstance(generated.get("emails"), list):
        return ["Response must be an object containing an 'emails' array"]

    expected_ids = [message["id"] for message in expected]
    actual = generated["emails"]
    actual_ids = [item.get("id") for item in actual if isinstance(item, dict)]

    if actual_ids != expected_ids:
        errors.append(f"Message IDs/order mismatch. Expected {expected_ids}; received {actual_ids}")

    for item in actual:
        if not isinstance(item, dict):
            errors.append("Every generated email must be an object")
            continue
        body = item.get("body")
        if not isinstance(body, str) or not body.strip():
            errors.append(f"{item.get('id', '<unknown>')}: body is empty")
            continue
        lowered = body.lower()
        for token in FORBIDDEN_BODY_TOKENS:
            if token.lower() in lowered:
                errors.append(f"{item.get('id')}: contains forbidden instructor token '{token}'")
        if "secret//noforn" in lowered and not item.get("id", "").startswith(("SEC-004", "SEC-005")):
            errors.append(f"{item.get('id')}: SECRET//NOFORN marking appears outside approved security threads")

    for message in expected:
        if message.get("classification") not in {"UNCLASSIFIED", "CUI"}:
            errors.append(f"{message['id']}: invalid mailbox classification {message.get('classification')}")
    return errors
