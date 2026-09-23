#!/usr/bin/env bash
# Executes the two fresh Phase-2 inputs. Saved for reproducibility.
set -euo pipefail
cd /mnt/openscience/audits/bio-sam-bam-basics/run
bash fresh/fresh_9_featurecounts_tags.sh > out/fresh_9_featurecounts_tags.txt 2>&1
python -u fresh/fresh_10_fetch_regions.py > out/fresh_10_fetch_regions.txt 2>&1
cat out/fresh_9_featurecounts_tags.txt
cat out/fresh_10_fetch_regions.txt
