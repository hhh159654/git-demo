#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "Usage: $0 paperN 'topic' 'domain'"
  exit 2
fi

PAPER="$1"
TOPIC="$2"
DOMAIN="$3"

git switch main
git pull --ff-only
git switch -c "$PAPER"

autoresearch init "$PAPER" --topic "$TOPIC" --domain "$DOMAIN"

echo
echo "Created branch/workspace: $PAPER"
echo "Next:"
echo "  git add \"$PAPER\""
echo "  git commit -m \"init $PAPER workspace\""
echo "  git push -u origin \"$PAPER\""
