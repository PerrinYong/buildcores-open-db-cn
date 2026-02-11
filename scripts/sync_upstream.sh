#!/usr/bin/env bash
set -euo pipefail

# Update upstream OpenDB nested submodule pointer.
#
# Usage:
#   ./scripts/sync_upstream.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

git rev-parse --is-inside-work-tree >/dev/null

CURRENT_BRANCH="$(git branch --show-current)"
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "Switching to main (was: $CURRENT_BRANCH)"
  git checkout main
fi

git submodule sync -- open-db-upstream
git submodule update --init --remote open-db-upstream

echo "Done. Review submodule pointer update, then commit and push."
