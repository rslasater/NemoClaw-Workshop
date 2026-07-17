# Brev Instructor Runbook

Use this runbook to reduce setup support during the Project ATaS NemoClaw workshop. The student should still perform the NemoClaw onboarding, model selection, claw naming, and policy application so they understand the environment they are operating.

## Instructor Goals

- Remove avoidable Docker, port, and package failures before the agent work starts.
- Make the fake email API visible in both places students need it: their browser and the NemoClaw sandbox.
- Keep the network policy explicit and inspectable.
- Preserve the learning moment around OpenShell policy, rather than silently widening egress.

## Pre-Class Checklist

Confirm these before students arrive:

- Brev credits or workshop code are active.
- Students know which Brev organization to use.
- Students using Windows have WSL installed and can open a WSL terminal.
- Students can authenticate with `brev login`.
- Students can generate or access an NVIDIA API key from build.nvidia.com.
- The target Brev image has Docker and Docker Compose v2.
- Port `8000` is reserved for the fake email API on the Brev instance.
- Students have the repo URL: `https://github.com/rslasater/NemoClaw-Workshop.git`.

## Recommended Student Flow

Give students this shorter command path after they connect to their Brev instance:

```bash
git clone https://github.com/rslasater/NemoClaw-Workshop.git
cd NemoClaw-Workshop
./scripts/setup-brev-instance.sh
```

Then have them configure NemoClaw manually:

```bash
curl -fsSL https://www.nvidia.com/nemoclaw.sh | bash
nemoclaw <claw-name>
nemoclaw <claw-name> policy-add --from-file ./atas-email-api.yaml --yes
openshell term
```

Students should use the API base URL printed by the setup script when prompting the claw.

## Port Forwarding Guidance

The email API runs on the Brev instance at remote port `8000`. For laptop browser access, students need a local terminal:

```bash
brev port-forward <instance-name> --port 8000:8000
```

The first number is the laptop port. The second number is the Brev instance port. If `localhost:8000` is already busy on the laptop:

```bash
brev port-forward <instance-name> --port 8001:8000
```

Students then open `http://localhost:8001`, while the email API and NemoClaw policy still use remote port `8000`.

Use Brev web tunnels only for browser UI sharing. For direct API calls from scripts, the Brev CLI port forward is the cleaner path.

## NemoClaw Policy Guidance

The setup helper generates `atas-email-api.yaml` because the policy needs the concrete Brev instance host IP. Do not commit the generated file.

Expected policy command:

```bash
nemoclaw <claw-name> policy-add --from-file ./atas-email-api.yaml --yes
```

Expected allowed endpoint shape:

```text
http://<brev-instance-host-ip>:8000
```

This follows current NemoClaw guidance for host-side HTTP services: bind the service to an address the OpenShell gateway can reach, then apply a custom preset with `policy-add --from-file`.

## Instructor Verification

On a student Brev instance, run:

```bash
cd NemoClaw-Workshop
./scripts/check-brev-lab.sh
```

Expected passes:

- `curl`, `docker`, `git`, `jq`, and `readelf` are installed.
- Docker daemon is reachable.
- Docker Compose v2 is available.
- Email API responds on `localhost:8000`.
- Email API responds on the detected host IP at port `8000`.
- `atas-email-api.yaml` exists and has no template placeholder.

If the student has a running claw, dry-run the policy:

```bash
./scripts/check-brev-lab.sh <claw-name>
```

## Common Failure Modes

Docker daemon is missing or unreachable:

```bash
docker info
docker compose version
```

Move the student to a Brev image with Docker enabled or start Docker if the image supports it.

Port `8000` is busy on the Brev instance:

```bash
ss -ltnp | grep ':8000'
```

Stop the conflicting service. Avoid changing the workshop port unless you are ready to regenerate policy and adjust all prompts.

Browser cannot reach webmail:

```bash
brev port-forward <instance-name> --port 8000:8000
```

Make sure this runs on the laptop, not inside the Brev instance. The forwarding terminal must stay open.

NemoClaw cannot reach the API:

```bash
curl http://127.0.0.1:8000/health
curl http://<detected-host-ip>:8000/health
nemoclaw <claw-name> policy-list
openshell term
```

The claw should use `http://<detected-host-ip>:8000`, not `http://localhost:8000`.

Policy applies but request still fails:

- Confirm the blocked request in `openshell term`.
- Confirm the requesting binary is one of the policy binaries.
- Confirm the path is in the policy. Attachments use `/emails/**` and `/sent/**`.
- If the response changed from policy denied to upstream unreachable, focus on host routing or firewall.

NemoClaw install asks for missing `binutils`:

```bash
sudo apt-get install -y binutils
```

The setup helper already installs it, but this command is harmless to repeat.

## Suggested Timing

- 0:00-0:10: Brev start, credits, SSH.
- 0:10-0:20: Repo clone and `setup-brev-instance.sh`.
- 0:20-0:35: NemoClaw install and onboarding.
- 0:35-0:45: Policy add, webmail check, first API test.
- 0:45+: Scenario investigation and briefing work.

## End Of Workshop

Have students stop instances from a local terminal:

```bash
brev stop --all
```

For students with multiple unrelated Brev instances, use:

```bash
brev list
brev stop <instance-name>
```

## References

- NVIDIA Brev connectivity and port forwarding: https://docs.nvidia.com/brev/cli/connectivity
- NVIDIA Brev instance management: https://docs.nvidia.com/brev/cli/instance-management
- NemoClaw Brev web UI flow: https://docs.nvidia.com/nemoclaw/user-guide/openclaw/deployment/brev-web-ui
- NemoClaw custom network policy: https://docs.nvidia.com/nemoclaw/user-guide/openclaw/network-policy/customize-network-policy
- NemoClaw troubleshooting, host-side HTTP services: https://docs.nvidia.com/nemoclaw/latest/reference/troubleshooting.html
