# Handoff: bio-splicing-quantification / audit-scientific-skill

- Updated: 2026-10-03
- Lane: 2
- Status: ready-for-phase
- Owner leaving: tooling worker (lane 2, full mode)
- Next role: audit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:alternative-splicing/splicing-quantification (source identity de91158720430e45ef20d81624a331dc9457edd99741b6e84e10da22f2315248, files=3, bytes=36158)
- Working tree: F:\OpenScience\wt\norm-bio-splicing-quantification (sparse cone: skills/bio-splicing-quantification)
- Branch/worktree: normalize/bio-splicing-quantification, started at 29f5446 (uncommitted)
- Candidate tree hash: 1e34dbd9664e334b3feb336a3d624ec99d39ca9b5ad9a056f1f7142448bd489c (files=5, bytes=37504; `skill_preflight --offline` PASS, re-verified 2026-10-03, unchanged)
- Applicable audit: none

## Completed this phase

- Verified candidate identity, then ran the Skill's own commands and `scripts/quantify_splicing.py` on real chrX 2v2 and planted data in shared staging (no env/data added).
- Wrote TOOLS.md with the per-surface coverage map, environment fingerprint, blockers and observations.
- Added four scripts to ecosystem tools (`smoke_splicequant*.sh`, `fp_splicequant.sh`); noted in the ecosystem TOOLS.md.
- Normalizer's Skill bytes untouched.

## Required next actions

1. Audit the candidate using TOOLS.md. Spend effort on the observed defects (O1-O3) and on rMATS / SUPPA2 / leafcutter / IRFinder concordance.
2. Label MAJIQ V3 as restricted-access and VAST-TOOLS as not executed; do not request tooling for either.

## Coverage map (detail: TOOLS.md)

| Surface | Status |
|---|---|
| rMATS-turbo 4.4.0 (Skill flags, paired real chrX + planted) | ready |
| pandas parse of `*.MATS.JC.txt` (inline snippet) | ready; snippet fails (O1) |
| `scripts/quantify_splicing.py` (parse_rmats_output, run_suppa2_quantification, filter_reliable_events) | ready; parse_rmats_output fails on 4 of 5 types (O2) |
| SUPPA2 2.4 generateEvents/psiPerEvent (as-suppa) | ready (planted PSI 0.8/0.2/0.5 exact; chrX 7 psi files) |
| regtools 1.0.0 + leafcutter_cluster_regtools.py | ready (0 clusters at `-m 50` on tiny data; 115 at `-m 5`) |
| IRFinder `FastQ` mode, **1.3.1** | ready (IRratio r=0.99997 vs BAM mode) |
| STAR/Salmon/kallisto upstream | ready, optional |
| MAJIQ V3 build/psi/voila | restricted-access (licence form, not attempted) |
| VAST-TOOLS (VASTDB 6.7 GB) | heavy-optional, not tooled; Skill must label not executed |
| MicroExonator, S-IRFindeR, iREAD, leafcutter2, IRFinder-S 2.0 | not installed, mention-only |

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| O1 | P1 candidate | open | TOOLS.md obs. 1; logs\smoke_splicequant (A2) | Audit: SKILL.md inline `se_jc[inc_cols].mean(axis=1)` raises TypeError on real rMATS output (comma-string IncLevel, also matches `IncLevelDifference`) |
| O2 | P1 candidate | open | TOOLS.md obs. 2 | Audit: `parse_rmats_output` KeyError (`exonStart_0base`, `exonEnd`) for A5SS/A3SS/MXE/RI; only SE works |
| O3 | P2 | open | TOOLS.md obs. 3 | Audit: SUPPA2 statsmodels<=0.14.x pin not stated (as-core 0.15.0 breaks suppa.py); TPM header must omit index-name cell |
| N1 | P2 | open | TOOLS.md obs. 4 | IRFinder-S 2.0 named; only IRFinder 1.3.1 available; `-m BuildRef` is FTP-only, use `BuildRefFromSTARRef` |
| N2 | P2 | restricted | TOOLS.md Blockers | MAJIQ V3 licence; user action: register and install; then tooling delta |
| N3 | P2 | deferred | SKILL.md Related Skills | Provider-style cross-skill names left as-is |

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-splicing-quantification\TOOLS.md, sha256 `48cde79a160428e3ae04f5505701b446bae203983b02aca6a9f3f21cdd1e00ed` (written before the handoff; recompute if edited)
- Environment fingerprint: combined sha256 `20c07bbbf63a972c04364225b028c9c83e0ee45a0ee9ee775cc56d7a8c26ad3c` (as-core 4c5897dd..., as-suppa 01529643..., as-irfinder 96dde80d...; `tools\fp_splicequant.sh`)
- Staging: F:\OpenScience\audit-envs\alternative-splicing\ (reused); smoke output `logs\smoke_splicequant\`; driver `wsl_run.sh 'bash /mnt/openscience/audit-envs/alternative-splicing/tools/smoke_splicequant.sh'`
- IRFinder reference lives at `logs\smoke_irfinder\ref` (do not rerun `tools\smoke_irfinder.sh`, it recreates that directory)
- Restricted-access items: MAJIQ V3
- Tooling impact: none (no Skill bytes changed in this phase)
- Heavy surfaces: VAST-TOOLS VASTDB only; no GPU

## Worktree safety

- Run-owned changes: F:\OpenScience\audits\bio-splicing-quantification\TOOLS.md; ecosystem tools\smoke_splicequant*.sh, tools\fp_splicequant.sh, logs\smoke_splicequant\, one appended note in alternative-splicing\TOOLS.md
- Pre-existing/user-owned changes: records `test/validate.bats` (untracked); shelf `.vscode/` (untracked); untouched
- Records state: this handoff uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
