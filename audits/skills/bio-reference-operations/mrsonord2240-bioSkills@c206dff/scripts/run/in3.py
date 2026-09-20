#!/usr/bin/env python
"""INPUT 3 (Edge): "My BAM says chr22, my reference says 22 (or the length/sequence differs) -- detect it, fix it,
and make CRAM work offline."  Contig-name / length / M5 identity, reheader, CRAM -T / REF_PATH / REF_CACHE,
seq_cache_populate.pl, and the factual tables in SKILL.md (GRCh38 flavours, contig naming)."""
import os, shutil, sys, re
sys.path.insert(0, '/mnt/openscience/audits/bio-reference-operations/run')
from auditlib import *
import pysam

D = f'{W}/work/in3'
shutil.rmtree(D, ignore_errors=True)
os.makedirs(D)
R = f'{W}/data/real'
shutil.copy(f'{R}/genome.fasta', f'{D}/hs.fa')
shutil.copy(f'{R}/test.paired_end.sorted.bam', f'{D}/h.bam')
shutil.copy(f'{R}/test.paired_end.sorted.bam.bai', f'{D}/h.bam.bai') if os.path.exists(f'{R}/test.paired_end.sorted.bam.bai') else sh('samtools index h.bam', D)
shutil.copy(f'{R}/test.paired_end.sorted.cram', f'{D}/real.cram')
S = parse_fasta(f'{D}/hs.fa')
open(f'{D}/hs_num.fa', 'w').write('>22\n' + '\n'.join(S['chr22'][i:i + 60] for i in range(0, len(S['chr22']), 60)) + '\n')

# ---------- 1. the Skill's own detection commands (SKILL.md 119-120) on a mismatching pair
rc, o, e = sh("samtools view -H h.bam | grep '^@SQ' | head -3; echo ---; samtools dict hs_num.fa | head -3", D)
print(o)
bam_sn = re.findall(r'SN:(\S+)', o.split('---')[0])
ref_sn = re.findall(r'SN:(\S+)', o.split('---')[1])
check('detection commands (SKILL 119-120) expose the mismatch: BAM contig "chr22" vs reference "22"', bam_sn == ['chr22'] and ref_sn == ['22'], (bam_sn, ref_sn))

# ---------- 2. "the silent killer": what really happens with each consumer
rc0, o0, e0 = sh('samtools mpileup -f hs.fa h.bam | wc -l', D)
ref_lines = int(o0.strip())
print('baseline mpileup lines with matching ref:', ref_lines)
rc, o, e = sh('samtools mpileup -f hs_num.fa h.bam 2>&1 | head -5; echo "pipe-rc=${PIPESTATUS[0]}"', D)
print('samtools mpileup w/ mismatched ref ->', o.strip()[:400])
mp_rc = int(re.search(r'pipe-rc=(\d+)', o).group(1))
mp_cnt = len([l for l in o.splitlines() if l and not l.startswith('[') and not l.startswith('pipe-rc')])
check('samtools mpileup with chr22-vs-22 mismatch: loud (non-zero rc or error text) rather than silent-empty', mp_rc != 0 or 'fail' in o.lower() or 'error' in o.lower(), f'rc={mp_rc}, out={o[:200]!r}')
rc, o, e = sh('bcftools mpileup -f hs_num.fa h.bam 2>&1 | grep -v "^##" | head -4; echo "rc=${PIPESTATUS[0]}"', D)
print('bcftools mpileup w/ mismatched ref ->', o.strip()[:400])
rc, o, e = sh('samtools consensus -T hs_num.fa h.bam 2>&1 | head -3; echo "rc=${PIPESTATUS[0]}"', D)
print('samtools consensus -T mismatched ref ->', o.strip()[:300])
rc, o, e = sh('samtools calmd h.bam hs_num.fa 2>&1 | head -2 | cut -c1-200; echo "rc=${PIPESTATUS[0]}"', D)
print('samtools calmd mismatched ref ->', o.strip()[:300])
try:
    pysam.FastaFile(f'{D}/hs_num.fa').fetch('chr22', 0, 10)
    pyres = 'no error'
