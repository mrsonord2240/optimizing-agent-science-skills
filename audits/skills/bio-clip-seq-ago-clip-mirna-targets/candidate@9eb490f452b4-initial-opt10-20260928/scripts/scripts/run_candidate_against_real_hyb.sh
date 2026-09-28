#!/usr/bin/env bash
set -euo pipefail

audit_root=/mnt/openscience/audits/bio-clip-seq-ago-clip-mirna-targets/initial-opt10-20260928
tool_root=/mnt/openscience/audit-envs/bio-clip-seq-ago-clip-mirna-targets
candidate=/mnt/openscience/wt/opt10-ago-clip/skills/bio-clip-seq-ago-clip-mirna-targets
work="$audit_root/work/real-wrapper"

case "$work" in
  "$audit_root"/work/*) ;;
  *) echo "refusing unexpected work path: $work" >&2; exit 70 ;;
esac
rm -rf "$work"
mkdir -p "$work"

export PATH="$tool_root/conda-env/bin:$tool_root/runtime/hyb/bin:/usr/bin:/bin"
export HYB_HOME="$tool_root/runtime/hyb"
cd "$work"

set +e
bash "$candidate/scripts/run_chimeric_eclip.sh" \
  "$tool_root/runtime/hyb/data/fastq/testdata.txt" \
  "$tool_root/work/wrapper/inputs/mir.fa" \
  "$tool_root/work/wrapper/inputs/mrna.fa" \
  "$tool_root/work/wrapper/inputs/expressed.tsv" \
  exact_prefix \
  > "$audit_root/evidence/real-wrapper.stdout" \
  2> "$audit_root/evidence/real-wrapper.stderr"
status=$?
set -e

{
  printf 'wrapper_exit=%s\n' "$status"
  printf 'created_files:\n'
  find "$work" -maxdepth 1 -type f -printf '%f\t%s bytes\n' | LC_ALL=C sort
  printf 'derived_line_counts:\n'
  for file in exact_prefix_mrna_chimeras.tsv exact_prefix_expressed_chimeras.tsv exact_prefix_mirna_target_counts.tsv; do
    if [[ -f "$file" ]]; then
      printf '%s\t%s\n' "$file" "$(wc -l < "$file")"
    else
      printf '%s\tMISSING\n' "$file"
    fi
  done
} > "$audit_root/evidence/real-wrapper-summary.txt"

test "$status" -eq 0
test -s "$tool_root/work/real-hyb/official_test_comp_hOH7_hybrids_ua.hyb"
test ! -s exact_prefix_mrna_chimeras.tsv
test ! -s exact_prefix_expressed_chimeras.tsv
test ! -s exact_prefix_mirna_target_counts.tsv
