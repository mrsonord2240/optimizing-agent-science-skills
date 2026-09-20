#!/bin/bash
D=/home/sci/micromamba/envs/as-core/lib/python3.13/site-packages/RSeQC*
ls -d $D
P=$(ls -d /home/sci/micromamba/envs/as-core/lib/python3.13/site-packages/qcmodule 2>/dev/null); echo "qcmodule: $P"
ls /home/sci/micromamba/envs/as-core/lib/python3.13/site-packages | grep -i -E "rseqc|qcmodule"
ls /home/sci/micromamba/envs/as-core/bin | grep -E "junction|infer"
