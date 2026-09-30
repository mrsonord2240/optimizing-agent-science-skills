#!/bin/bash
export MAMBA_ROOT_PREFIX=/home/sci/micromamba; MM=/home/sci/.local/bin/micromamba
exec 9>/mnt/openscience/runtime/locks/micromamba-mutate.lock; flock 9
$MM env remove -y -n np-reaudit-nucleoatac 2>&1 | tail -1; [ -d /home/sci/micromamba/envs/np-reaudit-nucleoatac ] && rm -rf /home/sci/micromamba/envs/np-reaudit-nucleoatac
echo gone=$([ -d /home/sci/micromamba/envs/np-reaudit-nucleoatac ] && echo no || echo yes)
