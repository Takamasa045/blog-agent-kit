#!/usr/bin/env sh
set -eu

usage() {
  cat <<'EOF'
Usage:
  sh scripts/auto-pull-vps-artifacts.sh

Environment:
  BLOG_AGENT_VPS_ARTIFACT_ENV  Optional path to a vps-artifacts.env file.

The env file must define:
  BLOG_AGENT_VPS_TARGET
  BLOG_AGENT_REMOTE_REPO
  BLOG_AGENT_LOCAL_ARTIFACT_ROOT

This syncs all remote output/artifacts/ files into the local artifact root.
It uses rsync without --delete, so it does not remove local files.
EOF
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

if [ "$#" -ne 0 ]; then
  usage >&2
  exit 2
fi

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
ENV_FILE=${BLOG_AGENT_VPS_ARTIFACT_ENV:-"$ROOT/tmp/vps-artifacts.env"}
LOCK_DIR="$ROOT/tmp/.auto-pull-vps-artifacts.lock"

timestamp() {
  date '+%Y-%m-%dT%H:%M:%S%z'
}

if [ ! -f "$ENV_FILE" ]; then
  echo "$(timestamp) missing env file: $ENV_FILE" >&2
  exit 1
fi

. "$ENV_FILE"

REMOTE_ROOT="${BLOG_AGENT_REMOTE_REPO%/}/output/artifacts"
LOCAL_ROOT="$ROOT/${BLOG_AGENT_LOCAL_ARTIFACT_ROOT%/}"

mkdir -p "$ROOT/tmp"
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  echo "$(timestamp) skipped: previous pull is still running"
  exit 0
fi

cleanup() {
  rmdir "$LOCK_DIR" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "$(timestamp) pull start: $BLOG_AGENT_VPS_TARGET:$REMOTE_ROOT -> $LOCAL_ROOT"
sh "$ROOT/scripts/pull-remote-artifacts.sh" \
  "$BLOG_AGENT_VPS_TARGET" \
  "$REMOTE_ROOT" \
  "$LOCAL_ROOT"
echo "$(timestamp) pull done"
