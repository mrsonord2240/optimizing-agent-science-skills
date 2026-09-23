#!/usr/bin/env bash
set -euo pipefail
in=''; out=''
while (($#)); do case "$1" in -in) in="$2"; shift 2;; -out) out="$2"; shift 2;; *) shift;; esac; done
cp "$in" "$out"
