#!/bin/bash
f=/home/sci/micromamba/envs/bio-atac-seq-footprinting-scprinter/lib/python3.11/site-packages/scprinter
sed -n 20,100p $f/preprocessing.py; echo ------; sed -n 140,160p $f/preprocessing.py; echo -----; sed -n 440,490p $f/utils.py
echo ---- detect_shift; grep -n "def detect_shift" -A60 $f/*.py | head -90
