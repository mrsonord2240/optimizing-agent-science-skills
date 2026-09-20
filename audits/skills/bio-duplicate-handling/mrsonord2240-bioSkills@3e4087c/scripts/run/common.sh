# sourced by every input script (inside WSL, after wsl_env.sh)
export PYTHONIOENCODING=utf-8
export RUN=/mnt/openscience/audits/bio-duplicate-handling/run
export D=$RUN/data
export SK=$RUN/skill_copy
export W=$RUN/work
mkdir -p $W
# the fixer's NEW env (biobambam2, pbmarkdup) is not in TOOLS.md; drive it with micromamba run
extra() { micromamba run -n af-dup-extra "$@"; }
# run the Nth fenced block under an exact heading of the Skill, verbatim
blk() { python $RUN/blocks.py "$SK/SKILL.md" "$@"; }
flagged() { samtools view -c -f 1024 "$1"; }
