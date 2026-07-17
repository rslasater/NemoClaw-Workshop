#!/usr/bin/env bash

set -uo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
PROJECT_DIR="$(cd -- "${SCRIPT_DIR}/.." >/dev/null 2>&1 && pwd)"

cd "${PROJECT_DIR}" || exit 1

PYTHON_BIN="${PYTHON_BIN:-python3}"
PROVIDER="${ATAS_PROVIDER:-openai-compatible}"
SLEEP_SECONDS="${ATAS_GENERATE_SLEEP_SECONDS:-2}"
RETRIES="${ATAS_GENERATE_RETRIES:-0}"
FORCE=0

usage() {
  cat <<'EOF'
Usage: scripts/generate_remaining.sh [options] [THREAD_ID ...]

Generate and validate Project ATaS threads without exiting on the first failure.

Options:
  --force              Regenerate threads even when emails.json already exists.
  --provider NAME      Provider to pass to atas_generator.cli generate.
                       Default: openai-compatible
  --retries N          Retry failed generation N times before recording failure.
                       Default: 0
  --sleep N            Seconds to sleep between successful threads.
                       Default: 2
  -h, --help           Show this help.

Environment overrides:
  PYTHON_BIN                    Python executable. Default: python
  ATAS_PROVIDER                 Provider name. Default: openai-compatible
  ATAS_GENERATE_RETRIES         Retry count. Default: 0
  ATAS_GENERATE_SLEEP_SECONDS   Sleep between successful threads. Default: 2
EOF
}

THREAD_ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)
      FORCE=1
      shift
      ;;
    --provider)
      PROVIDER="${2:-}"
      shift 2
      ;;
    --retries)
      RETRIES="${2:-0}"
      shift 2
      ;;
    --sleep)
      SLEEP_SECONDS="${2:-0}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      THREAD_ARGS+=("$1")
      shift
      ;;
  esac
done

mkdir -p generated/logs
FAILURES_FILE="generated/logs/failures.txt"
SUMMARY_FILE="generated/logs/summary.txt"
: > "${FAILURES_FILE}"
: > "${SUMMARY_FILE}"

log_summary() {
  echo "$*" | tee -a "${SUMMARY_FILE}"
}

record_failure() {
  local thread_id="$1"
  local stage="$2"
  local log_file="$3"
  echo "${thread_id} ${stage} ${log_file}" | tee -a "${FAILURES_FILE}" >/dev/null
}

run_logged() {
  local log_file="$1"
  shift

  {
    echo "[$(date -Is)] Running: $*"
    echo
  } > "${log_file}"

  "$@" 2>&1 | tee -a "${log_file}"
  return "${PIPESTATUS[0]}"
}

if [[ ${#THREAD_ARGS[@]} -gt 0 ]]; then
  THREAD_IDS=("${THREAD_ARGS[@]}")
else
  if ! mapfile -t THREAD_IDS < <("${PYTHON_BIN}" -m atas_generator.cli list-threads | awk 'NF { print $1 }'); then
    echo "Could not list threads. Check Python environment and package install." >&2
    exit 2
  fi
fi

total=${#THREAD_IDS[@]}
generated=0
valid=0
skipped=0
failed=0

log_summary "Starting generation run at $(date -Is)"
log_summary "Provider: ${PROVIDER}"
log_summary "Threads: ${total}"
log_summary

for thread_id in "${THREAD_IDS[@]}"; do
  [[ -z "${thread_id}" ]] && continue

  thread_dir="generated/threads/${thread_id}"
  emails_file="${thread_dir}/emails.json"
  generate_log="generated/logs/${thread_id}.generate.log"
  validate_log="generated/logs/${thread_id}.validate.log"

  echo
  echo "=== ${thread_id} ==="

  if [[ -f "${emails_file}" && "${FORCE}" -ne 1 ]]; then
    echo "Existing emails.json found; validating ${thread_id}"
    if run_logged "${validate_log}" "${PYTHON_BIN}" -m atas_generator.cli validate "${thread_id}"; then
      echo "Skipping ${thread_id}: already valid"
      skipped=$((skipped + 1))
      valid=$((valid + 1))
    else
      echo "Validation failed for existing ${thread_id}; leaving files for review"
      record_failure "${thread_id}" "validate-existing" "${validate_log}"
      failed=$((failed + 1))
    fi
    continue
  fi

  attempt=0
  generated_ok=0
  while [[ "${attempt}" -le "${RETRIES}" ]]; do
    attempt=$((attempt + 1))
    echo "Generating ${thread_id} (attempt ${attempt}/$((RETRIES + 1)))"
    if run_logged "${generate_log}" "${PYTHON_BIN}" -m atas_generator.cli generate "${thread_id}" --provider "${PROVIDER}"; then
      generated_ok=1
      generated=$((generated + 1))
      break
    fi
    echo "Generation failed for ${thread_id}; see ${generate_log}"
    [[ "${attempt}" -le "${RETRIES}" ]] && sleep "${SLEEP_SECONDS}"
  done

  if [[ "${generated_ok}" -ne 1 ]]; then
    record_failure "${thread_id}" "generate" "${generate_log}"
    failed=$((failed + 1))
    continue
  fi

  echo "Validating ${thread_id}"
  if run_logged "${validate_log}" "${PYTHON_BIN}" -m atas_generator.cli validate "${thread_id}"; then
    valid=$((valid + 1))
  else
    echo "Validation failed for ${thread_id}; see ${validate_log}"
    record_failure "${thread_id}" "validate" "${validate_log}"
    failed=$((failed + 1))
    continue
  fi

  sleep "${SLEEP_SECONDS}"
done

log_summary
log_summary "Completed generation run at $(date -Is)"
log_summary "Generated: ${generated}"
log_summary "Valid: ${valid}"
log_summary "Skipped existing valid: ${skipped}"
log_summary "Failed: ${failed}"
log_summary "Failure list: ${FAILURES_FILE}"

if [[ "${failed}" -gt 0 ]]; then
  echo
  echo "Some threads failed. Review ${FAILURES_FILE}; the script continued safely."
  exit 1
fi

echo
echo "All requested threads generated or validated successfully."
