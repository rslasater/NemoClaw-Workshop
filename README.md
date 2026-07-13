# Email Executive Assistant Lab

A local fake email provider for a 2-hour Agentic AI workshop with NemoClaw.

Students build an email executive assistant that can read a seeded inbox, prioritize messages, extract action items, draft replies, send a summary email to themselves, and inspect an audit trail.

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
- `POST /drafts`
- `GET /drafts`
- `POST /send-summary`
- `POST /send` intentionally demonstrates policy enforcement
- `GET /sent`
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
