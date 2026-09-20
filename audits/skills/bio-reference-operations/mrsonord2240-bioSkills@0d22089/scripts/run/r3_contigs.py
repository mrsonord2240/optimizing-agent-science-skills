#!/usr/bin/env python
"""INPUT 3 (regression of pre-fix input 3, greatly extended): contig-naming / GRCh38-flavour tables spot-checked against REAL files fetched
2026-09-20 (UCSC chrom.sizes, 1000G fai, Broad fai, hs37d5 fai, NCBI assembly reports + README, Ensembl REST), and the 'Rename Contigs Without
Re-aligning' reheader recipe run on real BAM/CRAM data (chr22 slice; HG00349 1000G BAM with the full hs38DH header)."""
import os, re, shutil, sys, json
sys.path.insert(0, '/mnt/openscience/audits/bio-reference-operations/run')
from auditlib import *
import pysam
N = f'{W}/ncbi'
def rd(p): return open(f'{N}/{p}', encoding='utf-8', errors='replace').read()
def sizes(p): return [l.split('\t')[:2] for l in rd(p).splitlines() if l.strip()]

print('##### A. table spot-checks against real files')
hg38 = sizes('hg38.chrom.sizes'); hg19 = sizes('hg19.chrom.sizes'); k = sizes('1kg.fai'); broad = sizes('broad38.fai'); hs37 = sizes('hs37d5.fai')
d38 = dict(hg38); d19 = dict(hg19)
check('UCSC hg38.fa: 455 contigs, 261 _alt, no chrEBV, chrM 16,569', len(hg38) == 455 and sum(1 for n, _ in hg38 if n.endswith('_alt')) == 261 and 'chrEBV' not in d38 and d38['chrM'] == '16569', (len(hg38), sum(1 for n, _ in hg38 if n.endswith('_alt'))))
check('UCSC hg19: chrM 16,571 bp (NOT 16,569)', d19['chrM'] == '16571' and len(hg19) == 93, d19['chrM'])
kd = dict(k)
alt = sum(1 for n, _ in k if n.endswith('_alt')); dec = sum(1 for n, _ in k if n.endswith('_decoy')); hla = sum(1 for n, _ in k if n.startswith('HLA-'))
check('1000G GRCh38_full_analysis_set_plus_decoy_hla: 3,366 contigs = 261 ALT + 2,385 decoy + 525 HLA + chrEBV present', len(k) == 3366 and alt == 261 and dec == 2385 and hla == 525 and 'chrEBV' in kd, (len(k), alt, dec, hla))
check('Broad Homo_sapiens_assembly38.fasta has the same 3,366 contigs (names+lengths+order) as the 1000G analysis set', [tuple(x) for x in broad] == [tuple(x) for x in k], (len(broad), len(k)))
h37 = dict(hs37)
check('1000G hs37d5: names 1..22,X,Y,MT + GL* + NC_007605 (EBV) + hs37d5 decoy; MT 16,569; chr1 has no "chr" prefix', all(str(i) in h37 for i in range(1, 23)) and 'X' in h37 and 'MT' in h37 and h37['MT'] == '16569' and 'NC_007605' in h37 and 'hs37d5' in h37 and any(n.startswith('GL') for n in h37) and 'chr1' not in h37, len(hs37))
g38 = [l.split('\t') for l in rd('GRCh38_report.txt').splitlines() if not l.startswith('#') and l.strip()]
raw = open(f'{N}/GRCh38_report.txt', 'rb').read()
check('assembly report has CRLF line ends (SKILL: "tab-separated, CRLF line ends")', b'\r\n' in raw)
rows = {r[0]: [c.strip() for c in r] for r in g38}
c1 = rows['1']; cM = rows['MT']
check('GRCh38 report col1/5/7/10 for chr1 = 1 / CM000663.2 / NC_000001.11 / chr1 (SKILL column map)', (c1[0], c1[4], c1[6], c1[9]) == ('1', 'CM000663.2', 'NC_000001.11', 'chr1'), c1[:10])
check('GRCh38 report MT: RefSeq NC_012920.1, UCSC chrM, length 16569', (cM[0], cM[6], cM[9], cM[8]) == ('MT', 'NC_012920.1', 'chrM', '16569'), cM[:10])
check('RefSeq FASTA header of GCF_000001405.40 begins NC_000001.11 (SKILL: RefSeq FASTA has no chr1)', rd('genomic_fna_head.txt').startswith('>NC_000001.11'), rd('genomic_fna_head.txt')[:60])
g37 = [l.split('\t') for l in rd('GRCh37_report.txt').splitlines() if not l.startswith('#') and l.strip()]
r37 = {r[0]: [c.strip() for c in r] for r in g37}
check('GRCh37 report: chr1 = NC_000001.10, MT = NC_012920.1 (16569); SKILL RefSeq GRCh37 row', r37['1'][6] == 'NC_000001.10' and r37['MT'][6] == 'NC_012920.1' and r37['MT'][8] == '16569', (r37['1'][6], r37['MT'][6:9]))
ens = json.load(open(f'{N}/ens_info.json')); ens_names = [x['name'] for x in ens['top_level_region']]
check('Ensembl GRCh38 top-level names: 1..22,X,Y,MT and unlocalized/unplaced as GenBank accessions (KI270757.1); no chr-prefix names', all(x in ens_names for x in [str(i) for i in range(1, 23)] + ['X', 'Y', 'MT', 'KI270757.1']) and not any(n.startswith('chr') for n in ens_names) and len(ens_names) == 194, len(ens_names))
# analysis-set README claims
rm = rd('README_analysis_sets.txt')
check('NCBI README: no_alt set = chromosomes+MT+unlocalized+unplaced+EBV, ALT omitted; full = no_alt + ALT; +hs38d1 adds decoys (SKILL flavour table)', 'alternate locus scaffolds are omitted' in rm and 'contains the alternate locus scaffolds in' in rm and 'human decoy sequences' in rm and 'chrEBV' in rm)
check('NCBI README also says PAR on chrY / centromere duplicates are hard-masked with N in analysis sets (a difference the SKILL table does not list)', 'hard-masked' in rm)
# map line of the SKILL: UCSC -> RefSeq
import subprocess
map_cmd = "grep -v '^#' GRCh38_report.txt | tr -d '\\r' | awk -F'\\t' '$10!=\"na\"{print $10 \"\\t\" $7}' > /tmp/map_ref_audit.tsv; wc -l < /tmp/map_ref_audit.tsv"
rc, o, e = sh(map_cmd, N)
maplines = open('/tmp/map_ref_audit.tsv').read().splitlines(); md = dict(l.split('\t') for l in maplines)
py = {r[9].strip(): r[6].strip() for r in g38 if r[9].strip() != 'na'}
check('SKILL map line (grep|tr|awk) == independent Python parse: same mapping for all rows', md == py and md['chr22'] == 'NC_000022.11' and md['chrM'] == 'NC_012920.1', (len(md), len(py)))
print('    n mapped UCSC->RefSeq rows:', len(md), '(hg38 UCSC contigs:', len(hg38), ')')
check('every hg38.chrom.sizes contig that has a UCSC-style name in the report maps (report is the rename map for _alt/_random/chrUn)', sum(1 for n, _ in hg38 if n in md) >= 450, sum(1 for n, _ in hg38 if n in md))
miss = [n for n, _ in hg38 if n not in md]; print('    hg38.fa contigs NOT in the report map:', miss[:10], len(miss))

