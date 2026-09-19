#!/bin/bash
# Input 3 (Edge) -- "sequence-only Foldseek via ProstT5" request naturally starts with SKILL.md's own
# Required Setup verification block. Testing that one line independently (ProstT5 weights + AFDB
# themselves are multi-GB, out of audit scope per TOOLS.md -- not re-downloaded here).
set -u
echo "=== SKILL.md 'Required Setup' verification line, verbatim ==="
echo '$ foldseek --version   # Foldseek 9+'
foldseek --version
echo "exit code: $?"
