#!/bin/bash
# Run a python script against live Ensembl BioMart with retry-with-backoff, per the audit
# brief's instruction not to conclude anything from a single attempt (Ensembl is documented
# as intermittently 500/429/outage-page flaky in this env's TOOLS.md). Retries on 429/500/503
# and connection errors; does NOT retry on AssertionError (a real logic failure).
PY="F:/OpenScience/audit-envs/database-access/Scripts/python.exe"
SCRIPT="$1"
OUT="$2"
MAX_TRIES=4
DELAYS=(5 15 30 60)

for i in $(seq 0 $((MAX_TRIES-1))); do
  echo "=== Attempt $((i+1))/$MAX_TRIES: $SCRIPT ===" >> "$OUT"
  cd "F:/OpenScience/audits/bio-biomart-queries/run"
  PYTHONIOENCODING=utf-8 "$PY" "$SCRIPT" >> "$OUT" 2>&1
  RC=$?
  if [ $RC -eq 0 ]; then
    echo "=== SUCCEEDED on attempt $((i+1)) ===" >> "$OUT"
    exit 0
  fi
  if grep -qE "429 Client Error|500 Server Error|503 Server Error|ConnectionError|ReadTimeout|ConnectTimeout" "$OUT"; then
    echo "=== Attempt $((i+1)) hit live-service flakiness, retrying after ${DELAYS[$i]}s ===" >> "$OUT"
    sleep "${DELAYS[$i]}"
    continue
  else
    echo "=== Attempt $((i+1)) failed with a non-retryable error, stopping ===" >> "$OUT"
    exit $RC
  fi
done
echo "=== ALL $MAX_TRIES ATTEMPTS EXHAUSTED (live-service flakiness) ===" >> "$OUT"
exit 1
