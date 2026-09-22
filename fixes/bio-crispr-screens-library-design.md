# Fix log: bio-crispr-screens-library-design (2026-09-16)

Branch `fix/r2-crispr-b` @ `F:\OpenScience\wt\crispr-b`, commit `829444b`.
Scope: Sam's 2026-09-16 override — fix every P0/P1/P2 in the report, plus the
two defects AUDIT.md names as "what keeps it at 81": the missing guide-spacing
filter and the SKILL.md/usage-guide.md Azimuth contradiction.

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| No minimum-spacing/independence filter on candidate guides — `find_sgrna_candidates` filters composition only; a short/GC-tied region can select near-duplicate guides that both count toward the per-gene quota | P1 | Added `select_independent_guides()` (greedy, `min_spacing=5`) to SKILL.md's "Score and Rank sgRNAs" section, wired into the Approach text and a new Quantitative-Thresholds row | ran — real TP53 CDS (NM_000546.6, fetched live via NCBI efetch `fasta_cds_na`), not synthetic. Naive top-12-by-score selection returned a pair 1nt apart (19/20nt shared sequence, min pairwise distance 1nt); `select_independent_guides(min_spacing=5)` on the same candidate pool raised the guaranteed minimum pairwise distance to 5nt while still filling all 12 slots from the next-best candidates. Script + output kept in this session's scratchpad (`verify_spacing_filter.py`) | This was the audit's own primary "what would flip it to 85+" item |
| SKILL.md vs usage-guide.md contradiction on Azimuth 2.0 usability | P1 | Rewrote SKILL.md's Version Compatibility section: states plainly Azimuth 2.0 (the `azimuth` PyPI package) must not be called, names the confirmed failure, and gives an ordered recommendation (1. this Skill's own GC heuristic, always available; 2. Broad CRISPick or R `crisprScore::getAzimuthScores()` for real Rule Set 2). Also fixed the "sgRNA Library Design" tool-list bullet that still named the broken `azimuth` package | ran — `import azimuth.model_comparison` reproduced live on this machine (Python 3.12, shared venv): `SyntaxError: Missing parentheses in call to 'print'`, matching TOOLS.md §3 and the audit's own live reproduction. CRISPick/crisprScore were **not** installed/run here (crisprScore isn't in TOOLS.md's installed-R-packages table) — flagged as unverified-in-this-env in the new text rather than presented as confirmed | Resolved in favor of usage-guide.md's version (Azimuth unusable), which matched what TOOLS.md and the audit both independently confirmed |
| Shipped `examples/design_library.py` implements a different, simpler algorithm (random sequences + GC heuristic) than the documented CDS/TSS method | P2 | Rewrote the script to call `find_sgrna_candidates`/`annotate_exon_position`/`select_independent_guides` against a synthetic per-gene CDS, same functions SKILL.md documents | ran — exit 0, 142 rows, 0 NaN in `sequence`, all 20 genes at the 4-guide quota, all spacers 20nt; independently re-checked with `pandas.read_csv` + `value_counts` | Kept the synthetic-CDS approach (not a real Ensembl pull) to keep the example runnable offline, same as before |
| Demo control-guide proportions (43.7%) don't match the ~1% NTC genome-scale target and carry no caveat | P2 | Added an inline comment ahead of the controls section and in the control-fraction print line, pointing at SKILL.md's Control Guides table | ran — comment appears in stdout and in the script; not a functional change | |
| No explicit stop-and-ask escape hatch for missing required inputs | P2 | Added step 0 to usage-guide.md's "What the Agent Will Do": stop and confirm gene list / genome / chemistry / TSS-or-exon source before designing | docs — text-only change, no code to run | |
| (unticketed, evidenced by Input 3) Neither doc warns the 75bp Calabrese CRISPRa window can undersupply the 6-guide quota | — | Added a caveat to `crispra_window()`'s docstring | docs — matches the audit's own Input-3 finding (2/4 synthetic TFs undersupplied) | Cheap, bundled in since already touching that function's neighborhood |

## Left unfixed

Nothing from `recommendations[]` or AUDIT.md's library-design section was left
unfixed. Two related-but-broader gaps were noted and deliberately left alone
per the brief's "keep diffs minimal, no broader coverage" rule:
- `crisprScore` (R) was not installed/smoke-tested in this pass — TOOLS.md
  didn't cover it, and installing it belongs to a tooling pass, not this fix.
  The new SKILL.md text says so explicitly rather than presenting it as
  verified.
- Non-ACGT input validation (static-score dock, not in `recommendations[]`)
  was left alone — no crash observed, out of the ticketed scope.

