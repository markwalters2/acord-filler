#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://127.0.0.1:18080}"
APP_DIR="${ACORD_APP_DIR:-/root/acord-api}"

health="$(curl -fsS "$BASE_URL/health")"
python3 - "$health" <<'PY'
import json
import sys

data = json.loads(sys.argv[1])
assert data["service"] == "acord-api-v2", data
assert data["schema_version"] == 2, data
assert data["database"] == "ok", data
assert set(data["forms"]) == {"24", "25", "28"}, data
assert isinstance(data["stats"], dict), data
PY

set -a
source "$APP_DIR/.env"
set +a

policy='{"insured":{"name":"Smoke Test LLC","address_line1":"1 Test Way","city":"Testville","state":"IL","zip":"60000"},"policy":{"carrier":"Test Carrier","number":"TEST-001","effective_date":"01/01/2026","expiration_date":"01/01/2027"},"coverages":{"gl":{"has":true,"occurrence":true,"occurrence_limit":"1000000","aggregate_limit":"2000000","policy_number":"TEST-001"}}}'
holder='{"name":"Smoke Test Holder","address_line1":"2 Holder Way","city":"Testville","state":"IL","zip":"60000"}'

output="$(mktemp -t acord-smoke-XXXXXX.pdf)"
trap 'rm -f "$output"' EXIT

curl -fsS \
  -H "x-api-key: $ACORD_API_KEY" \
  -F "form_type=25" \
  -F "policy_data=$policy" \
  -F "cert_holder=$holder" \
  -F 'agency={"name":"Alliance Risk"}' \
  -F "flatten=false" \
  "$BASE_URL/api/generate" \
  -o "$output"

python3 - "$output" <<'PY'
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
data = path.read_bytes()
assert len(data) > 10_000, len(data)
assert data.startswith(b"%PDF-"), data[:10]
PY
