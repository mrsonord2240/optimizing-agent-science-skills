#!/usr/bin/env python
"""INPUT 2 (Variant A): "Extract sequence for chr1:1000-2000, several regions, a whole chromosome, the reverse
complement, a subset reference" -- samtools faidx + pysam FastaFile, vs an independent slice of the FASTA text.
Also the documented failure modes / troubleshooting text of the usage-guide."""
import os, shutil, sys, re, io, contextlib
sys.path.insert(0, '/mnt/openscience/audits/bio-reference-operations/run')
from auditlib import *
import pysam

D = f'{W}/work/in2'
shutil.rmtree(D, ignore_errors=True)
os.makedirs(D)
for f in ('synth.fa',):
    shutil.copy(f'{W}/data/synthetic/{f}', f'{D}/ref.fa')            # 3 contigs, 80-col, soft-masked, N run
shutil.copy(f'{W}/data/real/genome.fasta', f'{D}/hs.fa')
shutil.copy(f'{W}/data/real/sars/MN908947.3.fasta', f'{D}/sars.fa')
shutil.copy(f'{W}/data/real/g1000/chr20_padded_1500000.fa', f'{D}/g1000.fa')
ENS = '/mnt/openscience/audit-envs/alignment-files/public-data/1000g/chr20_1400001-1500000.seq.txt'

S = parse_fasta(f'{D}/ref.fa')
print('contigs', {k: len(v) for k, v in S.items()})

# ---- 1. no .fai present: does a region query build the index by itself? (usage-guide says "Index the reference first")
check('no .fai before first query', not os.path.exists(f'{D}/ref.fa.fai'))
rc, o, e = sh('samtools faidx ref.fa chr1:1000-2000 > r1.fa', D)
check('faidx with a region and NO prior index still succeeds and creates ref.fa.fai (auto-index)', rc == 0 and os.path.exists(f'{D}/ref.fa.fai'), f'rc={rc}')

# ---- 2. SKILL.md line 44: samtools faidx reference.fa chr1:1000-2000  (1-based, inclusive)
recs = fa_records(open(f'{D}/r1.fa').read())
exp = S['chr1'][999:2000]
check('faidx chr1:1000-2000: header is ">chr1:1000-2000"', recs[0][0] == 'chr1:1000-2000', recs[0][0])
check('faidx chr1:1000-2000: 1001 bases = independent 1-based inclusive slice S[999:2000]', recs[0][1] == exp and len(exp) == 1001)
lines = open(f'{D}/r1.fa').read().splitlines()
print('observation: faidx output line width for an 80-col source =', max(len(l) for l in lines[1:]), '(help text says -n default 60; not a Skill claim)')

# case preservation, precisely on the soft-masked stretch (0-based 1000..1299 lowercase)
rc, o, e = sh('samtools faidx ref.fa chr1:1001-1300', D)
rec = fa_records(o)[0][1]
check('soft-masked lowercase preserved by faidx (chr1:1001-1300 all lowercase)', rec.islower() and rec == S['chr1'][1000:1300])

# ---- 3. multi region, whole chromosome, output to file
rc, o, e = sh('samtools faidx ref.fa chr1:1000-2000 chr2:3000-3007', D)
r = fa_records(o)
check('two regions -> two records with independent slices', len(r) == 2 and r[0][1] == S['chr1'][999:2000] and r[1][1] == S['chr2'][2999:3007], [x[0] for x in r])
rc, o, e = sh('samtools faidx ref.fa chr2', D)
r = fa_records(o)
check('whole chromosome chr2 equals independent sequence (header ">chr2", description dropped)', r[0][0] == 'chr2' and r[0][1] == S['chr2'], r[0][0])

# ---- 4. reverse complement (-i): header suffix
rc, o, e = sh('samtools faidx -i ref.fa chr1:1000-2000', D)
r = fa_records(o)
check('faidx -i: sequence = reverse complement of independent slice', r[0][1] == revcomp(S['chr1'][999:2000]))
check('faidx -i: header becomes "chr1:1000-2000/rc" (not documented in SKILL.md; --mark-strand no removes it)', r[0][0] == 'chr1:1000-2000/rc', r[0][0])
rc, o, e = sh('samtools faidx -i --mark-strand no ref.fa chr1:1000-2000', D)
check('--mark-strand no gives plain header', fa_records(o)[0][0] == 'chr1:1000-2000')