## Verification method notes

- All three changed files: `design_library.py` (`py_compile`, then executed
  from its actual worktree location), `SKILL.md`'s three python code blocks
  (extracted by regex, `py_compile`'d individually), `usage-guide.md` (prose
  only, no code).
- `select_independent_guides()` was verified twice: once against the
  synthetic-CDS example script (end-to-end run) and once standalone against
  a real gene's CDS (TP53, NM_000546.6) pulled live from NCBI's public,
  unauthenticated E-utilities — not just import-checked.
- Nothing installed into the shared venv or R library; no version changes.


# 2026-09-21: P2 fixes, redundancy pass, split

Branch `fix/crispr-screens-library-design` @ `F:\OpenScience\wt\crispr-screens-library-design`, commits `24de7b8` (fix), `f5995db` (redundancy), `41b30ac` (split). Env `crispr-screen-analyst` (Python 3.12, pandas/biopython from the shared venv). Audit: 3 P2s.

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| `find_sgrna_candidates` silently returns 0 candidates for lowercase input | P2 | `cds_sequence = cds_sequence.upper()` at the top of the function, in SKILL.md and in the verbatim copy in `examples/design_library.py` | ran: function extracted from SKILL.md, 900-nt random CDS gives 98 candidates upper and 98 lower, DataFrames equal, spacers uppercase; `design_library.py` re-run exit 0 and `py_compile`d | |
| Azimuth alternative (CRISPick / `crisprScore::getAzimuthScores()`) unverified here | P2 | none | n/a | left unfixed, see below |
| SKILL.md single 342-line file, usage-guide duplicates it | P2 | usage-guide de-duplicated; SKILL.md split 337 -> 228 lines into 4 `references/` files | ran: non-blank line multiset compare, ast.parse of every python fence, fence balance | see tables below |

## Left unfixed

- CRISPick / `crisprScore::getAzimuthScores()` unverified: `crisprScore` is not in `crispr-screen-analyst`'s `R-lib` (checked `ls R-lib` and TOOLS.md) and the brief forbids installing into the env; CRISPick is a web portal (no scriptable install). SKILL.md keeps its "verify the call signature" wording, which is accurate.
- The two `Related Skills` lists (SKILL.md and usage-guide.md) were kept: they are navigation, the brief assigns them to the guide, and SKILL.md's is the repo convention. Not a fact the agent acts on twice.

## Deleted passage -> new home

| deleted (usage-guide.md unless noted) | now |
| --- | --- |
| Prerequisites: CRISPOR clone, biopython/pandas/numpy, FlashFry JAR, crisprDesignData | SKILL.md Version Compatibility "Install:" paragraph (garbled comment line and the archived-Azimuth note dropped; SKILL.md already says Azimuth is unusable) |
| Prerequisites: required inputs; "What the Agent Will Do" step 0 and step 10 | SKILL.md "sgRNA Library Design": stop-and-confirm paragraph and Deliverable line |
| What the Agent Will Do steps 1-9 | already in SKILL.md sections (decision tree, scoring, filters, controls, oligo); guide now points to SKILL.md. Step 4 "Score on-target with Rule Set 2 / Azimuth" contradicted SKILL.md's "Azimuth must not be called" and step 9 "Twist 92K/244K" was wrong (SKILL.md: Twist ~300 nt; 92K = GenScript, 244K = Agilent); both dropped |
| Tips 1 (off-the-shelf libraries), 6 (Cas9 vs Cas12a not mixable) | SKILL.md decision tree, "Off-the-shelf first" paragraph |
| Tips 2 (tissue-specific TSS), 3 (plasmid sequencing), 4 (subpool), 5 (paralog GI), 7 (BE/PE efficiency) | already in SKILL.md: CRISPRi/a Critical nuance, Library QC, Subpool design, Library Composition, base-editor bullet |
| Library Specification Reference Table, Control Composition table | SKILL.md Genome-Wide Library table (now `references/library-catalog-and-pam.md`), Control Guides table, Quantitative Thresholds (coverage 500x) |
| SKILL.md Failure Modes "Wrong TSS" | SKILL.md CRISPRi/a "Critical nuance" (mechanism +/-100 bp, 1-10 kb annotation error, symptom) |
| SKILL.md Failure Modes "Wrong control proportion" | SKILL.md Control Guides "Critical pitfall" (<100 NTC, unstable null, erratic FDR) |
| SKILL.md Thresholds rows: CRISPRi window, CRISPRa window, NTCs, MIT specificity, library skew | decision-tree table, Control Guides table, Off-Target Scoring table, Library QC table; one pointer line under Thresholds |
| SKILL.md Common Errors rows: wrong TSS, Gini >0.3 | Failure Modes / CRISPRi-a Critical nuance; pointer line under Common Errors |

