# Fixed Skill's Bio.Phylo MCC comparison, VERBATIM from SKILL.md (mrsonord2240/bioSkills@966f838), run on the
# pre-fix audit's TreeAnnotator output (BEAST 2.7.7, SYNTHETIC loc1; MCC files copied, not regenerated).
import re
from Bio import Phylo

def node_heights(path):
    heights = {}
    for clade in Phylo.read(path, 'nexus').get_nonterminals():
        tips = frozenset(t.name for t in clade.get_terminals())
        med = re.search(r'height_median=([-\d.eE]+)', clade.comment or '')
        hpd = re.search(r'height_95%_HPD=\{([-\d.eE]+),([-\d.eE]+)\}', clade.comment or '')
        heights[tips] = (float(med.group(1)) if med else None, (float(hpd.group(1)), float(hpd.group(2))) if hpd else None)
    return heights

prior = node_heights('prioronly.mcc.tree')   # effective prior summary
post = node_heights('withdata.mcc.tree')     # posterior summary
for tips, (median, hpd) in post.items():
    # if the posterior median and HPD ~ the effective prior, the data did not inform this node
    print(sorted(tips), 'prior', prior.get(tips, 'clade not in prior MCC tree'), 'posterior', median, hpd)