# ---- 5. pysam 0-based half-open equivalence (SKILL.md 209-212; usage-guide 129-132)
with pysam.FastaFile(f'{D}/ref.fa') as ref:
    seq = ref.fetch('chr1', 999, 2000)
    check('pysam fetch("chr1",999,2000) == samtools faidx chr1:1000-2000 == independent slice', seq == S['chr1'][999:2000] and len(seq) == 1001)
    check('pysam get_reference_length / nreferences (usage-guide 138-143) match', ref.nreferences == 3 and [ref.get_reference_length(n) for n in ref.references] == [5000, 3007, 1000])
    # printed header in usage-guide "Extract Multiple Regions" is >{chrom}:{start+1}-{end}
    check('pysam fetch with out-of-range end silently clips (no error)', len(ref.fetch('chr2', 3000, 9999)) == 7)
    try:
        ref.fetch('chr2', 5000, 15000)
        emp = True
    except Exception as ex:
        emp = repr(ex)
    check('pysam fetch fully outside the contig returns empty string, no error', emp is True)

# ---- 6. usage-guide "Extract Multiple Regions" verbatim, regions from the guide (chr1 0-10000, chr2 5000-15000)
src = open(f'{W}/snippets/ug_10_python.txt').read().replace("'reference.fa'", f"'{D}/ref.fa'")
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(src, {})
out = buf.getvalue().splitlines()
heads = [l for l in out if l.startswith('>')]
print('ug_10 headers printed:', heads, '| total sequence lines:', len(out) - len(heads))
seqchars = sum(len(l) for l in out if not l.startswith('>'))
check('ug_10 verbatim: header claims chr1:1-10000 but only 5000 bases printed (no bounds check on a 5 kb contig)', heads[0] == '>chr1:1-10000' and seqchars == 5000, seqchars)
check('ug_10 verbatim: chr2 5000-15000 (outside 3007 bp contig) prints a header with an EMPTY record', heads[1] == '>chr2:5001-15000')

# ---- 7. real data: human chr22 slice, SARS-CoV-2, and Ensembl ground truth for chr20 (independent external source)
H = parse_fasta(f'{D}/hs.fa')
rc, o, e = sh('samtools faidx hs.fa chr22:1952-2100', D)
check('real human slice chr22:1952-2100 == independent slice', fa_records(o)[0][1] == H['chr22'][1951:2100])
SC = parse_fasta(f'{D}/sars.fa')
rc, o, e = sh('samtools faidx sars.fa MN908947.3:21563-25384', D)
r = fa_records(o)[0]
check('SARS-CoV-2 S gene MN908947.3:21563-25384 = 3822 nt, starts ATG, ends TAA', len(r[1]) == 3822 and r[1].startswith('ATGTTTGTTTTTCTTG') and r[1].endswith('TAA'), r[1][:20] + '..' + r[1][-6:])
ens = open(ENS).read().strip().upper()      # Ensembl REST: 20:1400001..1500000 (1-based inclusive) = 100000 bases
rc, o, e = sh('samtools faidx g1000.fa chr20:1400001-1500000', D)
check('1000G-slice reference: chr20:1400001-1500000 from padded FASTA == Ensembl REST sequence (external truth, 100000 bp)', fa_records(o)[0][1].upper() == ens and len(ens) == 100000)
rc, o, e = sh('samtools faidx g1000.fa chr20:1400001-1400100', D)
check('chr20:1400001-1400100 (first 100 real bases) == Ensembl first 100', fa_records(o)[0][1].upper() == ens[:100])
rc, o, e = sh('samtools faidx g1000.fa chr20:1400000-1400001', D)
check('one base before the real sequence is N (padding) -- 1-based edge check', fa_records(o)[0][1][0] == 'N' and fa_records(o)[0][1][1].upper() == ens[0])

