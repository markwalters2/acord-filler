#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${ACORD_APP_DIR:-/root/acord-api}"
BACKUP_DIR="$APP_DIR/backups"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"

install -d -m 700 "$BACKUP_DIR"

if [[ -f "$APP_DIR/data/telemetry.db" ]]; then
  sqlite3 "$APP_DIR/data/telemetry.db" \
    ".timeout 15000" \
    ".backup '$BACKUP_DIR/telemetry-$STAMP.db'"
fi

tar -C "$APP_DIR" -czf "$BACKUP_DIR/acord-data-$STAMP.tar.gz" \
  --exclude='data/telemetry.db-wal' \
  --exclude='data/telemetry.db-shm' \
  data

find "$BACKUP_DIR" -type f -mtime +14 -delete
