# Project ATaS Email Executive Assistant Lab

A local fake email provider for the Project ATaS Agentic AI workshop with NemoClaw.

Students build an executive assistant for LCDR James Maddox that can read a seeded inbox, prioritize messages, inspect attachments, extract action items, draft replies, send a summary email to themselves, and inspect an audit trail.

The current repository includes a working ATaS vertical slice: the `SEC-004` security thread and the `ATaS_Congressional_Brief_v13.pptx` attachment. The full 235-message mailbox blueprint lives under `project_atas_content_generator/scenario`.

## Development setup

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

## Run locally

```bash
cp .env.example .env
docker compose up --build
```

Open the API docs:

```text
http://localhost:8000/docs
```

Health check:

```bash
curl http://localhost:8000/health
```

Reset the seeded inbox:

```bash
curl -X POST http://localhost:8000/reset
```

## Key endpoints

- `GET /health`
- `GET /me`
- `GET /emails`
- `GET /emails/{email_id}`
- `GET /emails/{email_id}/attachments/{attachment_id}`
- `POST /drafts`
- `GET /drafts`
- `POST /send-summary`
- `POST /send` intentionally demonstrates policy enforcement
- `GET /sent`
- `GET /sent/{sent_id}/attachments/{attachment_id}`
- `GET /activity`
- `POST /reset`

## Safety model

Allowed:

- Read seeded emails
- Create draft replies
- Send a summary email to the authenticated student
- View audit logs
- Reset inbox state

Blocked by policy:

- Automatically sending email to external recipients

## Webmail interface

After starting the service, open:

- Webmail UI: http://localhost:8000/
- Interactive API documentation: http://localhost:8000/docs

The UI provides an inbox and message reader, reply-draft creation, policy-safe summary sending, sent and draft views, the activity audit log, and a full lab reset button.
