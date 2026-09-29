#!/usr/bin/env bash
set -euo pipefail
tooling=/mnt/openscience/audit-envs/bio-clip-seq-ago-clip-mirna-targets
runtime="$tooling/runtime/hyb"
export PATH="$tooling/conda-env/bin:$runtime/bin:/usr/bin:/bin"
printf 'user=%s\n' "$(id -un)"
printf 'WSL_INTEROP=%s\n' "${WSL_INTEROP-unset}"
printf '\n/mounts:\n'
findmnt -rn -o TARGET,SOURCE,FSTYPE,OPTIONS /mnt/openscience
if findmnt -rn -o TARGET /mnt/f; then exit 70; else printf '/mnt/f=unmounted\n'; fi
printf '\nversions:\n'
"$tooling/conda-env/bin/python" --version
"$tooling/conda-env/bin/bowtie2" --version | head -1
"$tooling/conda-env/bin/samtools" --version | head -1
"$tooling/conda-env/bin/bedtools" --version
"$tooling/conda-env/bin/umi_tools" --version
"$tooling/conda-env/bin/cutadapt" --version
perl -e 'print "Perl $^V\n"'
make --version | head -1
printf 'hyb_commit=%s\n' '028ab6371ce793ca5e86f475fce1f2cc6ad3c677'
printf 'lock_sha256=%s\n' "$(sha256sum "$tooling/environment-explicit.lock" | cut -d' ' -f1)"
printf 'fingerprint_sha256=%s\n' "$(sha256sum "$tooling/environment-fingerprint.json" | cut -d' ' -f1)"
