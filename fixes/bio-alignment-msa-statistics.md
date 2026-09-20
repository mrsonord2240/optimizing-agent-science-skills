# Fix log: bio-alignment-msa-statistics (alignment/msa-statistics)

## 2026-09-20

Fixer: Sonnet. Branch `fix/al-msastats` (from staging `main` 818f049), worktree `F:\OpenScience\wt\al-msastats`.
First audit: 66, Beta Only, not deployable, no veto, no P0 (P1 x4, P2 x4). A different agent re-audits.

Tools used (versions): Python 3.12.13 (Windows venv `audit-envs\alignment`) with Biopython 1.88, numpy 2.0.2, scipy 1.18.1;
WSL env `alignment` numpy 2.5.3 + Biopython 1.88 (selftest only); R 4.4.3 via `r.sh` with Biostrings 2.74.1, pwalign 1.2.0.
Nothing installed. Evidence data read from `F:\OpenScience\audits\bio-alignment-msa-statistics\run\data\` (read-only).

### Findings fixed (8 of 8 recommendations)

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| No case / gap-glyph / ambiguity normalisation | P1 | SKILL.md "Required Import and Normalisation": inline `normalize_alignment()` (`.`/`~` to `-`, upper-case, optional U to T) and `check_alphabet()`; every inline block starts from the normalised `alignment`. New `examples/msa_utils.py` (names as in msa-parsing: `normalize_alignment`, `is_nucleotide`, `load_alignment`, `example_path`); all examples load through it. Common Errors table rewritten around the silent-wrong symptoms | ran: MAFFT-lowercase HBB6 Ti/Tv 428/355 = 1.21 (was 0.00), DNA IC max 2.000 (was 29.90), IC/entropy/conservation equal the audit's independent references (diff <1e-15); Pfam seed with `.` gaps mean PID1 19.63% (audit reference 19.6%, was 32.0%), identical to the `-` version; hmmalign AFA (lowercase inserts + dots) IC max 5.507 = reference; messy collaborator alignment (case, `.`, X/B/Z/U/`*`, all-gap row): row0/row1 PID2 88.9% (audit reference 88.9%, was 40.0%), IC max 6.23 (was 21.3). Selftest asserts the lowercase / `.` / `~` / U round trip | MAFFT nucleotide output is lowercase: stated in the section |
| PID1 code contradicts its definition | P1 | `pairwise_identity`: PID1 denominator is the span from the pair's first to last aligned column (aligned pairs + internal gap columns); terminal overhangs and unaligned flanks excluded; table row reworded. `examples/identity_matrix.py`: `method` argument (pid1-pid4, argv[2]), default pid4 to match the text, NaN-aware `average_identity` | ran: hand example s1/s2 PID1-4 = 80.0/100/80.0/66.7 (function and vectorized); **135 real pairwise alignments (global/overlap/local; 76 rebuilt as MSA rows with overhang and unaligned flanks) equal `pwalign::pid` PID1-4 to 0.01, 0 differ** (incl. the audit's fragment pair 40.66%, old code 25.00%); Pfam seed (2628 pairs) and stress 300x300 (6000 sampled pairs): vectorized == function == the audit's independent `ref.pid_ref`; 2000x300 matrix PID1 33 s, PID4 29 s | Span definition chosen over a per-sequence "internal gap" definition because only the span matches pwalign on staggered local flanks; both agree on ordinary MSAs (0 differences on ~8600 pairs) |
| `alignment_score` charges gap/gap pairs | P1 | gap/gap pair scores 0; convention stated next to `sum_of_pairs` (residue/gap: flat penalty vs skipped) | ran SKILL.md block on the dotted Pfam seed: -215960 (audit textbook value; was -330976); hand example -12 unchanged and an all-gap column no longer changes it | |
| `information_content` 1e-9 fallback | P1 | letters outside the background dropped, column renormalised (SKILL.md and `entropy_analysis.py`); `check_alphabet()` reports the dropped counts on stderr | ran: IC == audit `ref.ic_ref` (drop-and-renormalise) to 1e-16 on Pfam seed (B/Z present; was +0.58 bits), hmmalign AFA, HBB6 upper and lower; `NNNN` under DNA background = 0, `AAAAN` = 2.0 bits | Same drop rule in `capra_singh_score` (raw JSD*gap penalty vs scipy reference diff 1.7e-16) and `pssm_with_pseudocounts` (differs from the auditor's reference only in columns with B/Z, where the reference keeps them in `n`) |
| `substitution_counts.py` Ti/Tv for protein, misses lowercase/RNA | P2 | Ti/Tv only when `is_nucleotide()`, over A/C/G/T pairs (N/ambiguity pairs reported separately, excluded); load maps U to T; protein prints a note instead of Ti/Tv. SKILL.md text updated | ran: shipped DNA example 4 Ti / 2 Tv / 2 ambiguity pairs (hand count); lowercase HBB6 428/355; protein alignment prints no Ti/Tv | |
| Conservation ignores occupancy | P2 | `column_conservation(..., min_occupancy=0.5)` returns NaN for empty columns and columns with < 50% residues; `average_conservation` returns (mean, columns used) skipping NaN; `conservation_profile` window centred (i-window//2 .. i+window//2) and NaN-aware; same in `conservation_profile.py` | ran: dotted Pfam seed average 34.3% over 118 columns (audit: 34.3% with >50%-gapped columns dropped; was 37.9%); hand example 89.6%; selftest asserts the NaN rule and window | Default 0.5 changes earlier numbers on gappy alignments on purpose; `min_occupancy=0` restores them |
| Stale or inaccurate statements | P2 | Deleted the false "`Array.get((c1,c2),0)` silently returns 0" claim; frontmatter `primary_tool` Bio.Align to Bio.AlignIO plus a sentence that `Bio.Align.read()` objects lack `get_alignment_length()`; `ROBINSON_BACKGROUND` replaced by the NCBI-tabulated published values (sum 1.0; text now Trp 1.3%, Leu 9.0%); "Laplace add-one" reworded to "total pseudocount of 1 spread by background"; Common Errors: removed the non-occurring ZeroDivisionError and Negative IC rows, KeyError corrected to IndexError, real symptoms added; Quick Reference IC range corrected (KL max 2 bits DNA, ~6.2 bits protein) with a "Higher means" column; `sum_of_pairs` warns with the skipped-pair count instead of skipping silently; GUIDANCE2 (standalone package no longer downloadable, no executable) removed from the identity-below-25% action, kept only in the pointer to `alignment/multiple-alignment` | ran: SP 186187 on the dotted seed with the B/Z warning; DistanceCalculator block runs on the normalised seed; published Robinson values asserted equal to the audit's `ROB_TRUE`; the `.get` claim was disproved by the audit run (returns 4.0 in 1.88) | Robinson table now defined once in `msa_utils.py` (three example copies removed) plus the inline SKILL.md block |
| Minor gaps | P2 | "Build a substitution matrix" prompt removed from usage-guide and "custom scoring matrices" removed from the Goal (claim deleted, not written: raw counts only; deleting is the smaller, honest change); built-in `.substitutions` snippet strips `-` first; undefined identities are NaN (all-gap sequence, no aligned pair); shipped `examples/data/example_protein.fasta`, `example_dna.fasta` and `examples/selftest.py` with hand-derived expected numbers (every example runs with no arguments); `entropy_analysis.py` picks protein vs DNA with `is_nucleotide()` instead of guessing from the first row | ran: `.substitutions` snippet has no `-` row/column; all-gap row identity NaN and the average ignores it (10 undefined pairs counted on the messy alignment); `selftest.py` passes on Windows numpy 2.0.2 and WSL numpy 2.5.3 | Kimura example also no longer prints `-0.000` |

### Redundancy removed (usage-guide.md vs SKILL.md)

| deleted passage | now lives |
| --- | --- |
| usage-guide "Prerequisites" (`pip install biopython numpy`) | SKILL.md "Version Compatibility" |
| usage-guide "Key Metrics Explained" table | SKILL.md "Quick Reference: Metrics" (new "Higher means" column) |
| usage-guide Tip 1 (four PID definitions, PID4 recommended) | SKILL.md "Percent Identity Definitions" |
| Tip 2 (conservation/entropy ignore gaps) | SKILL.md `ignore_gaps` arguments and Approach text |
| Tip 3 (BLOSUM62 for proteins, match/mismatch for DNA) | SKILL.md "Alignment Quality Metrics" Approach (added) |
| Tip 4 (gap-rich columns = uncertainty or guide-tree artifacts) | SKILL.md "When to Worry" table (guide-tree artifacts added) |
| Tips 5 and 6 (per-column confidence before inference; aligners support different topologies, report method) | SKILL.md "Quantifying Alignment Uncertainty" (topology/sensitivity sentence added) |
| Tip 7 (<25% identity twilight zone) | SKILL.md "When to Worry" table (already there) |
| SKILL.md PID table "Code" column (repeated the `pairwise_identity` function) | the function directly below |
| SKILL.md Information Content prose stating the Schneider vs KL choice twice | one paragraph after the code block |
| SKILL.md `import math` inside the entropy block and per-block `AlignIO.read` lines | the single normalising import block |
| Robinson table copies in `capra_singh_jsd.py`, `entropy_analysis.py`, `pssm.py` (examples are outside the rule; done against drift) | `examples/msa_utils.py` |

usage-guide keeps: overview, quick start, example prompts, what the agent does (with the normalise step added), and a pointer to SKILL.md sections. Where the two disagreed: usage-guide "PID1 (gap-inclusive)" vs SKILL.md "including internal gaps"; kept the SKILL.md definition, which the audit's pwalign runs support.

### Left unfixed

None of the audit's recommendations. Noted, out of scope:
- The Capra-Singh example still omits Henikoff sequence weights (audit: rank correlation 0.98 with the authors' script); SKILL.md now says so.
- Shannon entropy counts `X` and other letters as residues (it is not alphabet-bound); only IC, JSD and PSSM drop unknown letters.
- `Bio.Align.read()` alignments are documented as unsupported rather than ported.

### Verification

Scratch scripts only, not shipped: clean copy of the Skill, all 9 shipped examples run with no arguments (exit 0, empty stderr); `py_compile` on all 10 .py files; all 17 SKILL.md python blocks executed verbatim on the dotted Pfam seed; `pwalign::pid` comparison via `r.sh` (135 pairs); Windows and WSL `selftest.py`.
