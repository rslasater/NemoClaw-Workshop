# Project ATaS Email Executive Assistant Lab

Welcome to the Project ATaS workshop lab. In this exercise, you will use
NemoClaw/OpenClaw to build an executive assistant for LCDR James Maddox as he
prepares COL Jesse Abreu for a 0900 Senate Armed Services Committee briefing on
Project ATaS.

Your assistant will inspect a realistic seeded mailbox, identify the threads
that matter, review attachments when needed, and produce a concise congressional
briefing. The lab is designed around controlled tool access: the assistant can
read the workshop email API and use policy-safe actions, but it must not send
external email.

## What You Will Run

- A fake email API and webmail UI hosted on your Brev instance.
- A NemoClaw OpenClaw sandbox configured by you.
- A narrow network policy that allows your claw to reach only the workshop email
  API on port `8000`.
- A local port forward so you can inspect the webmail UI from your laptop.

## What You Will Practice

- Starting and connecting to an NVIDIA Brev instance.
- Running the workshop email service with Docker Compose.
- Configuring NemoClaw with the assigned model and policy tier.
- Granting an agent scoped access to a local HTTP service.
- Using OpenShell to inspect or approve blocked sandbox requests.
- Producing a briefing with a BLUF, key findings, risks, actions, open
  questions, and source citations.

## Start Here

The student workflow is in the Brev guide:

- [Brev Student Guide](docs/BREV_STUDENT_GUIDE.md)

At a high level, you will:

1. Start your assigned Brev instance.
2. Clone this repo on the Brev instance.
3. Run the setup helper:

   ```bash
   ./scripts/setup-brev-instance.sh
   ```

4. Copy the printed API base URL, which will look like `http://10.x.x.x:8000`.
5. Forward the webmail UI to your laptop with `brev port-forward`.
6. Install and configure NemoClaw/OpenClaw.
7. Add the generated email API policy:

   ```bash
   nemoclaw <claw-name> policy-add --from-file ./atas-email-api.yaml --yes
   ```

8. Ask your claw to verify `GET /health`, `GET /me`, and `GET /emails`.
9. Paste in the mission prompt and complete the briefing.

Do not use `localhost` as the API base URL inside the NemoClaw sandbox. Use the
`http://10.x.x.x:8000` URL printed by the setup script.

## The Mission

After your claw can read the API, give it the mission prompt from:

- [student-lab/mission-prompt.md](student-lab/mission-prompt.md)

Your final briefing should include:

- BLUF
- Key findings
- Risks or contradictions
- Recommended immediate actions before the briefing
- Open questions
- Source list with email IDs and attachment names

## Webmail And API

With the service running and port forwarding enabled, open the webmail UI from
your laptop:

```text
http://localhost:8000
```

If local port `8000` is already busy, forward `8001:8000` and open:

```text
http://localhost:8001
```

The API documentation is available at:

```text
http://localhost:8000/docs
```

## Safety Model

Allowed actions:

- Read seeded emails.
- Inspect attachments.
- Create draft replies.
- Send a summary email to the authenticated student through the policy-safe
  endpoint.
- View the activity audit log.
- Reset the lab inbox state.

Blocked by policy:

- Automatically sending email to external recipients.

## Troubleshooting

Run the lab check script on the Brev instance:

```bash
./scripts/check-brev-lab.sh
```

For common setup, port-forwarding, Docker, and policy issues, see the
[Brev Student Guide](docs/BREV_STUDENT_GUIDE.md#troubleshooting).

## Instructor And Development Notes

Instructor setup and classroom operations are covered in:

- [Brev Instructor Runbook](docs/BREV_INSTRUCTOR_RUNBOOK.md)

For local development outside Brev:

```bash
cp .env.example .env
docker compose up --build
```

Then open:

```text
http://localhost:8000/
```
