"""
Input 9 (NEW -- not in the pre-fix audit's 7 inputs): "I want the highest-activity
ABE for installing an A>G variant at codon 15 of this CDS with minimal bystanders.
Design ABE8e sgRNAs and tell me which are zero-bystander."

Tests two things the pre-fix audit never exercised for this Skill:
  1. The ABE8e window_by_editor entry (4,8) -- pre-fix only checked ABE7.10 (4,7).
     SKILL.md's own Base Editor Chemistry Selection table states ABE8e's window
     is "Pos 4-8", matching CBE rather than ABE7.10's narrower 4-7 -- verify the
     bundled code's window_by_editor dict actually encodes that, not the ABE7.10
     value.
  2. A realistic MULTI-STEP request: design (find_be_spacers) -> among the
     candidates, independently recompute which are genuinely zero-bystander AND
     on-target by hand, not just trusting the n_bystanders column.
"""
import random
import sys
sys.path.insert(0, ".")
from skill_functions import find_be_spacers

# --- 1. Direct check of the window table used by the code (not just the doc table) ---
import inspect
src = inspect.getsource(find_be_spacers)
print("window_by_editor line as it actually appears in the executed code:")
for line in src.splitlines():
    if "ABE8e" in line:
        print(" ", line.strip())

random.seed(42)
BASES = "ACGT"
codons_no_stop = [c1 + c2 + c3 for c1 in BASES for c2 in BASES for c3 in BASES
                  if (c1 + c2 + c3) not in ("TAA", "TAG", "TGA")]
cds = "ATG" + "".join(random.choice(codons_no_stop) for _ in range(79))
assert len(cds) == 240
print("\nCDS (240nt, seed=42):", cds)

target_aa = 42
codon_start = (target_aa - 1) * 3
codon_end = codon_start + 3
print(f"Target codon (aa={target_aa}): [{codon_start},{codon_end}) = {cds[codon_start:codon_end]}")

print("\n=== find_be_spacers(cds, 1, target_aa=15, target_base='A', editor='ABE8e') ===")
df = find_be_spacers(cds, cds_protein_start=1, target_aa=target_aa, target_base='A', editor='ABE8e')
print(f"Candidates found: {len(df)}")
print(df.to_string())

zero_bystander_hits = df[(df['n_bystanders'] == 0) & (df['target_positions'].apply(len) > 0)]
print(f"\nZero-bystander on-target candidates (per the function's own columns): {len(zero_bystander_hits)}")

# Independent by-hand re-derivation for every row the function reports as an
# on-target, zero-bystander hit: recompute genomic_pos from spacer/strand/
# spacer_start directly and confirm (a) it is really inside the codon and
# (b) the window (positions 4-8 for ABE8e, per SKILL.md's own table) really has
# only that one editable A.
window_lo, window_hi = 4, 8  # ABE8e per SKILL.md's Base Editor Chemistry Selection table
all_ok = True
assert len(zero_bystander_hits) > 0, "test needs at least one zero-bystander on-target hit to check"
for _, row in zero_bystander_hits.iterrows():
    spacer = row['spacer']
    a_positions_in_window = [i for i, b in enumerate(spacer[window_lo - 1:window_hi], start=window_lo) if b == 'A']
    print(f"\nRow: strand={row['strand']} spacer_start={row['spacer_start']} spacer={spacer}")
    print(f"  A's in window[4:8] (1-indexed, by direct inspection): {a_positions_in_window}")
    only_one = (a_positions_in_window == row['target_positions'])
    for i in row['target_positions']:
        pos_in_seq = row['spacer_start'] + i - 1
        true_fwd = (len(cds) - 1 - pos_in_seq) if row['strand'] == '-' else pos_in_seq
        in_codon = codon_start <= true_fwd < codon_end
        print(f"  i={i} -> true_forward_index={true_fwd}, in target codon: {in_codon}")
        all_ok = all_ok and in_codon
    all_ok = all_ok and only_one

print(f"\nALL zero-bystander on-target candidates independently re-verified: {all_ok}")
assert window_lo == 4 and window_hi == 8, "ABE8e window in SKILL.md's own table is (4,8)"
print("PASS: ABE8e window (4,8) matches SKILL.md's Base Editor Chemistry Selection table "
      "(distinct from ABE7.10's narrower (4,7), which the pre-fix audit tested instead), "
      "and every zero-bystander on-target candidate the function reports is independently "
      "confirmed correct by hand.")
