#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="${ROOT_DIR}/frontend"
BACKEND_DIR="${ROOT_DIR}/backend"
BACKEND_VENV_DIR="${BACKEND_DIR}/.venv"

copy_example_if_missing() {
  local example_file="$1"
  local target_file="$2"

  if [[ -f "${target_file}" ]]; then
    echo "Already present: ${target_file}"
    return
  fi

  cp "${example_file}" "${target_file}"
  echo "Created ${target_file} from ${example_file}"
}

ensure_command() {
  local command_name="$1"
  if ! command -v "${command_name}" >/dev/null 2>&1; then
    echo "Missing required command: ${command_name}" >&2
    exit 1
  fi
}

echo "Preparing local development environment for multi-media"

ensure_command npm
ensure_command python3

copy_example_if_missing "${ROOT_DIR}/.env.example" "${ROOT_DIR}/.env"
copy_example_if_missing "${BACKEND_DIR}/.env.example" "${BACKEND_DIR}/.env"
copy_example_if_missing "${FRONTEND_DIR}/.env.local.example" "${FRONTEND_DIR}/.env.local"

echo
echo "Installing frontend dependencies"
(
  cd "${FRONTEND_DIR}"
  npm install
)

echo
echo "Preparing backend virtual environment"
if [[ ! -d "${BACKEND_VENV_DIR}" ]]; then
  python3 -m venv "${BACKEND_VENV_DIR}"
  echo "Created ${BACKEND_VENV_DIR}"
else
  echo "Already present: ${BACKEND_VENV_DIR}"
fi

echo
echo "Installing backend dependencies"
"${BACKEND_VENV_DIR}/bin/pip" install --upgrade pip
"${BACKEND_VENV_DIR}/bin/pip" install -e "${BACKEND_DIR}[dev]"

cat <<'EOF'

Bootstrap complete.

Next steps:
1. Start PostgreSQL locally or run: docker compose -f deploy/docker-compose.yml up --build
2. Start backend:
   cd backend && .venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
3. Start frontend:
   cd frontend && npm run dev
4. Verify the main flow:
   API_BASE_URL=http://127.0.0.1:8000/api/v1 ./scripts/smoke_test.sh
5. Run backend regression tests through the project virtual environment:
   ./scripts/backend_test.sh
EOF
