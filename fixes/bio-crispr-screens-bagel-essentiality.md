# bio-crispr-screens-bagel-essentiality fixes (2026-09-16)

Worktree `F:\OpenScience\wt\crispr-a`, branch `fix/r2-crispr-a`. Fixer: Claude Sonnet 5. Runtime:
BAGEL2 build 115 (`hart-lab/bagel`, numpy-2.x patched per `TOOLS.md` Notes #1) in the
`crispr-screen-analyst` venv, Python 3.12. Verification data: real HAP1 TKOv3 pooled-knockout screen
(`F:\OpenScience\audits\bio-crispr-screens-bagel-essentiality\data\HAP1_TKOv3_reads.txt`, 70,754
sgRNAs / 18,053 genes) plus the candidate env's own `CEGv2.txt`/`NEGv1.txt`, copied to scratchpad.

Commit: `ead41a5` on `fix/r2-crispr-a`.

## Round-2 audit pass — 2026-09-16

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| BAGEL2 non-deterministic and undisclosed (Skill Veto T3 FAIL) | P0 | Added `-s <fixed-int>` to every `bf` example (SKILL.md, usage-guide.md, `run_bagel2.sh`); new "Reproducibility: Fixing the Random Seed" section | ran | Two unseeded `bf` runs differ on 18,026/18,053 genes (auditor's own runs); two full `fc→bf→pr` runs of the fixed `run_bagel2.sh` (bootstrap, `-NB 100`) with `-s 42` produced a byte-identical `bayes_factor.txt`; also byte-identical in CV mode via direct `bf -s 42` |
| `interpret_bagel()` flags 86.5% of genes as tumor suppressor on a dropout screen | P0 | Added a `screen_type` gate (default `'dropout'`, no TS calls unless `'enrichment'`/`'both'`), an assay-control exclusion set (`LacZ`/`luciferase`/`EGFP`), and a >5%-flagged `warnings.warn` sanity check | ran | Real HAP1 TKOv3 `bayes_factor.txt`: default now returns 0 TS calls and drops the 3 controls; `screen_type='enrichment'` still surfaces the real TSC1/TSC2 calls (now the two most-negative-BF entries, no longer masked by controls) and fires the warning at 86.6% |
| Reference-set failure modes documented inaccurately ("median BF near zero" claimed for every bad-reference case) | P1 | Failure Modes entry rewritten to give the actual per-misconfiguration symptom: species mismatch → hard crash; `-e`/`-n` swap → all-`nan` BF, exit 0; thin reference → the original "near zero" symptom (kept, now scoped) | ran | Species mismatch reproduced: `ValueError: dataset input should have multiple elements` (`scipy.stats.gaussian_kde`); `-e`/`-n` swap reproduced: all 18,053 genes' `BF` literally `nan`, exit 0 |
| Per-sgRNA `-r/--sgrna-bayes-factors` flag undocumented | P1 | Added the explicit `-r` invocation and its `RNA GENE <samples> BF` output schema to "Bayesian Reasoning Per Sgrna" | ran | Real output: RPS3's 4 per-sgRNA BF values sum to 78.9 vs gene-level BF 80.8 (within 2.4%) |
| `STD`/`NumObs` columns silently require `-b`; no runtime-cost note for `-NB 1000` | P2 | Output-columns table now states `-b`-only explicitly; added a ~20-25 min genome-scale runtime note | ran | CV-default run writes a 2-column `GENE\tBF` file; `-b` run adds `STD`/`NumObs` |
| (Found while fixing) `fc`/`bf` bash blocks had `# comment` after a line-continuation `\`, which ends the shell's continuation — every subsequent `-flag` line then ran as its own nonexistent command | broken command | Comments moved off continuation lines in SKILL.md and `examples/run_bagel2.sh` (also applied to the new `-s`/`-r` lines I added, which would otherwise repeat the same bug) | ran | Reproduced the break with the original text (`-n: command not found`, etc.); reassembled block via `echo`-substitution dry-run confirms a single correct command after the fix; `bash -n` and a full `fc→bf→pr` execution both pass |

All 5 `recommendations[]` entries (2 P0, 2 P1, 1 P2) fixed, plus one defect found while fixing
(broken bash line-continuation, pre-existing in the shipped `fc`/`bf` examples). Nothing left
unfixed for this Skill. `bash -n` clean on `examples/run_bagel2.sh`; the `interpret_bagel()`
snippet `py_compile`s clean and was run against real BAGEL2 output.

**Cross-Skill note for the `hit-calling` and `workflows/crispr-screen-pipeline` fixers:** the
seeding recipe is in this Skill's SKILL.md under "Reproducibility: Fixing the Random Seed" — cite
it rather than re-deriving; it documents the `-s` flag collision (build 115 declares `-s` for both
`--use-small-sample` and `--seed`; the seed option wins) that would otherwise silently mislead a
second fixer reading `--help` alone.


## Round-3 fix pass — 2026-09-21

Worktree `F:\OpenScience\wt\crispr-screens-bagel-essentiality`, branch `fix/crispr-screens-bagel-essentiality`,
commit `d1aad70`. Fixer: Claude Sonnet 5. Runtime: BAGEL2 build 115 (Python 3.12, pandas 3.0.5,
`crispr-screen-analyst` env); data = the audit's real HAP1 TKOv3 run outputs plus CEGv2/NEGv1/mouse CEG.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Reference-set failures (species mismatch traceback, swapped `-e`/`-n` all-`nan` exit 0) have no runtime guard | P1 | Wrote `examples/check_bagel_inputs.py` (`pre`: reference overlap >=100 genes each, `-c` columns exist, `-e` mean LFC < `-n` mean LFC; `post`: >5% `nan` BF fails, warns if no BF>6). Wired into `examples/run_bagel2.sh`; SKILL.md gets "Pre-flight" and "Post-run check" paragraphs. Chose "write it" (audit asked for code; pandas installed) | ran | correct call: pre OK (646/684 ess, 797/926 non present; LFC -2.665 vs +0.131), post OK 18053/18053. Swapped: pre exit 1 (LFC reversed), post on real all-`nan` file exit 1 (0/18053). Mouse CEG: pre exit 1 (0/621). Bad `-c`: exit 1. `run_bagel2.sh` run end to end on the real data (control HAP1_T0, CV mode instead of `-b` for time) exit 0. `py_compile`, `bash -n` clean |
| "clinical-grade" x4 with no practice boundary | P2 | Practice-boundary note at top of SKILL.md; "clinical-grade" -> "high-stringency"/"publication-grade" in SKILL.md and usage-guide | grep (no `clinical` left except the boundary note) | |
| "Bootstrap CI is wide" symptom did not reproduce (0/200 STD>|BF|) | P2 | Failure Mode retitled "Thin per-gene coverage"; symptom is now implausibly large BF magnitude (top ~2,400 on 3 sgRNA/gene synthetic vs ~132 on real HAP1), CI-spanning-zero kept but marked not reliable; fix no longer claims bootstrapping cures it (only provides `STD`) | audit run 04 (synthetic data, auditor's numbers; not rerun) | |
| (found) run_bagel2.sh comment called BF<-6 "negative selection" tumor suppressor, contradicting the Skill's own dropout rule | small | Comment corrected to point to `screen_type` gate | bash -n | |

### Redundancy removed (each fact once)

| deleted | now lives |
|---|---|
| usage-guide "What the Agent Will Do", Tips, Decision Cheat Sheet, Thresholds, Validation Checklist | SKILL.md (workflow, failure modes, ladder, interpret_bagel); usage-guide has a pointer paragraph |
| usage-guide Tip: CN-amplified regions appear essential | SKILL.md new Failure Mode "Negative BF for known essentials..." |
| usage-guide cheat sheet: drugZ for both directions, Chronos for panels, <4 sgRNA | SKILL.md Comparing section "Pick by case" and thin-coverage Failure Mode |
| usage-guide Tip: BF>6 calibration may not hold outside cancer lines | SKILL.md non-cancer Failure Mode |
| usage-guide Tip: "BAGEL2 calls more hits than MAGeCK under high variance" | dropped: unsupported by any run |
| SKILL.md Common Errors table (7 rows) | Failure Modes, Reproducibility, thin-coverage entries (every row had a home) |
| SKILL.md BF>6/12/30 rows in Quantitative Thresholds, 90%/FDR restatements, seed restatements (step 6, thresholds row, pre-fix commentary) | single BF ladder under "Precision-Recall Curve"; single Reproducibility section |
| SKILL.md TS paragraph and Interpret "Approach" restating 86.5% result | one verified paragraph after `interpret_bagel` |

Left unfixed: none. Not run: bootstrap (`-b -NB 1000`, ~20 min) end to end for `run_bagel2.sh`; the same `bf`
call in `-b` mode was run in the earlier pass.
