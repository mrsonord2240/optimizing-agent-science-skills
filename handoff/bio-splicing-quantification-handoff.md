# Handoff: bio-splicing-quantification / fix-scientific-skill

- Updated: 2026-10-03
- Lane: 2
- Status: ready-for-phase
- Owner leaving: initial-audit worker (lane 2)
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:alternative-splicing/splicing-quantification (subtree 6e11b64e5f1c319983ec851f3d922655291db35a)
- Working tree: F:\OpenScience\wt\norm-bio-splicing-quantification (sparse cone: skills/bio-splicing-quantification)
- Branch/worktree: normalize/bio-splicing-quantification, started at 29f5446 (uncommitted by design)
- Candidate tree hash: 1e34dbd9664e334b3feb336a3d624ec99d39ca9b5ad9a056f1f7142448bd489c (files=5, bytes=37504; `skill_preflight --offline` PASS before and after the audit; no Skill bytes edited, no audit-local repair)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-splicing-quantification\candidate@1e34dbd9664e-run-initial-1 (raw run: F:\OpenScience\audits\bio-splicing-quantification\run-initial-1; report.json, viewer.md). Score 64 numeric (Beta Only), recorded Reject because Research Veto M4 (code usability) FAILS. Static 69, execution 61.3, assertions 13/26.

## Completed this phase

- Verified identity, then executed rMATS (real chrX 2v2 and planted), SUPPA2 (planted, real, concordance with rMATS r 0.72-0.86), regtools + leafcutter (with and without XS tags), IRFinder, and the shipped script; the tooling leads O1-O3, N1 and N3 reproduced.
- Published the record (13 scripts/inputs) and regenerated INDEX, BACKLOG, STATUS.md and STATUS.html; `audits:check` passes.

## Required next actions

1. Fix SQ-01 to SQ-03 first (they clear the veto): working inline snippet, `parse_rmats_output` for all five event types, mean over IncLevel1/IncLevel2 only (never IncLevelDifference), junction filter on both groups; add a regression on `public-data\planted`.
2. Fix SQ-04 (XS-tag prerequisite for regtools/leafcutter) and SQ-05 (`IRFinder -m FastQ`, reference build via `BuildRefFromSTARRef`, IRFinder-S 2.0 unverified).
3. Then P2: SQ-06 to SQ-11. Execute every changed command again; classify tooling impact for re-audit.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| SQ-01 | P1 | open | run-initial-1\scripts\03_analyze.py sec. 1; evidence\03.log | Inline snippet raises TypeError on real JC output |
| SQ-02 | P1 | open | 03_analyze.py sec. 2 | parse_rmats_output KeyError for A5SS/A3SS/MXE/RI (columns: longExon*/shortE*/flanking*, 1stExon*/2ndExon*, riExon*) |
| SQ-03 | P1 | open | 03_analyze.py sec. 3 | mean_PSI wrong in 310/958 SE rows (IncLevelDifference included); filters use SAMPLE_1 only |
| SQ-04 | P1 | open | 01_run_tools.sh sec. E; 02_leafcutter_m5_irf.sh | No XS prerequisite: strand ?, 0 clusters (115 with XS at -m 5) |
| SQ-05 | P1 | open | 01_run_tools.sh sec. F | IRFinder literal syntax fails; IRFinder-S 2.0 not obtainable (1.3.1) |
| SQ-06 | P2 | open | 01_run_tools.sh sec. C-D | SUPPA2 TPM header contract; statsmodels<0.15 pin |
| SQ-07 | P2 | open | scripts/quantify_splicing.py | PSI filter 0.1-0.9 vs Skill 0.05-0.95; default-filter claim |
| SQ-08 | P2 | open | 03_analyze.py sec. 4 | JC IncFormLen excludes exon body (98 vs JCEC 149) |
| SQ-09 | P2 | open | viewer.md | Label MAJIQ V3 (restricted) and VAST-TOOLS (heavy-optional) as not executed; mark unsourced figures |
| SQ-10 | P2 | open | SKILL.md Related Skills | Names do not resolve on the shelf; STAR and alignment-free-quant Skills absent |
| SQ-11 | P2 | open | SKILL.md, usage-guide.md | BAM-list format, leafcutter script source, Skill-root LICENSE |

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-splicing-quantification\TOOLS.md, sha256 `48cde79a160428e3ae04f5505701b446bae203983b02aca6a9f3f21cdd1e00ed`
- Environment fingerprint: combined sha256 `20c07bbbf63a972c04364225b028c9c83e0ee45a0ee9ee775cc56d7a8c26ad3c` (as-core, as-suppa, as-irfinder; no environment changed)
- Run evidence: run-initial-1\out (local raw outputs), scripts\ and scripts\evidence (published); driver `wsl_run.sh 'bash /mnt/openscience/audits/bio-splicing-quantification/run-initial-1/scripts/01_run_tools.sh'`
- Deferred / static-only: MAJIQ V3 (restricted-access licence), VAST-TOOLS (heavy-optional), Shiba, MicroExonator, S-IRFindeR, iREAD, leafcutter2, IRFinder-S 2.0
- Restricted-access items: MAJIQ V3 (register under licence, install, then tooling delta)
- Tooling impact for the fixer to reassess: none expected unless the fix adds tools; IRFinder reference at `logs\smoke_irfinder\ref` is read-only (do not rerun `smoke_irfinder.sh`)

## Worktree safety

- Run-owned changes: F:\OpenScience\audits\bio-splicing-quantification\run-initial-1\; records repo audits\skills\bio-splicing-quantification\, audits\INDEX.md, BACKLOG.md, STATUS.md, STATUS.html (uncommitted for the orchestrator); this handoff
- Pre-existing/user-owned changes: records `test/validate.bats` (untracked), shelf `.vscode/` (untracked); untouched
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
