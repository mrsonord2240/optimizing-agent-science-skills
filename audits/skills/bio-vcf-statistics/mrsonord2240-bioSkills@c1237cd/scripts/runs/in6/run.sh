#!/bin/bash
# Input 6 (NEW, re-audit 2026-09-15, Edge): "Our cohort VCF was read-backed phased, so hets are written 0|1 or 1|0. Run your
# per-sample het allele-balance check and tell me whether any sample looks contaminated."
# Builds a SYNTHETIC phased copy of data/cohort.vcf (each 0/1 alternately written 0|1 and 1|0; AD unchanged) and compares the
# post-fix SKILL.md one-liner with an independent Python parse that counts every het genotype.
set -uo pipefail
source ../env.sh
S=../../data
cat > phase.py <<'EOF'
import sys
k = 0
out = open('phased.vcf', 'w', newline='\n')
for line in open(sys.argv[1]):
    if line.startswith('#'):
        out.write(line); continue
    f = line.rstrip('\n').split('\t')
    gi = f[8].split(':').index('GT')
    for j in range(9, len(f)):
        p = f[j].split(':')
        if p[gi] == '0/1':
            p[gi] = '0|1' if k % 2 == 0 else '1|0'; k += 1
        f[j] = ':'.join(p)
    out.write('\t'.join(f) + '\n')
EOF
cat > ab_indep.py <<'EOF'
import sys, collections
s = collections.defaultdict(float); n = collections.Counter()
for line in open(sys.argv[1]):
    if line.startswith('##'): continue
    f = line.rstrip('\n').split('\t')
    if line.startswith('#'): names = f[9:]; continue
    keys = f[8].split(':'); gi, ai = keys.index('GT'), keys.index('AD')
    for name, v in zip(names, f[9:]):
        p = v.split(':')
        gt = p[gi].replace('|', '/')
        if gt in ('0/1', '1/0') and len(p) > ai and p[ai] != '.':
            r, a = (int(x) for x in p[ai].split(',')[:2])
            if r + a > 0: s[name] += a / (r + a); n[name] += 1
for k in sorted(n): print(f"{k}\tmean het AB: {s[k]/n[k]:.3f} (n={n[k]})")
EOF
$PY phase.py $S/cohort.vcf; bgzip -c phased.vcf > phased.vcf.gz; bcftools index -f phased.vcf.gz
echo "GT codes in phased copy: $(bcftools query -f '[%GT\n]' phased.vcf.gz | tr -d '\r' | sort | uniq -c | tr '\n' ' ')"
echo "== SKILL.md one-liner (post-fix) verbatim, phased copy =="
bcftools query -f '[%SAMPLE\t%GT\t%AD\n]' phased.vcf.gz | \
    awk -F'\t' '($2=="0/1" || $2=="0|1") {split($3,a,","); d=a[1]+a[2]; if (d>0) {s[$1]+=a[2]/d; n[$1]++}}
        END {for (k in s) printf "%s\tmean het AB: %.3f (n=%d)\n", k, s[k]/n[k], n[k]}' | sort
echo "== independent Python parse, phased copy (0/1, 0|1, 1|0 all counted) =="
$PY ab_indep.py phased.vcf
echo "== SKILL.md one-liner on the unphased original (for reference) =="
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -f cohort.vcf.gz
bcftools query -f '[%SAMPLE\t%GT\t%AD\n]' cohort.vcf.gz | \
    awk -F'\t' '($2=="0/1" || $2=="0|1") {split($3,a,","); d=a[1]+a[2]; if (d>0) {s[$1]+=a[2]/d; n[$1]++}}
        END {for (k in s) printf "%s\tmean het AB: %.3f (n=%d)\n", k, s[k]/n[k], n[k]}' | sort
