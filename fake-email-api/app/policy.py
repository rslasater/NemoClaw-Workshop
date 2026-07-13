class PolicyError(Exception):
    pass


def ensure_summary_recipient_only(to_address: str, student_email: str) -> None:
    if to_address.strip().lower() != student_email.strip().lower():
        raise PolicyError(
            "Agents may only send summary emails to the authenticated student's email address."
        )
