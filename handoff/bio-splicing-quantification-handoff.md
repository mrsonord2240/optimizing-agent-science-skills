# Handoff: bio-splicing-quantification / prepare-scientific-skill-tooling

- Updated: 2026-10-03
- Lane: 2
- Status: ready-for-phase
- Owner leaving: normalize worker (lane 2)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:alternative-splicing/splicing-quantification (source identity de91158720430e45ef20d81624a331dc9457edd99741b6e84e10da22f2315248, files=3, bytes=36158)
- Working tree: F:\OpenScience\wt\norm-bio-splicing-quantification (sparse cone: skills/bio-splicing-quantification)
- Branch/worktree: normalize/bio-splicing-quantification, started at 29f5446 (uncommitted)
- Candidate tree hash: 1e34dbd9664e334b3feb336a3d624ec99d39ca9b5ad9a056f1f7142448bd489c (files=5, bytes=37504; from skill_preflight, PASS)
- Applicable audit: none

## Completed this phase

- Frontmatter made Marketplace-complete: added `category: Data Analysis`; name/license/author kept; dir renamed to match `name`.
- SKILL.md trimmed 27.4K -> 21.2K: per-tool failure modes, rMATS/leafcutter reconciliation, common-error table moved to `references/failure-modes-and-errors.md`; intron retention + microexon sections moved to `references/intron-retention-and-microexons.md`; each leaves a routing paragraph (operational two-family concordance rule kept inline).
- `examples/quantify_splicing.py` moved verbatim to `scripts/quantify_splicing.py` (syntax-checked); "Bundled Code" pointer added to SKILL.md. `usage-guide.md` unchanged.
- Version drift check: all stated minimums (rMATS-turbo 4.3+, SUPPA2 2.4+, leafcutter 0.2.9+, MAJIQ 3.0+, IRFinder-S 2.0+, kallisto 0.50+, Salmon 1.10+, pandas 2.2+, STAR 2.7.11+) are floors still satisfied by current releases (staging has rMATS 4.4.0, Salmon 2.7.0, kallisto 0.52.0, STAR 2.7.11b, pandas 3.0.6 on PyPI); left unchanged, no breakage found.
- LF, UTF-8 no BOM, no __pycache__, no nested LICENSE.

## Required next actions

1. Tooling: use `F:\OpenScience\audit-envs\alternative-splicing\TOOLS.md` (as-core, as-suppa, as-rleaf, as-irfinder, as-shiba already cover most surfaces); build the per-surface coverage map for this Skill.

## Runnable-surface inventory

- rMATS-turbo `rmats.py` (paired, --novelSS, --statoff) + pandas parse of `*.MATS.JC.txt`
- SUPPA2 `generateEvents` / `psiPerEvent` (`scripts/quantify_splicing.py`: run_suppa2_quantification, filter_reliable_events, parse_rmats_output)
- regtools `junctions extract` + `leafcutter_cluster_regtools.py`
- MAJIQ V3 `majiq build/psi`, `voila view` (academic licence)
- IRFinder (`FastQ` mode; Skill names IRFinder-S 2.0)
- Named without commands: Shiba, VAST-TOOLS, MicroExonator, STAR (`--alignSJoverhangMin 6` etc.), gffread, samtools filter, leafcutter_ds.R
- Dependency clues: pandas, suppa (needs statsmodels<=0.14.x; as-core's 0.15 breaks it), bioconda rmats/regtools, leafcutter R pkg (GitHub), perl vast-tools

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| N1 | P2 | deferred | TOOLS.md trap 19, 27 | Audit: SUPPA2 statsmodels pin not stated in Skill; IRFinder-S 2.0 vs installable 1.3.1 and `IRFinder FastQ` mode vs TOOLS.md note (`-m BuildRefFromSTARRef`/BAM) |
| N2 | P2 | deferred | TOOLS.md sec. 3 | MAJIQ V3 (licence-gated) and VAST-TOOLS (VASTDB 6.7 GB) not runnable without access/large download |
| N3 | P2 | deferred | SKILL.md Decision Tree | Skill text references `rna-quantification/alignment-free-quant`, `read-alignment/star-alignment` paths in Related Skills (provider-style names; left as-is) |

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\alternative-splicing\TOOLS.md (not re-fingerprinted here)
- Run evidence: `python tools/skill_preflight.py` -> PASS, warn: no Skill-root LICENSE (manifest must cite repository license evidence; siblings are the same)
- Restricted-access items: MAJIQ V3 licence; VAST-TOOLS VASTDB
- Tooling impact: none (no behavior change; code moved verbatim)
- Heavy surfaces: VAST-TOOLS VASTDB (6.7 GB) only; no GPU

## Worktree safety

- Run-owned changes: F:\OpenScience\wt\norm-bio-splicing-quantification\skills\bio-splicing-quantification\{SKILL.md,usage-guide.md,references\*,scripts\*}; branch normalize/bio-splicing-quantification
- Pre-existing/user-owned changes: records `test/validate.bats` (untracked); shelf `.vscode/` (untracked); untouched
- Records state: this handoff uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