except Exception as ex:
    pyres = repr(ex)
print('pysam fetch chr22 from ref named 22 ->', pyres)
check('pysam FastaFile.fetch("chr22") on a reference named "22" raises (KeyError)', 'KeyError' in pyres, pyres)
sh('samtools dict hs_num.fa -o hs_num.dict; samtools faidx hs_num.fa', D)
rc, o, e = sh("picard ValidateSamFile I=h.bam R=hs_num.fa MODE=SUMMARY 2>&1 | grep -E 'ERROR:|No errors'", D)
print('Picard ValidateSamFile vs hs_num.fa ->', o.strip()[:600])
check('Picard ValidateSamFile flags the chr22/22 dictionary mismatch (ERROR count > 0)', 'ERROR:' in o and 'No errors' not in o, o[:200])
rc, o, e = sh('gatk HaplotypeCaller -R hs_num.fa -I h.bam -L 22:1952-2100 -O x.vcf 2>&1 | grep -i -E "error|dictionar|contig" | head -3', D)
print('GATK HaplotypeCaller vs hs_num.fa ->', o.strip()[:600])
check('GATK HaplotypeCaller reports incompatible contigs (loud USER ERROR)', 'USER ERROR' in o or 'contig' in o.lower(), o[:200])

# ---------- 3. "for BAM there is no clean conversion -- re-align" (SKILL 123) -> test samtools reheader
rc, o, e = sh("samtools view -H h.bam | sed 's/SN:chr22/SN:22/' > h22.hdr; samtools reheader h22.hdr h.bam > h22.bam; samtools index h22.bam; samtools view -H h22.bam | grep '^@SQ'", D)
check('samtools reheader renamed @SQ chr22 -> 22 (BAM header only rewritten)', o.strip().split('\t')[1] == 'SN:22', o.strip())
a = sh("samtools view h.bam | awk -F'\t' -v OFS='\t' '{if($3==\"chr22\")$3=\"22\"; if($7==\"chr22\")$7=\"22\"; print}' | md5sum", D)[1].split()[0]
b = sh("samtools view h22.bam | md5sum", D)[1].split()[0]
check('all 5644 records identical after reheader except RNAME (record-stream md5 equal)', a == b, (a, b))
p1 = sh("samtools mpileup -f hs.fa h.bam 2>/dev/null | cut -f2-", D)[1]
p2 = sh("samtools mpileup -f hs_num.fa h22.bam 2>/dev/null | cut -f2-", D)[1]
check('mpileup (chr22 BAM+chr22 ref) == mpileup (22 BAM+22 ref) columns 2-6, %d lines' % len(p1.splitlines()), p1 == p2 and len(p1) > 1000)
rc, o, e = sh("picard ValidateSamFile I=h22.bam R=hs_num.fa MODE=SUMMARY 2>&1 | grep -E 'No errors|ERROR:'", D)
reh_ok = ('No errors found' in o)
check('Picard ValidateSamFile: reheadered BAM vs reference "22": No errors found', reh_ok, o.strip())
check('=> SKILL claim "for BAM there is no clean conversion -- re-align" is refuted: reheader gave identical records, identical pileup, and a validating BAM', reh_ok and a == b and p1 == p2)

