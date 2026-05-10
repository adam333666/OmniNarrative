#!/usr/bin/env bash
set -euo pipefail

API_BASE_URL="${API_BASE_URL:-http://127.0.0.1:8000/api/v1}"
POLL_INTERVAL_SECONDS="${POLL_INTERVAL_SECONDS:-1}"
MAX_POLLS="${MAX_POLLS:-20}"
SMOKE_TEST_REQUEST_FILE="${SMOKE_TEST_REQUEST_FILE:-}"
SMOKE_TEST_LABEL="${SMOKE_TEST_LABEL:-default}"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

if [[ -n "${SMOKE_TEST_REQUEST_FILE}" ]]; then
  if [[ ! -f "${SMOKE_TEST_REQUEST_FILE}" ]]; then
    echo "Smoke test request file not found: ${SMOKE_TEST_REQUEST_FILE}" >&2
    exit 1
  fi
  request_json="$(cat "${SMOKE_TEST_REQUEST_FILE}")"
else
  request_json='{
    "theme_text": "我想做一个关于时间旅行悖论的内容",
    "content_type": "science_popularization",
    "target_platform": "bilibili",
    "target_audience_text": "喜欢脑洞和科学设定的大学生与年轻上班族",
    "style_tone": "mysterious",
    "custom_style_text": "有一点哲学感，但不要太晦涩"
  }'
fi

echo "Smoke test label: ${SMOKE_TEST_LABEL}"

echo "[1/6] Checking health endpoint"
curl --fail --silent --show-error "${API_BASE_URL}/health" > "${TMP_DIR}/health.json"

echo "[2/6] Checking input options endpoint"
curl --fail --silent --show-error "${API_BASE_URL}/config/input-options" > "${TMP_DIR}/input-options.json"

echo "[3/6] Submitting a generation request"
curl \
  --fail \
  --silent \
  --show-error \
  --header "Content-Type: application/json" \
  --data "${request_json}" \
  "${API_BASE_URL}/creations/generate" > "${TMP_DIR}/generate.json"

generation_id="$(
  python3 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["generation_id"])' \
    "${TMP_DIR}/generate.json"
)"

echo "Generation created: ${generation_id}"

final_status=""
echo "[4/6] Polling generation status"
for (( attempt=1; attempt<=MAX_POLLS; attempt+=1 )); do
  curl \
    --fail \
    --silent \
    --show-error \
    "${API_BASE_URL}/creations/${generation_id}/status" > "${TMP_DIR}/status.json"

  final_status="$(
    python3 -c 'import json,sys; data=json.load(open(sys.argv[1], encoding="utf-8")); print(data["status"])' \
      "${TMP_DIR}/status.json"
  )"
  current_stage="$(
    python3 -c 'import json,sys; data=json.load(open(sys.argv[1], encoding="utf-8")); print(data["current_stage"])' \
      "${TMP_DIR}/status.json"
  )"
  stage_message="$(
    python3 -c 'import json,sys; data=json.load(open(sys.argv[1], encoding="utf-8")); print(data["stage_message"])' \
      "${TMP_DIR}/status.json"
  )"

  echo "  poll ${attempt}: status=${final_status} stage=${current_stage} message=${stage_message}"

  if [[ "${final_status}" == "FAILED" || "${final_status}" == "TIMEOUT" ]]; then
    echo "Smoke test failed during generation." >&2
    exit 1
  fi

  if [[ "${final_status}" == "PACKAGE_ASSEMBLING" || "${final_status}" == "DONE" ]]; then
    break
  fi

  sleep "${POLL_INTERVAL_SECONDS}"
done

if [[ "${final_status}" != "PACKAGE_ASSEMBLING" && "${final_status}" != "DONE" ]]; then
  echo "Smoke test timed out before reaching PACKAGE_ASSEMBLING or DONE." >&2
  exit 1
fi

echo "[5/6] Validating result and export endpoints"
curl --fail --silent --show-error "${API_BASE_URL}/creations/${generation_id}/result" > "${TMP_DIR}/result.json"
curl --fail --silent --show-error "${API_BASE_URL}/creations/${generation_id}/export/json" > "${TMP_DIR}/export.json"
curl --fail --silent --show-error "${API_BASE_URL}/creations/${generation_id}/export/md" > "${TMP_DIR}/export.md"
curl --fail --silent --show-error "${API_BASE_URL}/creations/${generation_id}/video-payload" > "${TMP_DIR}/video-payload.json"

echo "[6/6] Checking result envelope shape"
python3 -c '
import json
import sys

result = json.load(open(sys.argv[1], encoding="utf-8"))
payload = json.load(open(sys.argv[2], encoding="utf-8"))

for key in ("request_summary", "analysis", "result_package", "export_meta"):
    if key not in result:
        raise SystemExit(f"missing result key: {key}")

for key in ("video_meta", "segments", "shots", "characters", "scenes", "style_constraints", "subtitle_blocks", "audio_guides", "negative_constraints"):
    if key not in payload:
        raise SystemExit(f"missing video payload key: {key}")
' "${TMP_DIR}/result.json" "${TMP_DIR}/video-payload.json"

echo "Smoke test passed for generation ${generation_id}."
