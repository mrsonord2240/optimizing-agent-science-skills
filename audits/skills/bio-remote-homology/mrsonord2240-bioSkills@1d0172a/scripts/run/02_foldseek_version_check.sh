#!/bin/bash
# Regression: SKILL.md's fixed Required-Setup verification line for Foldseek.
set -e
echo "=== New (fixed) command ==="
foldseek 2>&1 | grep -i "^foldseek Version"
echo "exit=$?"
echo
echo "=== Old (broken) command, for contrast ==="
set +e
foldseek --version
echo "exit=$?"
