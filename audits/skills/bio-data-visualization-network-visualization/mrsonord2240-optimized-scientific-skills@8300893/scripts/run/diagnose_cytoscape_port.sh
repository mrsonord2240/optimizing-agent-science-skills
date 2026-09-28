#!/bin/bash
set -euo pipefail
echo "listener:"
ss -ltnp | grep ':1234' || true
echo "http probe:"
curl --max-time 2 -sv localhost:1234/v1 2>&1 || true
