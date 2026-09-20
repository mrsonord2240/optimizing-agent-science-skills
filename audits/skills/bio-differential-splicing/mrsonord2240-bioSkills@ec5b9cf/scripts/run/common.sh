#!/bin/bash
# Shared paths/handles; source inside WSL `science` (via wsl_run.sh). Never use bare Rscript: every R call goes through micromamba run -n as-rleaf.
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
AS=/mnt/openscience/audit-envs/alternative-splicing
R=/mnt/openscience/audits/bio-differential-splicing/run
P=$AS/public-data/planted
D=$AS/public-data/rnasplice
XB=$AS/public-data/derived/xs_bams
LC=$AS/tools/src/leafcutter
GTFX=$D/reference/genes_chrX.gtf
CORE="micromamba run -n as-core"
RL="micromamba run -n as-rleaf"
SU="micromamba run -n as-suppa"
SH="micromamba run -n as-shiba"
PA="micromamba run -n as-pairadise"
FORK_PROFILE=$AS/tools/pairadise_fork_profile.R
SK=$R/skill
# leafcutter: number of tested clusters (status Success) with p.adjust < 0.05, columns found by header name (the column order differs when a groups file carries covariates)
nsig() { awk -F'\t' 'NR==1{for(i=1;i<=NF;i++){if($i=="status")s=i; if($i=="p.adjust")p=i}} NR>1 && $s=="Success" && $p+0<0.05{n++} END{print n+0}' "$1"; }
ntested() { awk -F'\t' 'NR==1{for(i=1;i<=NF;i++){if($i=="status")s=i}} NR>1 && $s=="Success"{n++} END{print n+0}' "$1"; }
