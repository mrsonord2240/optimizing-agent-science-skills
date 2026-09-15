# Input 1, step 1: SKILL.md "Group Proteins by Parsimony with pyOpenMS" block, VERBATIM (file name as in the Skill)
from pyopenms import IdXMLFile, BasicProteinInferenceAlgorithm

protein_ids = []
peptide_ids = []
# protein_ids is FIRST in both load() and store() for IdXMLFile
IdXMLFile().load('peptides_1pct_fdr.idXML', protein_ids, peptide_ids)

inference = BasicProteinInferenceAlgorithm()
params = inference.getParameters()
# annotate_indistinguishable_groups reports indistinguishable proteins as ONE group
params.setValue('annotate_indistinguishable_groups', 'true')
inference.setParameters(params)
inference.run(peptide_ids, protein_ids)

# indistinguishable groups live on the protein identification run
for prot_id in protein_ids:
    for group in prot_id.getIndistinguishableProteins():
        leading = group.accessions[0]  # convention: highest-evidence accession first
        print(leading, group.probability, list(group.accessions))
