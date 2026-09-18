import random
random.seed(42)

def revcomp(s):
    comp = {'A':'T','T':'A','G':'C','C':'G'}
    return ''.join(comp[b] for b in reversed(s))

# Build a synthetic 220nt "genomic" sequence with a known NGG PAM placed so that
# a pegRNA edit (SNV) sits within 10nt of the nick site (cut_pos = pam_pos-3), a
# realistic design case. Random flanks + a hand-placed core so PAM/edit geometry
# is known exactly, not just hoped for.
random.seed(7)
flank_up = ''.join(random.choice('ACGT') for _ in range(90))
# Core: 20nt spacer target + NGG PAM + 20nt downstream containing the edit
spacer_target = "ACGTTGACCTGGAACGTTCA"   # 20 nt, arbitrary but fixed
pam = "TGG"                              # NGG PAM immediately after spacer (protospacer+PAM on + strand)
downstream = "CGATCCGTAAGCTTGGCCAATGGCCTTAAGGCCTTAACC"  # 40 nt after PAM; edit placed within this
flank_down = ''.join(random.choice('ACGT') for _ in range(90))

genomic_plus = flank_up + spacer_target + pam + downstream + flank_down

# cut site (Cas9 nick, PE uses nCas9 nick on non-target strand 3bp upstream of PAM)
pam_pos = len(flank_up) + len(spacer_target)          # 0-based index of PAM start
cut_pos = pam_pos - 3                                  # nick 3bp upstream of PAM (standard Cas9/PE geometry)

# Place the intended edit 6 nt downstream of the nick (well within PE's 1-30nt window,
# and within a typical 10-20nt RTT), inside `downstream`.
edit_offset_from_pam_end = 5   # edit is 5 nt into `downstream`, i.e. pam_pos+3+5
edit_abs_pos = pam_pos + 3 + edit_offset_from_pam_end
ref_base = genomic_plus[edit_abs_pos]
alt_base = {'A':'G','C':'T','G':'A','T':'C'}[ref_base]  # transition, arbitrary but deterministic
assert ref_base != alt_base

edited_plus = genomic_plus[:edit_abs_pos] + alt_base + genomic_plus[edit_abs_pos+1:]

# PRIDICT2 sequence format: xxxx(ref/alt)xxxx, edit-flanking bases OUTSIDE brackets,
# minimum 100nt up/downstream of the bracket.
pridict_seq = genomic_plus[:edit_abs_pos] + f"({ref_base}/{alt_base})" + genomic_plus[edit_abs_pos+1:]

print("GENOMIC_PLUS_LEN", len(genomic_plus))
print("PAM_POS(0-based)", pam_pos, "PAM", genomic_plus[pam_pos:pam_pos+3])
print("SPACER", genomic_plus[pam_pos-20:pam_pos])
print("CUT_POS(0-based, 3bp upstream of PAM)", cut_pos)
print("EDIT_ABS_POS(0-based)", edit_abs_pos, "dist_from_cut", edit_abs_pos-cut_pos)
print("REF/ALT", ref_base, alt_base)
print("PRIDICT_SEQ_LEN", len(pridict_seq))
print()
print("PRIDICT_SEQ=", pridict_seq)

with open("synthetic_variant1.txt","w") as f:
    f.write(pridict_seq)

# CSV per SKILL.md's DOCUMENTED format: columns sequence_name, sequence
with open("skill_documented_batch.csv","w") as f:
    f.write("sequence_name,sequence\n")
    f.write(f"SYN_VAR1,{pridict_seq}\n")

# CSV per the REAL required format: columns sequence_name, editseq
with open("corrected_batch.csv","w") as f:
    f.write("sequence_name,editseq\n")
    f.write(f"SYN_VAR1,{pridict_seq}\n")

print("Ground truth written: synthetic_variant1.txt, skill_documented_batch.csv, corrected_batch.csv")