## Split (SKILL.md 337 -> 228 lines)

Verbatim moves: `references/crispri-crispra-tss.md`, `references/library-catalog-and-pam.md` (Genome-Wide Library Selection + PAM Variants), `references/oligo-design.md`, `references/failure-modes.md`. SKILL.md keeps the decision tree, scoring taxonomy, ranking code, controls, QC, thresholds, Common Errors, and gets a "Reference Files" index plus pointers at the decision-tree rows, Deliverable, Library QC and Common Errors.

## Runnable code to scripts/ (commit `5a732bb`; SKILL.md 228 -> 186 lines)

| old location | new home | verified |
| --- | --- | --- |
| `references/crispri-crispra-tss.md` python block (`crispri_window`, `crispra_window`) | `scripts/tss_windows.py` (verbatim + argparse CLI) | ran: 4 mode/strand outputs asserted; audit `input2_crispri_library.csv` (30 guides) and `input3_crispra_library.csv` (8 guides) all inside the windows the script prints for TSS 0 |
| `references/oligo-design.md` python block (`build_oligo`) | `scripts/build_oligo.py` (verbatim + argparse CLI) | ran: subpool 1 and 2 outputs asserted exactly (71 nt), lowercase spacer accepted, 20 targeting spacers from audit `input6_design_library_output.csv` build within the 200 nt budget |
| SKILL.md python block (`find_sgrna_candidates`, `annotate_exon_position`, `select_independent_guides`) | not moved: duplicated `examples/design_library.py` verbatim, so the copy was deleted and SKILL.md points to the example; the docstring rationale (5-65% CDS window, spacing filter and TP53 check, lowercase note) kept as prose | example re-run exit 0 |

Both scripts' docstring rationale for the windows stays in `scripts/tss_windows.py`; the reference keeps only the CRISPRa quota caveat as prose. No python fences remain in SKILL.md or `references/`.


# 2026-09-21: final pass, phase 1

Branch `fix/crispr-screens-library-design` @ `F:\OpenScience\wt\crispr-screens-library-design`, commit `f7185c8`. Env `crispr-screen-analyst`. Checkpoint: `F:\OpenScience\audits\_final_pass\bio-crispr-screens-library-design\CHECKPOINT.md`.

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| `crisprScore::getAzimuthScores()` unverified (prior pass: not in R-lib) | P2 (revisit) | Installed crisprScore 1.10.0 (Bioconductor 3.20) into `crispr-screen-analyst`'s R-lib under `install.lock`; rewrote SKILL.md's Version Compatibility text from "neither was installed or smoke-tested" to the precise verified state | ran: `library(crisprScore)` loads from R-lib alone; `getAzimuthScores` confirmed as a real exported function, signature `(sequences, fork=FALSE)` matching the vignette; calling it on the vignette's own 30nt example reaches `basiliskStart()` and fails there (`LibMambaUnsatisfiableError: nothing provides vc 9.* needed by python-2.7.12-0` -- conda-forge/bioconda no longer carry the VC9 runtime Windows Python 2.7 needs) | Real upstream blocker, not a missing install step. 21 new R package names copied into R-lib, 0 existing versions changed (see `TOOLS.md`). Also found and fixed a separate toolchain trap: `BiocManager::install` tries to compile too-new `reticulate` from source and fails on this machine's g++ 15; `options(install.packages.compile.from.source="never")` uses the existing CRAN Windows binary instead -- logged in `TOOLS.md` so it isn't rediscovered |

## Left unfixed (this phase)

- `getAzimuthScores()` cannot execute here: needs a conda channel that still hosts `vc=9.*` + `python=2.7` win-64 builds, which conda-forge/bioconda have dropped. Pinning to an unmaintained legacy channel snapshot to run a 10+-year-old Python 2 model was judged out of scope for this pass. CRISPick (web submission) remains the working real-Rule-Set-2 path; SKILL.md says so.

## Re-verification (no changes needed)

Walked every other runnable block: `examples/design_library.py` (142 rows, matches exactly), `select_independent_guides()` independently re-verified against a fresh live NCBI fetch of TP53, `scripts/tss_windows.py` (all 4 mode/strand combos), `scripts/build_oligo.py` (both subpools, lowercase input, budget-overflow raise). All matched documented/expected output; no defects found.
