"""
Test the Skill's find_be_spacers() code verbatim (copied from SKILL.md) against a
synthetic CDS, as an agent would when asked:
"Design a CBE saturation library tiling BRCA1 RING domain (aa 1-100), 10-15 sgRNAs
per amino acid, minimize bystanders, annotate target+bystander." (Input 1, Canonical)

Also exercises the ABE7.10 path per Input 3 (Edge): "install MLH1 c.677A>G ... find
ABE7.10 sgRNAs that place A at position 5 with no bystanders."
"""
import pandas as pd
import re
from Bio.Seq import Seq

# ---- verbatim from SKILL.md ----
def find_be_spacers(cds_sequence, cds_protein_start, target_aa, target_base='C', editor='BE4max'):
    window_by_editor = {
        'BE3': (4, 8),       'BE4max': (4, 8),    'eA3A-BE3': (5, 7),
        'ABE7.10': (4, 7),   'ABE8.20': (4, 8),   'ABE8e': (4, 8),
        'evoCDA-BE': (1, 9),
    }
    window_lo, window_hi = window_by_editor[editor]
    aa_index = target_aa - cds_protein_start
    aa_start_nt = aa_index * 3
    candidates = []
    spacer_len = 20
    pam_pattern = re.compile(r'(?=([ACGT]GG))')
    for strand, seq in [('+', cds_sequence), ('-', str(Seq(cds_sequence).reverse_complement()))]:
        for pam_match in pam_pattern.finditer(seq):
            pam_pos = pam_match.start()
            spacer_start = pam_pos - spacer_len
            if spacer_start < 0:
                continue
            spacer = seq[spacer_start:pam_pos]
            edit_bases_in_window = []
            for i, b in enumerate(spacer[window_lo-1:window_hi], start=window_lo):
                if b == target_base:
                    edit_bases_in_window.append(i)
            if not edit_bases_in_window:
                continue
            target_codon_start = aa_start_nt
            target_codon_end = target_codon_start + 3
            target_position_in_spacer = []
            for i in edit_bases_in_window:
                genomic_pos = spacer_start + i - 1
                if target_codon_start <= genomic_pos < target_codon_end:
                    target_position_in_spacer.append(i)
            bystander_positions = [i for i in edit_bases_in_window if i not in target_position_in_spacer]
            candidates.append({
                'spacer': spacer,
                'strand': strand,
                'spacer_start': spacer_start,
                'target_positions': target_position_in_spacer,
                'bystander_positions': bystander_positions,
                'n_bystanders': len(bystander_positions),
            })
    return pd.DataFrame(candidates).sort_values('n_bystanders')
# ---- end verbatim ----

import random
random.seed(1)
BASES = "ACGT"
# 300nt synthetic CDS (100 codons), in-frame, no stop codons, with scattered NGG PAMs
codons_no_stop = [c1+c2+c3 for c1 in BASES for c2 in BASES for c3 in BASES
                  if (c1+c2+c3) not in ("TAA", "TAG", "TGA")]
cds = "ATG" + "".join(random.choice(codons_no_stop) for _ in range(99))
assert len(cds) == 300

print("=== Input 1 (Canonical): CBE (BE4max) tiling around aa 40 ===")
df = find_be_spacers(cds, cds_protein_start=1, target_aa=40, target_base='C', editor='BE4max')
print(f"Candidates found: {len(df)}")
if len(df):
    print(df.head(10).to_string())
    print("Any with target_positions non-empty (on-target hits)?",
          (df['target_positions'].apply(len) > 0).sum())
else:
    print("NO CANDIDATES -- would silently return an empty DataFrame with a KeyError-free"
          " but useless result for a real design task.")

print("\n=== Input 3 (Edge): ABE7.10, target A, aa 60, zero-bystander requirement ===")
df2 = find_be_spacers(cds, cds_protein_start=1, target_aa=60, target_base='A', editor='ABE7.10')
print(f"Candidates found: {len(df2)}")
if len(df2):
    print(df2.head(10).to_string())
    zero_bystander = df2[(df2['n_bystanders'] == 0) & (df2['target_positions'].apply(len) > 0)]
    print(f"Zero-bystander on-target candidates: {len(zero_bystander)}")
else:
    print("NO CANDIDATES")

print("\n=== Sanity check: does genomic_pos math actually align to the intended codon? ===")
# Manually verify target_positions really do fall in the target codon for a hit, if any exist
if len(df) and (df['target_positions'].apply(len) > 0).any():
    hit = df[df['target_positions'].apply(len) > 0].iloc[0]
    print("Example hit row:", dict(hit))
    codon_start = (40 - 1) * 3
    print(f"Target codon nt range (0-indexed): [{codon_start}, {codon_start+3})")
    print("CDS at that codon:", cds[codon_start:codon_start+3])
