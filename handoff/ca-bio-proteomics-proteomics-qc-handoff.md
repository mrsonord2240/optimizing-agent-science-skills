# Handoff: ca-bio-proteomics-proteomics-qc / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Lane: n/a (context-aware recut batch)
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-proteomics-proteomics-qc` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-proteomics-proteomics-qc`
- Branch/worktree: records repo working tree, no branch; no git writes made
- Candidate identity (preflight `--shape`, PASS): `c449743e76bbd79bf53583e23f8e714f7ef8a1423824e2add4298950dec8a107`, 19 files.
- Applicable audit: none carried over
- Warn carried: no Skill-root LICENSE (frontmatter `license: MIT`, author GPTomics kept)

## Structural summary

- `SKILL.md`: 37 lines, 8 routes (raw-signal, matrix-metrics, pca-batch, tmt-balance, diann-level1, ptxqc, diagnose, writeup), 7 rules, tested-versions line last. Siblings named: differential-abundance, quantification, dia-analysis.
- Scripts: `raw_qc.py`, `matrix_metrics.py`, `pca_batch.py`, `diann_level1.py` (existing, CLIs extended with `--out` and threshold options); new `tmt_balance.py` (the in-prose function promoted to a script), `ptxqc_report.R` (wraps `createReport`).
- References: `thresholds.md`, `background.md` (funnel, normalization-hides-loading, tool table, failure notes), `citations.md`, `qc-report-template.md` (example row now from the recut run).
- Dropped: `usage-guide.md`, `examples/qc_analysis.py` (simulated-data demo a script replaces), three reference files that duplicated the routes.
- Traps now in scripts: `raw_qc.py` refuses LFQ/Normalised/MaxLFQ prefix and no matching sample columns; `matrix_metrics.py`/`pca_batch.py` refuse missing columns; `pca_batch.py` refuses batch fully confounded with condition; `tmt_balance.py` refuses log/normalized tables; `diann_level1.py` refuses a report lacking the Level-1 columns. Inherited: single-sample group fallbacks and `not_testable` statuses.
- Version drift: shelf text said "pandas 3.0.5"; reran on pandas 3.0.6, numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1 with no API change.

## Runnable-surface inventory and runs

Environment: WSL `science`, micromamba env `as-viz` (Python, pandas 3.0.6, scikit-learn 1.9.1, scipy 1.18.1, numpy 2.5.3). Inputs copied from earlier audit data (`F:\OpenScience\audits\bio-proteomics-proteomics-qc\data`: synthetic MaxQuant `proteinGroups.txt`, a `_failed` variant with a planted low-load T4, synthetic TMT plexes) and a real DIA-NN 2.6.1 report (`audit-envs\mass-spec-proteomics-analyst\public-work\diann_libbased_mzml\diann_out\report.parquet`, 3 runs, 4851 rows).

| Script | State | Settings and key numbers |
|---|---|---|
| `raw_qc.py` | executed | default on clean data: nothing flagged, 60 of 1560 rows stripped; on failed data: T4 flagged (fold 0.41, ids 0.81, contaminant 13.6%); `--min-fold-total 0 --min-ids-frac 0` flags nothing; LFQ prefix trap exit 1 |
| `matrix_metrics.py` | executed | default: replicate r 0.958-0.967, median CV 24.2/23.5%, completeness 1368 of 1560; `--min-valid-frac 0` keeps 1560; bad-prefix trap exit 1 |
| `pca_batch.py` | executed | PC1 vs batch p=7e-8, PC2/PC3 p>0.9; repeated with `--batch-col replicate`; `--batch-col condition` confounded trap exit 1 |
| `tmt_balance.py` | executed | both plexes within 0.89-1.32x of median, nothing investigated; `--max-fold 100` nothing; log-table trap exit 1 |
| `diann_level1.py` | executed | real report: R^2 0.9994-0.9998, FWHM ratios 0.96-1.02, no flag; `--min-r2 0 --max-fwhm-ratio 100 --max-q 1` no flag; trap on the synthetic report without Level-1 columns exit 1 |
| `ptxqc_report.R` | unexecuted | PTXQC is not installed in any WSL environment (only in the Windows `mass-spec-proteomics-analyst` R-lib) |

No script was run with a flag that fires on the DIA-NN or TMT data; those flags are untested on a real fault.

## Open ambiguities for audit

- The MaxQuant and TMT inputs are synthetic, so the 0.5x/0.8x loading rule and 2x TMT band are untested on real data.
- `contaminant_pct` for DIA-NN reports is not offered; DIA-NN has no contaminant flag columns.
- Thresholds table mixes published, convention and script-default values; nothing was re-verified against the literature.
- `ptxqc_report.R` assumes `summary.txt` is the marker of a MaxQuant txt folder.

## Evidence

- `F:\OpenScience\fix-evidence\ca-recut\bio-proteomics-proteomics-qc\` (`run.sh`, `run2.sh`, `run.log`, `run2.log`, `out\`, `scripts_src\` copy used for the runs, `input\`).
- Tooling impact: none (no environment changes).

## Worktree safety

- Run-owned: `skills\ca-bio-proteomics-proteomics-qc\`, this handoff, one row in `skills\README.md`.
- Pre-existing/user-owned: `.claude/skills/normalize-scientific-skill/SKILL.md`, `test/validate.bats` untouched; sibling `ca-*` folders belong to other work.
- Product commits/pushes: none.

## Transition assertion

- Next-phase prerequisites met: yes.
