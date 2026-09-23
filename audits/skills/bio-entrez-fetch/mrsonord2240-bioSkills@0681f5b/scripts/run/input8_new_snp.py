"""
Input 8 (NEW -- probes net-new dbSNP content the fix added; never audited by anyone before this
pass, including the fixer's own unverified claim in fixes/bio-entrez-fetch.md):
"Get the chromosome, gene, and clinical significance for dbSNP rs429358 (one of the two SNPs
defining the APOE e4 haplotype)."

SKILL.md's own "dbSNP record by UID" fenced block (block_10), verbatim. rs429358 -> numeric UID
429358 (the 'rs' prefix is dropped for the numeric dbSNP UID, as SKILL.md's own text says).
"""
from Bio import Entrez

Entrez.email = 'bio-entrez-fetch-reaudit@openscience.local'
Entrez.tool = 'skill-reauditor-bio-entrez-fetch'

# block_09 defines `import xml.etree.ElementTree as ET`, which block_10 (snp_record) depends on,
# exactly as they appear back-to-back in SKILL.md's own document order.
exec(open(r'F:\OpenScience\audits\bio-entrez-fetch\run\skillmd_blocks\block_09.py').read())
exec(open(r'F:\OpenScience\audits\bio-entrez-fetch\run\skillmd_blocks\block_10.py').read())

uid = '429358'  # rs429358
rec = snp_record(uid)  # noqa: F821 -- defined by the exec() above, straight from SKILL.md
print(f'UID={uid}')
print(f'CHR={rec["chr"]}')
print(f'GENE={rec["gene"]}')
print(f'CLINICAL_SIGNIFICANCE={rec["clinical_significance"]}')
