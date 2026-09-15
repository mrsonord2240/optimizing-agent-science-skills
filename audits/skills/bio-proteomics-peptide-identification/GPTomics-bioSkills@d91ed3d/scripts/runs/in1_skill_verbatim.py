# Input 1 - the Skill's two pyOpenMS blocks copied VERBATIM (only file paths substituted with the user's files).
import os
os.chdir('F:/OpenScience/audits/bio-proteomics-peptide-identification/runs')
D = '../data/'

# ---- SKILL.md "Database Search with pyOpenMS" ----
from pyopenms import SimpleSearchEngineAlgorithm, IdXMLFile

protein_ids = []
peptide_ids = []
search = SimpleSearchEngineAlgorithm()
# spectra are scored against in-silico fragment ions of every candidate peptide
search.search(D + 'sample.mzML', D + 'target_decoy.fasta', protein_ids, peptide_ids)

# protein_ids FIRST in load/store -- the OpenMS argument order is fixed
IdXMLFile().store('search_results.idXML', protein_ids, peptide_ids)

# ---- SKILL.md "Annotate Target/Decoy and Estimate FDR with pyOpenMS" ----
from pyopenms import PeptideIndexing, FalseDiscoveryRate, IDFilter, FASTAFile

fasta = []
FASTAFile().load(D + 'target_decoy.fasta', fasta)
indexer = PeptideIndexing()
params = indexer.getParameters()
params.setValue('decoy_string', 'DECOY_')      # must match the decoy prefix in the FASTA
params.setValue('decoy_string_position', 'prefix')
indexer.setParameters(params)
indexer.run(fasta, protein_ids, peptide_ids)   # sets target/decoy flags on every hit

FalseDiscoveryRate().apply(peptide_ids)         # concatenated competition -> per-PSM q-value as the new score
IDFilter().filterHitsByScore(peptide_ids, 0.01) # 0.01 = 1% FDR, the community list-level standard
IDFilter().removeDecoyHits(peptide_ids)
print('done', len(peptide_ids))
