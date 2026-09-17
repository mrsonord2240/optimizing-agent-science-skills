"""
CRISPResso2's prime-editing quantification classifies a read as "Prime-edited" by
matching the edited allele against the amplicon built from
--prime_editing_pegRNA_extension_seq (reverse-complemented back onto the genomic
strand). This script performs that same substring/orientation check directly in
Python, independent of the Skill's own code, on a FRESH locus (not the one in
SKILL.md's own worked example) to confirm the fixed pegRNA-extension order
(RTT-then-PBS) is the one that can actually match, and the pre-fix documented
order (PBS-then-RTT) cannot -- without needing a live CRISPResso2/Docker run.

A live CRISPResso2 2.3.4 (Docker) run against this same locus was attempted this
audit pass (see run/make_crispresso_round2.py + params_round2.txt) but did not
complete: `docker run` hung with the container stuck in "Created" state across
four independent attempts (including a fresh mount directory, a previously-proven
mount directory, and a bare `docker run --rm ... CRISPResso --version` with no
mount at all), while `docker version`/`docker ps`/`docker rm` all responded
normally throughout -- a Docker Desktop container-start hang on this shared
machine, not a Skill defect. The pre-fix audit DID execute a real CRISPResso2 run
(see F:\\OpenScience\\audits\\_pre-fix-20260916\\...\\eval_viewer, Input 3) that
confirmed this exact mechanism on a different locus (40.0% Prime-edited vs 40.0%
true); this script is the substitute regression check for this pass.
"""
import random

COMP = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}


def revcomp(s):
    return ''.join(COMP[b] for b in reversed(s))


# Rebuild the same locus as make_crispresso_round2.py (self-contained, no import
# side effects from re-running that script's file-writing top level).
random.seed(2026)
flank_up = ''.join(random.choice('ACGT') for _ in range(40))
spacer = "TGGCATCGAACTGGTAACCG"
pam = "AGG"
downstream = "CTTGAGCCATTGACGTAAGCCTAGGTACCAGTTCAAGGTC"
flank_down = ''.join(random.choice('ACGT') for _ in range(40))
amplicon = flank_up + spacer + pam + downstream + flank_down
pam_pos = len(flank_up) + len(spacer)
cut_pos = pam_pos - 3
edit_dist = 8
edit_abs = cut_pos + edit_dist
ref_base = amplicon[edit_abs]
alt_base = {'A': 'C', 'C': 'A', 'G': 'T', 'T': 'G'}[ref_base]
edited_amplicon = amplicon[:edit_abs] + alt_base + amplicon[edit_abs + 1:]
pbs_len, rtt_len = 12, 16
pbs_geno = amplicon[cut_pos - pbs_len:cut_pos]
rtt_geno = list(amplicon[cut_pos:cut_pos + rtt_len])
rtt_geno[edit_dist] = alt_base
rtt_geno = ''.join(rtt_geno)
extension_correct = revcomp(rtt_geno) + revcomp(pbs_geno)
extension_wrong = revcomp(pbs_geno) + revcomp(rtt_geno)

correct_found = revcomp(extension_correct) in edited_amplicon
wrong_found = revcomp(extension_wrong) in edited_amplicon

print("revcomp(extension_correct) in edited_amplicon:", correct_found)
print("revcomp(extension_wrong)   in edited_amplicon:", wrong_found)
print("revcomp(extension_correct) in reference amplicon (should be False):",
      revcomp(extension_correct) in amplicon)

assert correct_found, "Fixed RTT-then-PBS order should match the edited allele"
assert not wrong_found, "Pre-fix PBS-then-RTT order should NOT match the edited allele"
print("\nPASS: fixed pegRNA-extension order (RTT-then-PBS) is the only one that can "
      "match CRISPResso2's edited-allele orientation check on this fresh locus; the "
      "pre-fix documented order (PBS-then-RTT) still cannot match, confirming SKILL.md's "
      "own warning text about the silent-zero symptom is accurate.")
