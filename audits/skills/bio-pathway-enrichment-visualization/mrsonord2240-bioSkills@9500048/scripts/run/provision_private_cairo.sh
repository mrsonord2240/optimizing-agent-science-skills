#!/usr/bin/env bash
set -euo pipefail
prefix=/home/sci/.local/share/openscience-pathway-enrichment-r-20260923-deps
mkdir -p "$prefix/debs" "$prefix/cairo"
cd "$prefix/debs"
apt download libcairo2-dev
deb=$(ls libcairo2-dev_*.deb | tail -1)
dpkg-deb -x "$deb" "$prefix/cairo"
test -f "$prefix/cairo/usr/lib/x86_64-linux-gnu/pkgconfig/cairo.pc"
test -f "$prefix/cairo/usr/include/cairo/cairo.h"
printf 'private_cairo_ready=%s\n' "$prefix"
