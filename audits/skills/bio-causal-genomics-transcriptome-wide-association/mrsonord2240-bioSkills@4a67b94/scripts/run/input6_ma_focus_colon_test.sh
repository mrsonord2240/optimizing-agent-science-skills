#!/bin/bash
# Input 6 (MA-FOCUS scope-boundary check): confirm whether the Skill's documented colon-separated
# multi-ancestry gwas/ref/weights syntax actually works against installed pyfocus 0.802.
# Result: pyfocus's OWN source (twas-venv/Scripts/focus, lines ~877/905/927) does
# args.gwas.split(":"), args.ref.split(":"), args.weights.split(":") -- i.e. colon IS the real
# separator, matching the Skill's docs -- even though --help text incorrectly says "semicolon".
# BUT on Windows, splitting on ":" also splits the drive-letter colon in an absolute path
# (F:/...), so a real 2-population colon-joined path is mis-parsed as 4 populations.
cd "F:/OpenScience/audit-envs/mendelian-randomization-analyst"
D6="F:/OpenScience/audits/bio-causal-genomics-transcriptome-wide-association/data/focus_ma"
mkdir -p "$D6"
touch "$D6/eur.sumstats.gz" "$D6/eas.sumstats.gz"
./twas-venv/Scripts/python.exe twas-venv/Scripts/focus finemap \
  "$D6/eur.sumstats.gz:$D6/eas.sumstats.gz" \
  "dummy_ref_eur:dummy_ref_eas" \
  "dummy_wgt_eur.db:dummy_wgt_eas.db" \
  --p-threshold 5e-8 --out "$D6/colon_test"
