#!/usr/bin/env python
"""INPUT 2 (regression of pre-fix input 2): faidx region extraction, revcomp, faidx error table, subset recipe, pysam fetch/multi-region
snippets - verbatim SKILL blocks - against an independent slice of the FASTA text, plus external truth (Ensembl REST chr20 bases)."""
import contextlib, io, os, shutil, sys
sys.path.insert(0, '/mnt/openscience/audits/bio-reference-operations/run')
from auditlib import *
import pysam
D = f'{W}/work/r2'; shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
shutil.copy(f'{W}/data/synthetic/synth.fa', f'{D}/ref.fa')        # 3 contigs, widths 80/60/70, soft-masked, N run (pre-fix synthetic ref)
shutil.copy(f'{W}/data/real/genome.fasta', f'{D}/hs.fa'); shutil.copy(f'{W}/data/real/sars/MN908947.3.fasta', f'{D}/sars.fa')
shutil.copy(f'{W}/data/real/g1000/chr20_padded_1500000.fa', f'{D}/g1000.fa')
S = parse_fasta(f'{D}/ref.fa'); print({k: len(v) for k, v in S.items()})
def blk(n): return open(f'{W}/snippets/{n}.txt').read()

# skill_02..06: region, multi region, chromosome, revcomp
rc, o, e = sh('samtools faidx ref.fa chr1:1000-2000', D); r = fa_records(o)
check('SKILL faidx chr1:1000-2000 == independent 1-based inclusive slice (1001 bases), header chr1:1000-2000', r[0][0] == 'chr1:1000-2000' and r[0][1] == S['chr1'][999:2000])
check('faidx auto-indexed (SKILL: builds the .fai itself the first time)', os.path.exists(f'{D}/ref.fa.fai'))
rc, o, e = sh('samtools faidx ref.fa chr1:1001-1300', D)
check('soft-mask case preserved by faidx (chr1:1001-1300 all lowercase)', fa_records(o)[0][1].islower() and fa_records(o)[0][1] == S['chr1'][1000:1300])
rc, o, e = sh('samtools faidx ref.fa chr1:1000-2000 chr2:3000-3007 chr2', D); r = fa_records(o)
check('3 requests -> 3 records equal independent slices', [x[1] for x in r] == [S['chr1'][999:2000], S['chr2'][2999:3007], S['chr2']])
rc, o, e = sh('samtools faidx -i ref.fa chr1:1000-2000', D); r = fa_records(o)
check('SKILL -i: header chr1:1000-2000/rc, seq == revcomp(independent slice)', r[0][0] == 'chr1:1000-2000/rc' and r[0][1] == revcomp(S['chr1'][999:2000]), r[0][0])
rc, o, e = sh('samtools faidx -i --mark-strand no ref.fa chr1:1000-2000', D); r = fa_records(o)
check('SKILL --mark-strand no: plain header, still revcomp', r[0][0] == 'chr1:1000-2000' and r[0][1] == revcomp(S['chr1'][999:2000]))

# faidx Errors table (samtools 1.24)
rc, o, e = sh('samtools faidx ref.fa 22:1-100', D)
check('Errors table row 1: wrong contig name -> rc 1, [faidx] Failed to fetch sequence in 22:1-100', rc == 1 and 'Failed to fetch sequence in 22:1-100' in e, f'rc={rc} {e.strip()}')
rc, o, e = sh('samtools faidx nofile.fa chr1', D)
check('Errors table row 2: missing FASTA -> rc 1, Failed to open the file ... Could not load fai index', rc == 1 and 'Failed to open the file' in e and 'Could not load fai index' in e, f'rc={rc} {e.strip()[:160]}')
rc, o, e = sh('samtools faidx ref.fa chr1:6000-7000', D)
check('Errors table row 3: region beyond contig end -> rc 0, [faidx] Zero length sequence, empty record', rc == 0 and 'Zero length sequence' in e and fa_records(o)[0][1] == '', f'rc={rc} {e.strip()}')
rc, o, e = sh('samtools faidx ref.fa chr1:4990-6000', D)
check('overlapping the contig end -> clipped to 11 bases, rc 0', rc == 0 and len(fa_records(o)[0][1]) == 11, e.strip())
open(f'{D}/desc.fa', 'w').write('>chrX some description here\nACGTACGTAC\n')
rc, o, e = sh('samtools faidx desc.fa >/dev/null; cut -f1 desc.fa.fai', D)
check('SKILL names are the first word of each > line: fai name = chrX', o.strip() == 'chrX', o)
rc, o, e = sh('cat ref.fa.fai', D)
f = o.splitlines()[0].split('\t'); check('FAI columns for chr1: name,len,offset,linebases,linewidth = chr1,5000,offset,80,81', f[0] == 'chr1' and f[1] == '5000' and f[3] == '80' and f[4] == '81', f)

