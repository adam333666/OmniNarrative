#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="${ROOT_DIR}/frontend"
BACKEND_DIR="${ROOT_DIR}/backend"
PLAYWRIGHT_DB_PATH="/tmp/multi_media_playwright.db"
BACKEND_LOG="/tmp/multi_media_playwright_backend.log"
FRONTEND_LOG="/tmp/multi_media_playwright_frontend.log"
BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
  if [[ -n "${FRONTEND_PID}" ]] && kill -0 "${FRONTEND_PID}" 2>/dev/null; then
    kill "${FRONTEND_PID}" 2>/dev/null || true
    wait "${FRONTEND_PID}" 2>/dev/null || true
  fi
  if [[ -n "${BACKEND_PID}" ]] && kill -0 "${BACKEND_PID}" 2>/dev/null; then
    kill "${BACKEND_PID}" 2>/dev/null || true
    wait "${BACKEND_PID}" 2>/dev/null || true
  fi
}

ensure_process_alive() {
  local pid="$1"
  local log_path="$2"
  local label="$3"

  if ! kill -0 "${pid}" 2>/dev/null; then
    echo "${label} exited before becoming ready."
    cat "${log_path}" || true
    exit 1
  fi
}

trap cleanup EXIT

echo "[1/3] Running backend regression bundle"
"${ROOT_DIR}/scripts/backend_test.sh" \
  tests/test_m35_generation_orchestrator.py \
  tests/test_m41_internal_trend_api.py \
  tests/test_m46_export_payload_compat.py \
  tests/test_m51_generation_checkpoint_restore.py \
  tests/test_m52_generation_checkpoint_state_snapshot.py \
  tests/test_m53_checkpoint_aware_result_builder.py \
  tests/test_m58_rsshub_trend_ingestion.py \
  tests/test_m69_trend_template_summary_fields.py

echo
echo "[2/3] Running frontend production build"
(
  cd "${FRONTEND_DIR}"
  npm run build
)

echo
echo "[3/3] Running Playwright E2E regression"
(
  rm -f "${PLAYWRIGHT_DB_PATH}"

  (
    cd "${BACKEND_DIR}"
    HTTP_PROXY= HTTPS_PROXY= ALL_PROXY= NO_PROXY=127.0.0.1,localhost no_proxy=127.0.0.1,localhost \
      DATABASE_URL="sqlite+pysqlite:////tmp/multi_media_playwright.db" \
      INTERNAL_API_KEY=playwright-internal-key \
      GENERATION_AUTO_START_ENABLED=true \
      ./.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8100
  ) >"${BACKEND_LOG}" 2>&1 &
  BACKEND_PID=$!

  sleep 8
  ensure_process_alive "${BACKEND_PID}" "${BACKEND_LOG}" "Playwright backend"

  (
    cd "${FRONTEND_DIR}"
    HTTP_PROXY= HTTPS_PROXY= ALL_PROXY= NO_PROXY=127.0.0.1,localhost no_proxy=127.0.0.1,localhost \
      NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8100/api/v1 \
      INTERNAL_API_KEY=playwright-internal-key \
      npm run dev -- --hostname 127.0.0.1 --port 3100
  ) >"${FRONTEND_LOG}" 2>&1 &
  FRONTEND_PID=$!

  sleep 8
  ensure_process_alive "${FRONTEND_PID}" "${FRONTEND_LOG}" "Playwright frontend"

  (
    cd "${FRONTEND_DIR}"
    PLAYWRIGHT_USE_EXTERNAL_SERVERS=1 \
      PLAYWRIGHT_BASE_URL=http://127.0.0.1:3100 \
      HTTP_PROXY= HTTPS_PROXY= ALL_PROXY= NO_PROXY=127.0.0.1,localhost no_proxy=127.0.0.1,localhost \
      npm run test:e2e
  )
)

echo
echo "Demo regression passed."