# synthetic chr -> Ensembl style incl. chrM -> MT
sy = f'{W}/data/synthetic'
shutil.copy(f'{sy}/synth_chr.bam', f'{D}/s.bam'); shutil.copy(f'{sy}/synth_numeric.fa', f'{D}/s_num.fa')
rc, o, e = sh("samtools view -H s.bam | sed -e 's/SN:chrM/SN:MT/' -e 's/SN:chr/SN:/' > s.hdr; samtools reheader s.hdr s.bam > s_num.bam; samtools index s_num.bam; samtools dict s_num.fa -o s_num.dict; picard ValidateSamFile I=s_num.bam R=s_num.fa MODE=SUMMARY IGNORE=MISSING_READ_GROUP 2>&1 | grep -E 'No errors|ERROR:|Error Type'; samtools view -c s_num.bam 1:1-5000", D)
print(o.strip())
check('synthetic BAM chr1/chr2/chrM -> 1/2/MT via reheader validates against Ensembl-style reference', 'ERROR:' not in o and ('Error Type' in o or 'No errors' in o) and o.strip().splitlines()[-1] == '305', o.strip()[-120:])
# VCF path the Skill DOES describe
rc, o, e = sh("bcftools mpileup -f hs.fa h.bam 2>/dev/null | bcftools call -mv -Ov 2>/dev/null > v.vcf; grep -vc '^#' v.vcf; printf 'chr22\\t22\\n' > map.txt; bcftools annotate --rename-chrs map.txt v.vcf 2>/dev/null | grep -v '^#' | cut -f1 | sort -u", D)
print('bcftools annotate --rename-chrs ->', o.strip().replace('\n', ' | '))
check('bcftools annotate --rename-chrs works for VCF (SKILL 123) : contig chr22 -> 22', o.strip().splitlines()[-1] == '22', o.strip())

# ---------- 4. CRAM offline: -T, REF_PATH, REF_CACHE, M5.
# NOTE: `samtools view -c` does not decode bases, so it neither needs the reference nor checks M5. Full decode is used below.
# Every step gets its own EMPTY REF_CACHE dir because htslib writes each -T reference it uses into the cache.
def env(tag, path='/nonexistent/%2s/%2s/%s'):
    return f'env REF_PATH={path} REF_CACHE=$PWD/rc_{tag}/%2s/%2s/%s '


def norm(sam):
    """canonical form: fixed columns + sorted optional tags (CRAM re-orders tags)"""
    out = []
    for l in sam.splitlines():
        f = l.split('\t')
        out.append('\t'.join(f[:11]) + '\t' + '\t'.join(sorted(f[11:])))
    return out


rc, o, e = sh('samtools view -C -T hs.fa h.bam -o h.cram; samtools view -H h.cram | grep "^@SQ"', D)
print(o.strip())
m5 = re.search(r'M5:(\w+)', o).group(1)
dm5 = re.search(r'M5:(\w+)', sh('samtools dict hs.fa', D)[1]).group(1)
check('CRAM header @SQ M5 == samtools dict M5 == md5(uppercase seq) (1922b52e...)', m5 == dm5 == md5(S['chr22'].upper()) == '1922b52e1af6977302717072ebaca0a1', (m5, dm5))
# (a) -c does not need the reference at all
os.rename(f'{D}/hs.fa', f'{D}/hs.fa.bak')
for f in ('hs.fa.fai',):
    if os.path.exists(f'{D}/{f}'):
        os.rename(f'{D}/{f}', f'{D}/{f}.bak')