print('##### B. reheader recipe on real data')
D = f'{W}/work/r3'; shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
def blk(n): return open(f'{W}/snippets/{n}.txt').read()
b12 = blk('skill_12_bash')
open(f'{D}/skill12.txt', 'w').write(b12)
# B1: hand-written map chr22->22 (first comment of the block), real BAM + renamed reference
shutil.copy(f'{W}/data/real/test.paired_end.sorted.bam', f'{D}/sample.bam'); shutil.copy(f'{W}/data/real/test.paired_end.sorted.bam.bai', f'{D}/sample.bam.bai')
shutil.copy(f'{W}/data/real/genome.fasta', f'{D}/genome.fasta')
with open(f'{D}/map.tsv', 'w') as f: f.write('chr22\t22\n')
awk_line = [l for l in b12.split('\n')]
# run the two lines of the block that build renamed.hdr + reheader + index, verbatim (lines 3-5 of the snippet)
lines = b12.split('\n')
i_start = next(i for i, l in enumerate(lines) if l.startswith('samtools view -H sample.bam | awk'))
i_end = next(i for i, l in enumerate(lines) if l.startswith('samtools reheader'))
recipe = '\n'.join(lines[i_start:i_end + 1])
open(f'{D}/recipe1.sh', 'w').write(recipe + '\n')
rc, o, e = sh('bash recipe1.sh; echo rc=$?', D)
check('SKILL reheader recipe (awk + reheader + index) on the real chr22 BAM: rc 0, renamed.bam + .bai exist', 'rc=0' in o and os.path.exists(f'{D}/renamed.bam') and os.path.exists(f'{D}/renamed.bam.bai'), o + e[:200])
rc, o, e = sh('samtools view -H renamed.bam | grep "^@SQ"', D); check('renamed header @SQ is SN:22 LN:40001', o.strip() == '@SQ\tSN:22\tLN:40001', o)
orig = sh('samtools view sample.bam', D)[1].splitlines(); ren = sh('samtools view renamed.bam', D)[1].splitlines()
def norm(l):
    f = l.split('\t'); f[2] = f[2].replace('chr22', 'X').replace('22', 'X') if f[2] not in ('*',) else f[2]
    if f[6] not in ('=', '*'): f[6] = 'X'
    return '\t'.join(f)
