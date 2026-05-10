#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SAMPLE_DIR="${ROOT_DIR}/docs/testing/evaluation_samples"

if [[ ! -d "${SAMPLE_DIR}" ]]; then
  echo "Missing evaluation sample directory: ${SAMPLE_DIR}" >&2
  exit 1
fi

for sample in "${SAMPLE_DIR}"/*.json; do
  sample_name="$(basename "${sample}" .json)"
  echo
  echo "===== Running evaluation sample: ${sample_name} ====="
  SMOKE_TEST_LABEL="${sample_name}" \
  SMOKE_TEST_REQUEST_FILE="${sample}" \
  "${ROOT_DIR}/scripts/smoke_test.sh"
done

echo
echo "Evaluation sample pack passed."
