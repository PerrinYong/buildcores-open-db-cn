#!/usr/bin/env bash
set -euo pipefail

# Sync upstream repo into this fork.
#
# Usage:
#   ./scripts/sync_upstream.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

UPSTREAM_URL="https://github.com/buildcores/buildcores-open-db.git"
UPSTREAM_REMOTE="upstream"

git rev-parse --is-inside-work-tree >/dev/null

if ! git remote get-url "$UPSTREAM_REMOTE" >/dev/null 2>&1; then
  git remote add "$UPSTREAM_REMOTE" "$UPSTREAM_URL"
fi

git fetch "$UPSTREAM_REMOTE" --prune

CURRENT_BRANCH="$(git branch --show-current)"
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "Switching to main (was: $CURRENT_BRANCH)"
  git checkout main
fi

git merge --no-edit "$UPSTREAM_REMOTE/main"

echo "Done. Review changes, then push: git push origin main"
