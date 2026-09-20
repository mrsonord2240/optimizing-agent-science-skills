#!/bin/bash
mkdir -p /mnt/openscience/audits/bio-splicing-qc/run/rseqc_src
cp /home/sci/micromamba/envs/as-core/bin/junction_annotation.py /home/sci/micromamba/envs/as-core/bin/junction_saturation.py /home/sci/micromamba/envs/as-core/bin/infer_experiment.py /mnt/openscience/audits/bio-splicing-qc/run/rseqc_src/
cp -r /home/sci/micromamba/envs/as-core/lib/python3.13/site-packages/qcmodule /mnt/openscience/audits/bio-splicing-qc/run/rseqc_src/
find /mnt/openscience/audits/bio-splicing-qc/run/rseqc_src -name __pycache__ -exec rm -rf {} + 
ls -R /mnt/openscience/audits/bio-splicing-qc/run/rseqc_src | head -30
