#!/usr/bin/env bash
set -euo pipefail

: "${A800_SSH_ALIAS:?Set A800_SSH_ALIAS in config/local/a800.env}"

MIN_FREE="${A800_MIN_FREE_MIB:-60000}"
MAX_UTIL="${A800_MAX_UTIL_PCT:-5}"
POLL="${A800_POLL_SEC:-60}"

echo "Waiting for a candidate GPU."
echo "Thresholds: free >= ${MIN_FREE} MiB, utilization <= ${MAX_UTIL}%"
echo "This script NEVER launches a job. Manual coordination is still required."

while true; do
  OUT="$(ssh "$A800_SSH_ALIAS" \
    "nvidia-smi --query-gpu=index,memory.free,utilization.gpu --format=csv,noheader,nounits" \
    2>/dev/null || true)"

  if [[ -z "$OUT" ]]; then
    echo "$(date -Is) unable to query GPU; retrying..."
    sleep "$POLL"
    continue
  fi

  FOUND=""
  while IFS=',' read -r idx free util; do
    idx="$(echo "$idx" | xargs)"
    free="$(echo "$free" | xargs)"
    util="$(echo "$util" | xargs)"
    if [[ "$free" =~ ^[0-9]+$ && "$util" =~ ^[0-9]+$ ]] \
       && (( free >= MIN_FREE )) && (( util <= MAX_UTIL )); then
      FOUND="$idx"
      break
    fi
  done <<< "$OUT"

  if [[ -n "$FOUND" ]]; then
    echo "$(date -Is) candidate GPU detected: index=$FOUND"
    echo "Run tools/a800_status.sh and confirm ownership/coordination before starting any job."
    exit 0
  fi

  echo "$(date -Is) no candidate GPU"
  sleep "$POLL"
done
