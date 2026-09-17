"""
Build test variants for the re-audit of bio-crispr-screens-prime-editing-screens
(fixed Skill, fork commit 6847328).

- variant_realistic: the exact same locus that crashed the PRE-FIX script with
  KeyError (edit 5nt into `downstream`, i.e. close to the nick -- this is the
  geometry the pre-fix hardcoded pbs_length=12 mis-handled). Regression target.
- variant_minus: a second, independently constructed locus where the only
  usable NGG PAM sits on the minus strand, forcing find_pegrna_candidates()
  through its strand == '-' branch. New input (not in the pre-fix audit).
- variant_no_pam: a locus with the edit >30nt from the nearest NGG PAM, i.e.
  genuinely not PE-designable -- tests the new "skip, don't crash the whole
  batch" guard. New input.
"""
import random

COMP = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}


def revcomp(s):
    return ''.join(COMP[b] for b in reversed(s))


random.seed(7)
flank_up = ''.join(random.choice('ACGT') for _ in range(90))
spacer_target = "ACGTTGACCTGGAACGTTCA"   # 20 nt
pam = "TGG"
downstream = "CGATCCGTAAGCTTGGCCAATGGCCTTAAGGCCTTAACC"  # 40 nt after PAM
flank_down = ''.join(random.choice('ACGT') for _ in range(90))

genomic_plus = flank_up + spacer_target + pam + downstream + flank_down
pam_pos = len(flank_up) + len(spacer_target)
cut_pos = pam_pos - 3
edit_offset_from_pam_end = 5
edit_abs_pos = pam_pos + 3 + edit_offset_from_pam_end
ref_base = genomic_plus[edit_abs_pos]
alt_base = {'A': 'G', 'C': 'T', 'G': 'A', 'T': 'C'}[ref_base]
edited_plus = genomic_plus[:edit_abs_pos] + alt_base + genomic_plus[edit_abs_pos + 1:]
pridict_seq_realistic = genomic_plus[:edit_abs_pos] + f"({ref_base}/{alt_base})" + genomic_plus[edit_abs_pos + 1:]

print("=== variant_realistic (regression, matches pre-fix crash locus) ===")
print("PAM_POS", pam_pos, "PAM", genomic_plus[pam_pos:pam_pos + 3], "CUT_POS", cut_pos,
      "EDIT_ABS_POS", edit_abs_pos, "dist_from_cut", edit_abs_pos - cut_pos, "REF/ALT", ref_base, alt_base)

# 60nt-context CSV for the bundled script (edit at context position 30)
ctx_start = edit_abs_pos - 30
ctx_end = edit_abs_pos + 30
context_realistic = genomic_plus[ctx_start:ctx_end]
assert context_realistic[30] == ref_base
print("CONTEXT_REALISTIC(60nt, edit@30)=", context_realistic)

with open("intended_variants_round2.csv", "w") as f:
    f.write("variant_id,chrom,pos,ref,alt,context\n")
    f.write(f"VAR_REALISTIC,chr1,{edit_abs_pos},{ref_base},{alt_base},{context_realistic}\n")

# --- variant_minus: PAM only findable on the minus strand ---
random.seed(99)
flank_up2 = ''.join(random.choice('ACGT') for _ in range(90))
# Design on the MINUS strand: choose a minus-strand spacer+PAM, then write the
# plus-strand genomic sequence as its reverse complement so the plus-strand
# scan won't find an NGG PAM near the edit except via the '-' branch.
minus_spacer = "TTGCAACCGGTTACGAATGC"   # 20nt, arbitrary
minus_pam = "CGG"                        # NGG on minus strand
minus_downstream = "AGCTTGGACCGTTACGGATCTTAACCGGTTAGGCCAAGT"  # 40nt after PAM on minus strand
# minus-strand 5'->3' local sequence: spacer + pam + downstream
minus_local = minus_spacer + minus_pam + minus_downstream
# The plus strand at this locus is the revcomp of the minus-strand local sequence,
# read 5'->3' on the + strand (i.e. downstream(revcomp) + pam(revcomp) + spacer(revcomp)).
plus_local = revcomp(minus_local)
flank_down2 = ''.join(random.choice('ACGT') for _ in range(90))
genomic_plus2 = flank_up2 + plus_local + flank_down2

# Edit position: 5nt into minus_downstream (mirrors variant_realistic's geometry),
# expressed in the MINUS-strand local frame, then mapped back to + coordinates.
minus_cut = len(minus_spacer) + len(minus_pam) - 3  # not used directly; kept for reference
minus_edit_pos = len(minus_spacer) + len(minus_pam) + 5  # 5nt into minus_downstream
minus_ref = minus_local[minus_edit_pos]
minus_alt = {'A': 'G', 'C': 'T', 'G': 'A', 'T': 'C'}[minus_ref]

# Map minus-local position -> plus_local position -> absolute + position
plus_local_pos = len(minus_local) - 1 - minus_edit_pos
edit_abs_pos2 = len(flank_up2) + plus_local_pos
ref_base2 = genomic_plus2[edit_abs_pos2]
alt_base2 = COMP[minus_alt]
assert ref_base2 == COMP[minus_ref], (ref_base2, COMP[minus_ref])

ctx_start2 = edit_abs_pos2 - 30
ctx_end2 = edit_abs_pos2 + 30
context_minus = genomic_plus2[ctx_start2:ctx_end2]
assert context_minus[30] == ref_base2

print("\n=== variant_minus (new input: forces the '-' strand branch) ===")
print("edit_abs_pos2", edit_abs_pos2, "ref/alt(+strand)", ref_base2, alt_base2)
print("CONTEXT_MINUS(60nt, edit@30)=", context_minus)

# --- variant_no_pam: edit far (>30nt) from any NGG PAM -> should be skipped, not crash ---
random.seed(123)
no_pam_ctx = ''.join(random.choice('ACGT') for _ in range(60))
# Force position 30 to a definite ref base and scrub any NGG within range by
# construction check below; regenerate until no NGG within 35nt either side.
import re as _re
def has_nearby_pam(seq, edit_pos=30, window=35):
    lo, hi = max(0, edit_pos - window), min(len(seq), edit_pos + window)
    return bool(_re.search(r'[ACGT]GG', seq[lo:hi])) or bool(_re.search(r'CC[ACGT]', seq[lo:hi]))

tries = 0
while has_nearby_pam(no_pam_ctx) and tries < 5000:
    no_pam_ctx = ''.join(random.choice('ACGT') for _ in range(60))
    tries += 1
ref_base3 = no_pam_ctx[30]
alt_base3 = {'A': 'G', 'C': 'T', 'G': 'A', 'T': 'C'}[ref_base3]
print("\n=== variant_no_pam (new input: no workable PAM within range) ===")
print("tries", tries, "no NGG/CCN within 35nt of edit:", not has_nearby_pam(no_pam_ctx))
print("CONTEXT_NO_PAM=", no_pam_ctx)

with open("variants_round2_batch.csv", "w") as f:
    f.write("variant_id,chrom,pos,ref,alt,context\n")
    f.write(f"VAR_REALISTIC,chr1,{edit_abs_pos},{ref_base},{alt_base},{context_realistic}\n")
    f.write(f"VAR_MINUS,chr2,{edit_abs_pos2},{ref_base2},{alt_base2},{context_minus}\n")
    f.write(f"VAR_NO_PAM,chr3,30,{ref_base3},{alt_base3},{no_pam_ctx}\n")

print("\nWrote intended_variants_round2.csv and variants_round2_batch.csv")
