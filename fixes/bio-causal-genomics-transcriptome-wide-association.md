# Fix log: bio-causal-genomics-transcriptome-wide-association (2026-09-19)

Source: `causal-genomics/transcriptome-wide-association`. Audit: 80/100, Limited Release, deployable,
2 P1 + 3 P2 open. Fix commit: `fix/cg-twas` @ `4a67b94` in
`F:\OpenScience\external\mrsonord2240__bioSkills` (worktree `F:\OpenScience\wt\cg-twas`, not merged).

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| `pip install pyfocus` (bare, as usage-guide.md instructed) crashes every `focus` call: pandas>=2.2 removed `delim_whitespace`, called throughout pyfocus 0.802's data-loading code | P1 | Pinned `pandas<2.2` + `setuptools<81` (pyfocus imports `pkg_resources`, gone from recent setuptools) in SKILL.md Tool Install Notes, the FOCUS section, `examples/focus_finemap.sh`, and usage-guide.md | ran | The pin alone is not sufficient -- see next row, found only by pushing the verification further than the pin |
| Pinning pandas alone still crashes: `AttributeError: module 'numpy' has no attribute 'warnings'` -- `ldref.py`/`exprref.py` call the removed `np.warnings` alias, and no numpy version with Python 3.11/3.12 wheels still has it | P1 (same root issue as above; audit's own suggested fix was incomplete) | Documented a 2-line post-install source patch (`sed`, replacing `np.warnings.*` with the already-imported/added stdlib `warnings` module) in SKILL.md Tool Install Notes | ran -- isolated fresh venv (Python 3.12), patched pyfocus 0.802: `focus finemap` then runs through real GWAS parsing, LD-ref parsing, weight-DB parsing, and the full genome-wide independent-region scan with no crash (own-fixture data; stopped at "no overlapping weights" only because the test used an S-PrediXcan-schema DB, not a real FOCUS DB -- a fixture limitation, not a Skill bug) | Verified in a scratchpad venv, never the shared candidate env (`twas-venv`), per the no-shared-version-change rule |
| `focus finemap` also crashes with "Please specify independent regions location..." unless `--locations` is passed, even single-ancestry -- contradicts the shipped example's own comment that it's optional | P1-adjacent (blocks the same fix's own verification) | Added `--locations 38:EUR` to SKILL.md's FOCUS CLI example and `examples/focus_finemap.sh`; corrected the wrong comment | ran (real pyfocus 0.802 CLI) | |
| FUSION.post_process.R crashes on single-SNP ("top1") genes: `Error in wgt.matrix[qc$flip, ] : incorrect number of dimensions` | P1 | Documented the crash, root cause (`wgt.matrix[m.keep,]` missing `drop=FALSE`), and a 2-line patch in Common Errors | ran -- reproduced the exact crash on real planted FUSION fixtures (`gusevlab/fusion_twas` HEAD, GENE1/GENE2 synthetic top1 weights over a real 957-indiv/14389-SNP LD panel) | |
| The documented single-line patch (`drop=FALSE` on `wgt.matrix`) is not sufficient by itself | P1 (same finding, deeper) | Documented a second required `drop=FALSE` on `cur.genos = genos$bed[,m[m.keep]]` (the very next line) in Common Errors, both occurrences (lines ~168/170 and ~251/254) | ran -- with both patches, `FUSION.post_process.R` completes and correctly retains the true signal (GENE1, JOINT.P=8e-11) while dropping the null gene (GENE2, COND.P=0.58) against ground truth | Found only because I verified the audit's suggested one-line fix by actually running it, not by reading source alone |
| MA-FOCUS colon-separated paths collide with Windows drive letters | P2 (cheap) | Documented as a general FOCUS caveat (not MA-FOCUS-specific -- confirmed it also breaks single-ancestry runs) in SKILL.md's FOCUS section and `examples/focus_finemap.sh` | ran -- an absolute `F:/...` single-ancestry path mis-detected "2 populations" | Audit had framed this as MA-FOCUS-only; broadened per the reproduced evidence |
| (found during verification, not in audit recommendations) SMulTiXcan.py example missing `--cutoff_condition_number`, a failed dynamic-audit assertion (Input 4) | not listed / cheap | Added the flag to SKILL.md's S-MultiXcan example and a Common Errors row | confirmed via audit's own assertion evidence (`InvalidArguments` without it); not independently re-run | |
| (found during verification) `examples/focus_finemap.sh`'s PIP filter reads a `pip` column that installed pyfocus 0.802 never writes -- real output is `pips_pop1`/`pips_me` | not in audit | Fixed the awk filter and added a Common Errors row | confirmed by reading `pyfocus/finemap.py`'s `create_output()` (renames columns to `pips_pop{i+1}`/`pips_me`); not exercised end-to-end since my synthetic run never reached the PIP stage (fixture DB was the wrong schema) | Silent-wrong-answer bug, not a crash -- would have passed unnoticed |

## Left unfixed

- P2 "464-line SKILL.md, no references/ split" and P2 "FUSION has no standalone example script" --
  restructuring/new-content, out of scope for a defect fix pass.
- Did not build a real FOCUS-format weight database, so the pyfocus pin+patch fix was verified through
  the entire pipeline except the final PIP computation itself (blocked on "no overlapping weights" from
  a mismatched fixture schema, not a Skill or pyfocus defect) -- a future audit with a real `focus
  import`-built DB should confirm PIP output values.

## Needs Sam

Nothing blocking. Two of the four "P1" rows above are the audit's original findings; the other two are
deeper bugs the same code paths hit immediately after applying the audit's own suggested one-line fixes
-- flagging in case the re-auditor wants to weigh that when re-scoring reliability.


# Fix log addendum: bio-causal-genomics-transcriptome-wide-association (2026-09-21)

Source: `causal-genomics/transcriptome-wide-association`. Re-audit 2026-09-19: 87/100, Production Ready,
1 P1 + 3 P2 open. Fix commit: `fix/causal-genomics-transcriptome-wide-association` in worktree
`F:\OpenScience\wt\causal-genomics-transcriptome-wide-association` (not merged). Older entries above untouched.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| pyfocus pin+patch insufficient: `focus finemap` crashes at "Calculating PIPs" with `DataFrame.pivot() takes 1 positional argument` (`finemap.py:1012`) then `'DataFrame' object has no attribute 'append'` (`:188`) | P1 | SKILL.md Tool Install Notes: two more `sed` patches (keyword `pivot`; `pd.concat` for `append`), restructured the note into a bullet list of the four upstream problems, re-dated to 2026-09-21; Common Errors row added; `examples/focus_finemap.sh` header updated | ran: fresh venv (pyfocus 0.802, pandas 2.1.4, numpy 1.26.4, setuptools 80.10.2), extracted the doc's own sed block from SKILL.md and ran it; unpatched run fails (`np.warnings`), patched run completes with `pips_pop1=1` for planted true gene, 3.44e-08 for NULL.MODEL; awk PIP filter of the example run on that output returns only the true gene | Same fixture design as the re-audit (bundled 957-indiv LD, planted Z=7.2), rebuilt by me |
| `focus import ... fusion` needs undocumented mygene+rpy2 (+ R as shared lib); fails silently with empty DB | P2 | SKILL.md FOCUS section: requirement + silent-failure note + runnable direct-build script (`load_db`/`build_model`) from a `panel.tsv`; Common Errors row; example script comment | ran: the script extracted from SKILL.md built a DB that `focus finemap` consumed (above). `focus import` failure mode itself: audit run + `pyfocus/models/convert.py` source (only `log.error` on ImportError); not re-run | Chose "write it": tool is installed, audit expected it to run |
| 464-line SKILL.md, no references/ split | P2 | not fixed | | restructuring, out of scope |
| FUSION has no standalone example script | P2 | not fixed | | new content, out of scope |

## Redundancy removed (dedup pass)

| deleted passage | content now lives |
|---|---|
| usage-guide.md install code blocks (pyfocus pip, MetaXcan/FUSION git clone, `install.packages(...)`) | SKILL.md Tool Install Notes (the R package list moved into the FUSION bullet; guide points there) |
| usage-guide.md Quick Start list | duplicated Example Prompts; deleted |
| usage-guide.md "What the Agent Will Do" | restated SKILL.md pipeline and failure-mode sections; deleted |
| usage-guide.md Ancestry-Matched Prediction Panels table | moved to SKILL.md, Ancestry mismatch failure mode |
| usage-guide.md GTEx v8 N<100 tissue table | moved to SKILL.md, Low-N tissue failure mode |
| usage-guide.md Tips (10 bullets) | each already in SKILL.md: Tissue Selection Protocol, FOCUS "Fix", Ancestry Fix, HLA, Low-N, Triangulation rule, decision-tree rows (drug-target, splice-TWAS), FUSION Pipeline, version-pinning lines; the one unique fact (post_process returns no PIPs) added to FUSION Pipeline |
| usage-guide.md overview paragraph 2 and "--joint" aside in FUSION prompt | shortened to a pointer |
| SKILL.md symptom/fix restating `post_process.R` default conditional analysis (2 places) | FUSION Pipeline section |
| SKILL.md S-MultiXcan paragraph repeating the cutoff error | Common Errors row (kept) plus one sentence |
| SKILL.md Common Errors causes/solutions for delim_whitespace, np.warnings, `--locations`, Windows paths | pointers to Tool Install Notes / FOCUS section, which hold the detail |

Left unfixed: nothing else open. `focus import` end-to-end (with mygene+rpy2) was not run: rpy2 needs a
shared-library R, which this machine's R is not; the direct-build route was verified instead.


## 2026-09-21 (structure)

Worktree `F:\OpenScience\wt\causal-genomics-transcriptome-wide-association`, branch `fix/causal-genomics-transcriptome-wide-association`.
Commits: split `a2a9881`, scripts `a70dce4`. No behaviour or claim changed.

**Split: SKILL.md 544 -> 189 lines.** Verbatim moves into `references/` (no `references/` existed):
`algorithmic-taxonomy.md`, `tissue-and-model-selection.md`, `failure-modes.md`, `fusion-pipeline.md`,
`spredixcan-smultixcan.md`, `focus-finemapping.md`, `escalation-and-reconciliation.md`,
`reporting-and-review.md`, `citations.md`. Stayed in SKILL.md: scope, PredictDB/MASHR model choice,
decision tree (rows now point at the reference files), triangulation, thresholds, Common Errors, Tool
Install Notes, Related Skills, plus a new "Reference Files" index. Checked by multiset comparison: every
original non-blank line is in the new files except 23 intentional edits (9 decision-tree pointers, 5
H2 -> H1 titles, 9 cross-reference retargets such as "see FOCUS section" -> path). All 5 bash fences
pass `bash -n`, the python fence `py_compile`.

**Scripts:**

| old location | new | how run |
|---|---|---|
| SKILL.md FUSION Pipeline bash block (loop + `post_process.R`), now `references/fusion-pipeline.md` | `scripts/fusion_twas.sh` (positional args, `RSCRIPT`, `LOCUS_WIN`; header concatenation fixed so only one header line survives; `post_process` now runs per chromosome instead of a hard-coded `--chr 22`) | Audit fixture `data/fusion` (copied), `fusion_twas` HEAD clone with the documented `drop=FALSE` patch, via `r.sh` (`RSCRIPT=`), `CHRS=1`: TWAS.Z GENE1 6.5 (p 8e-11), GENE2 -0.557; `joint_included` = GENE1, `joint_dropped` = GENE2 (COND.P 0.58); same as the 2026-09-19 log |
| FOCUS section python block (direct DB build), now `references/focus-finemapping.md` | `scripts/build_focus_db.py` (panel.tsv + out.db args; optional `cv_r2`/`cv_r2_pval` columns) | Panel of 2 genes on the audit fusion LD panel, GWAS Z 7.2 planted at the true gene's SNP; then `focus finemap` on that DB: `pips_pop1` = 1.0 for GENE_TRUE, 3.44e-08 for NULL.MODEL (asserted) |
| S-PrediXcan + S-MultiXcan bash block | deleted; pointer to `examples/s_predixcan_pipeline.sh` (duplicate) | not re-run: example untouched |

Env: pyfocus 0.802 (pandas 2.1.4, numpy 1.26.4, setuptools 80.10.2, SQLAlchemy 2.0.54) was installed into a
private throwaway venv in my own scratchpad subdirectory (`...\scratchpad\twas\venv`), with the SKILL.md
sed patches applied; nothing was installed into the shared env, R-lib or `twas-venv`, and TOOLS.md is
untouched. R only through the env's `r.sh`.

**Stayed inline:** the `focus finemap` CLI calls (about 10 lines, a single command; the example
`focus_finemap.sh` holds the long form), the MA-FOCUS call, the `focus import` one-liner, and the
pyfocus `sed` patch block in Tool Install Notes (8 lines, and Common Errors points at it).


# Final-pass Phase 1 (2026-09-21)

Worktree `F:\OpenScience\wt\causal-genomics-transcriptome-wide-association`, branch
`fix/causal-genomics-transcriptome-wide-association` @ `3e246f1`. Walked every runnable block in the
Skill (not just what the prior fixer touched) from a fresh scratchpad venv/clone, per
`FINAL_PASS_BRIEF.md`. Full detail:
`F:\OpenScience\audits\_final_pass\bio-causal-genomics-transcriptome-wide-association\CHECKPOINT.md`.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| `examples/focus_finemap.sh` / `references/focus-finemapping.md` `LD_REF_PREFIX` written FUSION-style, chr-templated (`1000G_EUR/chr`) | P2 | `focus finemap`'s `ref` arg goes straight to `pandas_plink.read_plink()` (exact prefix or real glob only, no chr-substitution); fixed to a single combined prefix + glob alternative note; Common Errors row added | ran | Found only by testing `read_plink()` directly against the audit's real fusion LD fixture; the literal chr-templated path 404s exactly as predicted |
| `examples/s_predixcan_pipeline.sh` Step 3 filter used `awk -F','` against `SMulTiXcan.py --output *.csv` | P2 (silent-wrong-answer) | `SMulTiXcan.py` hard-codes `sep="\t"` regardless of extension (`metax/cross_model/Utilities.py:50`); filter fixed to `-F'\t'`; Common Errors row added | ran | Old filter returned 0 rows silently on a real S-MultiXcan run; fixed filter correctly isolates the true-signal gene |

Everything else re-verified with no defect found: pyfocus pin+patch (fresh scratchpad venv,
`build_focus_db.py` + `focus finemap`, real PIP output matching prior ground truth), FUSION pipeline
(`scripts/fusion_twas.sh` with the documented `drop=FALSE` patch, exact match to prior ground truth),
`SPrediXcan.py`/`SMulTiXcan.py` against real audit fixtures (exact match to FUSION's independently
computed TWAS.Z). Confirmed the shared `twas-venv` is still unpatched (pandas 3.0.5) -- the
private-scratchpad-venv approach for pyfocus remains correct; nothing installed or changed in any
shared env this phase.

**Still blocked:** `focus import ... fusion` (mygene+rpy2 route) needs R built as a shared library,
which this machine's runtime R is not. Already documented with a verified working alternative
(`scripts/build_focus_db.py`); not a new gap, not chased further.
