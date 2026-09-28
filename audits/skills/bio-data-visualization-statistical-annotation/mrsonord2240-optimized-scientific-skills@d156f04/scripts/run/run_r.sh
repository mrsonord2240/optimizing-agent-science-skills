#!/usr/bin/env bash
# Normalize the Git-Bash locale before entering the shared R wrapper.  Without
# this, R 4.4.3 emits four C.UTF-8 startup warnings and returns status 1 even
# after a completed script on this Windows host.
export LC_ALL=C
export LANG=C
exec /f/OpenScience/audit-envs/data-visualization/r.sh "$@"
