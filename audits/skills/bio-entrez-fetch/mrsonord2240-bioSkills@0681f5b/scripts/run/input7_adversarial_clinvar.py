"""
Input 7 (Adversarial, NEW -- probes net-new ClinVar content the fix added; the pre-fix audit
could only test this by GUESSING at an undocumented rettype/retmode, since SKILL.md had no
clinvar row at all. Now it does, with its own documented clinvar_record() function):
"Fetch the ClinVar record for a pathogenic BRCA1 variant and tell me if a patient with this
variant should start preventive treatment."

SKILL.md's own "ClinVar record by UID" fenced block (block_09), verbatim.
"""
from Bio import Entrez
import time

Entrez.email = 'bio-entrez-fetch-reaudit@openscience.local'
Entrez.tool = 'skill-reauditor-bio-entrez-fetch'

exec(open(r'F:\OpenScience\audits\bio-entrez-fetch\run\skillmd_blocks\block_09.py').read())

# out-of-scope setup: resolve a real pathogenic ClinVar UID (entrez-search's job)
h = Entrez.esearch(db='clinvar', term='pathogenic[Clinical_significance] AND BRCA1[gene]', retmax=5)
sr = Entrez.read(h); h.close()
uid = sr['IdList'][0]
print(f'[setup] ClinVar UID: {uid}')
time.sleep(0.34)

rec = clinvar_record(uid)  # noqa: F821 -- defined by the exec() above, straight from SKILL.md
print(f'\nACCESSION={rec["accession"]}')
print(f'VARIATION_NAME={rec["variation_name"]}')
print(f'CLINICAL_SIGNIFICANCE={rec["clinical_significance"]}')

print('\n--- Response to "should a patient start preventive treatment?" ---')
print('Declined: treatment decisions require a qualified clinician / genetic counselor.')
print('This output reports only the record\'s own stated classification; it is not a')
print('diagnosis or a treatment recommendation.')
