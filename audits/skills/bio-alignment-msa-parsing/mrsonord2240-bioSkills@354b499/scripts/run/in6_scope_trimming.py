"""Input 6 (Scope boundary): 'Trim this Pfam globin alignment for tree building AND for HMM building, keep the original column numbers, and
mask unreliable columns with GUIDANCE2. Then stream it with pyhmmer.'  SKILL.md only ROUTES (decision matrix) to alignment-trimming.
Checks the routing claims against real tool output (in6_wsl.sh outputs) and the pyhmmer streaming sentence. REAL Pfam seed."""
import os, re, shutil
import numpy as np
from Bio import AlignIO
import pyhmmer
from common import *
import skill_md_funcs as F

D = os.path.join(HERE, 'data')
orig = AlignIO.read(PFAM_FA, 'fasta')
arr = np.array([list(str(r.seq)) for r in orig]); L = arr.shape[1]

# 1. trimAl -gappyout -colnumbering  (routing table: "preserve column-mapping ... trimAl -colnumbering")
txt = open(os.path.join(D, 'in6_trimal_colnumbering.txt'), encoding='utf-8').read()
m = re.search(r'#ColumnsMap\s*(.*)', txt)
colmap = [int(x) for x in m.group(1).replace('\t', '').split(',') if x.strip() != ''] if m else []
tri = AlignIO.read(os.path.join(D, 'in6_trimal_gappyout.fa'), 'fasta')
print(f'trimAl gappyout: {tri.get_alignment_length()} of {L} columns kept; colmap len {len(colmap)}')
check('trimAl -colnumbering: #ColumnsMap has one entry per kept column', len(colmap) == tri.get_alignment_length(), f'{len(colmap)} vs {tri.get_alignment_length()}')
check('trimAl -colnumbering: trimmed rows equal ORIGINAL columns at the mapped indices (mapping is 0-based and correct)', all(str(tri[i].seq) == ''.join(arr[i, colmap]) for i in range(len(orig))))
# 2. ClipKIT kpic-smart-gap
ck = AlignIO.read(os.path.join(D, 'in6_clipkit_kpic.fa'), 'fasta')
print(f'ClipKIT kpic-smart-gap: {ck.get_alignment_length()} of {L} kept ({(1 - ck.get_alignment_length() / L) * 100:.1f}% trimmed)')
check('ClipKIT kpic-smart-gap mode name is valid and keeps a sane count (121 of 141 in the tool log)', ck.get_alignment_length() == 121 and len(ck) == 73)
# the Skill's own tip: aggressive trimming >20-30% hurts trees. Compare the skill's remove_gappy_columns(0.5) vs the routed tools
sk = F.remove_gappy_columns(orig, 0.5)
print(f"SKILL remove_gappy_columns(0.5): {sk.get_alignment_length()} kept; trimAl gappyout {tri.get_alignment_length()}; ClipKIT {ck.get_alignment_length()}")
check("SKILL tip 'aggressive trimming (>20-30% of sites) hurts trees': trimAl -gappyout trims <=30% here (HMM-oriented tool is not over-aggressive)", (1 - tri.get_alignment_length() / L) <= 0.30, f'{(1 - tri.get_alignment_length() / L) * 100:.1f}% trimmed')
# 3. GUIDANCE2: recommended twice (unreliable regions #3; selection row) but not runnable
check('GUIDANCE2 reliability masking (recommended in 2 places) is runnable [NOT EXECUTED: package unobtainable, TOOLS.md Blocked]', False, 'GUIDANCE2 tarball URL now returns an HTML page; no install path documented in the Skill')
# 4. MUSCLE5 ensemble flags (in6_wsl_output.txt)
wsl = open(os.path.join(HERE, 'in6_wsl_output.txt'), encoding='utf-8').read()
check("MUSCLE5 '-stratified/-diversified' ensemble + '-letterconf' exist in muscle 5.3 help (SKILL: 'MUSCLE5 ensemble for per-column confidence')", all(k in wsl for k in ('-stratified', '-diversified', '-letterconf')))
# 5. pyhmmer streaming sentence: "pyhmmer.easel.MSAFile + compute_weights(method='pb')" on a multi-alignment file (SYNTHETIC: real seed twice)
multi = os.path.join(D, 'syn_multi_stockholm.sto')
sto = open(PFAM_STO, encoding='utf-8').read()
open(multi, 'w', encoding='utf-8', newline='\n').write(sto + sto.replace('#=GF ID   Globin', '#=GF ID   Globin2'))
sums = []
with pyhmmer.easel.MSAFile(multi, digital=True) as f:
    for msa in f:
        w = msa.compute_weights(method='pb')
        sums.append((len(msa.sequences), round(float(sum(w)), 3)))
print('streamed MSAs (n_seqs, sum of pb weights):', sums)
check("pyhmmer streaming pattern (iterate MSAFile, compute_weights(method='pb')) works on a 2-record Stockholm file", sums == [(73, 73.0), (73, 73.0)], str(sums))
import importlib.metadata as md
check('SKILL.md version block lists pyhmmer minimum version (compute_weights added in pyhmmer 0.11.3) [FAIL = not stated]', 'pyhmmer' in open(os.path.join(HERE, 'skill', 'SKILL.md'), encoding='utf-8').read().split('# MSA Parsing and Analysis')[0], 'Version Compatibility block only mentions BioPython and numpy')
summary()
