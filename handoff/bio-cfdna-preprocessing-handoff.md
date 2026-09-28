# Handoff: bio-cfdna-preprocessing / candidate-ready

- Updated: 2026-09-28T13:36:00-07:00
- Lane: 4
- Status: candidate-ready
- Owner leaving: reaudit-scientific-skill
- Next role: orchestrator

## Source identity

- Origin: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:liquid-biopsy/cfdna-preprocessing`; upstream subtree `aeaf01458e707a8084c054de0411d9a641b36e5a` remained read-only.
- Working tree: `F:\OpenScience\wt\opt10-cfdna\skills\bio-cfdna-preprocessing`; branch `optimize/ten-20260928-lane4-cfdna`; HEAD `0bc0b31fc52742dbec1034f698103434cc9460c3`.
- Certified candidate: `sha256-manifest-v1:148b254a310719e781dacc9a782cd45f61e6cc8dd508124e1941d589458b47e1` (7 files, 696-byte manifest), independently identical before and after execution.
- Final audit: `F:\OpenScience\audits\bio-cfdna-preprocessing\reaudit-opt10-20260928`; `report.json` SHA-256 `b35c496ce12d8447f450dca102efe7d3e1a6d23de65831a20a7f998f77922a8d`; `viewer.md` SHA-256 `3d7a2dc9553b856ca4714f7951a07f76502181f99d3e864e01a330efb4526423`.

## Completed this phase

- Independently reinspected all 7 candidate files and verified the strict schema, both veto gates, scientific claims, runnable topology, path safety, output readability, and every prior finding.
- Ran four persistent fresh workflows: simplex 4 final records; duplex 2; second duplex repeat 2; metacharacter-path simplex 4. All final BAMs are coordinate-sorted, indexed, and pass `samtools quickcheck`.
- Verified RX/ZA/ZB on 32/32 extracted and first-zipped records; query-grouped FASTQ/BWA/Zipper topology; MI on 32/32 grouped records; queryname filtering before coordinate sort/index.
- Ran the shipped live suite: 6/6 tests, 0 skips, exit 0 in 427.209 seconds, including ten consecutive complete calls with stable four-record output.
- Reproduced public and fresh-bound fragment QC, flag/bound/empty behavior, argv-only safety, assay-conditional guidance, and six primary DOI records.
- Strict validator passed: static 96, execution 96.2, Layer 1 average 38.6/40, Layer 2 average 57.6/60, assertions 25/25, final 96 Production Ready.

## Required next actions

1. Preserve the exact candidate identity when assembling the single run-closing product commit; after commit, bind the accepted audit to the resulting provider commit/tree as required by the records contract. The orchestrator published the exact final audit as `candidate@148b254a3107-reaudit-opt10-20260928` with nine explicit artifacts; raw/published report SHA-256 values match and generated audit views pass `audits:check`.
2. Continue the ten-skill batch workflow; no further fixer or tooling-delta pass is required for this lane.

## Open findings and blockers

| ID | Severity | Final state | Evidence | Required disposition |
|---|:---:|---|---|---|
| CFD-001 | P0 | closed | `evidence/reaudit-results.json`: RX/ZA/ZB 32/32 across all fresh runs | none |
| CFD-002 | P0 | closed | captured `samtools fastq` → `bwa mem -C -p` → `ZipperBams`; 32 mapped/tagged records | none |
| CFD-003 | P0 | closed | queryname filter inputs; coordinate/indexed/quickcheck final BAMs | none |
| CFD-004 | P0 | closed | zero `shell=True`/`eval`/`exec`; literal semicolon/dollar/bracket paths pass with no side effect | none |
| CFD-005 | P1 | closed | flag fixture accepts 1/5; invalid bounds and empty BAM pass | none |
| CFD-006 | P1 | closed | conditional guidance concepts and six primary DOI records verified | none |
| Access/tooling blocker | P0 | none | all advertised surfaces executed in the pinned environment | none |

## Environment and evidence

- Tooling: `F:\OpenScience\audit-envs\bio-cfdna-preprocessing\TOOLS.md`, SHA-256 `fdb57ccfb05205d8eb35a05bd140d526a14ba55108ba33fd88d7127872b4e6ed`; fingerprint SHA-256 `32602b728943ee66f7f2156df0a5a5cd08410d0cdd46e56c7af35233ac6336a7`.
- Environment: WSL `science` / `sci`; Python 3.12.14; NumPy 1.26.4; pysam 0.22.1; fgbio 4.1.1; bwa 0.7.19-r1273; samtools 1.24; lock SHA-256 `de8e635467ca49547a3b9d678525df4944ac48eb9d4fec7a3c8a121f57a8f269`.
- Evidence: `evidence/reaudit-results.json` SHA-256 `870b90dc411ca8e1e90714f048d0325a0b8cf4675a862d53debdc746e6ca1571`; shipped-suite summary SHA-256 `743cceefc111d1a79256083ff75da529acc1beb5eef04d9497323aae856268e9`; full suite stderr SHA-256 `aff0498532db5764e949b4ce86e95dd5b78b35c7c7208041afed6090246ba945`.
- Failed or blocked surfaces: none. Java 25 emits a future native-access warning for fgbio; all current calls complete and it is not a candidate blocker.

## Worktree safety

- Candidate bytes remained unchanged; product status is still only the pre-existing untracked candidate subtree, with no cache artifact retained.
- Run-owned writes are confined to the raw re-audit root and this canonical handoff; persistent binary stages are under raw `work/` and are not required publication artifacts.
- No product commit, push, PR, release, shared audit publication, Marketplace action, origin-checkout change, or sibling-lane change was made.

## Transition assertion

- Next-phase prerequisites met: yes.
- Exact candidate is **candidate-ready**: score 96, static 96, execution 96.2, Layer 1 38.6/40, Layer 2 57.6/60, assertions 25/25, both veto gates PASS, no open P0/P1/P2, and every accessible advertised surface executed with inspected passing output.
