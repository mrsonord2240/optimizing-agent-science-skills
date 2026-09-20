#!/bin/bash
# sourced by every input script. Runs inside WSL `science` via wsl_run.sh (env alignment-files on PATH).
export RUN=/mnt/openscience/audits/bio-alignment-sorting/run
export PD=/mnt/openscience/audit-envs/alignment-files/public-data
export DATA=$RUN/data
export SKILLDIR=$RUN/skill
export WORK=$RUN/work
mkdir -p "$WORK"
PASSN=0; FAILN=0
# check "label" <shell-test-command...>  -> prints PASS/FAIL, counts
check() {
  local label="$1"; shift
  if "$@" >/dev/null 2>&1; then echo "  [PASS] $label"; PASSN=$((PASSN+1)); else echo "  [FAIL] $label"; FAILN=$((FAILN+1)); fi
}
# eq "label" A B -> string equality
eq() {
  if [ "$2" = "$3" ]; then echo "  [PASS] $1 ($2)"; PASSN=$((PASSN+1)); else echo "  [FAIL] $1 (got '$2' expected '$3')"; FAILN=$((FAILN+1)); fi
}
so() { samtools view -H "$1" | grep -a '^@HD' | head -1; }
# order-independent record digest (headers excluded)
recmd5() { samtools view "$1" | sort | md5sum | cut -c1-12; }
nrec() { samtools view -c "$1"; }
summary() { echo "== assertions: PASS=$PASSN FAIL=$FAILN =="; }
