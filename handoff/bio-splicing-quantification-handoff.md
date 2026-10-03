# Handoff: bio-splicing-quantification / reaudit-scientific-skill

- Updated: 2026-10-03
- Lane: 2
- Status: ready-for-phase
- Owner leaving: tooling worker (lane 2, delta pass, run-tooling-delta-1)
- Next role: reaudit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:alternative-splicing/splicing-quantification
- Working tree: F:\OpenScience\wt\norm-bio-splicing-quantification\skills\bio-splicing-quantification (untracked/uncommitted by design)
- Branch/worktree: normalize/bio-splicing-quantification, started at 29f5446
- Candidate tree hash: 0c0354add99bca532a1c7168b94a08a1923249a1a7adfddd7f7e9997953355bf (files=5, bytes=42079); `skill_preflight --offline` PASS (one expected no-Skill-root-LICENSE warning); Skill bytes not touched this phase
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-splicing-quantification\candidate@1e34dbd9664e-run-initial-1 (identity 1e34dbd9664e, 64, Reject, veto M4); fixed by run-fix-1 (FIX-LOG: F:\OpenScience\audits\bio-splicing-quantification\run-fix-1\FIX-LOG.md), so a fresh re-audit of the new identity is required

## Completed this phase

- Coverage map refreshed for the changed surfaces, each re-executed on the fixed candidate: inline rMATS snippet, `parse_rmats_output` (5 event types x JC/JCEC, exact vs independent means), `filter_reliable_events(psi_range)`, `write_suppa_tpm` + SUPPA2 (planted 0.8/0.2/0.5), IRFinder `-m FastQ` SE and PE, `-m BuildRefFromSTARRef`; `statsmodels<0.15` recorded against as-suppa (0.14.6)
- Environment fault reproduced (rc 1, "could not open readFilesIn=/dev/fd/63") and repaired in staging: `tools\bin\IRFinder` now puts as-core bin first; documented command works unmodified (rc 0, ref built; FastQ SE/PE rc 0, 7,955 rows, IRratio r = 1.0 vs fixer's run)
- Environment fingerprint UNCHANGED (combined 20c07bbb...); no env, package or dataset changed
- `TOOLS.md` rewritten in delta mode; ecosystem TOOLS.md note updated (as-irfinder row, trap 27)

## Required next actions

1. Fresh re-audit of identity 0c0354add99b...; use TOOLS.md coverage rows 2, 3, 4, 5, 5b, 8, 8b as the executable surface for the fixed behaviour
2. Label MAJIQ V3/VOILA (restricted licence) and VAST-TOOLS (heavy optional) as not executed; do not attempt them

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| SQ-01..SQ-11 | P1/P2 | fixed by run-fix-1, awaiting independent re-audit | run-fix-1\FIX-LOG.md | verify on the new identity |

Blockers: none. Restricted/not executed by design: MAJIQ V3/VOILA (licence form), VAST-TOOLS (VASTDB 6.7 GB); also Shiba, MicroExonator, S-IRFindeR, iREAD, IRFinder-S 2.0 (installable is IRFinder 1.3.1).

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-splicing-quantification\TOOLS.md (sha256 in the tooling report; environment fingerprint unchanged, combined `20c07bbbf63a972c04364225b028c9c83e0ee45a0ee9ee775cc56d7a8c26ad3c`)
- Run evidence: F:\OpenScience\audits\bio-splicing-quantification\run-tooling-delta-1\ (scripts\ 20-23, evidence\ 20_repro_before, 21_after_fix, 22_delta_smoke, 23_irf_fastq, 24_fingerprint, IRFinder.wrapper.orig; out\ local raw)
- Staging: F:\OpenScience\audit-envs\alternative-splicing\ ; changed only tools\bin\IRFinder and its TOOLS.md. Do NOT rerun tools\smoke_irfinder.sh (recreates logs\smoke_irfinder\ref)
- Restricted-access items: MAJIQ V3 (unchanged)
- Tooling impact: none (delta resolved; nothing further to refresh)

## Worktree safety

- Run-owned changes: run-tooling-delta-1\, audits TOOLS.md, staging tools\bin\IRFinder, staging TOOLS.md, this handoff
- Pre-existing/user-owned changes: records test/validate.bats (untracked), shelf .vscode/ (untracked); untouched
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
