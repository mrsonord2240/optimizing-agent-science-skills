# Input 4 step 1: SKILL.md "Bayesian Inference + Group FDR with EPIFANY" block, VERBATIM
import pyopenms
from pyopenms import IdXMLFile

# CONFIRM the class name at the installed version before use:
#   help(pyopenms.EpifanyAlgorithm)
algo_cls = getattr(pyopenms, 'EpifanyAlgorithm')

protein_ids = []
peptide_ids = []
IdXMLFile().load('peptides_with_pep.idXML', protein_ids, peptide_ids)

algo = algo_cls()
algo.inferPosteriorProbabilities(protein_ids, peptide_ids, False)

for prot_id in protein_ids:
    for group in prot_id.getIndistinguishableProteins():
        print(group.accessions[0], group.probability)
