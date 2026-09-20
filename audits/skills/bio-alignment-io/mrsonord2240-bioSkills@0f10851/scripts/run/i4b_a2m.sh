#!/bin/bash
# REAL data: hmmbuild on real Pfam PF00042 seed, hmmalign 8 real UniProt globins -> real A2M; HH-suite reformat.pl (WSL env bio) for A3M<->A2M.
D=/mnt/openscience/audits/bio-alignment-io/run/data/a2m; mkdir -p $D; cd $D
P=/mnt/openscience/audit-envs/alignment/public-data/msa
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
hmmbuild --amino pf.hmm $P/PF00042_seed.sto > hmmbuild.log </dev/null; grep -E '^LENG' pf.hmm
hmmalign --amino --outformat A2M pf.hmm $P/globins_uniprot.fasta > globins_hmm.a2m </dev/null
grep -c '>' globins_hmm.a2m
# Pfam seed -> aligned FASTA (dash gaps) -> A3M (first sequence as match reference) -> A2M
sed 's/\./-/g' $P/PF00042_seed.sto >/dev/null
python - <<'PY'
from Bio import AlignIO
a = AlignIO.read('/mnt/openscience/audit-envs/alignment/public-data/msa/PF00042_seed.sto', 'stockholm')
AlignIO.write(a, 'pf.fa', 'fasta')
PY
sed -i '/^>/!s/\./-/g' pf.fa
which reformat.pl hhfilter
reformat.pl fas a3m pf.fa pf.a3m -M first </dev/null >/dev/null 2>&1
reformat.pl a3m a2m pf.a3m pf.a2m </dev/null >/dev/null 2>&1
# first-record pitfall: move record 5 to the top and reformat again
python - <<'PY'
recs=[]; cur=None
for l in open('pf.a3m'):
    if l.startswith('>'): recs.append([l,''])
    else: recs[-1][1]+=l
order=[recs[5]]+[r for i,r in enumerate(recs) if i!=5]
open('pf_reordered.a3m','w').write(''.join(h+s for h,s in order))
PY
reformat.pl a3m a2m pf_reordered.a3m pf_reordered.a2m </dev/null >/dev/null 2>&1
hhfilter -i pf_reordered.a3m -id 100 -o pf_reordered_hhf.a3m </dev/null >/dev/null 2>&1
ls -l