# ---- 8. SKILL "Common Operations": extract chromosome, subset, chrom sizes
rc, o, e = sh('samtools faidx ref.fa chr1 > chr1.fa; samtools faidx chr1.fa; cut -f1,2 chr1.fa.fai', D)
check('extract chr1 -> chr1.fa -> index; fai length 5000', o.strip() == 'chr1\t5000', o)
check('extracted chr1.fa sequence equals source chr1 (case preserved, N run intact)', parse_fasta(f'{D}/chr1.fa')['chr1'] == S['chr1'])
# subset where one requested contig does not exist (SKILL uses chr1 chr2 chr3; usage-guide lists chr1..chrM)
rc, o, e = sh('samtools faidx ref.fa chr1 chr2 chr3 > subset.fa; echo "faidx rc=$?"; samtools faidx subset.fa; echo "index rc=$?"; grep -c ">" subset.fa', D)
print('subset output:', o.strip().replace('\n', ' | '), '| stderr:', e.strip())
check('subset with a missing contig (chr3): faidx exits NON-zero and stderr names the failure', 'faidx rc=0' not in o and 'Failed to fetch sequence in chr3' in e, o + e)
check('...and the follow-up documented command (faidx subset.fa) ALSO fails (subset.fa holds an empty >chr3 record, 3 headers): failure is loud, not silent', 'index rc=1' in o and o.strip().endswith('3'), o)
rc, o, e = sh('samtools faidx ref.fa chr1 chr2 chr3 chrM -c > subset_c.fa; echo rc=$?; grep ">" subset_c.fa', D)
print('with -c:', o.strip().replace('\n', ' | '), '| stderr:', e.strip())

# ---- 9. troubleshooting text in usage-guide
rc, o, e = sh('samtools faidx nofile.fa chr1', D)
print('missing FASTA ->', rc, e.strip())
check('usage-guide "faidx reference file not found" scenario: real message is fai_build3_core / Could not load fai index (not that title); rc non-zero', rc != 0 and 'No such file' in e, e.strip())
rc, o, e = sh('samtools faidx ref.fa 1:1-100', D)
print('wrong contig name (1 vs chr1) ->', rc, e.strip())
check('contig-name mismatch "1" vs "chr1": faidx fails loudly (rc!=0) with "Failed to fetch sequence in 1" (usage-guide calls it "invalid region")', rc != 0 and 'Failed to fetch sequence in 1' in e, e.strip())
rc, o, e = sh('samtools faidx ref.fa chr1:6000-7000', D)
print('region beyond contig end ->', rc, repr(o[:60]), e.strip())
rc, o, e = sh('samtools faidx ref.fa chr1:4990-6000', D)
print('region overlapping the contig end ->', rc, [len(x[1]) for x in fa_records(o)], e.strip())
check('region overlapping contig end is clipped to contig end (11 bases) with a warning, rc 0', rc == 0 and len(fa_records(o)[0][1]) == 11)
rc, o, e = sh('samtools faidx ref.fa chr1:6000-7000', D)
check('region wholly beyond contig end: rc 0 with an EMPTY record (only a stderr warning)', rc == 0 and fa_records(o)[0][1] == '', e.strip())

# ---- 10. quick reference block from SKILL.md (Check Reference Setup), fetch chr1:1-100 vs independent
rc, o, e = sh('samtools faidx ref.fa chr1:1-100', D)
check('SKILL "Test fetch" chr1:1-100 correct', fa_records(o)[0][1] == S['chr1'][:100])

# ---- 11. a FASTA with a >NNN description line and a "chr1:1000-2000"-style contig name (region-parsing trap)
open(f'{D}/colon.fa', 'w').write('>chr22:16570000-16610000 slice\nACGTACGTACGTACGTACGT\nACGTACGTAC\n')
rc, o, e = sh('samtools faidx colon.fa chr22:16570000-16610000; echo rc=$?; samtools faidx colon.fa chr22:16570000-16610000:1-5; echo rc=$?', D)
print('colon-named contig ->', o.strip().replace('\n', ' | '), '|', e.strip())

summary()
