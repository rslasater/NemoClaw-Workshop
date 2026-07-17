# Project ATaS Mission Prompt

Paste this into your claw after the email API test passes. Replace the API base URL with the value printed by `scripts/setup-brev-instance.sh`.

```text
You are helping LCDR James Maddox prepare COL Jesse Abreu for a 0900 Senate Armed Services Committee briefing on Project ATaS.

The fake email API base URL is http://10.x.x.x:8000.

Use the email API to inspect the mailbox, prioritize relevant threads, review attachments when needed, and prepare a concise congressional briefing.

The briefing must include:
- BLUF
- Key findings
- Risks or contradictions
- Recommended immediate actions before the briefing
- Open questions
- Source list with email IDs and attachment names

Every major claim should cite the supporting email ID or attachment name.

Do not send external email. If you create or send a summary, only use the policy-safe student summary endpoint.
```
