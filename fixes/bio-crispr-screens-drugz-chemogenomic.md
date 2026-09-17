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
