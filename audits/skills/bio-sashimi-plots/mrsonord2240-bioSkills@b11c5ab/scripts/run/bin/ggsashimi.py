#!/bin/bash
# PATH shim so the Skill's bare `ggsashimi.py` resolves to the GitHub clone run in the ggplot2 3.4.4 env (the Skill's pin).
# GGENV=as-viz-gg35 / as-viz overrides the env for the ggplot2 bisect.
exec micromamba run -n ${GGENV:-as-viz-gg34} python /mnt/openscience/audit-envs/alternative-splicing/tools/src/ggsashimi/ggsashimi.py "$@"
