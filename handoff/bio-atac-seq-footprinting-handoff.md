# Handoff: bio-atac-seq-footprinting / reaudit-scientific-skill

- Updated: 2026-09-30 (PDT, fix-run2)
- Lane: 1
- Status: ready-for-phase
- Owner leaving: fix-scientific-skill worker (fix-run2, lane 1)
- Next role: reaudit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/footprinting
- Working tree: `F:\OpenScience\wt\atac-footprinting`; candidate `skills\bio-atac-seq-footprinting` (untracked, uncommitted)
- Branch/worktree: `fix/atac-footprinting`, starting commit `3186916`
- Candidate tree hash: `sha256-manifest-v1 a71e561087bc769f5b14f703c8c535d1fda3a7f90de84d2a4b0dc7ccfb2ade87` (7 files, 42157 bytes; no `__pycache__`, LF). Predecessor `3b6efb4b...690a13e` (delta-tested) and audited `737bd941...84e4cd` are superseded.
- Applicable audit: `F:\OpenScience\audits\bio-atac-seq-footprinting\initial-audit-20260930\` (audited the old identity; re-audit required)

## Completed this phase

- TOOL-D1 fixed: `references/usage-guide.md` RGT line now `pip install --no-deps --force-reinstall --no-cache-dir rgt==1.0.2`, with one sentence saying why (bioconda copy makes plain pip a no-op).
- TOOL-D2 fixed: the stale "not re-run" sentence replaced by one saying the pinned scPrinter line was re-run fresh, builds from source, and needs a C/C++ compiler and git (stated once there).
- Verified in a fresh throwaway env `fpx-rgt` under the lock: old recipe rc 0 but no-op (`RGTDATA` empty); corrected recipe wrote `data.config` and HMMs; `setupGenomicData.py --hg38` on chr1 rc 0; `rgt-hint` on the fix-run chr1 input rc 0, 358 footprints, coordinates identical to the fix-run output. Env removed, live envs unchanged (`g1_run.out`, `g2_cleanup.out`).
- `method-reference.md` row (~131) only points to the usage guide; consistent, unchanged.

## Required next actions

1. Independent re-audit of the new identity. Focus: RGT data recipe, `run_tobias.sh` guards, CTCF QC semantics, concordance definition, scPrinter recipe.

## Fix dispositions (from fix phase, unchanged)

| ID | Sev | State | Note |
|---|---|---|---|
| FOOT-001 | P1 | fixed | warn + exit 3, `ALLOW_NO_CTCF=1` opt-out; tooling delta re-ran it (rc 3 / rc 0) |
| FOOT-002 | P1 | fixed (bulk classic route) | script + pins + fragment recipe; pinned line now re-run fresh and passes; scATAC/cluster and seq2PRINT training out of scope |
| FOOT-003 | P1 | fixed | one env per tool; all four recipes re-solved fresh in this delta, rc 0 |
| FOOT-004 | P2 | fixed | RGT data recipe corrected (TOOL-D1) and verified end to end; HINT gives 358 footprints |
| FOOT-005 | P2 | fixed | `_jaspar.txt` URL 200, sha256 equals cached file |
| FOOT-006 | P2 | fixed | \|change\| ranking among p <= 0.05, verified independently again |
| FOOT-007 | P2 | fixed | quoting and one-match globs (fix-phase runs C/D; not repeated here) |
| FOOT-008 | P2 | fixed | per-condition all/bound/unbound, uncorrected vs corrected; no ChIP-anchored check |
| FOOT-009 | P2 | fixed | concordance measured: HINT 0.406 bound vs 0/31 unbound |
| FOOT-010 | P2 | fixed | crash claim dropped, `-A` documented |
| FOOT-011..015 | P3 | fixed | claim removals/softening, MA0139.2, hyphen flags |

## Findings closed this phase

| ID | Severity | State | Evidence |
|---|---|---|---|
| TOOL-D1 | P2 | fixed | `F:\OpenScience\audits\bio-atac-seq-footprinting\fix-run2\{scripts\g1_rgt_recipe.sh,logs\g1_run.out}` |
| TOOL-D2 | P3 | fixed | usage-guide sentence; compiler need evidenced by `delta-run\logs\d1_scp_pins.log`, TOOLS.md row 14 |

No open findings or restricted-access blockers.

## Environment and evidence

- Tool inventory: `F:\OpenScience\audits\bio-atac-seq-footprinting\TOOLS.md`
- Environment fingerprint: live envs unchanged (`bio-atac-seq-footprinting` 2e685696a81e5d90, `-rgt` 4417c93cad60a195, `-pydnase` bd5268030526965b, `-scprinter` 82f4ffe4c02264e6); fresh-recipe fingerprint `2376c2c2c5ad3f0f` (sha256[:16] of `delta-run\logs\fingerprints.txt`)
- Coverage map: TOOLS.md rows 1-14 (rows 11-14 new in delta)
- Run evidence: `F:\OpenScience\audits\bio-atac-seq-footprinting\{fix-run2,delta-run,fix-run}`
- Restricted-access items: none
- Tooling impact: none (doc-only recipe change; my own fresh-env run verified the corrected recipe end to end; no dependency, version or script changed)

## Worktree safety

- Run-owned changes: `references/usage-guide.md` (only file edited in the Skill), `fix-run2\` records, this handoff
- Pre-existing/user-owned changes (untouched): `tools\run_mercury_worker.py`, `tools\test_run_mercury_worker.py`; other lanes' handoffs
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
