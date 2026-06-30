#!/usr/bin/env sh
set -eu

usage() {
  cat <<'EOF'
Usage:
  sh scripts/pull-remote-artifacts.sh <ssh-target> <remote-artifact-dir> <local-output-dir>

Example:
  sh scripts/pull-remote-artifacts.sh \
    user@host.example \
    /home/user/blog-agent-kit/output/artifacts/2026-06-30-demo \
    output/remote-artifacts/2026-06-30-demo

This pulls reviewable artifacts only. It does not delete local files.
EOF
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

if [ "$#" -ne 3 ]; then
  usage >&2
  exit 2
fi

REMOTE_TARGET=$1
REMOTE_DIR=${2%/}
LOCAL_DIR=${3%/}

if [ -z "$REMOTE_TARGET" ] || [ -z "$REMOTE_DIR" ] || [ -z "$LOCAL_DIR" ]; then
  usage >&2
  exit 2
fi

mkdir -p "$LOCAL_DIR"

rsync -av --prune-empty-dirs \
  --include='*/' \
  --include='*.md' \
  --include='*.txt' \
  --include='*.json' \
  --include='*.csv' \
  --include='*.tsv' \
  --include='*.html' \
  --include='*.pdf' \
  --include='*.zip' \
  --include='*.tar' \
  --include='*.tar.gz' \
  --include='*.png' \
  --include='*.jpg' \
  --include='*.jpeg' \
  --include='*.webp' \
  --include='*.gif' \
  --include='*.svg' \
  --include='*.mp4' \
  --include='*.mov' \
  --include='*.webm' \
  --include='*.mkv' \
  --include='*.wav' \
  --include='*.mp3' \
  --include='*.flac' \
  --exclude='*' \
  "$REMOTE_TARGET:$REMOTE_DIR/" \
  "$LOCAL_DIR/"

echo "Artifacts copied to: $LOCAL_DIR"
