#!/usr/bin/env bash
# NEW INPUT 8 (part a) -- "Compute PolyFun per-SNP priors genome-wide using the baseline-LF
# reference, then fine-map this locus with susie_rss prior_weights set from PolyFun output."
# (usage-guide.md "Functional Priors" prompt, SKILL.md "Functional Priors with PolyFun" section.)
#
# This code path was UNTESTED in the pre-fix audit (2026-09-17): "No FINEMAP/SuSiEx/PAINTOR/DAP-G
# binaries or PolyFun venv exist anywhere on this machine ... scored by inspection." PolyFun is
# now installed (git clone omerwe/polyfun, twas-venv) per this audit's TOOLS.md, with its OWN
# bundled real GWAS example data. This is a genuine execution of SKILL.md's exact documented
# command:
#   polyfun.py --compute-h2-L2 --no-partitions --output-prefix ... --sumstats ... \
#       --ref-ld-chr ... --w-ld-chr ...
#
# --sumstats example_data/sumstats.parquet is PolyFun's own bundled real GWAS summary statistics
# (confirmed real, not synthetic: 182,454 genome-wide SNPs; the chr22 subset used below has
# N=383,290, matching TOOLS.md's independently-documented "RBC.sumstats.small.parquet ... real
# published GWAS, red-blood-cell trait" entry for this same PolyFun clone).
#
# TOOLS.md flagged a risk for this run: "polyfun.py calls pd.read_csv(..., delim_whitespace=True)
# in at least 3 places; twas-venv's pandas is 3.0.5, which REMOVED that kwarg (hard TypeError)."
# This --compute-h2-L2 code path does NOT hit that code path (it uses pd.read_table(sep='\s+') and
# pd.read_parquet, not delim_whitespace) -- confirmed by running it end-to-end below without
# modifying twas-venv (no pandas pin needed, no install-lock taken).

set -euo pipefail
cd "/f/OpenScience/audit-envs/mendelian-randomization-analyst/tools/finemapping/polyfun"

PYTHONIOENCODING=utf-8 /f/OpenScience/audit-envs/mendelian-randomization-analyst/twas-venv/Scripts/python.exe \
  polyfun.py --compute-h2-L2 --no-partitions \
  --output-prefix F:/OpenScience/audits/bio-causal-genomics-fine-mapping/run/final-pass-20260923/polyfun_out/testout \
  --sumstats example_data/sumstats.parquet \
  --ref-ld-chr example_data/annotations. \
  --w-ld-chr example_data/weights.
