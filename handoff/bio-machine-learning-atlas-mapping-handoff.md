# Handoff: bio-machine-learning-atlas-mapping / prepare-scientific-skill-tooling

- Updated: 2026-10-03
- Lane: 3
- Status: ready-for-phase
- Owner leaving: normalize worker (lane 3, machine-learning batch)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/atlas-mapping
- Source identity (skill_preflight, measured on F:\OpenScience\bioSkills-Improved): d48f2ad8492785a79adc83d230a2921db572afe1687859498c4407d57512dba4 (files=4, bytes=29582)
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping
- Branch/worktree: normalize/ml-lane3 from 29f5446 (sparse cone: the four machine-learning Skills of this batch; shared with the three sibling Skills)
- Candidate tree hash: d4048dcc887b51c820dba4669bf05620829970e083f7512d24a2539953ad48a6 (files=5, bytes=30516), taken from `python tools/skill_preflight.py`
- Preflight: PASS; warn: no Skill-root LICENSE (manifest must cite repository license evidence; frontmatter `license: MIT` is present, shelf root LICENSE is MIT, GPTomics)
- Applicable audit: none

## Completed this phase

- Directory named to the Skill ID; frontmatter gains `category: Data Analysis` (name, license, author unchanged).
- `examples/*.py` moved to `scripts/` with only version headers and deprecated-API fixes changed; SKILL.md routes to each with a run line.
- "Per-Method Failure Modes" (and reconciliation table where present) moved to `references/failure-modes.md`, routed from SKILL.md with a read-when line.
- Version drift resolved: scvi-tools 1.5 / scanpy 1.12 / anndata 0.13 / scikit-learn 1.9 / celltypist 1.7 compat line and script headers; SCVI/SCANVI `prepare_query_anndata`, `load_query_data`, `from_scvi_model`, `predict(soft=True)` signatures checked against 1.5.1.
- Scripts re-run against the current environments (see Environment); LF, UTF-8 no BOM, no pycache.

## Structural summary

- `SKILL.md` (core workflow, taxonomy, decision tree, thresholds, common errors, citations), `usage-guide.md` (unchanged), `references/failure-modes.md`, `scripts/` (2 files).
- Scientific content, defaults, thresholds, and citations unchanged.

## Runnable-surface inventory

- `scripts/ood_gating_demo.py` - synthetic, CPU, seconds; ran OK (anndata 0.13, sklearn 1.9).
- `scripts/scarches_annotation.py` - real-data template: needs `reference_labeled.h5ad` (obs `cell_type`, `batch`, `layers['counts']`) and `query.h5ad` in cwd; trains reference scVI 100 epochs + scANVI + surgery. Syntax-checked only. HEAVY: GPU advised, run time and input size depend on the atlas; tooling must supply a small public reference/query or a synthetic substitute.
- SKILL.md inline snippets (scVI/scANVI surgery, kNN OOD gate): scArches calls smoke-ran on a synthetic 2-batch dataset (CPU, 3 epochs, scvi-tools 1.5.1). Methods named but with no code: Symphony (R), Azimuth/Seurat, CellTypist, scPoli, popV, treeArches/scHPL, scGPT/Geneformer.

Dependency clues: scvi-tools, scanpy, anndata, scikit-learn, celltypist (usage-guide `pip install` line); torch via scvi-tools; Symphony/Azimuth need R (not exercised).

## Required next actions

1. Tooling worker: map the surfaces above to the staged environment and record coverage; flag any surface needing public inputs.
2. Do not edit Skill bytes without re-running preflight and updating the identity above.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| none | - | - | - | No blocker. Notes for audit: Unaudited: CellTypist normalization claim, treeArches/popV descriptions, citation accuracy; `predict(soft=True)` returned an ndarray (not a DataFrame) in the smoke run. |

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\ (scvi-tools 1.5.1, scanpy 1.12.4, anndata 0.13.3, celltypist 1.7.1, torch 2.14, CPU-only); TOOLS.md there
- Run evidence: scripts executed in place from the worktree with `PYTHONDONTWRITEBYTECODE=1`; no transcripts saved.
- Restricted-access items: none
- Tooling impact: changed (scripts moved from `examples/` to `scripts/`; deprecated sklearn API replaced)

## Worktree safety

- Run-owned changes: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping\ (untracked, new to the shelf); this handoff
- Pre-existing/user-owned changes: records repo untracked `test/validate.bats` and a modified `handoff/bio-splicing-quantification-handoff.md` (another worker); shelf untracked `.vscode/`; none touched
- Records state: uncommitted handoff file
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
