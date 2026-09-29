#!/usr/bin/env bash
set -euo pipefail
ENV=/mnt/openscience/audit-envs/bio-comparative-genomics-ancestral-reconstruction
printf 'user=%s\n' "$(id -un)"
printf 'WSL_INTEROP=%s\n' "${WSL_INTEROP-<unset>}"
if mountpoint -q /mnt/f; then echo 'mnt_f=mounted'; exit 1; else echo 'mnt_f=not-mounted'; fi
"$ENV/conda-env/bin/python" --version
"$ENV/conda-env/bin/iqtree2" --version
"$ENV/conda-env/bin/java" -version 2>&1 | head -n 1
"$ENV/conda-env/bin/Rscript" -e 'cat(R.version.string, "ape", as.character(packageVersion("ape")), "phytools", as.character(packageVersion("phytools")), "geiger", as.character(packageVersion("geiger")), "corHMM", as.character(packageVersion("corHMM")), "OUwie", as.character(packageVersion("OUwie")), "\n")'
sha256sum "$ENV/environment-explicit.lock"