def norm_o(l):
    f = l.split('\t')
    if f[2] != '*': f[2] = 'X'
    if f[6] not in ('=', '*'): f[6] = 'X'
    return '\t'.join(f)
check('renamed.bam: all 5644 records identical to the original except RNAME/RNEXT (independent text compare)', len(orig) == len(ren) == 5644 and [norm_o(l) for l in orig] == [norm_o(l) for l in ren] and all(l.split('\t')[2] in ('22', '*') for l in ren))
mp0 = sh('samtools mpileup -f genome.fasta sample.bam 2>/dev/null | md5sum', D)[1]
# renamed reference
sh("sed '1s/^>chr22/>22/' genome.fasta > genome22.fa; samtools faidx genome22.fa", D)
mp1 = sh('samtools mpileup -f genome22.fa renamed.bam 2>/dev/null | cut -f2- | md5sum; samtools mpileup -f genome.fasta sample.bam 2>/dev/null | cut -f2- | md5sum', D)[1].split()
check('mpileup of renamed.bam vs renamed reference == original (positions/bases identical)', mp1[0] == mp1[2], mp1)
rc, o, e = sh('samtools view -c renamed.bam 22:1952-4700; samtools view -c sample.bam chr22:1952-4700', D); check('region query 22:1952-4700 count == chr22:1952-4700 count (5642)', o.split() == ['5642', '5642'], o)
rc, o, e = sh('picard ValidateSamFile I=renamed.bam R=genome22.fa MODE=SUMMARY 2>&1 | grep -E "No errors found|^ERROR" | head -3', D); check('Picard 3.5.0 ValidateSamFile renamed.bam vs reference named 22: No errors found', 'No errors found' in o, o)
# the Check line of the block (diff ...)
chk = next(l for l in lines if l.startswith('diff <('))
open(f'{D}/chk.sh', 'w').write('#!/bin/bash\n' + chk.replace('ref.fa.fai', 'genome22.fa.fai') + '\n')
rc, o, e = sh('bash chk.sh', D); check('SKILL Check line (diff SN/LN vs fai) prints OK for the matching reference', o.strip() == 'OK', o + e)
# B1b: mismatches must NOT print OK: wrong length, wrong name, different order
open(f'{D}/bad_len.fai', 'w').write('22\t40000\t4\t60\t61\n')
open(f'{D}/bad_name.fai', 'w').write('chr22\t40001\t4\t60\t61\n')
for nm in ('bad_len', 'bad_name'):
    open(f'{D}/chk_{nm}.sh', 'w').write('#!/bin/bash\n' + chk.replace('ref.fa.fai', f'{nm}.fai') + '\n')
    rc, o, e = sh(f'bash chk_{nm}.sh', D); check(f'SKILL Check line does NOT print OK for {nm} (mismatch caught)', 'OK' not in o and o.strip() != '', o[:120])

