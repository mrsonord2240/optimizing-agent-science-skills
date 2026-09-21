#!/bin/bash
cd /mnt/openscience/audits/bio-outlier-splicing-detection/run
micromamba run -n as-drop Rscript scripts/21_ae_repro.R /mnt/openscience/audits/bio-outlier-splicing-detection/run/ex_drop/fraser_workdir > logs/22_ae_repro.log 2>&1
grep -n "loaded\|AE,\|PCA q\|Error" logs/22_ae_repro.log | cut -c1-200
