#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENDOR="$ROOT/.vendor/AutoResearch-reference"

if [[ -d "$VENDOR/.git" ]]; then
  echo "Reference checkout already exists: $VENDOR"
  echo "Update manually if you intentionally want a newer upstream."
  exit 0
fi

mkdir -p "$ROOT/.vendor"
git clone --depth 1 https://github.com/Grain-Wang/AutoResearch.git "$VENDOR"

echo
echo "Reference cloned to:"
echo "  $VENDOR/AutoResearchClaw"
echo
echo "Optional editable install:"
echo "  pip install -e \"$VENDOR/AutoResearchClaw\""
echo
echo "The .vendor directory is gitignored."
