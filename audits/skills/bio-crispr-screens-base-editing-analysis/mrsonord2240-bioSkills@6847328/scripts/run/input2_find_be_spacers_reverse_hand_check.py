"""
Input 2 (Variant A, NEW, hand-constructed regression for the P0 fix):
"Install a C>T variant at a specific codon; find me the CBE spacer."

This is the single most important regression in this audit. The pre-fix defect was:
genomic_pos computed in reverse-complement coordinate space, compared directly
against forward-strand codon bounds with no conversion. The fixer's own test
(fixes/bio-crispr-screens-base-editing-analysis.md) found a case where this
mis-called a true OFF-target hit as "target" (false positive). To check the fix
is a general coordinate conversion and not a patch tuned to that one direction,
this test is built independently to trigger the OPPOSITE failure mode: a true
ON-target edit that the unconverted math would have called "bystander" (false
negative / missed target).

Derivation (worked out by hand before writing any code):
  - cds length L = 100. Target codon = amino acid 30 (1-indexed protein start),
    aa_index = 29, codon nt range = [87, 90).
  - Pick the true edited base at forward-CDS index genomic_pos = 88 (middle of
    the codon) -- this MUST be inside [87, 90).
  - The function only ever inspects the reverse-complement strand's characters
    for target_base='C'. On the reverse-complement string `seq`, the base at
    position pos_in_seq = L - 1 - genomic_pos = 100 - 1 - 88 = 11 must read 'C'.
    Since seq[k] = complement(cds[L-1-k]), seq[11] = complement(cds[88]).
    complement(cds[88]) = 'C'  =>  cds[88] must be 'G'.
  - Choose the PAM/spacer geometry so that this position falls inside the
    editing window (BE4max window = positions 4-8, 1-indexed within the
    spacer): pick window position i=5, spacer_start = pos_in_seq - i + 1
    = 11 - 5 + 1 = 7. Then PAM must start at pam_pos = spacer_start + 20 = 27,
    i.e. seq[27:30] must match the NGG pattern -> require seq[28]='G', seq[29]='G'.
  - seq[28] = complement(cds[99-28]) = complement(cds[71]) = 'G' => cds[71]='C'
    seq[29] = complement(cds[99-29]) = complement(cds[70]) = 'G' => cds[70]='C'
    seq[27] free -> set cds[72]='A' => seq[27]='T' (valid NGG: 'TGG').
  - To keep exactly ONE editable C in the window (avoid extra bystanders muddying
    the check), force the other window positions to be non-C:
    i=4 -> seq[10] = complement(cds[89]);  set cds[89]='A' => seq[10]='T'
    i=6 -> seq[12] = complement(cds[87]);  set cds[87]='A' => seq[12]='T'
    i=7 -> seq[13] = complement(cds[86]);  set cds[86]='A' => seq[13]='T'
    i=8 -> seq[14] = complement(cds[85]);  set cds[85]='A' => seq[14]='T'
  - Every other position in the 100nt CDS is filled with a fixed, non-special
    'A' repeat (never 'G' or creating stray PAMs at spacer_start=7) so the only
    engineered candidate at (strand='-', spacer_start=7) is unambiguous.

Predicted ground truth (by hand, before running anything):
  - UNCONVERTED (buggy) math: genomic_pos = pos_in_seq = 11. Codon check:
    87 <= 11 < 90 -> False -> the true on-target C would be called a BYSTANDER.
    This is a missed target -- the opposite failure direction from the fixer's
    own example (which produced a false on-target), so this independently
    stresses the general correctness of the conversion, not just one case.
  - CONVERTED (fixed) math: genomic_pos = L - 1 - pos_in_seq = 100 - 1 - 11 = 88.
    Codon check: 87 <= 88 < 90 -> True -> correctly called TARGET.
"""
import sys
sys.path.insert(0, ".")
from skill_functions import find_be_spacers

L = 100
cds = list("A" * L)
# Engineered positions (see derivation above)
cds[88] = 'G'   # -> seq[11] = 'C' (the true on-target editable base)
cds[71] = 'C'   # -> seq[28] = 'G' (PAM position 2)
cds[70] = 'C'   # -> seq[29] = 'G' (PAM position 3)
cds[72] = 'A'   # -> seq[27] = 'T' (PAM position 1, any base)
cds[89] = 'A'   # -> seq[10] = 'T' (window i=4, must not be C)
cds[87] = 'A'   # -> seq[12] = 'T' (window i=6, must not be C)
cds[86] = 'A'   # -> seq[13] = 'T' (window i=7, must not be C)
cds[85] = 'A'   # -> seq[14] = 'T' (window i=8, must not be C)
cds_sequence = "".join(cds)
assert len(cds_sequence) == L

from Bio.Seq import Seq
seq = str(Seq(cds_sequence).reverse_complement())
print("Constructed CDS:", cds_sequence)
print("Its reverse complement (`seq`, what the function scans on strand='-'):", seq)
print("seq[7:27] (intended spacer):", seq[7:27])
print("seq[27:30] (intended PAM):", seq[27:30])
print("seq[11] (should be 'C', the on-target base):", seq[11])

target_aa = 30
codon_start = (target_aa - 1) * 3
codon_end = codon_start + 3
print(f"\nTarget codon (aa={target_aa}), forward-CDS range [{codon_start}, {codon_end}) = {cds_sequence[codon_start:codon_end]}")
print("Hand-predicted true forward index of the edited base: 88 (cds[88] =", cds_sequence[88], ")")
print("88 in [", codon_start, ",", codon_end, ")?", codon_start <= 88 < codon_end)

print("\n=== Running the FIXED find_be_spacers() from SKILL.md ===")
df = find_be_spacers(cds_sequence, cds_protein_start=1, target_aa=target_aa, target_base='C', editor='BE4max')
print(f"Total candidates: {len(df)}")

row = df[(df['strand'] == '-') & (df['spacer_start'] == 7)]
print("\nEngineered candidate row (strand='-', spacer_start=7):")
print(row.to_string())

assert len(row) == 1, f"Expected exactly 1 engineered candidate row, got {len(row)}"
row = row.iloc[0]

print("\n--- Verdict ---")
print("target_positions:", row['target_positions'])
print("bystander_positions:", row['bystander_positions'])

if row['target_positions'] == [5]:
    print("PASS: fixed code correctly classifies the hand-verified true on-target C as TARGET.")
elif row['bystander_positions'] == [5]:
    print("FAIL: fixed code still misclassifies the true on-target C as BYSTANDER "
          "(the missed-target failure mode this test was built to catch).")
else:
    print("UNEXPECTED result shape:", dict(row))

# Show explicitly what the OLD (unconverted) math would have produced, for contrast.
pos_in_seq = 7 + 5 - 1  # spacer_start + i - 1
unconverted_genomic_pos = pos_in_seq
converted_genomic_pos = L - 1 - pos_in_seq
print(f"\nFor reference -- unconverted (pre-fix) genomic_pos = {unconverted_genomic_pos} "
      f"(in [{codon_start},{codon_end})? {codon_start <= unconverted_genomic_pos < codon_end}) "
      f"-> pre-fix code would have called this a BYSTANDER (false negative).")
print(f"Converted (fixed) genomic_pos = {converted_genomic_pos} "
      f"(in [{codon_start},{codon_end})? {codon_start <= converted_genomic_pos < codon_end}) "
      f"-> fixed code calls this TARGET, matching the hand-derived ground truth.")
