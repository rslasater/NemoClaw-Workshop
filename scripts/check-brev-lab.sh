#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

API_PORT="${EMAIL_API_PORT:-8000}"
POLICY_FILE="${POLICY_FILE:-atas-email-api.yaml}"
FAILURES=0

pass() {
  printf "PASS: %s\n" "$*"
}

warn() {
  printf "WARN: %s\n" "$*" >&2
}

fail_check() {
  printf "FAIL: %s\n" "$*" >&2
  FAILURES=$((FAILURES + 1))
}

have_cmd() {
  command -v "$1" >/dev/null 2>&1
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

  hostname -I 2>/dev/null | awk '{print $1}'
}

check_command() {
  local cmd="$1"
  if have_cmd "$cmd"; then
    pass "${cmd} is installed"
  else
    fail_check "${cmd} is missing"
  fi
}

check_command curl
check_command docker
check_command git
check_command jq
check_command readelf

if have_cmd docker; then
  if docker info >/dev/null 2>&1; then
    pass "Docker daemon is reachable"
  else
    fail_check "Docker daemon is not reachable"
  fi

  if docker compose version >/dev/null 2>&1; then
    pass "Docker Compose v2 is available"
  else
    fail_check "Docker Compose v2 is missing"
  fi
fi

if curl -fsS "http://127.0.0.1:${API_PORT}/health" >/dev/null 2>&1; then
  pass "Email API responds on localhost:${API_PORT}"
else
  fail_check "Email API is not healthy on localhost:${API_PORT}. Run scripts/setup-brev-instance.sh."
fi

HOST_IP="$(detect_host_ip)"
if [[ -n "$HOST_IP" ]] && curl -fsS "http://${HOST_IP}:${API_PORT}/health" >/dev/null 2>&1; then
  pass "Email API responds on ${HOST_IP}:${API_PORT}"
else
  fail_check "Email API is not reachable through the detected host IP. Set EMAIL_API_HOST_OVERRIDE if detection picked the wrong address."
fi

if [[ -f "$POLICY_FILE" ]]; then
  if grep -q "EMAIL_API_HOST_REPLACE_ME" "$POLICY_FILE"; then
    fail_check "${POLICY_FILE} still contains the template host placeholder"
  else
    pass "${POLICY_FILE} exists and does not contain the template placeholder"
  fi
else
  fail_check "${POLICY_FILE} is missing. Run scripts/setup-brev-instance.sh."
fi

if have_cmd nemoclaw; then
  pass "nemoclaw is installed"
  if [[ $# -gt 0 && -f "$POLICY_FILE" ]]; then
    if nemoclaw "$1" policy-add --from-file "./${POLICY_FILE}" --dry-run >/dev/null 2>&1; then
      pass "NemoClaw accepts ${POLICY_FILE} for sandbox $1 in dry-run mode"
    else
      warn "NemoClaw dry-run failed for sandbox $1. Confirm the claw is running, then inspect the error manually."
    fi
  fi
else
  warn "nemoclaw is not installed yet. This is okay before the manual NemoClaw setup step."
fi

if [[ "$FAILURES" -gt 0 ]]; then
  printf "\n%d check(s) failed.\n" "$FAILURES" >&2
  exit 1
fi

printf "\nAll checked Brev lab prerequisites passed.\n"
