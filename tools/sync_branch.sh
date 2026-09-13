#!/usr/bin/env bash
set -euo pipefail

BRANCH="${1:-$(git branch --show-current)}"

if [[ -z "$BRANCH" ]]; then
  echo "Cannot determine current branch."
  exit 2
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Working tree is not clean. Commit/stash before syncing."
  git status --short
  exit 3
fi

git fetch origin "$BRANCH"
git pull --ff-only origin "$BRANCH"
echo "Synced $BRANCH"
