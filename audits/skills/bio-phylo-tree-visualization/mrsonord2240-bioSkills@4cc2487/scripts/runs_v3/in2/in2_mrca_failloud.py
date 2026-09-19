"""Input 2 (Variant A) regression + fix verification:
'Color the great-apes clade red on my IQ-TREE tree (primates16.treefile). Root on the
strepsirrhines outgroup first if you need to.'

Verifies the SKILL.md 'Color branches by group' recipe's ValueError fail-loud check
(added at commit 4cc2487) on TWO paths, executed against the real IQ-TREE fixture
data/iq/primates16.treefile (16-tip primate tree, unrooted-as-stored):

  Path A (BUG reproduction): call common_ancestor on the raw file as parsed by
  Phylo.read (no rooting) -- reproduces the exact pre-fix defect (MRCA spans far more
  than the intended clade) and must trip the raise.
  Path B (CORRECT path, exactly the SKILL.md recipe): root_with_outgroup on the
  strepsirrhine outgroup first, then common_ancestor -- must return exactly the
  intended 5-tip great-apes clade and must NOT raise.
"""
import re
from Bio import Phylo

TREEFILE = 'data/iq/primates16.treefile'
INTENDED = {'Homo_sapiens', 'Pan_troglodytes', 'Pan_paniscus', 'Gorilla_gorilla', 'Pongo_abelii'}


def clear_support_names(tree):
    for clade in tree.get_nonterminals():
        if clade.name and re.fullmatch(r'[\d.]+/[\d.]+', clade.name):
            clade.name = None


def check_and_color(tree, label):
    mrca = tree.common_ancestor({'name': 'Homo_sapiens'}, {'name': 'Pongo_abelii'})
    mrca_tips = set(t.name for t in mrca.get_terminals())
    print(f'[{label}] MRCA tip count: {len(mrca_tips)} -- tips: {sorted(mrca_tips)}')
    if mrca_tips != INTENDED:
        raise ValueError(f'MRCA gave {sorted(mrca_tips)}, not the intended clade {sorted(INTENDED)} '
                          f'-- check the outgroup/rooting and the tip names passed to common_ancestor')
    mrca.color = 'red'
    print(f'[{label}] PASS -- exact intended clade colored, no raise')
    return mrca_tips


# --- Path A: bug reproduction (no rooting before common_ancestor) ---
print('=== Path A: common_ancestor WITHOUT rooting first (bug path) ===')
tree_a = Phylo.read(TREEFILE, 'newick')
clear_support_names(tree_a)
try:
    check_and_color(tree_a, 'A-no-root')
    print('Path A RESULT: NO RAISE (unexpected if this file exhibits the bug)')
except ValueError as e:
    print('Path A RESULT: RAISED ValueError as expected ->', e)

print()

# --- Path B: correct path, exactly the SKILL.md recipe ---
print('=== Path B: root_with_outgroup THEN common_ancestor (SKILL.md recipe) ===')
tree_b = Phylo.read(TREEFILE, 'newick')
tree_b.root_with_outgroup({'name': 'Microcebus_murinus'}, {'name': 'Otolemur_garnettii'})
clear_support_names(tree_b)
try:
    tips = check_and_color(tree_b, 'B-rooted')
    print('Path B RESULT: NO RAISE, tips exactly match intended clade:', tips == INTENDED)
except ValueError as e:
    print('Path B RESULT: RAISED unexpectedly ->', e)
