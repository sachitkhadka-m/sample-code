#!/bin/bash
set -euo pipefail # stop on errors, unset vars, and pipe failures

# ─── Config ───────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SUBMODULE_PATH="module-main"
SUBMODULE_BRANCH="main"
MAIN_BRANCH="main"
LOG_FILE="$SCRIPT_DIR/sync-submodule.log"
LOCKFILE="/tmp/sync-submodule.lock"
ORIGINAL_DIR="$(pwd)"

# ─── Logger ───────────────────────────────────────
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# ─── Cleanup trap ─────────────────────────────────
trap 'cd "$ORIGINAL_DIR"' EXIT

# ─── Lock: prevent concurrent runs ───────────────
exec 200>"$LOCKFILE"
flock -n 200 || { log "ERROR: Another instance is already running"; exit 1; }

# ─── Start ────────────────────────────────────────
log "========================================="
log "Starting submodule sync (Backend Main Team)"

# ─── Safety Check 1: submodule folder exists? ─────
if [ ! -d "$SUBMODULE_PATH" ]; then
  log "ERROR: Submodule directory '$SUBMODULE_PATH' not found!"
  exit 1
fi

# ─── Safety Check 2: are we on the right branch? ──
CURRENT_MAIN_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_MAIN_BRANCH" != "$MAIN_BRANCH" ]; then
  log "ERROR: Main project is on '$CURRENT_MAIN_BRANCH', expected '$MAIN_BRANCH'"
  exit 1
fi

# ─── Step 1: Pull latest in submodule ─────────────
log "Pulling latest from submodule/$SUBMODULE_BRANCH..."
cd "$SUBMODULE_PATH"

# verify submodule is on correct branch
git checkout "$SUBMODULE_BRANCH"
git pull origin "$SUBMODULE_BRANCH"

SUBMODULE_COMMIT=$(git rev-parse --short HEAD)
log "Submodule is now at commit: $SUBMODULE_COMMIT"

cd "$ORIGINAL_DIR"

# ─── Step 2: Only commit if something changed ─────
if git diff --quiet "$SUBMODULE_PATH"; then
  log "No changes detected in submodule. Nothing to commit."
  exit 0
fi

# ─── Step 3: Stage + Commit + Push ────────────────
log "Changes detected. Staging submodule..."
git add "$SUBMODULE_PATH"
git commit -m "chore: sync submodule to $SUBMODULE_COMMIT [skip ci]"

log "Pushing to main project..."
git push --recurse-submodules=check origin "$MAIN_BRANCH"

log "Successfully synced submodule! (Backend Main Team)"
log "========================================="
