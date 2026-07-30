#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${ACORD_APP_DIR:-/root/acord-api}"
SERVICE_NAME="acord-api"

if [[ $EUID -ne 0 ]]; then
  echo "deploy.sh must run as root" >&2
  exit 1
fi

cd "$APP_DIR"
git fetch --prune origin
git pull --ff-only origin main

install -d -m 700 "$APP_DIR/data" "$APP_DIR/backups"

if [[ ! -f "$APP_DIR/.env" ]]; then
  umask 077
  api_key="$(openssl rand -hex 32)"
  jwt_secret="$(openssl rand -hex 48)"
  admin_password="$(openssl rand -base64 30 | tr -d '\n')"
  cat >"$APP_DIR/.env" <<EOF
ACORD_API_KEY='$api_key'
ACORD_JWT_SECRET='$jwt_secret'
ACORD_ADMIN_USERNAME='admin'
ACORD_ADMIN_PASSWORD='$admin_password'
ACORD_ADMIN_EMAIL='mark.walters@joinalliancerisk.com'
ACORD_ADMIN_DISPLAY_NAME='Mark Walters'
ACORD_ALLOWED_ORIGINS='https://acord-demo.vercel.app'
EOF
  chmod 600 "$APP_DIR/.env"
  printf '%s\n' "$admin_password" >"$APP_DIR/.bootstrap-admin"
  chmod 600 "$APP_DIR/.bootstrap-admin"
fi

python3 -m venv "$APP_DIR/.venv"
"$APP_DIR/.venv/bin/python" -m pip install --quiet --upgrade pip
"$APP_DIR/.venv/bin/python" -m pip install --quiet -r "$APP_DIR/requirements.txt"

install -m 644 "$APP_DIR/systemd/acord-api.service" /etc/systemd/system/acord-api.service
install -m 644 "$APP_DIR/systemd/acord-api-backup.service" /etc/systemd/system/acord-api-backup.service
install -m 644 "$APP_DIR/systemd/acord-api-backup.timer" /etc/systemd/system/acord-api-backup.timer
install -m 755 "$APP_DIR/scripts/backup_data.sh" /usr/local/sbin/acord-api-backup
install -m 644 "$APP_DIR/ops/acord-api.nginx.conf" /etc/nginx/conf.d/acord-api.conf

if command -v pm2 >/dev/null 2>&1; then
  pm2 delete pawn-acord-api >/dev/null 2>&1 || true
  pm2 save >/dev/null 2>&1 || true
fi

systemctl daemon-reload
nginx -t
systemctl enable acord-api.service acord-api-backup.timer nginx.service
systemctl start acord-api.service acord-api-backup.timer nginx.service
systemctl reload nginx.service

"$APP_DIR/scripts/smoke_test.sh" "http://127.0.0.1:18080"
echo "ACORD API deployment passed semantic health and generation checks"
