#!/bin/bash
# usage: bash wenv.sh <env> <cmd...>   (Git Bash) -> runs inside WSL micromamba env, cwd = run/
e=$1; shift
MSYS2_ARG_CONV_EXCL='*' wsl.exe -d science -- bash -lc "cd /mnt/openscience/audits/bio-splice-variant-prediction/run && export PYTHONDONTWRITEBYTECODE=1 && micromamba run -n $e $*"
