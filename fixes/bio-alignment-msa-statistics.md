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

## 2026-09-21

Fixer: Sonnet. Branch `fix/alignment-msa-statistics` (from staging `main` 431aa55), worktree `F:\OpenScience\wt\alignment-msa-statistics`.
Audit: Production Ready with 5 P2s (report `eval_report_bio-alignment-msa-statistics_result.json`). Commits: `c63c33e` fix, `c263706` split, plus the examples/ pointer refactor (see the scripts/ step).
Tools (versions): Python 3.12 (Windows venv `audit-envs\alignment`) with Biopython 1.88, numpy 2.0.2; WSL env `alignment` numpy 2.5.3 (selftest only). Nothing installed. Data read from `F:\OpenScience\audits\bio-alignment-msa-statistics\run\data\`.

### Findings (5 of 5 fixed)

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| `average_conservation` ZeroDivisionError when no column reaches `min_occupancy` | P2 | SKILL.md block returns `(nan, 0)` and the caller prints "No column has >= min_occupancy residues"; `conservation_profile.py` exits with the same message instead of `nan% over 0` plus a numpy RuntimeWarning | ran the SKILL.md block verbatim on a 4-fragment alignment: `(nan, 0)`; on the dotted Pfam seed: 34.3% over 118 columns (unchanged); CLI on the fragment file prints the message, exit 1 | |
| NaN conservation with no NaN-aware ranking guidance | P2 | SKILL.md "Ranking columns" paragraph and a NaN-filtering `top10` snippet beside Per-Column Conservation | ran the snippet verbatim on the Pfam globin seed: naive top-10 values 1.0 ... 0.37, NaN-free 1.0 ... 0.63 (audit's numbers) | |
| `is_nucleotide()` 0.9 threshold misclassifies IUPAC-rich DNA | P2 | `msa_utils.is_nucleotide`: nucleotide when >= 90% A/C/G/T/U/N, or >= 50% and the remainder is IUPAC ambiguity codes (RYSWKMBDHV); rule stated in SKILL.md; docstring points at `pick_background()`'s label as the check | ran: real HBB MAFFT alignment with 11.9% R/Y/S/W/K/M injected (old rule saw 88.1% and called it protein) is now DNA with the DNA background; Pfam PF00042 and PF00069 seeds, hmmalign AFA, MAFFT protein alignments stay protein; RF00050 RNA seed stays nucleotide | The audit's literal fix "count the full IUPAC set" would classify protein as DNA (full IUPAC letters are ~66% of protein residues), so the 50% core floor is kept |
| selftest leaves gap/gap fix, `is_nucleotide`, JSD smoothing untested | P2 | New `examples/alignment_scores.py` (the two SKILL.md functions, importable); `gap_statistics()` made a function in `gap_statistics.py`; `selftest.py` now asserts `alignment_score` -12 and `sum_of_pairs` 78 (hand-derived) unchanged by two extra all-gap columns, closed-form JSD for a delta column, the gap penalty (`-,G,G` scaled by 2/3), lambda smoothing (lambda 1 and 0.5), `is_nucleotide`/`pick_background` on DNA, protein and 12% IUPAC DNA, the format map, the Kimura 0.85 cut-off and gap totals | ran `selftest.py` on Windows numpy 2.0.2 and WSL numpy 2.5.3; mutation check: is_nucleotide always False, JSD gap penalty removed, JSD smoothing removed, gap_statistics total and gap-free wrong, gap/gap scored, `.aln` mapped to fasta, Kimura cut-off 0.9 -> 8 of 8 killed (audit's 4 survivors included) | Inline SKILL.md/reference blocks stay as the teaching text; `alignment_scores.py` holds the same code so the test exercises what is shipped |
| Minor: `guess_format()` two-way, A2M route, Kimura 0.85 band | P2 | `FORMAT_BY_EXTENSION` (.sto/.stk Stockholm, .aln/.clw Clustal, .phy PHYLIP-relaxed, .nex Nexus, else FASTA), documented in SKILL.md; the A2M sentence in the normalisation block points ragged hmmalign A2M loading to `alignment/alignment-io`; `kimura_protein_distance.py` docstring says inf means p >= 0.85 by convention (formula finite to p ~ 0.854) | ran: the Pfam seed written as .aln/.phy/.nex/.sto and reloaded through `load_alignment` with identical rows; `identity_matrix.py x.aln pid2` and `conservation_profile.py x.phy` ran; A2M raggedness checked against `alignment-io/SKILL.md` "A2M / A3M Conventions" (docs) | |

Also ran all 9 shipped examples with no arguments under `-W error::RuntimeWarning` (exit 0, empty stderr), `py_compile` on every changed `.py`, and, after the split, every complete Python block of SKILL.md and `references/` in one namespace on the dotted Pfam seed (13 run, 5 `...` skeletons skipped): `alignment_score` -215960 and SP 186187 as in the 2026-09-20 fix, average conservation 34.3% over 118 columns.

### Redundancy

usage-guide.md and SKILL.md were already deduplicated on 2026-09-20; no change. New passages were added once (ranking snippet, IUPAC rule, format map).

### Split (SKILL.md 499 -> 291 lines)

Verbatim moves (non-blank lines compared before vs SKILL.md + `references/`: only the 4 lines that pointed at moved sections differ; 18 Python fences parse, the bash fence passes `bash -n`):

| old location (SKILL.md section) | new home |
| --- | --- |
| Capra-Singh Jensen-Shannon Divergence | `references/capra-singh-jsd.md` |
| Substitution Counts (with Built-in Pairwise Substitutions, BLOSUM62 Lambda) | `references/substitution-counts.md` |
| Information Content (Shannon entropy, KL) + PSSM + Neff + MI-APC | `references/information-content-pssm.md` |
| Gap Statistics | `references/gap-statistics.md` |
| Alignment Quality Metrics (alignment_score, Sum of Pairs, SP bias) | `references/alignment-quality-scores.md` |
| Distance Correction Models | `references/distance-correction.md` |
| References (bibliography) | `references/bibliography.md` |

Pointer edits: "use `pssm_with_pseudocounts()` above" and "`information_content()` earlier in this skill" now name `references/information-content-pssm.md`; two decision-table rows gained a reference pointer; a "Reference Files" index was added.

### scripts/ step (Sam, 2026-09-21): inline copies replaced by pointers to examples/ (`refactor` commit, SKILL.md 291 -> 251 lines)

Sam's answer: where a 15+ line block duplicates an `examples/` script, delete the inline copy and point at the example. Nothing was moved to `scripts/` (the examples already are the runnable code).

| old location (inline block) | now |
| --- | --- |
| SKILL.md "Required Import": `normalize_alignment`, `check_alphabet`, `AlignIO.read` line (30 lines) | 4-line import from `examples/msa_utils.py` + `load_alignment`; the `upper=False` A2M/A3M note and the ragged-A2M pointer moved into the prose and into `normalize_alignment`'s docstring |
| SKILL.md `pairwise_identity` (24 lines) | `from identity_matrix import pairwise_identity` (`examples/identity_matrix.py`) |
| SKILL.md `average_conservation` (17 lines) | `from conservation_profile import average_conservation`; the function did not exist in the example, so it was added there (the CLI now uses it) |
| references/information-content-pssm.md `shannon_entropy` (19 lines), `ROBINSON_BACKGROUND` + `DNA_UNIFORM` + `information_content` (16 lines) | imports from `examples/entropy_analysis.py` and `examples/msa_utils.py` (`pick_background`); run command `python examples/entropy_analysis.py [alignment]`; the "values below" and "defined in the IC section above" pointers now name `examples/msa_utils.py` |
| references/alignment-quality-scores.md `alignment_score` (19 lines), `sum_of_pairs` (18 lines) | imports from `examples/alignment_scores.py`; run command `python examples/alignment_scores.py [alignment]` |

Where inline and example differed the example version was kept: `check_alphabet` (example prints counts and the dropped fraction, takes a label), the `ValueError` text of `pairwise_identity`. Removed lines checked against the examples programmatically: the 15 not found verbatim are the equivalent differently-written lines above plus the pointer sentence. Blocks under 15 lines (`column_conservation`, `conservation_profile`, `gap_profile`, the NaN ranking snippet) and `...` skeletons stay inline.

Verified: all 13 complete Python blocks of SKILL.md and `references/` run verbatim in one namespace (cwd = Skill directory) on the dotted Pfam seed with the same numbers as before (`alignment_score` -215960, SP 186187, mean conservation 34.3% over 118 columns, top-10 `[17, 77, 11, ...]`); all 9 examples run with no arguments under `-W error` (exit 0, empty stderr); `selftest.py` passes on Windows numpy 2.0.2 and WSL numpy 2.5.3; `conservation_profile.py` on the sparse fragment file still exits with the message.

### Left unfixed

None of the 5 findings. Noted, not changed:
- Kimura `inf` for 0.85 <= p < 0.854 is kept as a documented convention rather than extended to the formula's true pole (a cut-off change would alter shipped behaviour the audit's EMBOSS `distmat` cross-check accepted).
- A2M loading is not implemented here (ragged hmmalign A2M has no AlignIO reader); the Skill points to `alignment/alignment-io`.

## 2026-09-21 (final pass, Phase 1)

Fixer/auditor: Sonnet. Branch `fix/alignment-msa-statistics`, worktree `F:\OpenScience\wt\alignment-msa-statistics`, tip commit `f3a7a62`. Checkpoint: `F:\OpenScience\audits\_final_pass\bio-alignment-msa-statistics\CHECKPOINT.md`.

Walked every runnable block (not just what earlier passes touched): 13 non-skeleton Python blocks in `SKILL.md`+`references/*.md` (one namespace, dotted Pfam seed) and all 11 files under `examples/` (9 examples + `msa_utils.py` + `selftest.py`, Windows venv and WSL) — all ran clean, numbers match the 2026-09-20/21 fix log exactly, no defects found. Also re-ran CLI examples on real (non-toy) data and confirmed the `.aln`/`.phy`/`.nex`/`.sto` format round-trip via `load_alignment`.

### Findings (1 of 1 fixed)

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| `references/distance-correction.md` `modeltest-ng` bash block had never been executed by any prior fixer or auditor | P2 (found this pass) | Installed ModelTest-NG 0.1.7 into WSL env `alignment` (bioconda, public download, install-lock protocol, before/after `micromamba list --json` diff shows only this package added); added a "Checked on ModelTest-NG 0.1.7" note plus the >=3-real-sequence / no-ragged-input caveat next to the block; tool recorded in `audit-envs\alignment\TOOLS.md` | ran `modeltest-ng -i alignment.fasta -d nt -t ml -p 4` on the real 6-sequence HBB CDS alignment: best model K80+I (BIC) / TPM2uf+I (AIC/AICc); `-d aa -t ml -p 4` on the 8-sequence globin protein alignment: DAYHOFF+G4 (BIC) / LG+I+F (AIC) | the shipped 3-row toy `example_dna.fasta` and the A2M `globins_hmmalign.afa` both fail to parse (needs >=3 clean sequences); real, normalised alignments work |

### Left unfixed

None. The two 2026-09-21 "left unfixed" items above were re-checked and remain deliberate, settled design decisions (not blocked on any resource): nothing here needs Sam's decision.
