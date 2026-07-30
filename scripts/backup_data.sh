#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${ACORD_APP_DIR:-/root/acord-api}"
BACKUP_DIR="$APP_DIR/backups"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"

install -d -m 700 "$BACKUP_DIR"

if [[ -f "$APP_DIR/data/telemetry.db" ]]; then
  python3 - "$APP_DIR/data/telemetry.db" "$BACKUP_DIR/telemetry-$STAMP.db" <<'PY'
import sqlite3
import sys

source = sqlite3.connect(sys.argv[1], timeout=15)
destination = sqlite3.connect(sys.argv[2])
with destination:
    source.backup(destination)
destination.close()
source.close()
PY
fi

tar -C "$APP_DIR" -czf "$BACKUP_DIR/acord-data-$STAMP.tar.gz" \
  --exclude='data/telemetry.db-wal' \
  --exclude='data/telemetry.db-shm' \
  data

find "$BACKUP_DIR" -type f -mtime +14 -delete
