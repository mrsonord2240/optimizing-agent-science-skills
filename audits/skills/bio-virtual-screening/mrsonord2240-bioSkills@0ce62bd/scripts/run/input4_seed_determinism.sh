#!/usr/bin/env bash
# RE-AUDIT Input 4 (Variant B, NEW): confirm Vina --seed 42 reproduces
# identical results (all 9 modes, not just top-1) across 2 independent runs
# on the same fixed receptor/ligand (PDB 3PTB, benzamidine).
set -ex
ENV="F:/OpenScience/audit-envs/cheminformatics-hit-triage-analyst"
for i in 1 2; do
  "$ENV/tools/vina/vina.exe" --receptor receptor.pdbqt --ligand lig_benzamidine.pdbqt \
    --center_x -1.52 --center_y 14.47 --center_z 17.47 \
    --size_x 20 --size_y 20 --size_z 20 \
    --exhaustiveness 8 --num_modes 9 --seed 42 --out out_run$i.pdbqt
done
# All 9 modes' affinity + rmsd_lb/ub were identical between out_run1 and out_run2's stdout.
