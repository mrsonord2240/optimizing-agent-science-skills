#!/usr/bin/env python3
"""NEW input 10, step 2: assert on GATK 4.6.2.0's own --help (captured by n10_caller_docs.sh) what it filters by default, and compare with the
SKILL.md rationale for the germline (HaplotypeCaller) and somatic (Mutect2) assay rows. Everything else in the assay table stays unverified
(callers not installed), which this script states rather than hides."""
import re, sys
from lib import check, finish

D, SK = sys.argv[1], sys.argv[2]
txt = open(f'{SK}/SKILL.md', encoding='utf-8').read()
def defaults(tool):
    t = open(f'{D}/gatk_{tool}.txt', encoding='utf-8', errors='replace').read()
    m = re.search(r'--disable-read-filter,-DF <String>.*?Possible values: \{(.*?)\}', t, re.S)
    filt = set(re.findall(r'\w+ReadFilter', m.group(1)))
    mq = re.search(r'--minimum-mapping-quality <Integer>\s+Minimum mapping quality to keep \(inclusive\)\s+Default value: (\d+)', t)
    return filt, int(mq.group(1)) if mq else None
hc, hc_mq = defaults('HaplotypeCaller'); m2, m2_mq = defaults('Mutect2')
print('HaplotypeCaller default filters:', sorted(hc), 'min MAPQ', hc_mq)
print('Mutect2 default filters:', sorted(m2), 'min MAPQ', m2_mq)
check('GATK HaplotypeCaller default filters: MAPQ>=20, not duplicate, not secondary (consistent with the germline row -F 3328 -q 20)',
      {'MappingQualityReadFilter', 'NotDuplicateReadFilter', 'NotSecondaryAlignmentReadFilter'} <= hc and hc_mq == 20, f'min MAPQ {hc_mq}')
check('Mutect2 default filters also enforce MAPQ>=20 (so "somatic callers handle low MAPQ" is not what GATK Mutect2 does)',
      'MappingQualityReadFilter' in m2 and m2_mq == 20, f'min MAPQ {m2_mq}')
check('Mutect2 default filters include NonChimericOriginalAlignmentReadFilter (chimeric reads dropped by the caller itself)', 'NonChimericOriginalAlignmentReadFilter' in m2)
row = [l for l in txt.splitlines() if l.startswith('| Somatic short-variant')][0]
print('SKILL.md somatic row:', row)
check('SKILL.md somatic row claim "somatic callers handle low MAPQ" is supported for Mutect2', 'handle low MAPQ' not in row or m2_mq is None, 'CONTRADICTED by GATK: Mutect2 drops MAPQ<20 by default' if 'handle low MAPQ' in row else '')
print('Rows not verifiable here (callers not installed): Strelka2, DeepVariant, clair3, Sniffles, cuteSV, Manta, GRIDSS, Delly, SvABA -> stated as unverified in the report')
finish()
