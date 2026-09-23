"""
Input 1 (Canonical, NEW -- not from the pre-fix audit): "Design a CBE saturation
library tiling a 60-codon target region (aa 1-60) of a synthetic CDS. 10-15 sgRNAs
per amino acid where at least one C in the editing window (positions 4-8) hits the
target codon. Annotate each sgRNA with predicted target + bystander variants."

Uses a fresh synthetic CDS (seed 7, different from the pre-fix audit's seed-1 CDS)
and a different target_aa (aa 22) so this is not just a re-run of the old input.
"""
import random
import sys
sys.path.insert(0, ".")
from skill_functions import find_be_spacers

random.seed(7)
BASES = "ACGT"
codons_no_stop = [c1 + c2 + c3 for c1 in BASES for c2 in BASES for c3 in BASES
                  if (c1 + c2 + c3) not in ("TAA", "TAG", "TGA")]
cds = "ATG" + "".join(random.choice(codons_no_stop) for _ in range(59))
assert len(cds) == 180
print("CDS (180nt, seed=7):", cds)

print("\n=== find_be_spacers(cds, 1, target_aa=25, target_base='C', editor='BE4max') ===")
df = find_be_spacers(cds, cds_protein_start=1, target_aa=25, target_base='C', editor='BE4max')
print(f"Candidates found: {len(df)}")
print(df.to_string())

hits = df[df['target_positions'].apply(len) > 0]
print(f"\nOn-target hits: {len(hits)}")
codon_start = (25 - 1) * 3
codon_end = codon_start + 3
print(f"True target codon (0-indexed forward CDS range): [{codon_start}, {codon_end}) = {cds[codon_start:codon_end]}")

# Independent by-hand check for every reported hit (both strands): recompute the
# true forward-CDS index of the reported target position from the row's own
# spacer/strand/spacer_start and confirm it really lands inside the codon.
ok = True
for _, row in hits.iterrows():
    for i in row['target_positions']:
        pos_in_seq = row['spacer_start'] + i - 1
        if row['strand'] == '-':
            true_fwd = len(cds) - 1 - pos_in_seq
        else:
            true_fwd = pos_in_seq
        in_codon = codon_start <= true_fwd < codon_end
        print(f"  strand={row['strand']} spacer_start={row['spacer_start']} i={i} "
              f"-> true_forward_index={true_fwd} in_target_codon={in_codon}")
        ok = ok and in_codon
print("\nALL reported on-target hits independently verified inside the true codon:", ok)