rc, o, e = sh(env('a') + 'samtools view -c h.cram', D)
check('OBSERVATION: `samtools view -c cram` succeeds with NO reference (5644) -- count-only never decodes bases, so it is not a valid test of "CRAM needs the reference"', rc == 0 and o.strip() == '5644', o.strip())
# (b) full decode without reference
rc, o, e = sh(env('b') + 'samtools view h.cram | wc -l', D)
rc_b = sh(env('b') + 'samtools view h.cram >/dev/null', D)
print('full decode, no -T, unreachable REF_PATH, empty cache ->', rc_b[0], rc_b[2].strip()[:300])
check('full CRAM decode without a reachable reference fails (rc != 0) with a message naming the reference/M5', rc_b[0] != 0 and ('reference' in rc_b[2].lower() or 'md5' in rc_b[2].lower()), rc_b[2].strip()[:200])
rcr = sh(env('b2') + 'samtools view real.cram >/dev/null', D)
check('real nf-core CRAM (UR points nowhere) without -T: fails (rc != 0)', rcr[0] != 0, rcr[2].strip()[:200])
os.rename(f'{D}/hs.fa.bak', f'{D}/hs.fa')
# (c) -T decode, record-level comparison with the source BAM
rc, o, e = sh(env('c') + 'samtools view -T hs.fa h.cram', D)
cram_sam = o
bam_sam = sh('samtools view h.bam', D)[1]
check('CRAM decode with -T hs.fa (usage-guide 232): 5644 records, every record equals the source BAM (fixed columns + tag set)', len(cram_sam.splitlines()) == 5644 and norm(cram_sam) == norm(bam_sam), len(cram_sam.splitlines()))
rc, o, e = sh(env('c2') + 'samtools view -T hs.fa real.cram | wc -l', D)
check('real nf-core CRAM decodes with -T hs.fa: 5644 records', o.strip() == '5644', o.strip() + e[:150])
# (d) M5: reference with same name+length but one base different
mut = list(S['chr22']); i0 = 3000
mut[i0] = 'A' if mut[i0] != 'A' else 'C'
open(f'{D}/mut.fa', 'w').write('>chr22\n' + '\n'.join(''.join(mut)[i:i + 60] for i in range(0, len(mut), 60)) + '\n')
mm5 = re.search(r'M5:(\w+)', sh('samtools dict mut.fa', D)[1]).group(1)
check('one-base-different reference has a different M5 (same name and LN) -> M5 is the identity check', mm5 != dm5, (mm5, dm5))
r = sh(env('d') + 'samtools view -T mut.fa h.cram >/dev/null', D)
print('CRAM full decode against the 1-base-different reference ->', r[0], r[2].strip()[:300])
check('CRAM enforces M5 match on read-back (SKILL 95): full decode with mutated ref fails with an MD5 error', r[0] != 0 and ('md5' in r[2].lower() or 'M5' in r[2]), r[2].strip()[:200])
r = sh('samtools view -T mut.fa h.bam | wc -l', D)
check('BAM has no M5 check: same mutated ref is accepted for a BAM (5644 records) -> the M5 protection is CRAM-only', r[1].strip() == '5644')
# (e) seq_cache_populate.pl -root (SKILL 313) and offline decode via REF_PATH / REF_CACHE
os.makedirs(f'{D}/cache', exist_ok=True)
rc, o, e = sh('seq_cache_populate.pl -root $PWD/cache hs.fa 2>&1 | tail -3; find cache -type f | head', D)
print('seq_cache_populate ->', o.strip()[:400])
check('seq_cache_populate.pl -root <dir> ref.fa populates <dir>/19/22/b52e1af6977302717072ebaca0a1 (the M5 path)', 'cache/19/22/b52e1af6977302717072ebaca0a1' in o, o.strip()[-120:])
os.rename(f'{D}/hs.fa', f'{D}/hs.fa.bak')
r1 = sh('env REF_PATH=$PWD/cache/%2s/%2s/%s REF_CACHE=$PWD/rc_e1/%2s/%2s/%s samtools view h.cram | wc -l', D)
check('offline full decode via REF_PATH=<cache>/%2s/%2s/%s, no -T, no network: 5644 records', r1[1].strip() == '5644', r1[1].strip() + r1[2][:200])
r2 = sh('env REF_PATH=/nonexistent/%2s/%2s/%s REF_CACHE=$PWD/cache/%2s/%2s/%s samtools view h.cram | wc -l', D)
print('REF_CACHE=<populated dir> with REF_PATH unreachable ->', r2[1].strip(), r2[2].strip()[:200])
check('offline full decode via REF_CACHE=<populated dir> only (the SKILL step-3 comment: "pre-populate CRAM REF_CACHE"): 5644 records', r2[1].strip() == '5644', r2[1].strip() + r2[2][:200])
r3 = sh('env REF_PATH=$PWD/cache/%2s/%2s/%s REF_CACHE=$PWD/rc_e3/%2s/%2s/%s samtools view real.cram | wc -l', D)
check('real nf-core CRAM (no usable UR) decodes offline from the populated cache alone: 5644', r3[1].strip() == '5644', r3[1].strip() + r3[2][:200])
os.rename(f'{D}/hs.fa.bak', f'{D}/hs.fa')

