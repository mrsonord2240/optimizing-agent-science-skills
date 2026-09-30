# Handoff: bio-atac-seq-footprinting / fix-scientific-skill

- Updated: 2026-09-30 (PDT)
- Lane: 1
- Status: ready-for-phase
- Owner leaving: audit-scientific-skill worker (lane 1, initial audit)
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/footprinting (subtree 7ded85e1af526f2912805fe6da472f78fe2940e8)
- Working tree: `F:\OpenScience\wt\atac-footprinting`; candidate `skills\bio-atac-seq-footprinting` (untracked, uncommitted)
- Branch/worktree: `fix/atac-footprinting`, starting commit `3186916`
- Candidate tree hash: `sha256-manifest-v1 737bd9416e385a3e91eba2ca2d4f5849c575840e866f46392c0e5533cf84e4cd` (5 files); recomputed live at audit start and end, unchanged
- Applicable audit: `F:\OpenScience\audits\bio-atac-seq-footprinting\initial-audit-20260930\report.json` (same identity)

## Completed this phase

- Initial audit: final 70 (Beta Only), static 75, execution avg 66.2, assertions 13/22, no veto. Schema check passed (`scripts\validate_report.py`).
- Executed: run_tobias.sh unmodified (rc 0, biology 4/4), NFR/shift/TOBIAS-on-NFR, edge cases, HINT-ATAC, Wellington (default and -A), scPrinter on GPU.
- Records written: `report.json`, `findings.json` (15 findings), `viewer.md`, `source-identity.json`, `scripts\`, `logs\`, `out\`. Not published to the records repo (orchestrator does that).
- No audit-local repair; no Skill bytes changed.

## Required next actions

1. P1 first: FOOT-001 (run_tobias.sh else-branch for missing CTCF QC), FOOT-002 (scPrinter tested recipe with pins, or narrow claims), FOOT-003 (split-env install, state channels).
2. P2: FOOT-004 to FOOT-010 (rgt data + HINT command, JASPAR `_jaspar.txt` URL, summary sort, quote variables and check outputs, CTCF QC at unselected sites, define the concordance statistic, Wellington `-A`).
3. P3: FOOT-011 to FOOT-015 (stranded-mode claim, tool-table rows, MA0139.2, flag spellings, unsourced numbers).
4. Old normalization items N3 and N4 were not in the received handoff text; N2 is FOOT-007, N1 is closed. Re-derive N3/N4 from the Skill if still wanted.
5. Independent re-audit after fixes; tooling impact to classify (install line, HINT/Wellington/scPrinter recipes change the environment build).

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| FOOT-001 | P1 | open | logs\a2_no_ctcf_and_spaces.log | warn/fail when no CTCF bed |
| FOOT-002 | P1 | open | logs\a8_scprinter.log | tested pinned scPrinter recipe or narrow claims |
| FOOT-003 | P1 | open | logs\a4_static_claims.log | separate envs; TOBIAS alone works |
| FOOT-004 | P2 | open | logs\a9_hint_no_rgtdata.log | RGT data setup + HINT command |
| FOOT-005 | P2 | open | logs\a4_static_claims.log | `_pfms_jaspar.txt` URL |
| FOOT-006 | P2 | open | logs\a1b_assertions.log | fix sort or comment |
| FOOT-007 | P2 | open | logs\a2_no_ctcf_and_spaces.log | quote, array-expand globs, check outputs |
| FOOT-008 | P2 | open | out\a7_ctcf_profiles.png | QC at unselected sites; state what pass shows |
| FOOT-009 | P2 | open | logs\a5b_concordance.log | define overlap statistic |
| FOOT-010 | P2 | open | logs\a5_hint_wellington.log | Wellington `-A`, drop crash claim |
| FOOT-011 to FOOT-015 | P3 | open | findings.json | see ledger |

Deferred/blocked: full-depth whole-genome run (data are chr1 slices, 1.0 M/5.5 M reads); seq2PRINT training and scATAC cluster mode (not run); PIQ/seqOutBias/chromBPNet bias (static-only).

## Environment and evidence

- Tool inventory: `F:\OpenScience\audits\bio-atac-seq-footprinting\TOOLS.md`, sha256[:16] `c8b391741b2801f1` (env fingerprints: main `2e685696a81e5d90`, rgt `4417c93cad60a195`, pydnase `bd5268030526965b`, scprinter `82f4ffe4c02264e6`)
- Run evidence: `F:\OpenScience\audits\bio-atac-seq-footprinting\initial-audit-20260930\{scripts,logs,out}`; heavy runs in `F:\OpenScience\audit-envs\bio-atac-seq-footprinting\audit-20260930\` (a1 reusable for downstream checks)
- Restricted-access items: none
- Tooling impact: none from audit (no Skill change); fixes to install/tool recipes will change it
- Gotchas: Git Bash needs `MSYS_NO_PATHCONV=1` for `wsl.exe ... bash /mnt/...`; do not run heavy TOBIAS jobs concurrently (one lost an output under 3-way load, not reproduced); scripts must stay LF.

## Worktree safety

- Run-owned changes: `F:\OpenScience\audits\bio-atac-seq-footprinting\initial-audit-20260930\`, `...\audit-envs\bio-atac-seq-footprinting\audit-20260930\`, this handoff
- Pre-existing/user-owned changes (untouched): `tools\run_mercury_worker.py`, `tools\test_run_mercury_worker.py`; other lanes' handoffs
- Records state: uncommitted, unpublished
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