# B2: HG00349 1000G BAM (full hs38DH header): run the block's map + awk + reheader verbatim with the RefSeq assembly report
G = f'{D}/g'; os.makedirs(G)
shutil.copy(f'{W}/data/real/g1000/HG00349.chr20_1400000-1500000.bam', f'{G}/sample.bam'); shutil.copy(f'{W}/data/real/g1000/HG00349.chr20_1400000-1500000.bam.bai', f'{G}/sample.bam.bai')
shutil.copy(f'{N}/GRCh38_report.txt', f'{G}/GCF_000001405.40_GRCh38.p14_assembly_report.txt')
NL = chr(10); TAB = chr(9)
open(f'{G}/recipe2.sh', 'w').write(NL.join(lines[:i_end + 1]) + NL)     # comment + map line + awk + reheader (block up to the reheader line), VERBATIM
rc, o, e = sh('bash recipe2.sh; echo rc=$?', G)
print('    verbatim block on the full hs38DH header ->', (o + e).strip().replace(NL, ' | ')[:300])
na_map = [l for l in open(f'{G}/map.tsv').read().splitlines() if l.endswith(TAB + 'na')]
check('DEFECT CONFIRMED (check passes when the defect is reproduced): SKILL map line emits old<TAB>na for the 4 contigs with no RefSeq accession, reheader fails on a full hg38 header (Duplicate entry na) and leaves a 0-byte renamed.bam', len(na_map) == 4 and 'rc=1' in o and 'Duplicate entry "na"' in (o + e) and os.path.getsize(f'{G}/renamed.bam') == 0, (na_map, (o + e)[:200]))
# same block with the one-token fix ($7 != "na") to test the rest of the recipe on the real header
fixed = NL.join(lines[:i_end + 1]).replace('$10!="na"{', '$10!="na" && $7!="na"{')
open(f'{G}/recipe2b.sh', 'w').write(fixed + NL)
rc, o, e = sh('bash recipe2b.sh; echo rc=$?', G)
check('with awk filter $7!="na" added, the block runs on the real 1000G BAM (rc 0, renamed.bam written)', 'rc=0' in o and os.path.exists(f'{G}/renamed.bam'), o + e[:200])
hdr0 = [l.split('\t') for l in sh('samtools view -H sample.bam | grep "^@SQ"', G)[1].splitlines()]
hdr1 = [l.split('\t') for l in sh('samtools view -H renamed.bam | grep "^@SQ"', G)[1].splitlines()]
mp = dict(l.split('\t') for l in open(f'{G}/map.tsv').read().splitlines())
n0 = [h[1][3:] for h in hdr0]; n1 = [h[1][3:] for h in hdr1]
exp = [mp.get(n, n) for n in n0]
check('1000G BAM header: 3,366 @SQ before and after; every name mapped through the report map or left unchanged (HLA-*, *_decoy, chrEBV have no RefSeq name)', len(n0) == len(n1) == 3366 and n1 == exp, (len(n0), sum(1 for a, b in zip(n0, n1) if a != b)))
check('lengths and M5 unchanged by reheader for all 3,366 contigs (LN/M5 fields compared as text)', [h[2:] for h in hdr0] == [h[2:] for h in hdr1])
print('    renamed:', sum(1 for a, b in zip(n0, n1) if a != b), 'unchanged:', sum(1 for a, b in zip(n0, n1) if a == b), '| chr20 ->', n1[n0.index('chr20')], '| chrM ->', n1[n0.index('chrM')], '| HLA / decoy / EBV kept:', n1[n0.index('chrEBV')])
o0 = sh('samtools view sample.bam | cut -f1,4-6,8- | md5sum', G)[1]; o1 = sh('samtools view renamed.bam | cut -f1,4-6,8- | md5sum', G)[1]
names = set(sh('samtools view renamed.bam | cut -f3 | sort -u', G)[1].split())
check('1000G renamed.bam: 9601 records, identical apart from RNAME/RNEXT (cut -f1,4-6,8- md5: RNAME and RNEXT excluded), reads now on NC_000020.11', o0 == o1 and sh('samtools view -c renamed.bam', G)[1].strip() == '9601' and 'NC_000020.11' in names, names)
# B3: the sed one-liner on the real hs38DH header
sed = next(l for l in lines if l.startswith('samtools view -H sample.bam | sed'))
open(f'{G}/sed.sh', 'w').write('#!/bin/bash\n' + sed + '\n')
rc, o, e = sh('bash sed.sh; grep "^@SQ" renamed.hdr | cut -f2 | sed "s/SN://"', G)
sq_sed = o.split(); print('    sed one-liner output names (first 5, and a few non-primary):', sq_sed[:3], [n for n in sq_sed if n.startswith('1_KI')][:1], [n for n in sq_sed if n.startswith('Un_')][:1], [n for n in sq_sed if n.startswith('HLA')][:1], [n for n in sq_sed if 'EBV' in n])
prim = [str(i) for i in range(1, 23)] + ['X', 'Y', 'MT']
check('sed one-liner turns chr1..22/X/Y/chrM into Ensembl names 1..22/X/Y/MT for the primary chromosomes', all(p in sq_sed for p in prim))
mangled = [n for n in sq_sed if n not in ens_names and n not in n0]
print('    sed output names that exist in neither Ensembl nor the BAM (mangled non-primary contigs):', len(mangled), mangled[:4])
check('OBSERVATION: sed one-liner on a full hs38DH header also rewrites non-primary contigs (chr1_KI..._alt -> 1_KI..._alt, chrUn_ -> Un_): SKILL says primary chromosomes only', len(mangled) > 0, len(mangled))

