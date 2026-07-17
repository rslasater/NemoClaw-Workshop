#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

API_PORT="${EMAIL_API_PORT:-8000}"
STUDENT_ID="${STUDENT_ID:-student-01}"
STUDENT_EMAIL="${STUDENT_EMAIL:-student-01@workshop.example}"
POLICY_FILE="${POLICY_FILE:-atas-email-api.yaml}"

log() {
  printf "\n==> %s\n" "$*"
}

warn() {
  printf "WARN: %s\n" "$*" >&2
}

fail() {
  printf "ERROR: %s\n" "$*" >&2
  exit 1
}

have_cmd() {
  command -v "$1" >/dev/null 2>&1
}

install_apt_dependencies() {
  if [[ "${SKIP_APT_INSTALL:-0}" == "1" ]]; then
    log "Skipping apt dependency install because SKIP_APT_INSTALL=1"
    return
  fi

  if ! have_cmd apt-get; then
    warn "apt-get is not available. Install binutils, curl, git, jq, and ca-certificates manually if needed."
    return
  fi

  log "Installing host dependencies used by NemoClaw and lab checks"
  sudo apt-get update
  sudo apt-get install -y binutils ca-certificates curl git jq
}

check_docker() {
  log "Checking Docker and Docker Compose"

  have_cmd docker || fail "Docker is not on PATH. Use a Brev image with Docker installed or install Docker before the workshop."
  docker info >/dev/null || fail "Docker is installed but not reachable. Start Docker, then rerun this script."
  docker compose version >/dev/null || fail "Docker Compose v2 is not available. Install the Docker Compose plugin."
}

check_port() {
  if ! have_cmd ss; then
    return
  fi

  if ss -ltn | awk '{print $4}' | grep -Eq "(:|\\])${API_PORT}$"; then
    if curl -fsS "http://127.0.0.1:${API_PORT}/health" >/dev/null 2>&1; then
      log "Port ${API_PORT} is already serving the workshop email API"
      return
    fi

    fail "Port ${API_PORT} is already in use by another service. Stop it or set EMAIL_API_PORT to an unused port."
  fi
}

write_env_file() {
  if [[ -f .env ]]; then
    log "Using existing .env"
    return
  fi

  log "Creating .env"
  {
    printf "STUDENT_ID=%s\n" "$STUDENT_ID"
    printf "STUDENT_EMAIL=%s\n" "$STUDENT_EMAIL"
    printf "EMAIL_API_PORT=%s\n" "$API_PORT"
    printf "EMAIL_API_BASE=http://localhost:%s\n" "$API_PORT"
  } > .env
}

start_email_api() {
  log "Starting the fake email API"
  STUDENT_ID="$STUDENT_ID" STUDENT_EMAIL="$STUDENT_EMAIL" docker compose up -d --build
}

wait_for_api() {
  log "Waiting for the email API health check"

  for _ in $(seq 1 60); do
    if curl -fsS "http://127.0.0.1:${API_PORT}/health" >/dev/null 2>&1; then
      return
    fi
    sleep 2
  done

  docker compose ps || true
  fail "Email API did not become healthy at http://127.0.0.1:${API_PORT}/health"
}

detect_host_ip() {
  if [[ -n "${EMAIL_API_HOST_OVERRIDE:-}" ]]; then
    printf "%s\n" "$EMAIL_API_HOST_OVERRIDE"
    return
  fi

  if have_cmd ip; then
    local route_ip
    route_ip="$(ip -4 route get 1.1.1.1 2>/dev/null | awk '{for (i=1; i<=NF; i++) if ($i == "src") {print $(i+1); exit}}')"
    if [[ -n "$route_ip" ]]; then
      printf "%s\n" "$route_ip"
      return
    fi
  fi

  if have_cmd hostname; then
    local host_ip
    host_ip="$(hostname -I 2>/dev/null | awk '{print $1}')"
    if [[ -n "$host_ip" ]]; then
      printf "%s\n" "$host_ip"
      return
    fi
  fi

  fail "Could not detect a non-loopback host IP. Set EMAIL_API_HOST_OVERRIDE and rerun."
}

verify_host_ip_route() {
  local host_ip="$1"

  log "Checking email API through detected host IP ${host_ip}"
  curl -fsS "http://${host_ip}:${API_PORT}/health" >/dev/null ||
    fail "The API is healthy on localhost but not on ${host_ip}:${API_PORT}. Check host firewall or Docker port publishing."
}

write_policy_file() {
  local host_ip="$1"

  log "Writing ${POLICY_FILE}"
  cat > "$POLICY_FILE" <<YAML
preset:
  name: atas-email-api
  description: "Project ATaS fake email API on this Brev instance"

network_policies:
  atas_email_api:
    name: atas_email_api
    endpoints:
      - host: ${host_ip}
        port: ${API_PORT}
        protocol: rest
        enforcement: enforce
        rules:
          - allow: { method: GET, path: "/" }
          - allow: { method: GET, path: "/health" }
          - allow: { method: GET, path: "/me" }
          - allow: { method: GET, path: "/openapi.json" }
          - allow: { method: GET, path: "/docs" }
          - allow: { method: GET, path: "/emails" }
          - allow: { method: GET, path: "/emails/**" }
          - allow: { method: GET, path: "/drafts" }
          - allow: { method: POST, path: "/drafts" }
          - allow: { method: POST, path: "/send-summary" }
          - allow: { method: POST, path: "/send" }
          - allow: { method: GET, path: "/sent" }
          - allow: { method: GET, path: "/sent/**" }
          - allow: { method: GET, path: "/activity" }
          - allow: { method: POST, path: "/reset" }
    binaries:
      - { path: /usr/local/bin/node }
      - { path: /usr/local/bin/openclaw }
      - { path: /usr/bin/curl }
      - { path: /usr/bin/python3 }
      - { path: /usr/local/bin/python3 }
YAML
}

print_next_steps() {
  local host_ip="$1"

  cat <<EOF

Ready.

Email API on the Brev instance:
  http://127.0.0.1:${API_PORT}

Email API base URL for the NemoClaw sandbox:
  http://${host_ip}:${API_PORT}

Generated NemoClaw policy file:
  ${ROOT_DIR}/${POLICY_FILE}

After the student creates and starts a claw, apply the policy:
  nemoclaw <claw-name> policy-add --from-file ./${POLICY_FILE} --yes

To view the webmail UI from the student's laptop, keep a local terminal open:
  brev port-forward <instance-name> --port ${API_PORT}:${API_PORT}

Then open:
  http://localhost:${API_PORT}

If localhost:${API_PORT} is already busy on the laptop, use:
  brev port-forward <instance-name> --port 8001:${API_PORT}
  http://localhost:8001
EOF
}

install_apt_dependencies
check_docker
check_port
write_env_file
start_email_api
wait_for_api
HOST_IP="$(detect_host_ip)"
verify_host_ip_route "$HOST_IP"
write_policy_file "$HOST_IP"
print_next_steps "$HOST_IP"
