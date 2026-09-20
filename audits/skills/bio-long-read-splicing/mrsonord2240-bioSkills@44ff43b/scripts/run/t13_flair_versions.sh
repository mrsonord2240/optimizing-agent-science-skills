#!/bin/bash
# Which FLAIR release still accepts the SKILL's `flair correct --genome ... --shortread ...`? Download wheels/sdists only (no install) and read the argparse spec.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
W=/tmp/flair_versions; rm -rf $W; mkdir -p $W; cd $W
micromamba run -n as-lr pip index versions flair-brookslab 2>&1 | head -3
for v in 2.0.0 2.1.0 2.2.0; do
  micromamba run -n as-lr pip download flair-brookslab==$v --no-deps -d $W/$v > $W/dl_$v.log 2>&1 || { echo "$v: download failed: $(tail -1 $W/dl_$v.log)"; continue; }
  f=$(ls $W/$v/* | head -1); echo "== $v ($f)"
  mkdir -p $W/x$v; cd $W/x$v
  case $f in *.whl) unzip -q -o $f ;; *.tar.gz) tar xzf $f ;; esac
  grep -rhn -E "'--genome'|\"--genome\"|'--shortread'|\"--shortread\"|--junction_tab|--junction_bed" --include=*.py . 2>/dev/null | grep -i -E "correct|add_argument" | head -6
  ls -R . | grep -i "flair_correct\|flair.py" | head -3
  cd $W
done