# ---------- 5. real length/M5 mismatch: 1000G BAM vs padded chr20 FASTA
G = f'{W}/data/real/g1000'
shutil.copy(f'{G}/HG00349.chr20_1400000-1500000.bam', f'{D}/g.bam'); shutil.copy(f'{G}/chr20_padded_1500000.fa', f'{D}/g.fa')
rc, o, e = sh("samtools view -H g.bam | grep -P '^@SQ\\tSN:chr20\\t'; samtools dict g.fa | grep chr20", D)
print(o)
lines = o.strip().splitlines()
bl = int(re.search(r'LN:(\d+)', lines[0]).group(1)); fl = int(re.search(r'LN:(\d+)', lines[1]).group(1))
bm = re.search(r'M5:(\w+)', lines[0]); fm = re.search(r'M5:(\w+)', lines[1]).group(1)
check('1000G BAM header chr20 LN=64444167 vs FASTA LN=1500000: lengths differ', bl == 64444167 and fl == 1500000, (bl, fl))
check('1000G BAM header carries M5 for chr20 and it differs from the FASTA M5 (names equal, identity differs)', bm is not None and bm.group(1) != fm, (bm.group(1) if bm else None, fm))
sh('samtools dict g.fa -o g.dict', D)
rc, o, e = sh('picard ValidateSamFile I=g.bam R=g.fa MODE=SUMMARY 2>&1 | grep -E "No errors|ERROR|mismatch|Mismatch" | head -4', D)
print('Picard vs padded FASTA ->', o.strip()[:500])
check('Picard ValidateSamFile catches the 1000G length/dictionary mismatch (ERROR count > 0)', 'ERROR' in o and 'No errors' not in o, o.strip()[:200])

# ---------- 6. factual tables in SKILL.md checked against public sources fetched 2026-09-20 (ncbi/ folder)
rep = [l.split('\t') for l in open(f'{W}/ncbi/GRCh38_report.txt').read().splitlines() if l and not l.startswith('#')]
row1 = [r for r in rep if r[0] == '1'][0]
head = open(f'{W}/ncbi/genomic_fna_head.txt').read().strip()
print('NCBI RefSeq chr1: sequence name in the genomic FASTA =', head[:14], '; UCSC-style name only in report column 10 =', row1[9])
check('SKILL table row "NCBI RefSeq (recent): chr1 / chrM" -- the RefSeq FASTA names contigs NC_000001.11 / NC_012920.1, not chr1/chrM', head.startswith('>NC_000001.11') and row1[6] == 'NC_000001.11', head[:40])
fai = [l.split('\t')[0] for l in open(f'{W}/ncbi/1kg.fai').read().splitlines()]
n_alt = sum(1 for n in fai if n.endswith('_alt')); n_hla = sum(1 for n in fai if n.startswith('HLA-')); n_decoy = sum(1 for n in fai if 'decoy' in n)
print('1000G GRCh38 reference (GRCh38_full_analysis_set_plus_decoy_hla): contigs', len(fai), 'alt', n_alt, 'HLA', n_hla, 'decoy', n_decoy, 'chrEBV' in fai)
check('SKILL row "1000G analysis set: ALT no, HLA no" contradicts the 1000G FTP reference itself (261 _alt contigs, 525 HLA contigs, decoy, EBV)', n_alt > 0 and n_hla > 0 and 'chrEBV' in fai, (n_alt, n_hla))
readme = open(f'{W}/ncbi/README_1000G.txt').read()
check('the 1000G file IS the bwakit hs38DH-style set (README: unpacked from bwakit-0.7.12) -> SKILL lists 1000G and hs38DH as different flavours', 'bwakit' in readme)
gb = open(f'{D}/g.bam','rb').read(0)
hdr = sh('samtools view -H g.bam', D)[1]
check('local 1000G BAM header (real data) confirms ALT + HLA + EBV contigs exist in the 1000G flavour', '_alt' in hdr and 'HLA-' in hdr and 'chrEBV' in hdr)

summary()
