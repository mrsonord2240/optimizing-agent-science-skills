#!/usr/bin/env python
"""Small extra checks: pysam FastaFile without a .fai (SKILL 25: "auto-uses .fai"), determinism of samtools consensus
(Skill Veto T3), and the example script's behaviour with a read-only directory / spaces in the path."""
import os, shutil, sys
sys.path.insert(0, '/mnt/openscience/audits/bio-reference-operations/run')
from auditlib import *
import pysam

D = f'{W}/work/in7'
shutil.rmtree(D, ignore_errors=True)
os.makedirs(D)
shutil.copy(f'{W}/data/synthetic/synth.fa', f'{D}/new.fa')
shutil.copy(f'{W}/data/synthetic/synth_chr.bam', f'{D}/x.bam'); shutil.copy(f'{W}/data/synthetic/synth_chr.bam.bai', f'{D}/x.bam.bai')
check('no .fai yet', not os.path.exists(f'{D}/new.fa.fai'))
with pysam.FastaFile(f'{D}/new.fa') as f:
    s = f.fetch('chr1', 0, 20)
check('pysam.FastaFile on a FASTA WITHOUT .fai works and writes new.fa.fai next to it (SKILL 25 "auto-uses .fai index")', len(s) == 20 and os.path.exists(f'{D}/new.fa.fai'), s)

# determinism: 3 identical runs of default + Bayesian ambig consensus
h = []
for i in range(3):
    sh('samtools consensus --ambig x.bam -o r%d.fa' % i, D)
    h.append(md5(open(f'{D}/r{i}.fa').read()))
check('samtools consensus --ambig is deterministic across 3 runs (identical md5)', len(set(h)) == 1, h[0])

# example script with a path containing a space
os.makedirs(f'{D}/my ref', exist_ok=True)
shutil.copy(f'{D}/new.fa', f'{D}/my ref/r.fa')
rc, o, e = sh('bash %s/skill/examples/prepare_reference.sh "my ref/r.fa"' % W, D)
check('prepare_reference.sh handles a path with a space (quoted expansions)', rc == 0 and os.path.exists(f'{D}/my ref/r.dict') and os.path.exists(f'{D}/my ref/r.chrom.sizes'), (rc, e[:150]))
# read-only dir
os.makedirs(f'{D}/ro', exist_ok=True)
shutil.copy(f'{D}/new.fa', f'{D}/ro/r.fa')
os.chmod(f'{D}/ro', 0o555)
rc, o, e = sh('bash %s/skill/examples/prepare_reference.sh ro/r.fa; echo "exit=$?"' % W, D)
print('read-only dir ->', o.strip()[-120:].replace('\n', ' | '), '|', e.strip()[:200])
check('prepare_reference.sh in a read-only directory stops at the first failing step with a non-zero exit (set -e)', 'exit=0' not in o, (o[-60:], e[:120]))
os.chmod(f'{D}/ro', 0o755)
# the script never checks whether samtools is installed / fai already exists (idempotent overwrite) -> re-run overwrites dict silently
rc, o, e = sh('bash %s/skill/examples/prepare_reference.sh "my ref/r.fa" > /dev/null; echo "exit=$?"' % W, D)
check('re-running prepare_reference.sh over existing outputs succeeds (idempotent overwrite)', 'exit=0' in o, o.strip())
summary()
