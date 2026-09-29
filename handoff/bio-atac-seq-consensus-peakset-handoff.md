# Handoff: bio-atac-seq-consensus-peakset / final independent re-audit

## 1. State

- Updated: 2026-09-29; lane 1.
- Status: candidate-ready for the exact fixed identity below.
- Owner leaving: `reaudit-scientific-skill`.
- Next role: orchestrator for candidate commit and intake; audit agent performed no commit or publication.

## 2. Candidate identity

- Candidate: `F:\OpenScience\wt\mercury-pilot-consensus-peakset\skills\bio-atac-seq-consensus-peakset`.
- Branch/base: `optimize/mercury-pilot-consensus-peakset` / `4cc6cabc39ee01dcf3e828e3f8a164b7e155f4fb`.
- Certified identity: `sha256-manifest-v1 f370a4b24019a815c46f0ed9f0b2171d45a382ed277fc113a4aa77ebec2ba808` (5 files; 29,569 bytes; 453-byte canonical manifest). Identity was checked before and after independent guard testing.
- Full manifest and origin provenance: `F:\OpenScience\audits\bio-atac-seq-consensus-peakset\final2-mercury-pilot-20260929\source-identity.json`.
- The prior `87fb708bbca9ff4b4d07e1158e42be3585c1a50605888dbede3ad07332d0964e` identity is superseded; its prior Reject does not describe these bytes.

## 3. Verdict and readiness metrics

- Verdict: **candidate-ready**, score 91/100, Production Ready.
- Static: 85/100; dynamic average: 94.3/100; Layer 1: 38/40; Layer 2: 56/60; assertions: 15/15 (100%); veto gates: none; open P0: none.
- BAP-003 is resolved on the current bytes. Exact R and connected Python guard fragments were independently tested before summit arithmetic/output construction. Prior BAP-001/BAP-002 shell evidence was reused only after matching script bytes, runtime fingerprint, and cached inputs.
- No remaining finding IDs.

## 4. Report and evidence paths

- Raw audit root: `F:\OpenScience\audits\bio-atac-seq-consensus-peakset\final2-mercury-pilot-20260929`.
- Strict schema report: `...\report.json`; readable view: `...\viewer.md`; identity/provenance: `...\source-identity.json`.
- Guard evidence: `...\evidence\r-guard.log`, `...\evidence\python-guard.log`, with reproducible harnesses in the same directory.
- Reuse rationale, hashes, output counts, and shell invalid-case disposition: `...\evidence\shell-evidence-reuse.md`.
- Required core public output: 3,000 pooled → 2,927 iterative → 2,886 fixed-width final BED and matching SAF. Two-file mode: 400 pooled → 393 iterative → 388 final BED and SAF. Recorded output checks cover schemas, width, bounds, sorting, non-overlap, blacklist filtering, and BED/SAF correspondence.

## 5. Failed or blocked surfaces and exact after-action

- No failed required surface and no unresolved blocker to candidate readiness.
- Full optional dependency-backed R and pybedtools workflows were not run because `GenomicRanges`, `rtracklayer`, and `pybedtools` are unavailable. They are explicitly not counted as executed. If those optional runtimes are enabled later, run valid and invalid summit-offset cases end-to-end and inspect resulting range/BED outputs; no packages were installed in this audit.
- Mercury's post-fix `set -e` claim was advisory, not accepted as a finding: saved direct shell evidence was checked; both malformed-nine-column and negative-summit inputs exit 1, issue one file/line diagnostic, and create no output directory.

## 6. Worktree and scope

- Worktree remains at base commit with only the pre-existing untracked Skill subtree; no candidate bytes changed, no files staged or committed.
- Origin checkout remained read-only. No product/control commit, push, release, publication, or Marketplace action occurred.
- Audit artifacts are confined to the lane-1 raw final root; the exact content identity was checked before/after.

## 7. Next role

- Route exact identity `f370a4b24019a815c46f0ed9f0b2171d45a382ed277fc113a4aa77ebec2ba808` to the orchestrator as **candidate-ready** for commit and intake. This is not yet `ready` or `done`; those states require the orchestrator's commit and intake process.
- Report: `F:\OpenScience\audits\bio-atac-seq-consensus-peakset\final2-mercury-pilot-20260929\report.json`.
