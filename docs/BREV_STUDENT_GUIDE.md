# Brev Student Guide

This guide gets your Project ATaS email lab running on a Brev instance, then connects your NemoClaw sandbox to it. You will still configure NemoClaw yourself so you understand the agent, model, and policy choices.

## What You Will Run

- A fake email API and webmail UI on your Brev instance.
- A NemoClaw OpenClaw sandbox that is allowed to call that email API.
- A local port forward so your laptop browser can inspect the webmail UI.

## Before You Start

You need:

- An NVIDIA Brev account.
- Workshop credits or the workshop code from your instructor.
- An NVIDIA API key from build.nvidia.com if the lab uses NVIDIA Cloud inference.
- WSL on Windows if you are using the Brev CLI from a Windows laptop.

Keep three terminals in mind:

- Local terminal: WSL or your laptop terminal. Use it for `brev` commands and port forwarding.
- Brev terminal: SSH shell on the Brev instance. Use it for Docker, repo setup, and NemoClaw.
- OpenShell terminal: `openshell term`. Use it to inspect or approve blocked sandbox requests.

## 1. Start And Connect To Your Brev Instance

Use the Brev UI to start your assigned instance. If you created or restarted it in the web UI, sync your local CLI:

```bash
brev refresh
brev list
```

Open a shell to the instance:

```bash
brev shell <instance-name>
```

You should land on the Brev instance, usually under `/home/ubuntu/workspace`.

## 2. Get The Workshop Repo

Run this on the Brev instance:

```bash
git clone https://github.com/rslasater/NemoClaw-Workshop.git
cd NemoClaw-Workshop
```

If the repo is already present:

```bash
cd NemoClaw-Workshop
git pull
```

## 3. Start The Email Lab

Run the setup helper from the repo root:

```bash
./scripts/setup-brev-instance.sh
```

The script:

- Installs host packages used by the lab checks, including `binutils`.
- Confirms Docker and Docker Compose are reachable.
- Starts the fake email API with `docker compose up -d --build`.
- Waits for `GET /health`.
- Generates `atas-email-api.yaml` for this specific Brev instance.

When it finishes, copy the API base URL it prints. It will look like:

```text
http://10.x.x.x:8000
```

Use that URL when talking to your claw. Do not use `localhost` from inside the NemoClaw sandbox.

## 4. View The Webmail UI From Your Laptop

In a local terminal, not inside the Brev SSH session, run:

```bash
brev port-forward <instance-name> --port 8000:8000
```

Keep that terminal open. Then open:

```text
http://localhost:8000
```

If port `8000` is already busy on your laptop:

```bash
brev port-forward <instance-name> --port 8001:8000
```

Then open:

```text
http://localhost:8001
```

## 5. Install And Configure NemoClaw

Run these commands on the Brev instance:

```bash
sudo apt-get install -y binutils
curl -fsSL https://www.nvidia.com/nemoclaw.sh | bash
```

Follow the NemoClaw onboarding prompts:

- Select OpenClaw.
- Use your NVIDIA API key from build.nvidia.com when prompted.
- Select the model your instructor assigned, such as DeepSeek V4 Pro.
- Name your claw. The examples below use `zoidberg`, but you can choose your own name.
- Choose a balanced policy tier unless your instructor says otherwise.

Start your claw:

```bash
nemoclaw <claw-name>
```

In a second Brev terminal, open the OpenShell request monitor:

```bash
openshell term
```

## 6. Allow The Claw To Reach The Email API

Run this from the workshop repo root on the Brev instance:

```bash
nemoclaw <claw-name> policy-add --from-file ./atas-email-api.yaml --yes
nemoclaw <claw-name> policy-list
```

The policy allows the claw to call the workshop email API on port `8000`. It does not give the claw general network access.

## 7. Ask Your Claw To Test The Email API

In OpenClaw, introduce yourself and give it the API base URL printed by the setup script:

```text
My name is [your name]. I am doing the Project ATaS workshop.

The fake email API base URL is http://10.x.x.x:8000.

Please verify the API with:
- GET /health
- GET /me
- GET /emails

Then summarize what tools and permissions the email API appears to provide.
```

If the request is blocked, look at `openshell term`. Approve only the expected host and port from your generated `atas-email-api.yaml`.

## 8. Mission Prompt

After the claw can read the API, give it the mission:

```text
You are helping LCDR James Maddox prepare COL Jesse Abreu for a 0900 Senate Armed Services Committee briefing on Project ATaS.

Use the email API to inspect the mailbox, prioritize relevant threads, review attachments when needed, and prepare a concise congressional briefing.

The briefing must include:
- BLUF
- Key findings
- Risks or contradictions
- Recommended immediate actions before the briefing
- Open questions
- Source list with email IDs and attachment names

Do not send external email. If you create or send a summary, only use the policy-safe student summary endpoint.
```

## Troubleshooting

Run the lab check script on the Brev instance:

```bash
./scripts/check-brev-lab.sh
```

Common fixes:

- Docker is not reachable: start Docker or ask an instructor to move you to a Brev image with Docker enabled.
- Port `8000` is busy on the Brev instance: stop the other service or ask an instructor before changing ports.
- Laptop browser cannot open the webmail UI: restart `brev port-forward` and make sure the terminal stays open.
- Claw cannot reach the API: confirm you applied `atas-email-api.yaml`, use the printed `http://10.x.x.x:8000` base URL, and inspect `openshell term`.
- Local port conflict: forward `8001:8000` and open `http://localhost:8001`.

## Shutdown

When the workshop is complete, stop your Brev instance from your local terminal:

```bash
brev stop --all
```

You can also stop it from the Brev web UI.

## References

- NVIDIA Brev connectivity and port forwarding: https://docs.nvidia.com/brev/cli/connectivity
- NVIDIA Brev instance stop command: https://docs.nvidia.com/brev/cli/instance-management
- NemoClaw Brev web UI flow: https://docs.nvidia.com/nemoclaw/user-guide/openclaw/deployment/brev-web-ui
- NemoClaw custom network policy: https://docs.nvidia.com/nemoclaw/user-guide/openclaw/network-policy/customize-network-policy
- NemoClaw host-side HTTP service troubleshooting: https://docs.nvidia.com/nemoclaw/latest/reference/troubleshooting.html
