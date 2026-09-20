# source inside WSL: source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
export RUN=/mnt/openscience/audits/bio-sashimi-plots/run
export PYTHONIOENCODING=utf-8
export SRC=$AS/tools/src
# ggsashimi wrapper pinned to the Skill's ggplot2 (3.4.4) env; gg41 = the old default env (ggplot2 4.0.3)
ggs()   { micromamba run -n as-viz-gg34 python $SRC/ggsashimi/ggsashimi.py "$@"; }
ggs35() { micromamba run -n as-viz-gg35 python $SRC/ggsashimi/ggsashimi.py "$@"; }
ggs40() { micromamba run -n as-viz python $SRC/ggsashimi/ggsashimi.py "$@"; }