# skill_32 subset recipe: && chain, missing contig, and success case; dict step
os.makedirs(f'{D}/sub1'); shutil.copy(f'{D}/ref.fa', f'{D}/sub1/reference.fa')
script = blk('skill_32_bash')          # chr1 chr2 chr3 (chr3 absent in synth.fa)
open(f'{D}/sub1/sub.sh', 'w').write(script)
rc, o, e = sh('bash sub.sh; echo "chain rc=$?"; ls', f'{D}/sub1')
check('SKILL subset recipe with a missing contig (chr3): chain stops, rc 1, no subset.dict written', 'chain rc=1' in o and 'subset.dict' not in o.split('chain rc=1')[1], o.replace('\n', ' | ') + e.strip()[:120])
os.makedirs(f'{D}/sub2'); shutil.copy(f'{D}/ref.fa', f'{D}/sub2/reference.fa')
open(f'{D}/sub2/sub.sh', 'w').write(script.replace('chr3', 'chrM'))
rc, o, e = sh('bash sub.sh; echo "chain rc=$?"; cat subset.dict | cut -f1-3; cat subset.fa.fai | cut -f1,2', f'{D}/sub2')
check('SKILL subset recipe with existing contigs (chr1 chr2 chrM): rc 0, subset.fa.fai + 3-@SQ subset.dict (5000/3007/1000)', 'chain rc=0' in o and 'LN:5000' in o and 'LN:3007' in o and 'LN:1000' in o and o.count('@SQ') == 3, o.replace('\n', ' | '))
sub = parse_fasta(f'{D}/sub2/subset.fa'); check('subset.fa sequences equal the source contigs (case + N preserved)', sub == {k: S[k] for k in ('chr1', 'chr2', 'chrM')})

# pysam snippets, verbatim: skill_20 (fetch), 21 (lengths), 22 (fetch all), 23 (multi-region)
def run_py(name, ref):
    src = blk(name).replace("'reference.fa'", f"'{ref}'")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): exec(src, {'pysam': pysam})   # SKILL blocks after the first rely on the earlier import pysam
    return buf.getvalue()
o20 = run_py('skill_20_python', f'{D}/ref.fa')
check('SKILL pysam fetch(chr1,999,2000) prints the same 1001 bases as faidx chr1:1000-2000', o20.strip() == S['chr1'][999:2000])
o21 = run_py('skill_21_python', f'{D}/ref.fa'); check('SKILL pysam lengths print 5,000 / 3,007 / 1,000 bp', '5,000 bp' in o21 and '3,007 bp' in o21 and '1,000 bp' in o21, o21.replace('\n', ' | '))
o22 = run_py('skill_22_python', f'{D}/ref.fa'); check('SKILL fetch-all prints 3 records with 100-base previews', o22.count('>') == 3 and S['chr2'][:100] in o22)
o23 = run_py('skill_23_python', f'{D}/ref.fa')
heads = [l for l in o23.splitlines() if l.startswith('>') or l.startswith('skip')]
print('multi-region output headers:', heads)
seq_chars = sum(len(l) for l in o23.splitlines() if not l.startswith('>') and not l.startswith('skip'))
check('SKILL multi-region loop: chr1 clipped to contig end (>chr1:1-5000, 5000 bases), chr2:5001-15000 skipped as outside (no empty record)', heads == ['>chr1:1-5000', 'skip chr2:5001-3007: outside the contig'] and seq_chars == 5000, heads)
with pysam.FastaFile(f'{D}/ref.fa') as ref:
    check('prose claim: fetch truncates at the contig end / returns empty string past it', len(ref.fetch('chr2', 3000, 9999)) == 7 and ref.fetch('chr2', 5000, 15000) == '')

# real data + external truth
H = parse_fasta(f'{D}/hs.fa')
rc, o, e = sh('samtools faidx hs.fa chr22:1952-2100', D); check('real human slice chr22:1952-2100 == independent slice', fa_records(o)[0][1] == H['chr22'][1951:2100])
rc, o, e = sh('samtools faidx sars.fa MN908947.3:21563-25384', D); s = fa_records(o)[0][1]
check('SARS-CoV-2 S gene MN908947.3:21563-25384 is 3822 nt, ATG...TAA (external biological truth)', len(s) == 3822 and s.startswith('ATG') and s.endswith('TAA'), s[:12] + '..' + s[-5:])
ens = open(f'{W}/data/real/g1000/chr20_1400001-1500000.seq.txt').read().strip().upper()
rc, o, e = sh('samtools faidx g1000.fa chr20:1400001-1500000', D); check('chr20:1400001-1500000 == Ensembl REST GRCh38 sequence (100000 bp, external truth)', fa_records(o)[0][1].upper() == ens and len(ens) == 100000)
rc, o, e = sh('samtools faidx ref.fa chr1 > chr1.fa; samtools faidx chr1.fa; cut -f1,2 chr1.fa.fai; cut -f1,2 ref.fa.fai > chrom.sizes; cat chrom.sizes', D)
check('Extract chromosome + Get Chromosome Sizes blocks: chr1 5000; chrom.sizes lists 3 contigs', o.startswith('chr1\t5000\n') and 'chr2\t3007' in o and 'chrM\t1000' in o, o.replace('\n', ' | '))
summary()
