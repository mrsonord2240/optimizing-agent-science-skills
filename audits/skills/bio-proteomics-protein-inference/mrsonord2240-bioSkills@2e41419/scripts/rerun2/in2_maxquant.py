# Re-audit 2026-09-15, Input 2 (Variant A, regression). MaxQuant proteinGroups.txt (SYNTHETIC shared table).
# Follows the fixed decision-tree row: drop Reverse/REV__, Potential contaminant, Only identified by site; Protein IDs =
# members, Majority protein IDs = >= half the group's peptides, first = leading; Unique peptides = unique to the GROUP.
# Picked-group FDR via the Skill's sketch with the prefix passed explicitly ('REV__').
import pandas as pd

def picked_group_fdr(groups, decoy_prefix, min_decoys=10):   # SKILL.md verbatim (fork 575ab94)
    n_decoy = sum(g['is_decoy'] for g in groups)
    if n_decoy == 0 or not any(a.startswith(decoy_prefix) for g in groups for a in g['accessions']):
        raise ValueError(f'no decoy groups with prefix {decoy_prefix!r}; keep decoys upstream or fix the prefix')
    if n_decoy < min_decoys:
        print(f'WARNING: only {n_decoy} decoy groups; the protein FDR estimate is not meaningful')
    by_base = {}
    for g in groups:
        base = frozenset(a.replace(decoy_prefix, '') for a in g['accessions'])
        if base not in by_base or g['score'] > by_base[base]['score']:
            by_base[base] = g
    picked = sorted(by_base.values(), key=lambda g: g['score'], reverse=True)
    targets = decoys = 0
    for g in picked:
        if g['is_decoy']:
            decoys += 1
        else:
            targets += 1
        g['fdr'] = decoys / targets if targets else 1.0
    running_min = 1.0
    for g in reversed(picked):
        running_min = min(running_min, g['fdr'])
        g['qvalue'] = running_min
    return [g for g in picked if not g['is_decoy'] and g['qvalue'] <= 0.01]

pg = pd.read_csv('../data/proteinGroups.txt', sep='\t', low_memory=False)
flag = lambda c: pg[c].astype(str).eq('+')
print('rows', len(pg), '| Reverse', int(flag('Reverse').sum()), '| REV__ in Protein IDs', int(pg['Protein IDs'].str.contains('REV__').sum()),
      '| CON', int(flag('Potential contaminant').sum()), '| site-only', int(flag('Only identified by site').sum()))
keep = pg[~(flag('Reverse') | flag('Potential contaminant') | flag('Only identified by site'))].copy()
keep['members'] = keep['Protein IDs'].str.split(';')
keep['leading'] = keep['members'].str[0]
keep['n_members'] = keep['members'].str.len()
keep['n_majority'] = keep['Majority protein IDs'].str.split(';').str.len()
print('target groups kept', len(keep), '| multi-member', int((keep.n_members > 1).sum()),
      '| groups where Majority < all members', int((keep.n_majority < keep.n_members).sum()))
print('Q-value<=0.01 (MaxQuant protein FDR):', int((keep['Q-value'] <= 0.01).sum()))
print('razor-assigned (Razor+unique > Unique):', int((keep['Razor + unique peptides'] > keep['Unique peptides']).sum()),
      '| Unique peptides < 2 (flag, do not drop):', int((keep['Unique peptides'] < 2).sum()))

nocon = pg[~(flag('Potential contaminant') | flag('Only identified by site'))]
gl = [{'accessions': r.split(';'), 'score': s, 'is_decoy': all(a.startswith('REV__') for a in r.split(';'))}
      for r, s in zip(nocon['Protein IDs'], nocon['Score'])]
res = picked_group_fdr([dict(g) for g in gl], 'REV__')
print("Skill picked_group_fdr(prefix='REV__') passing:", len(res))
try:
    picked_group_fdr([dict(g) for g in gl], 'DECOY_')
except ValueError as e:
    print("prefix 'DECOY_' on MaxQuant table -> ValueError:", e)
# is_decoy computed with DECOY_ while REV__ rows present: guard uses is_decoy sum + prefix scan
gl_bad = [{'accessions': r.split(';'), 'score': s, 'is_decoy': all(a.startswith('DECOY_') for a in r.split(';'))}
          for r, s in zip(nocon['Protein IDs'], nocon['Score'])]
try:
    picked_group_fdr([dict(g) for g in gl_bad], 'DECOY_')
except ValueError as e:
    print("consistent-but-wrong DECOY_ labelling -> ValueError:", e)
cols = ['leading', 'Protein IDs', 'Majority protein IDs', 'Gene names', 'Peptides', 'Razor + unique peptides', 'Unique peptides', 'Q-value', 'Score']
keep[cols].sort_values('Score', ascending=False).to_csv('in2_group_table.csv', index=False)
print(keep[keep.n_members > 1][cols].head(3).to_string(index=False))
