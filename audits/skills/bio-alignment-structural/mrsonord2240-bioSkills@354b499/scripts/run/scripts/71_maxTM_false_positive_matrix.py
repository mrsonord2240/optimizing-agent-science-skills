"""Ground-truth check of the Skill's rule: 'the standard metric is the larger of the two TM-scores (normalised by the shorter chain); TM > 0.5 = same fold'.
All-vs-all over real, first-chain structures with KNOWN different folds (globin / kinase / calmodulin EF-hand / ubiquitin beta-grasp / protein G beta-grasp / tetanus toxin beta-jellyroll-ish).
Reports how many known-different-fold pairs the max() rule calls 'same fold' (>0.5) vs the rule of normalising by the LONGER chain (min())."""
import sys, subprocess, itertools
sys.dont_write_bytecode = True
sys.path.insert(0, 'skill/examples'); import tm_align_pairwise as t
D = 'data/real_pdb/'
fold = {'1MBN': 'globin', '1A3N': 'globin', '2LHB': 'globin', '1ATP': 'kinase', '1HCK': 'kinase', '2ITZ': 'kinase', '1CLL': 'EF-hand', '1UBQ': 'b-grasp', '1PGA': 'b-grasp', '1DIW': 'toxin'}
rows = []
for a, b in itertools.combinations(fold, 2):
    r = t.parse_outfmt2(subprocess.run(['TMalign', D+a+'.pdb', D+b+'.pdb', '-outfmt', '2'], capture_output=True, text=True).stdout)
    rows.append((a, b, fold[a] == fold[b], max(r['tm1'], r['tm2']), min(r['tm1'], r['tm2']), r['length1'], r['length2']))
diff = [r for r in rows if not r[2]]; same = [r for r in rows if r[2]]
fp_max = [r for r in diff if r[3] > 0.5]; fp_min = [r for r in diff if r[4] > 0.5]
print('pairs known different fold:', len(diff), '| same fold:', len(same))
print('FALSE same-fold calls with max(TM) > 0.5:', len(fp_max)); [print('   %s(%d) vs %s(%d) [%s vs %s]: max=%.3f min=%.3f' % (a, l1, b, l2, fold[a], fold[b], mx, mn)) for a, b, s, mx, mn, l1, l2 in fp_max]
print('FALSE same-fold calls with min(TM) > 0.5 (normalise by longer chain):', len(fp_min))
print('same-fold pairs called same fold: max-rule %d/%d, min-rule %d/%d' % (sum(r[3] > .5 for r in same), len(same), sum(r[4] > .5 for r in same), len(same)))
print('interpret_tmscore on the worst false positive:', t.interpret_tmscore(max(r[3] for r in fp_max)) if fp_max else None)
assert len(fp_max) >= 1 and len(fp_min) == 0
