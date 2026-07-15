# Project ATaS Content Generator

A reproducible authoring pipeline for the Project ATaS workshop mailbox.

The generator uses the approved mailbox blueprint to author complete email threads, validate them, preserve stable authoring message IDs, and export a student-facing seed consumed by the fake email API.

## What it does

1. Loads the approved thread catalog, message blueprint, and persona knowledge states.
2. Builds a detailed prompt for one complete conversation.
3. Sends that prompt to an OpenAI-compatible Chat Completions endpoint.
4. Requires strict JSON containing only message IDs and email bodies.
5. Validates continuity-sensitive invariants and classification rules.
6. Stores each thread separately for human review and Git versioning.
7. Exports approved threads into a student-safe mailbox seed with instructor metadata removed and scenario IDs replaced by opaque IDs.

## Layout

```text
project_atas_content_generator/
├── atas_generator/             # Generator package
├── scenario/                   # Approved source-of-truth blueprint
├── generated/
│   └── threads/
│       └── ATAS-001/
│           ├── prompt.md
│           ├── emails.json
│           └── generation.json
├── tests/
├── .env.example
├── pyproject.toml
└── README.md
```

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Inspect the plan

```bash
atas-generate list-threads
atas-generate prompt ATAS-001 --output /tmp/ATAS-001-prompt.txt
```

## Test without an LLM

The mock provider confirms generation, validation, and merge mechanics:

```bash
atas-generate generate ATAS-001 --provider mock
atas-generate validate ATAS-001
atas-generate merge --allow-incomplete --output generated/preview-emails.json
```

## Connect an OpenAI-compatible endpoint

```bash
cp .env.example .env
atas-generate generate ATAS-001 --provider openai-compatible
```

Expected environment variables:

```text
ATAS_LLM_BASE_URL=http://localhost:8001/v1
ATAS_LLM_MODEL=your-model-name
ATAS_LLM_API_KEY=
ATAS_LLM_TIMEOUT=180
```

The endpoint must implement `POST /v1/chat/completions` and return the usual `choices[0].message.content` field. The generator requests JSON-object output. If a local model server does not support `response_format`, remove that field in `atas_generator/providers.py`.

## Review workflow

Generate one thread, review `generated/threads/<THREAD>/emails.json`, edit it directly when needed, then validate it:

```bash
atas-generate generate ATAS-003
atas-generate validate ATAS-003
```

Keep the reviewed thread folder under version control. Regeneration only replaces that thread.

## Generate remaining threads robustly

For long generation runs, use the resumable script instead of a `set -e` shell loop:

```bash
bash scripts/generate_remaining.sh
```

The script validates existing thread outputs, skips valid ones, records failures in `generated/logs/failures.txt`, and continues to the next thread when generation or validation fails.

Useful variants:

```bash
bash scripts/generate_remaining.sh --retries 1 --sleep 5
bash scripts/generate_remaining.sh --force ATAS-003
bash scripts/generate_remaining.sh ATAS-007 CONG-002 CONG-004
```

## Build the final mailbox

After all threads are generated and reviewed:

```bash
atas-generate merge --output generated/emails.json
```

Copy `generated/emails.json` into the fake email API data directory and update the seed loader to use it.

For a reviewed slice or API-ready seed file:

```bash
atas-generate export-api-seed --thread-id SEC-004 --output ../fake-email-api/data/atas_seed_emails.json
```

`export-api-seed` keeps the reviewed source files stable for validation, but the API seed uses opaque `msg_...` message IDs and `att_...` attachment IDs. It also strips thread scaffolding such as `conversation_id` and `thread_index` so students and agents cannot shortcut the investigation by reading scenario labels.

## Safety and scenario constraints

- The mailbox contains only `UNCLASSIFIED` and limited `CUI` messages.
- No standalone classified email is generated.
- One unclassified email thread may reference a presentation containing an erroneously embedded fictional slide marked `SECRET//NOFORN`.
- The prompt forbids real operational details, collection capabilities, target information, and instructor metadata.
- The export step strips `authoring_metadata`, truth mappings, and scenario thread labels before producing the student mailbox.
