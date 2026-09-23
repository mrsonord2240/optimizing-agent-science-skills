#!/usr/bin/env bash
# Capture package-version state without modifying the shared audit environment.
# Usage: bash snapshot_env.sh <r-wrapper> <python> <output-dir> <tag>
set -euo pipefail
r_wrapper="$1"
python_bin="$2"
out_dir="$3"
tag="$4"
mkdir -p "$out_dir"
"$python_bin" --version >"$out_dir/${tag}_python_version.txt"
"$python_bin" -m pip freeze | LC_ALL=C sort >"$out_dir/${tag}_pip_freeze.txt"
# Do not start an outer R process for a metadata query: this Windows R runtime
# can tear down with SIGSEGV after a package metadata call. Read the two
# package DESCRIPTION files that this audit uses; no package is loaded.
r_lib="$(dirname "$r_wrapper")/R-lib"
for pkg in IHW qvalue; do
  printf '%s=' "$pkg"
  grep '^Version:' "$r_lib/$pkg/DESCRIPTION"
done >"$out_dir/${tag}_r_packages.txt"
if find "$r_lib" -name '00LOCK-*' -print -quit | grep -q .; then
  echo 'unexpected R install lock present' >&2
  exit 1
fi
