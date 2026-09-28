#!/usr/bin/env bash
set -euo pipefail
source /mnt/openscience/audit-envs/bio-atac-seq-allele-specific-accessibility/wsl_env.sh

AUDIT=/mnt/openscience/audits/bio-atac-seq-allele-specific-accessibility/reaudit-opt10-20260928
RUN="$AUDIT/runs/real-rasqual"
LOG="$AUDIT/evidence/real-rasqual.txt"
PY=/home/sci/micromamba/envs/atac-core/bin/python
DRIVER="$ASA_CANDIDATE/scripts/run_rasqual_features.py"
rm -rf -- "$RUN"
mkdir -p "$AUDIT/evidence"

"$PY" "$DRIVER" --features "$AUDIT/inputs/rasqual-two-features.tsv" \
  --counts "$RASQUAL_SRC/data/Y.bin" --offsets "$RASQUAL_SRC/data/K.bin" \
  --vcf "$RASQUAL_SRC/data/chr11.gz" --samples 24 --matrix-rows 2 \
  --output-dir "$RUN"

"$PY" - "$RUN" > "$LOG" <<'PY'
import csv, hashlib, math, pathlib, sys
run = pathlib.Path(sys.argv[1])
with (run / "association_summary.tsv").open(encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))
assert rows
indices = {int(row["feature_index"]) for row in rows}
names = {row["feature_name"] for row in rows}
assert indices == {1, 2}, indices
assert names == {"C11orf21", "TSPAN32"}, names
raw = [float(row["p_value"]) for row in rows]
adj = [float(row["adj_p"]) for row in rows]
assert all(math.isfinite(x) and 0.0 <= x <= 1.0 for x in raw + adj)
assert all(a + 1e-18 >= p for p, a in zip(raw, adj))

# Independently recompute BH over the complete two-feature row family.
n = len(raw)
expected = [1.0] * n
running = 1.0
for rank, idx in reversed(list(enumerate(sorted(range(n), key=raw.__getitem__), start=1))):
    running = min(running, raw[idx] * n / rank)
    expected[idx] = running
assert all(abs(a - b) <= 1e-14 for a, b in zip(adj, expected))
print(f"rasqual_rows={n}")
print(f"feature1_rows={sum(int(row['feature_index']) == 1 for row in rows)}")
print(f"feature2_rows={sum(int(row['feature_index']) == 2 for row in rows)}")
print(f"min_raw_p={min(raw):.12g}")
print(f"min_adj_p={min(adj):.12g}")
print("two_feature_indices=PASS")
print("finite_probability_range=PASS")
print("complete_family_bh_recomputation=PASS")
print(f"association_summary_sha256={hashlib.sha256((run / 'association_summary.tsv').read_bytes()).hexdigest()}")
PY

set +e
"$PY" "$DRIVER" --features "$AUDIT/inputs/rasqual-two-features.tsv" \
  --counts "$RASQUAL_SRC/data/Y.bin" --offsets "$RASQUAL_SRC/data/K.bin" \
  --vcf "$RASQUAL_SRC/data/chr11.gz" --samples 24 --matrix-rows 2 \
  --output-dir "$RUN" > "$RUN.reuse.stdout" 2> "$RUN.reuse.stderr"
reuse_rc=$?
set -e
test "$reuse_rc" -eq 2
grep -q 'output directory already exists' "$RUN.reuse.stderr"
echo 'output_reuse_refusal=PASS' >> "$LOG"
echo "rasqual_commit=$(git -C "$RASQUAL_SRC" rev-parse HEAD)" >> "$LOG"
echo 'real_rasqual_reaudit=PASS' >> "$LOG"
cat "$LOG"