# B4: SA/XA claim with a tiny BAM built with pysam
hd = {'HD': {'VN': '1.6', 'SO': 'coordinate'}, 'SQ': [{'SN': 'chr1', 'LN': 1000}, {'SN': 'chr2', 'LN': 800}]}
T = f'{D}/t'; os.makedirs(T)
with pysam.AlignmentFile(f'{T}/sample.bam', 'wb', header=hd) as out:
    a = pysam.AlignedSegment(out.header); a.query_name = 'r1'; a.query_sequence = 'ACGTACGTAC'; a.flag = 0; a.reference_id = 0; a.reference_start = 10
    a.mapping_quality = 60; a.cigartuples = [(0, 10)]; a.query_qualities = pysam.qualitystring_to_array('IIIIIIIIII')
    a.set_tag('SA', 'chr2,100,+,5S5M,60,0;'); a.set_tag('XA', 'chr2,+200,10M,1;'); a.set_tag('OA', 'chr1,11,+,10M,60,0;'); out.write(a)
pysam.index(f'{T}/sample.bam')
open(f'{T}/map.tsv', 'w').write('chr1\t1\nchr2\t2\n')
open(f'{T}/r.sh', 'w').write('\n'.join(lines[i_start:i_end + 1]) + '\nsamtools view renamed.bam | cut -f3,7,12-\nsamtools view -b -x SA -x XA renamed.bam > stripped.bam; samtools view stripped.bam | cut -f3,12-\n')
rc, o, e = sh('bash r.sh', T)
print('    tags after reheader / after -x SA -x XA:', o.strip().replace('\n', ' || '))
check('SKILL claim: SA:Z/XA:Z/OA:Z keep old names after reheader; view -b -x SA -x XA removes SA and XA (OA stays)', 'SA:Z:chr2' in o.split('\n')[0] and 'XA:Z:chr2' in o.split('\n')[0] and 'SA:Z' not in o.split('\n')[1] and 'XA:Z' not in o.split('\n')[1] and 'OA:Z:chr1' in o.split('\n')[1], o)

