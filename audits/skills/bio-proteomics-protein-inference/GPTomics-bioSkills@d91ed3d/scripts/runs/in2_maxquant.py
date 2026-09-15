# Input 2 (Variant A): interpret a MaxQuant proteinGroups.txt (SYNTHETIC, shared audit table) the way the Skill directs:
# "MaxQuant output -> parse groups as-is; quantify on UNIQUE peptides"; report groups with a leading protein,
# keep group membership, do NOT impose a two-peptide rule.
import pandas as pd
pg = pd.read_csv('../data/proteinGroups.txt', sep='\t', low_memory=False)
n0 = len(pg)
flag = lambda c: pg[c].astype(str).eq('+')
bk = pd.DataFrame({'Reverse (REV__ decoy)': flag('Reverse'), 'Potential contaminant': flag('Potential contaminant'),
                   'Only identified by site': flag('Only identified by site')})
print('rows', n0, '| bookkeeping:', bk.sum().to_dict())
keep = pg[~bk.any(axis=1)].copy()
keep['members'] = keep['Protein IDs'].str.split(';')
keep['n_members'] = keep['members'].str.len()
keep['leading_protein'] = keep['members'].str[0]            # MaxQuant orders Protein IDs by peptide evidence
keep['majority_members'] = keep['Majority protein IDs'].str.split(';').str.len()
keep['razor_only_peptides'] = keep['Razor + unique peptides'] - keep['Unique peptides']
keep['shared_not_razor'] = keep['Peptides'] - keep['Razor + unique peptides']
keep['isoform_members'] = keep['members'].apply(lambda m: sum('-' in a for a in m))
print('target groups after removing REV/CON/site:', len(keep), '| protein-group Q-value<=0.01:', int((keep['Q-value'] <= 0.01).sum()))
print('multi-member groups:', int((keep.n_members > 1).sum()), '| groups containing an isoform accession (-N):', int((keep.isoform_members > 0).sum()))
print('groups with razor-assigned peptides (Razor+unique > Unique):', int((keep.razor_only_peptides > 0).sum()))
print('single-peptide groups (Peptides==1):', int((keep.Peptides == 1).sum()), '| <2 unique peptides:', int((keep['Unique peptides'] < 2).sum()))
# decoy context: MaxQuant's own protein FDR (REV__ rows) -- how many decoys vs targets at the reported score floor
rev = pg[flag('Reverse')]
print('REV__ rows', len(rev), 'max Q-value', rev['Q-value'].max(), '| REV__ are one-hit:', bool((rev.Peptides == 1).all()))
cols = ['leading_protein', 'Protein IDs', 'Gene names', 'n_members', 'Peptides', 'Razor + unique peptides', 'Unique peptides', 'Q-value', 'Score']
print('\nExample multi-member groups:')
print(keep[keep.n_members > 1][cols].head(5).to_string(index=False))
# What the Skill's picked_group_fdr would do if an agent reran it on this table with its default prefix
def picked_group_fdr(groups, decoy_prefix='DECOY_'):
    by_base = {}
    for g in groups:
        base = frozenset(a.replace(decoy_prefix, '') for a in g['accessions'])
        if base not in by_base or g['score'] > by_base[base]['score']:
            by_base[base] = g
    picked = sorted(by_base.values(), key=lambda g: g['score'], reverse=True)
    targets = decoys = 0
    for g in picked:
        if g['is_decoy']: decoys += 1
        else: targets += 1
        g['fdr'] = decoys / targets if targets else 1.0
    running_min = 1.0
    for g in reversed(picked):
        running_min = min(running_min, g['fdr']); g['qvalue'] = running_min
    return [g for g in picked if not g['is_decoy'] and g['qvalue'] <= 0.01]
allg = pg[~flag('Potential contaminant') & ~flag('Only identified by site')]
gl = [{'accessions': r.split(';'), 'score': s, 'is_decoy': all(a.startswith('DECOY_') for a in r.split(';'))} for r, s in zip(allg['Protein IDs'], allg['Score'])]
p_default = picked_group_fdr([dict(g) for g in gl])
gl2 = [{'accessions': r.split(';'), 'score': s, 'is_decoy': all(a.startswith('REV__') for a in r.split(';'))} for r, s in zip(allg['Protein IDs'], allg['Score'])]
p_rev = picked_group_fdr([dict(g) for g in gl2], decoy_prefix='REV__')
print(f"\nSkill picked_group_fdr, default prefix 'DECOY_': {len(p_default)} pass, of which REV__ rows counted as TARGETS: {sum(g['accessions'][0].startswith('REV__') for g in p_default)}")
print(f"Skill picked_group_fdr, prefix 'REV__': {len(p_rev)} pass")
out = keep[cols + ['majority_members', 'razor_only_peptides']].sort_values('Score', ascending=False)
out.to_csv('in2_protein_group_table.csv', index=False)
print('wrote in2_protein_group_table.csv', out.shape)
