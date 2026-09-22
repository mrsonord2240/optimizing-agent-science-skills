# bio-crispr-screens-drugz-chemogenomic fixes (2026-09-16)

Worktree `F:\OpenScience\wt\crispr-c`, branch `fix/r2-crispr-c`. Fixer: Claude Opus 5 (orchestrating
session). Runtime: `drugz.py` from `hart-lab/drugz` (the clone in
`audit-envs\crispr-screen-analyst\tools\dl\drugz`, run under that candidate's venv, pandas 2.x).
Data: the audit's own synthetic chemogenomic screen built on real HAP1 TKOv3 counts
(`audits\bio-crispr-screens-drugz-chemogenomic\data\`, planted sensitizers and suppressors as ground
truth), copied to `F:\OpenScience\wt\_fixdata\drugz\`.

## Round-2 audit pass — 2026-09-16

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `examples/run_drugz.py` Step 2 joins raw CEGv2.txt lines, so `-r` matches nothing and the "CEG-excluded" run is identical to the unfiltered one | P0 | Parse column 1, skip the header, then assert that genes actually disappeared from the output (`assert removed`) | ran | Fixed parsing excludes **646 of 684** listed CEGv2 genes (18,054 -> 17,408 genes in the output); the old join excludes **0** and still exits 0 |
| "Removing Genes from Null Distribution" documents `-r` as a file (`cat > remove_essential.txt`, `-r remove_essential.txt`) while the CLI block says comma-delimited names | P0 root cause (internal contradiction) | Section rewritten: `-r` is a comma-delimited gene list (`args.remove_genes.split(',')`), it drops those genes before Z-scoring so they vanish from the output, with a shell one-liner to build the list from a reference file and a `comm` check that the exclusion happened | ran + docs (`drugz.py` argparse and `load_reads`) | Retitled "Removing Reference Genes from the Analysis" -- `-r` excludes, it does not re-weight a null |
| No documented relationship between total guide count and `--half_window_size` | P1 | New paragraph after the algorithm: the window is indexed absolutely, needs roughly 4x `--half_window_size` guides, default 500 assumes a genome-scale library; set it to about a quarter of total guides for pilot libraries. Distinguished from the per-gene sgRNA count | ran | 200-guide table at the default: `IndexError: single positional indexer is out-of-bounds`; same table with `--half_window_size 50` (4x): completes, 51 gene rows |
| Dose-response section's only code is commented-out pseudocode | P1 | `dose_consistent_hits()` in SKILL.md and a runnable `per_dose_drugz()` in the shipped example, both implementing the consistency rule | ran | Built a 3-dose set from the audit's mid-dose arm (low = geometric mean of vehicle and mid) and ran it: **6 of 6 planted sensitizers recovered, no others**; `monotonic` reported as supporting evidence only |
| No numeric threshold for cross-dose "consistency" | P2 | Rule stated: same `normZ` sign at every tested dose and FDR < 0.05 at the top dose; `\|normZ\|` growing with dose is supporting evidence, not a requirement | ran (same run) | Matches the quantitative style of the Skill's other threshold tables |
| (Found while fixing) Failure mode "Inconsistent results between repeats of drugZ ... aggregate multiple drugZ runs with different bootstrap seeds" -- drugZ has no sampling step and no seed | internal contradiction | Retitled "Unstable hits across libraries or sub-samples"; states that a rerun cannot show instability and points to replicate hold-out or guide bootstrapping instead | ran | Two runs on identical input produced byte-identical output files (`cmp`) |
| (Found while fixing) shipped example shells out to bare `python`, which picks up whatever interpreter is first on PATH | shipped script | Uses `sys.executable` at all three call sites | ran | Reproduced the failure (`ModuleNotFoundError: No module named 'pandas'` from a different interpreter), then the whole example ran end to end: 646 genes excluded, 6 sensitizers, 7 suppressors -- exactly the planted ground truth (6 sensitizers, 6 suppressors + the drug-target paradox gene) |

All 4 `recommendations[]` entries (1 P0, 2 P1, 1 P2) fixed, plus three defects found while fixing.
Nothing left unfixed. `py_compile` clean on `examples/run_drugz.py`.

## Re-audit fix pass — 2026-09-21

Worktree `F:\OpenScience\wt\crispr-screens-drugz-chemogenomic`, branch `fix/crispr-screens-drugz-chemogenomic`. Fixer: Claude Sonnet 5. Runtime: `drugz.py` from the `crispr-screen-analyst` clone (git HEAD 2026-09-16), Python 3.12.13, pandas 3.0.5. Data: the audit's synthetic counts (`audits\bio-crispr-screens-drugz-chemogenomic\data\`).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Common Errors table has no `IndexError: single positional indexer is out-of-bounds` row | P1 | Row added, pointing to the "Library size vs `--half_window_size`" section | ran | 200-guide table at default: IndexError; with `--half_window_size 50`: completes, 51 gene rows |
| No guidance for low replicate concordance or a crashed run | P2 | New failure-mode subsection "Low replicate concordance (Pearson < 0.85) or a crashed run"; Pearson > 0.85 added to Quantitative Thresholds (it lived only in usage-guide) | ran | Dropping the third replicate (`-c Veh_r1,Veh_r2 -x Drug_r1,Drug_r2`) runs, 18,053 genes; a misspelled sample name gives `KeyError: ['VehX'] not in index` |
| (Found) main `bash` block put `# comments` after line-continuation backslashes, so pasting it runs `-i ...` etc. as separate commands | shipped snippet | Comments moved above the command | ran | Reproduced the break with a minimal script (`b: command not found`); the fixed block then ran on the audit data, 18,051 genes |
| (Found) usage-guide typo ("excludele` with CEGv2") and the claim that `-r` "excludes from the null" (it drops the genes) | doc defect | Removed with the dedup below | docs (`drugz.py` `load_reads`) | |

### Redundancy removed (every deleted passage and where it now lives)

| deleted from `usage-guide.md` | now |
|---|---|
| Prerequisites (clone, pip helpers, required inputs, matched time point) | SKILL.md "Run drugZ" **Input** paragraph (plus existing Version Compatibility clone line) |
| Quick Start bullets | example prompts (kept, merged) |
| What the Agent Will Do (10 steps) | SKILL.md Run / Failure Modes / Comparison sections |
| Tips (8 bullets) | each already in SKILL.md (Day-0 failure mode, drug-target-as-suppressor failure mode, drugZ vs MLE tables, `-r` section); "essentiality plus drug" moved to the SKILL.md comparison table; low-Pearson tip to the new failure mode |
| Decision Cheat Sheet | SKILL.md comparison table (+ new essentiality row) |
| Thresholds table | SKILL.md Quantitative Thresholds (+ Pearson > 0.85 row); pseudocount "raise for low-count" now a comment on `-p` |
| Validation Checklist | SKILL.md failure modes; "library coverage / MAGeCK count QC" added to the Input paragraph |

Inside SKILL.md: the "Dose consistency rule" stated twice (dose section and comparison section) now lives once in "Drug-Dose and Time-Course Designs"; the comparison section points to it. No disagreement between copies.

Both `recommendations[]` entries (1 P1, 1 P2) fixed, plus two defects found. Nothing left unfixed. No `.py`/`.sh` changed in the Skill, so no compile step; `examples/run_drugz.py` untouched.

## 2026-09-21 (structure)

Worktree `F:\OpenScience\wt\crispr-screens-drugz-chemogenomic`, branch `fix/crispr-screens-drugz-chemogenomic`. Fixer: Claude Sonnet 5. Structure only; no behaviour or claim changed.

**Split** (commit `refactor(...): split SKILL.md into references/`): SKILL.md 318 -> 243 lines (230 after the scripts commit). Verbatim moves, compared non-blank line by line (nothing lost; only the two section headings became file titles, and four pointer edits/index lines were added); both bash fences in the new files pass `bash -n`.

| section | now |
|---|---|
| "Removing Reference Genes from the Analysis" (37 lines) | `references/reference-gene-removal.md` |
| "Failure Modes" (43 lines, six subsections) | `references/failure-modes.md` |

SKILL.md gained a "Reference Files" index and pointers: the `-r` comment in the Run block, the "Hits dominated by essentials" Common Errors row, the Pearson threshold row, and a line after the comparison table. Kept in SKILL.md: scope, algorithm, Run block, dose design, comparison table, Quantitative Thresholds, Common Errors, install.

**Scripts** (commit `refactor(...): move runnable code to scripts/`):

| old location | script | how run |
|---|---|---|
| SKILL.md "Drug-Dose and Time-Course Designs", `dose_consistent_hits()` python block (17 lines) | `scripts/dose_consistent_hits.py` (function verbatim, plus CLI, header comment, `--top-dose` validated) | env `crispr-screen-analyst` Python, on the 3-dose drugZ outputs in `_fixdata\drugz\` (built from the audit's synthetic data): `--top-dose high low=... mid=... high=...` returned exactly the 6 planted sensitizers, all normZ < 0 (asserted); `--direction supp` returned the 6 planted suppressors plus the RGS2 drug-target paradox gene; a bad `--top-dose` errors cleanly |

Stayed inline: the bash blocks (all under 15 lines; short invocations and a 3-line CEGv2 `-r` recipe). `examples/run_drugz.py` untouched; its `per_dose_drugz()` also runs drugZ per dose, so it is not a copy of the script.
