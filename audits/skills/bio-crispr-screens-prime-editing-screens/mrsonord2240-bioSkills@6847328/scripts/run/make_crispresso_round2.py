"""
Fresh CRISPResso2 regression test for the fixed pegRNA-architecture diagram,
using a DIFFERENT locus/composition than the pre-fix audit (which used
160/160/80 = 40/40/20). This one uses 150/210/60 reads = 35%/49%/14%, and a
different spacer/PAM/edit, to independently confirm the fix generalizes
rather than just reproducing the Skill's own worked example.
"""
import random

COMP = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}


def revcomp(s):
    return ''.join(COMP[b] for b in reversed(s))


random.seed(2026)
flank_up = ''.join(random.choice('ACGT') for _ in range(40))
spacer = "TGGCATCGAACTGGTAACCG"      # 20nt, fresh spacer (distinct from other tests)
pam = "AGG"                          # NGG PAM
downstream = "CTTGAGCCATTGACGTAAGCCTAGGTACCAGTTCAAGGTC"  # 41nt after PAM
flank_down = ''.join(random.choice('ACGT') for _ in range(40))

amplicon = flank_up + spacer + pam + downstream + flank_down
pam_pos = len(flank_up) + len(spacer)
cut_pos = pam_pos - 3
edit_dist = 8  # edit 8nt downstream of nick
edit_abs = cut_pos + edit_dist
ref_base = amplicon[edit_abs]
alt_base = {'A': 'C', 'C': 'A', 'G': 'T', 'T': 'G'}[ref_base]  # transversion this time
edited_amplicon = amplicon[:edit_abs] + alt_base + amplicon[edit_abs + 1:]

pbs_len, rtt_len = 12, 16
pbs_geno = amplicon[cut_pos - pbs_len:cut_pos]
rtt_geno = list(amplicon[cut_pos:cut_pos + rtt_len])
rtt_geno[edit_dist] = alt_base
rtt_geno = ''.join(rtt_geno)
pbs_rc = revcomp(pbs_geno)
rtt_rc = revcomp(rtt_geno)
extension_correct = rtt_rc + pbs_rc      # RTT-then-PBS (fixed SKILL.md order)
extension_wrong = pbs_rc + rtt_rc        # PBS-then-RTT (pre-fix documented order)

print("amplicon len", len(amplicon))
print("spacer", spacer, "PAM", amplicon[pam_pos:pam_pos + 3], "cut_pos", cut_pos)
print("edit", ref_base, "->", alt_base, "at", edit_abs, "dist_from_cut", edit_dist)
print("pbs_geno", pbs_geno, "rtt_geno(edited)", rtt_geno)
print("extension_correct (RTT+PBS revcomp)", extension_correct)
print("extension_wrong   (PBS+RTT revcomp)", extension_wrong)
print("revcomp(extension_correct) in edited_amplicon:", revcomp(extension_correct) in edited_amplicon)
print("revcomp(extension_wrong)   in edited_amplicon:", revcomp(extension_wrong) in edited_amplicon)

# 5bp deletion byproduct at the nick (indel outcome distinct from clean ref or clean edit)
del_len = 5
indel_amplicon = amplicon[:cut_pos] + amplicon[cut_pos + del_len:]

n_ref, n_edit, n_indel = 150, 210, 60  # 35% / 49% / 14% of 420 reads -- different mix than pre-fix
reads = []
for i in range(n_ref):
    reads.append((f"REF_{i}", amplicon))
for i in range(n_edit):
    reads.append((f"EDIT_{i}", edited_amplicon))
for i in range(n_indel):
    reads.append((f"DEL_{i}", indel_amplicon))
random.shuffle(reads)

with open("pe_reads_round2.fastq", "w") as f:
    for name, seq in reads:
        qual = "I" * len(seq)
        f.write(f"@{name}\n{seq}\n+\n{qual}\n")

with open("params_round2.txt", "w") as f:
    f.write(f"amplicon={amplicon}\n")
    f.write(f"spacer={spacer}\n")
    f.write(f"extension_correct={extension_correct}\n")
    f.write(f"extension_wrong={extension_wrong}\n")
    f.write(f"n_reads={len(reads)} n_ref={n_ref} n_edit={n_edit} n_indel={n_indel}\n")
    f.write(f"ground_truth_pct: ref_bucket={100*(n_ref+n_indel)/len(reads):.4f} "
            f"prime_edited_bucket={100*n_edit/len(reads):.4f} "
            f"modified_within_ref_bucket={100*n_indel/(n_ref+n_indel):.4f}\n")

print("\nWrote pe_reads_round2.fastq (%d reads) and params_round2.txt" % len(reads))
