#!/usr/bin/env bash
set -u

root=/mnt/openscience/audit-envs/bio-clinical-biostatistics-adaptive-designs
rscript="$root/conda-env/bin/Rscript"
candidate=/mnt/openscience/wt/opt10-adaptive-designs/skills/bio-clinical-biostatistics-adaptive-designs
mkdir -p "$root/evidence" "$root/work/full-script"
summary="$root/evidence/candidate-section-status.tsv"
printf 'section\texit_code\tclassification\n' > "$summary"

for section in $(seq 1 10); do
  log="$root/evidence/section-$(printf '%02d' "$section").log"
  json="$root/evidence/section-$(printf '%02d' "$section").json"
  timeout 600 "$rscript" "$root/tools/run_candidate_section.R" "$section" "$json" > "$log" 2>&1
  code=$?
  classification=$("$rscript" -e "x<-jsonlite::read_json('$json'); cat(x\$status)" 2>/dev/null || printf 'NO_JSON')
  printf '%s\t%s\t%s\n' "$section" "$code" "$classification" >> "$summary"
done

cd "$root/work/full-script" || exit 70
timeout 600 "$rscript" "$candidate/scripts/adaptive_designs.R" > "$root/evidence/full-script.log" 2>&1
code=$?
printf '%s\n' "$code" > "$root/evidence/full-script.exit-code"
exit 0
