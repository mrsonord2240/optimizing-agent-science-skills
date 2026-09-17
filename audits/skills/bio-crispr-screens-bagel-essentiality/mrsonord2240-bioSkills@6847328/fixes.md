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
