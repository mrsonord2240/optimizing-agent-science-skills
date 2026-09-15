from Bio import Phylo

prior = Phylo.read('prioronly.mcc.tree', 'nexus')   # effective prior summary
post = Phylo.read('withdata.mcc.tree', 'nexus')      # posterior summary
for c_prior, c_post in zip(prior.get_nonterminals(), post.get_nonterminals()):
    # if the posterior median and HPD ~ the effective prior, the data did not inform this node
    print(c_prior.confidence, c_post.confidence)     # compare per-node summaries side by side
