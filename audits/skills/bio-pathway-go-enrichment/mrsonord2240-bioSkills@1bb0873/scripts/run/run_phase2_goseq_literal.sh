#!/usr/bin/env bash
# Execute the current SKILL.md GOseq fence verbatim after a synthetic DE prelude.
set -euo pipefail

audit_root=/mnt/openscience/audits/bio-pathway-go-enrichment
skill=/mnt/openscience/wt/pathway-go-enrichment/pathway-analysis/go-enrichment/SKILL.md
rscript=/home/sci/openscience-go-audit-20260923/bin/Rscript
{
  cat "$audit_root/run/phase2_goseq_prelude.R"
  printf '\n'
  sed -n '132,174p' "$skill"
  cat <<'RSCRIPT'
stopifnot(nrow(go) > 0L, 'padj' %in% names(go), all(is.finite(go$padj) | is.na(go$padj)))
cat('INPUT6_OK literal_rows=', nrow(go), 'padj=', 'padj' %in% names(go), '\n', sep = '')
RSCRIPT
} | "$rscript" - > "$audit_root/run/phase2_goseq_literal.out" 2>&1
cat "$audit_root/run/phase2_goseq_literal.out"
