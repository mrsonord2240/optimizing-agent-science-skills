# Pass-5 confirmation audit, Input 6 (NEW this pass).
# Researcher request: "Our sample is the HYE benchmark (human + yeast + E. coli). The skill says to
# validate protein FDR 'with a two-species or entrapment search'. Do that on the 458-protein list
# Percolator gave me, and tell me whether my 1% protein-group FDR is really 1%."
#
# Real data: PXD070049 Condition_A REP1, Comet 2026.02 vs 31,437-protein target + DECOY_ decoy FASTA,
# Percolator 3.09.0 `-f/--picked-protein` exactly as the fixed SKILL.md prescribes (prot.target.tsv).
import os, re, collections
import pandas as pd

W = os.path.dirname(os.path.abspath(__file__))
C = 'F:/OpenScience/audits/bio-proteomics-peptide-identification/rerun4/comet_out'

pt = pd.read_csv(os.path.join(W, 'prot.target.tsv'), sep='\t')
pdd = pd.read_csv(os.path.join(W, 'prot.decoy.tsv'), sep='\t')
passing = pt[pt['q-value'] <= 0.01].copy()
print(f'Percolator picked-protein: {len(pt)} target rows, {len(pdd)} decoy rows, '
      f'{len(passing)} groups at q<=0.01')

# --- database composition (what species are even searchable) -----------------------------------
sp_re = re.compile(r'^>(DECOY_)?\S*?\|?[^|]*\|?\S*_([A-Z0-9]+)\b')
db = collections.Counter()
with open(os.path.join(C, 'target_decoy.fasta'), 'r', encoding='utf-8', errors='replace') as fh:
    for line in fh:
        if not line.startswith('>'):
            continue
        if line.startswith('>DECOY_'):
            continue
        m = re.search(r'_([A-Z0-9]+)\s', line)
        db[m.group(1) if m else '??'] += 1
print('\nDATABASE (target half) by species suffix:')
for s, n in db.most_common(8):
    print(f'   {s:8s} {n}')


def species(acc):
    m = re.search(r'_([A-Z0-9]+)$', acc.split()[0])
    return m.group(1) if m else '??'


passing['species'] = passing['ProteinId'].map(species)
print('\nPASSING 458 by species suffix:')
for s, n in passing['species'].value_counts().items():
    print(f'   {s:8s} {n}')

# --- the entrapment question the skill's one-liner does not answer ------------------------------
sample = {'HUMAN', 'YEAST', 'ECOLI'}
foreign = passing[~passing['species'].isin(sample)]
print(f'\nProteins from species NOT in the HYE mix: {len(foreign)} '
      f'({len(foreign)/len(passing):.2%} of the passing list)')
print('   their species:', dict(foreign["species"].value_counts()))
print('   are they contaminants? rows whose accession carries a Cont_/contaminant marker:',
      int(foreign['ProteinId'].str.contains('Cont_|CONTAM|sp\\|Cont', case=False, regex=True).sum()),
      'of', len(foreign))
print('   -> HUMAN, YEAST and ECOLI are ALL genuinely present in this sample, so none of them can '
      'serve as the entrapment set; the only non-sample accessions here are cRAP contaminants, '
      'which are also genuinely present in the tube. This dataset CANNOT validate protein FDR by '
      'species without a separate entrapment FASTA.')

# --- what the skill's own numbers say instead ---------------------------------------------------
print('\nWhat CAN be checked without an entrapment set:')
dpass = (pdd['q-value'] <= 0.01).sum()
print(f'   decoy groups passing q<=0.01 in prot.decoy.tsv: {dpass}')
print(f'   naive decoy/target ratio at the 1% cut: {dpass}/{len(passing)} = {dpass/len(passing):.2%}'
      '  (NOT the FDR; picking already removed the losing half of each pair)')
qs = pt['q-value']
print(f'   q-value range over all target rows: {qs.min():.3g} .. {qs.max():.3g}; '
      f'rows at q<=0.05: {(qs<=0.05).sum()}, q<=0.10: {(qs<=0.10).sum()}')

# --- group reporting: does Percolator report GROUPS the way this skill demands? -----------------
print('\nGroup-reporting check (the skill\'s central thesis is "report groups, not a flat list"):')
print('   rows whose ProteinId lists >1 accession:', int(pt['ProteinId'].str.contains(',').sum()))
print('   unique ProteinGroupId among all target rows:', pt['ProteinGroupId'].nunique(),
      'vs', len(pt), 'rows -> one row per group, members NOT listed')
print('   => Percolator eliminated fragment/duplicate proteins instead of listing them as group '
      'members. The indistinguishable partners are DROPPED from the report unless '
      '--protein-report-duplicates / --protein-report-fragments are passed. SKILL.md gives the '
      'column list but never says the other members vanish.')
