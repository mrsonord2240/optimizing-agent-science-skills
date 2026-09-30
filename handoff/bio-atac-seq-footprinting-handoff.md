# Handoff: bio-atac-seq-footprinting / orchestrator (commit and intake)

- Updated: 2026-09-30 (PDT, final re-audit)
- Lane: 1
- Status: candidate-ready
- Owner leaving: reaudit-scientific-skill worker (independent; did not fix, tool or initially audit)
- Next role: optimize-scientific-skills orchestrator (commit the exact bytes to make them `ready`, then intake)

## Readiness decision

**candidate-ready** for `sha256-manifest-v1 a71e561087bc769f5b14f703c8c535d1fda3a7f90de84d2a4b0dc7ccfb2ade87` (7 files, 42,157 bytes). No veto, no open P0 or P1.

| Metric | Value | Gate |
|---|---|---|
| Final | 86 (Production Ready) | >= 85 |
| Static | 87 | >= 80 |
| Execution average | 85.5 (6 inputs) | >= 85 |
| Layer 1 / Layer 2 | 34.8 / 50.7 | >= 32 / >= 48 |
| Assertion pass rate | 27/28 = 96.4 % | >= 90 % |

The execution average clears the gate by 0.5; the one failed assertion (input 3) is the residual P2 below.

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/footprinting
- Working tree: `F:\OpenScience\wt\atac-footprinting\skills\bio-atac-seq-footprinting` (untracked, uncommitted)
- Branch/worktree: `fix/atac-footprinting`, starting commit `3186916`
- Candidate tree hash: `sha256-manifest-v1 a71e561087bc769f5b14f703c8c535d1fda3a7f90de84d2a4b0dc7ccfb2ade87`, recomputed live before and after execution; no `__pycache__`
- Applicable audit: `F:\OpenScience\audits\bio-atac-seq-footprinting\reaudit-run\` (`report.json`, `viewer.md`, `source-identity.json`, `scripts/`, `logs/`, `out/`); not published to the records repo

## Completed this phase

- FOOT-001..003 (P1) retested by execution in fresh recipe envs: CTCF guard rc 3 / `ALLOW_NO_CTCF=1` rc 0, scPrinter bulk route (GPU) bound > unbound at modes 10-30, all four env recipes rc 0 with tested versions (throwaway `ra-footprint*` envs removed; live envs unchanged).
- FOOT-004..015 retested: RGT recipe (plain pip no-op, corrected line works, HINT 358 footprints), ranking equals independent |change| order, spaces-in-path and missing-input guards, concordance recomputed in pure python, JASPAR URL 200.
- Canonical smoke `run_tobias.sh` unmodified (GM12878 vs K562, chr1): rc 0, biology and CTCF profile asserted, PDFs rendered and inspected.
- Excluded modes are labelled untested in SKILL.md, usage guide and method reference.

## Open findings (all P2; none blocks candidate-ready)

| ID | Severity | State | Evidence | Disposition |
|---|---|---|---|---|
| FOOT-008 residual (report rec. 1) | P2 | open | `reaudit-run/logs/r2_check.out` (shim run N) | With corrected == uncorrected the script exits 0 silently; bound dip 7.14 vs 6.67. Skill discloses the limit. Optional: warn on missing corrected-vs-uncorrected gain |
| Report rec. 2 | P2 | open | `references/usage-guide.md` scPrinter block | Bare `pip install` lines do not name the environment |
| Report rec. 3 | P2 | open | `reaudit-run/logs/r3_scp_missing.log` | Missing fragment file gives a raw traceback (rc 1) |

## Failed or blocked surfaces

- None failed. Blocked or untested (after-action, not counted as executed): full-depth (50M read) whole-genome run (resource-infeasible; chr1 slices only); scATAC/cluster scPrinter and seq2PRINT training (excluded, labelled in the Skill); ChIP-anchored CTCF validation (not shipped); PIQ, seqOutBias, chromBPNet bias model (no Skill code).

## Environment and evidence

- Tool inventory: `F:\OpenScience\audits\bio-atac-seq-footprinting\TOOLS.md` (sha256 `303b1224...1484f`); fresh-env fingerprints `reaudit-run\logs\r5_fingerprints.txt`
- Restricted-access items: none
- Tooling impact: none (no Skill bytes or dependencies changed by this phase)
- Rubric: `skill-auditor.zip` sha256 `e54e9ff8...f0de`

## Worktree safety

- Run-owned changes: `F:\OpenScience\audits\bio-atac-seq-footprinting\reaudit-run\`, this handoff; heavy artifacts `F:\OpenScience\audit-envs\bio-atac-seq-footprinting\reaudit-run\` (disposable)
- Pre-existing/user-owned changes (untouched): `tools\run_mercury_worker.py`, `tools\test_run_mercury_worker.py`
- Records state: uncommitted, unpublished
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes. Orchestrator commits the exact audited bytes and publishes the record (`tools/publish_audits.py --run-dir ... --artifact ...`, then `npm run audits:index` and `audits:check`); any Skill byte change invalidates this record.