# B5: CRAM reheader claim
C = f'{D}/c'; os.makedirs(C)
shutil.copy(f'{W}/data/real/test.paired_end.sorted.cram', f'{C}/sample.cram'); shutil.copy(f'{D}/genome.fasta', f'{C}/genome.fasta'); shutil.copy(f'{D}/genome22.fa', f'{C}/genome22.fa'); shutil.copy(f'{D}/genome22.fa.fai', f'{C}/genome22.fa.fai')
shutil.copy(f'{D}/map.tsv', f'{C}/map.tsv')
sh('samtools faidx genome.fasta', C)
rc, o, e = sh('samtools view -T genome.fasta -H sample.cram | awk -F"\\t" -v OFS="\\t" \'NR==FNR{m[$1]=$2; next} /^@SQ/{for(i=2;i<=NF;i++) if($i~/^SN:/){n=substr($i,4); if(n in m) $i="SN:" m[n]}} {print}\' map.tsv - > renamed.hdr; samtools reheader renamed.hdr sample.cram > renamed.cram; echo rc=$?', C)
print('    CRAM reheader stderr:', e.strip()[:200])
check('CRAM reheader runs (rc 0, output written; the SKILL says it may warn Failed to populate reference - no warning here, the nf-core CRAM header carries no M5)', 'rc=0' in o and os.path.exists(f'{C}/renamed.cram'), (o + e)[:250])
a1 = sh('samtools view -T genome22.fa renamed.cram | md5sum', C)[1].split()[0]
a2 = sh('samtools view -T genome.fasta sample.cram | sed "s/\\tchr22\\t/\\t22\\t/" | md5sum', C)[1].split()[0]
n1 = sh('samtools view -T genome22.fa -c renamed.cram', C)[1].strip()
check('renamed CRAM decodes with -T genome22.fa to 5644 records identical to the original (RNAME changed only)', n1 == '5644' and a1 == a2, (n1, a1[:8], a2[:8]))
# B6: CRAM M5 enforcement: mutate one base of the reference, keep the name
ref = parse_fasta(f'{C}/genome.fasta')['chr22']; i = 2500; mut = ref[:i] + ('A' if ref[i].upper() != 'A' else 'C') + ref[i + 1:]
open(f'{C}/mut.fa', 'w').write('>chr22\n' + '\n'.join(mut[j:j + 60] for j in range(0, len(mut), 60)) + '\n')
rc, o, e = sh('samtools faidx mut.fa; samtools view -T mut.fa sample.cram | wc -l', C)
print('    mutated-reference CRAM decode:', rc, o.strip(), e.strip()[:200])
check('SKILL claim "CRAM enforces M5 match on read-back": decode with a reference differing at 1 base fails (MD5 mismatch) instead of silently decoding', 'M5' in e or 'MD5' in e or 'md5' in e or 'mismatch' in e.lower(), e.strip()[:200])
# VCF rename claim
rc, o, e = sh("printf 'chr1\t1\nchr2\t2\nchrM\tMT\n' > vmap.tsv; cp %s/data/synthetic/variants.vcf.gz* . ; bcftools annotate --rename-chrs vmap.tsv variants.vcf.gz | grep -v '^##' | cut -f1,2 | head -8; bcftools annotate --rename-chrs vmap.tsv variants.vcf.gz | grep -c '^##contig=<ID=MT'" % W, T)
check('SKILL: bcftools annotate --rename-chrs map.tsv renames VCF records and ##contig lines (chr1->1, chrM->MT)', o.split()[:4] == ['#CHROM', 'POS', '1', '201'] or ('1	201' in o and o.strip().splitlines()[-1] == '1'), o.replace(chr(10), ' | '))
summary()
