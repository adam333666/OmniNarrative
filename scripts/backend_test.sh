#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="${ROOT_DIR}/backend"
BACKEND_VENV_DIR="${BACKEND_DIR}/.venv"
DEFAULT_TEST_DB_URL="sqlite+pysqlite:////tmp/multi_media_test_stage.db"

if [[ ! -x "${BACKEND_VENV_DIR}/bin/python" ]]; then
  echo "Missing backend virtual environment at ${BACKEND_VENV_DIR}" >&2
  echo "Run ./scripts/dev_bootstrap.sh first." >&2
  exit 1
fi

export PYTHONPATH="${BACKEND_DIR}"
export DATABASE_URL="${DATABASE_URL:-${DEFAULT_TEST_DB_URL}}"

if [[ "$#" -eq 0 ]]; then
  set -- tests
fi

cd "${BACKEND_DIR}"
exec "${BACKEND_VENV_DIR}/bin/pytest" "$@"
