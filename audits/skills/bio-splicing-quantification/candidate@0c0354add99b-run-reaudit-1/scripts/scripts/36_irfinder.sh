#!/bin/bash
# SQ-05: IRFinder commands exactly as references/intron-retention-and-microexons.md states them (1.3.1), via the staged wrapper (no PATH workaround).
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
AS=/mnt/openscience/audit-envs/alternative-splicing
O=/mnt/openscience/audits/bio-splicing-quantification/run-reaudit-1/out/irf; R=$AS/public-data/rnasplice/fastq
rm -rf $O; mkdir -p $O; cd $O
IRFinder --version 2>&1 | head -2
echo "== literal OLD syntax (initial finding): IRFinder FastQ -r REF -d out x.fq"
IRFinder FastQ -r $O/ref -d $O/old $R/ERR188383_chrX_1.fastq.gz > old.log 2>&1; echo "old-syntax rc=$?"; tail -2 old.log | cut -c1-160
echo "== BuildRefFromSTARRef (documented)"
( time IRFinder -m BuildRefFromSTARRef -r $O/ref -x $AS/logs/smoke_irfinder/starref ) > build.log 2>&1; echo "build rc=$?"; tail -4 build.log | cut -c1-200; ls $O/ref
echo "== FastQ SE"
IRFinder -m FastQ -r $O/ref -t 8 -d $O/se $R/ERR188383_chrX_1.fastq.gz > se.log 2>&1; echo "se rc=$?"
echo "== FastQ PE"
IRFinder -m FastQ -r $O/ref -t 8 -d $O/pe $R/ERR188383_chrX_1.fastq.gz $R/ERR188383_chrX_2.fastq.gz > pe.log 2>&1; echo "pe rc=$?"
micromamba run -n as-core python - <<PY
import pandas as pd, numpy as np
se=pd.read_csv('$O/se/IRFinder-IR-nondir.txt',sep='\t',comment='#'); pe=pd.read_csv('$O/pe/IRFinder-IR-nondir.txt',sep='\t',comment='#')
print('cols', list(se.columns)[:14]); print('rows se/pe', len(se), len(pe))
print('IRratio range se', se.IRratio.min(), se.IRratio.max(), 'pe', pe.IRratio.min(), pe.IRratio.max())
print('IRratio r SE vs PE (same sample)', np.corrcoef(se.IRratio.fillna(0), pe.IRratio.fillna(0))[0,1])
print('introns IRratio>0.1 se/pe', int((se.IRratio>0.1).sum()), int((pe.IRratio>0.1).sum()))
b=pd.read_csv('/mnt/openscience/audits/bio-splicing-quantification/run-tooling-delta-1/out/fixed/se/IRFinder-IR-nondir.txt',sep='\t',comment='#')
print('IRratio r vs delta-pass SE (independent rebuild)', np.corrcoef(se.IRratio.fillna(0), b.IRratio.fillna(0))[0,1], 'rows', len(b))
PY
