#!/usr/bin/env sh
set -eu

usage() {
  cat <<'EOF'
Usage:
  sh scripts/install-auto-pull-launch-agent.sh [interval-seconds]

Example:
  sh scripts/install-auto-pull-launch-agent.sh 1800

Installs a macOS LaunchAgent that runs scripts/auto-pull-vps-artifacts.sh.
Default interval: 1800 seconds.
EOF
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

if [ "$#" -gt 1 ]; then
  usage >&2
  exit 2
fi

INTERVAL=${1:-1800}
case "$INTERVAL" in
  *[!0-9]* | "")
    echo "interval-seconds must be a positive integer" >&2
    exit 2
    ;;
esac

if [ "$INTERVAL" -le 0 ]; then
  echo "interval-seconds must be a positive integer" >&2
  exit 2
fi

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
LABEL="com.takamasa.blog-agent-kit.pull-vps-artifacts"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOG_DIR="$ROOT/tmp"

mkdir -p "$HOME/Library/LaunchAgents" "$LOG_DIR"

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>$LABEL</string>

  <key>ProgramArguments</key>
  <array>
    <string>/bin/sh</string>
    <string>$ROOT/scripts/auto-pull-vps-artifacts.sh</string>
  </array>

  <key>WorkingDirectory</key>
  <string>$ROOT</string>

  <key>RunAtLoad</key>
  <true/>

  <key>StartInterval</key>
  <integer>$INTERVAL</integer>

  <key>StandardOutPath</key>
  <string>$LOG_DIR/auto-pull-vps-artifacts.log</string>

  <key>StandardErrorPath</key>
  <string>$LOG_DIR/auto-pull-vps-artifacts.err.log</string>
</dict>
</plist>
EOF

plutil -lint "$PLIST"

UID_VALUE=$(id -u)
launchctl bootout "gui/$UID_VALUE" "$PLIST" 2>/dev/null || true
launchctl bootstrap "gui/$UID_VALUE" "$PLIST"
launchctl kickstart -k "gui/$UID_VALUE/$LABEL"

echo "Installed LaunchAgent: $PLIST"
echo "Interval seconds: $INTERVAL"
