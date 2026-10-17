# Handoff: ca-bio-analytical-validation / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Lane: n/a (context-aware recut batch)
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-analytical-validation` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-analytical-validation`
- Branch/worktree: records repo working tree, no branch; no git writes made
- Candidate identity (preflight `--shape`, PASS): `219a403267cd55b3a16b47357728ae2d7645cd918354d73c0f2865bc02f24a3b`, 11 files.
- Applicable audit: none carried over (the shelf Skill was audited; the scripts' validation logic is unchanged)
- Warn carried: no Skill-root LICENSE. The shelf frontmatter had no `license`/`author`; added `license: MIT`, `author: GPTomics` per the provider convention.

## Structural summary

- `SKILL.md`: 34 lines, 5 routes (ge-poisson, lod95-probit, panel-integrated-lod, audit-claim, reference-materials), 7 rules, tested-versions line last.
- Scripts: `ge_and_poisson.py`, `lod95_probit.py`, `panel_integrated_lod.py`. The validated library functions are untouched; each `__main__` demo was replaced by a CLI that takes the user's numbers or CSV and writes one TSV.
- References: `background.md`, `citations.md`.
- Dropped: `usage-guide.md`, `examples/detection_limits.py` (contrived-model demo the scripts replace; its simulated dilution is not validation evidence).
- Traps in scripts: VAF above 1 refused as a percent; library refusals surfaced as `REFUSED:` exits (separation, non-bracketing, thin replicates, k above N, unreachable grid).
- Version drift: shelf comments said numpy 1.26+/scipy 1.12+/statsmodels 0.14+; ran on numpy 2.5.3, scipy 1.18.1, statsmodels 0.15.0 (the `PerfectSeparationWarning` import still works).

## Runnable-surface inventory and runs

Environment: WSL `science`, micromamba env `as-viz`. Inputs under `F:\OpenScience\fix-evidence\ca-recut\bio-analytical-validation\input`: a contrived dilution series (the shelf script's own fixture, 40 replicates x 5 levels, seeded blanks) and a series derived from the published ETAM-seq sensitivity table in `audits\bio-analytical-validation\data` (midpoint AF, 100 replicates per level assumed, so only a stand-in).

| Script | State | Settings and key numbers |
|---|---|---|
| `ge_and_poisson.py` | executed | 3/10/30 ng x 1e-3/1e-4 default: 95% presence needs 2,995.7 GE at 1e-3, 29,957 GE (98.9 ng) at 1e-4; also `--min-molecules 2 --target 0.9 --ge-per-ng 330`; `--vaf 5` refused |
| `lod95_probit.py` | executed | contrived series with blanks: LoD95 0.003725 VAF, CI 0.002578-0.005383, LoB 0.00027; ETAM-seq-derived at `--confidence 0.90 --min-replicates 5`: 0.00397, CI 0.00326-0.00484; separation, percent-VAF and thin-replicate traps all refused |
| `panel_integrated_lod.py` | executed | 30 ng, k=2: 16/32/48 loci give 3.42e-5, 1.67e-5, 1.10e-5; 10 ng, k=1, target 0.5; `--min-loci 5 --n-loci 4` refused |

No script filters data, so there is no drops-nothing setting.

## Open ambiguities for audit

- The ETAM-seq-derived series assumes 100 replicates per level; its LoD95 is illustrative.
- `--vaf 0.1` is accepted (10%); only values above 1 are caught as percents.
- Thresholds (3 pg convention, duplex floors, ichorCNA 3%) are carried from the source text and were not re-verified against the literature.
- Grid for the panel bound is fixed at 1e-6 to 1e-2.

## Evidence

- `F:\OpenScience\fix-evidence\ca-recut\bio-analytical-validation\` (`run.sh`, `run2.sh`, `run.log`, `out\`, `input\`, `scripts_src\`).
- Tooling impact: none.

## Worktree safety

- Run-owned: `skills\ca-bio-analytical-validation\`, this handoff, one row in `skills\README.md`.
- Pre-existing/user-owned: `.claude/skills/normalize-scientific-skill/SKILL.md`, `test/validate.bats` untouched; the old `handoff\bio-analytical-validation-handoff.md` left as is.
- Product commits/pushes: none.

## Transition assertion

- Next-phase prerequisites met: yes.
