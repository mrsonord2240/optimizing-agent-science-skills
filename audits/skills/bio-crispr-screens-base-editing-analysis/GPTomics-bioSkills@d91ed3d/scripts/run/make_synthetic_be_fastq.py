"""
Build a synthetic base-editing (CBE) amplicon FASTQ with planted C->T conversions
at a known target position and a known bystander position, as ground truth.

No real base-editing amplicon FASTQ was found in CRISPResso2's published test set
(only Cas9-nuclease samples) -- see public-data/editing/README.md. Per the audit
brief, we build a synthetic amplicon instead, with planted conversions at known
bystander positions and rates as ground truth.

Design:
  - 150bp amplicon, no repeats, unambiguous NW alignment.
  - 20nt protospacer + NGG PAM inserted at a fixed offset.
  - Target C at protospacer position 5 (from PAM-distal end, 1-indexed) -- inside
    the canonical CBE editing window (positions 4-8).
  - Bystander C at protospacer position 7 -- also inside the window.
  - No other C in the 4-8 window (so conversion at other window positions cannot
    happen and confound the ground truth).
  - Four read populations, exactly as planned:
      40% unmodified            (neither C converted)
      30% target-only edited    (position 5 C->T only)
      20% target+bystander      (positions 5 and 7 C->T)
      10% bystander-only edited (position 7 C->T only)
    Total N=200 reads, single-end, full-amplicon-length reads (150bp), Q40 flat
    quality, no sequencing errors and no indels (clean substitution-only ground
    truth so the base-editor code path is being tested, not alignment robustness).
"""
import random

random.seed(20260916)

UP = "GCTAGCATCGATGCATGGATCGTAGCTAGCATGCATCGTAGCTAGGATCGCATGCTAGCATG"  # 63nt, no stray NGG near end
PROTOSPACER = "TGATCACGTAGCATGCACG"  # 19nt placeholder, fixed below to 20nt with explicit C's
# Build protospacer explicitly, 20nt, PAM-distal position 1 .. PAM-proximal position 20:
# position:  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20
# base:      T  G  A  T  C  A  C  G  T  A  G  C  A  T  G  C  A  C  G  T
# target C at position 5, bystander C at position 7 -- both inside window 4-8.
# positions 4,6,8 in the window are A, A, G (not C) so they cannot confound.
PROTOSPACER = "TGATCACGTAGCATGCACGT"
assert len(PROTOSPACER) == 20, len(PROTOSPACER)
assert PROTOSPACER[4] == "C"  # 0-indexed 4 == 1-indexed position 5 (target)
assert PROTOSPACER[6] == "C"  # 0-indexed 6 == 1-indexed position 7 (bystander)
for i in (3, 5, 7):  # 1-indexed positions 4, 6, 8 must NOT be C
    assert PROTOSPACER[i] != "C", (i, PROTOSPACER[i])
PAM = "TGG"
DOWN = "CATGCTAGCATGGATCGTACGATGCATCGTAGCATGCATGGATCGATGCATCGATGCATGCATCGTAGCTAGCATGCATCG"

AMPLICON = UP + PROTOSPACER + PAM + DOWN
assert len(AMPLICON) >= 140, len(AMPLICON)

TARGET_IDX = len(UP) + 4      # 0-indexed position of the target C in the amplicon
BYSTANDER_IDX = len(UP) + 6   # 0-indexed position of the bystander C in the amplicon
assert AMPLICON[TARGET_IDX] == "C"
assert AMPLICON[BYSTANDER_IDX] == "C"

N_READS = 200
POPULATIONS = [
    ("unmodified", 0.40, False, False),
    ("target_only", 0.30, True, False),
    ("target_and_bystander", 0.20, True, True),
    ("bystander_only", 0.10, False, True),
]
counts = {}
remaining = N_READS
for i, (name, frac, _, _) in enumerate(POPULATIONS):
    if i == len(POPULATIONS) - 1:
        counts[name] = remaining
    else:
        c = round(N_READS * frac)
        counts[name] = c
        remaining -= c
assert sum(counts.values()) == N_READS, counts

records = []
qual = "I" * len(AMPLICON)  # flat Q40
read_id = 0
for name, frac, edit_target, edit_bystander in POPULATIONS:
    n = counts[name]
    for _ in range(n):
        seq = list(AMPLICON)
        if edit_target:
            seq[TARGET_IDX] = "T"
        if edit_bystander:
            seq[BYSTANDER_IDX] = "T"
        seq = "".join(seq)
        read_id += 1
        records.append((f"@SYN_BE_{read_id:04d}_{name}", seq, qual))

random.shuffle(records)

with open("synthetic_cbe.fastq", "w") as f:
    for rid, seq, q in records:
        f.write(f"{rid}\n{seq}\n+\n{q}\n")

with open("ground_truth.txt", "w") as f:
    f.write(f"amplicon_seq\t{AMPLICON}\n")
    f.write(f"guide_seq\t{PROTOSPACER}\n")
    f.write(f"target_position_0indexed\t{TARGET_IDX}\n")
    f.write(f"bystander_position_0indexed\t{BYSTANDER_IDX}\n")
    f.write(f"n_reads\t{N_READS}\n")
    for name, frac, edit_target, edit_bystander in POPULATIONS:
        f.write(f"pop_{name}\t{counts[name]}\ttarget_edited={edit_target}\tbystander_edited={edit_bystander}\n")
    target_editing_rate = (counts["target_only"] + counts["target_and_bystander"]) / N_READS
    bystander_editing_rate = (counts["bystander_only"] + counts["target_and_bystander"]) / N_READS
    f.write(f"ground_truth_target_editing_pct\t{target_editing_rate*100:.2f}\n")
    f.write(f"ground_truth_bystander_editing_pct\t{bystander_editing_rate*100:.2f}\n")

print("Wrote synthetic_cbe.fastq with", N_READS, "reads")
print("Amplicon:", AMPLICON)
print("Protospacer (20nt):", PROTOSPACER, " PAM:", PAM)
print("Target C at amplicon 0-idx", TARGET_IDX, "| Bystander C at amplicon 0-idx", BYSTANDER_IDX)
print("Population counts:", counts)
print(f"Ground truth target editing % = {(counts['target_only']+counts['target_and_bystander'])/N_READS*100:.2f}")
print(f"Ground truth bystander editing % = {(counts['bystander_only']+counts['target_and_bystander'])/N_READS*100:.2f}")
