# Handoff: bio-atac-seq-consensus-peakset / committed-byte delta re-audit

## 1. State

- Updated: 2026-09-29; lane 1.
- Status: candidate-ready for the exact committed identity below; this delta audit confirms the prior certification.
- Owner leaving: `reaudit-scientific-skill`.
- Next role: orchestrator; no further product changes are needed for this line-ending delta.

## 2. Candidate identity

- Candidate: `F:\OpenScience\wt\mercury-pilot-consensus-peakset-committed\skills\bio-atac-seq-consensus-peakset`.
- Commit: `5266f50978572b5379ce4ea1b9f2869048cff6c6`; detached worktree clean.
- Certified identity: `sha256-manifest-v1 95aec81162f6948184a6645892e40554840d8ebb5eded0ac5ec354366b7745d2` (5 files; 29,267 bytes; 453-byte canonical manifest).
- Delta from prior certified identity `f370a4b24019a815c46f0ed9f0b2171d45a382ed277fc113a4aa77ebec2ba808`: only 302 CRLF pairs in `references/method-reference.md` became LF. Contents compare equal after line-ending normalization; the other four files have identical hashes and sizes.
- Exact manifest and top-level origin/candidate provenance: `F:\OpenScience\audits\bio-atac-seq-consensus-peakset\final3-commit-bytes-20260929\source-identity.json`.

## 3. Verdict and readiness metrics

- Verdict: **candidate-ready**, 91/100, Production Ready.
- Static 85/100; dynamic average 94.3/100; Layer 1 38/40; Layer 2 56/60; assertions 15/15 (100%); no veto or open P0.
- R and connected Python summit guards were rerun against the exact committed LF reference file. Both pass before coordinate arithmetic/output construction.
- No remaining finding IDs.

## 4. Report and evidence paths

- Raw audit root: `F:\OpenScience\audits\bio-atac-seq-consensus-peakset\final3-commit-bytes-20260929`.
- Schema report: `...\report.json`; readable summary: `...\viewer.md`; exact source provenance and manifest: `...\source-identity.json`.
- Guard harnesses/logs: `...\evidence\check_r_guard.R`, `...\evidence\r-guard.log`, `...\evidence\check_py_guard.py`, `...\evidence\python-guard.log`.
- Verified shell evidence reuse basis: `...\evidence\shell-evidence-reuse.md`; linked detailed output evidence remains in `F:\OpenScience\audits\bio-atac-seq-consensus-peakset\final2-mercury-pilot-20260929\evidence`.

## 5. Failed or blocked surfaces and after-action

- No failed required surfaces or unresolved findings.
- Full optional Bioconductor and pybedtools workflows remain unavailable because `GenomicRanges`, `rtracklayer`, and `pybedtools` are absent; they are not counted as executed. If later required, use an approved environment with these dependencies and inspect valid/invalid narrowPeak end-to-end output. No installation or download occurred.
- Primary shell public and multi-file execution evidence was reused only after checking script SHA-256, live runtime fingerprint, mount/config hashes, and cached input hashes. The shell was unchanged by the commit normalization.

## 6. Worktree and scope

- Audited detached worktree at commit `5266f50978572b5379ce4ea1b9f2869048cff6c6` was clean; candidate files were not edited.
- Origin checkout remained read-only. No commit, push, release, publication, Marketplace action, or unrelated cleanup was performed by this audit.

## 7. Next role

- Route exact identity `95aec81162f6948184a6645892e40554840d8ebb5eded0ac5ec354366b7745d2` to the orchestrator as **candidate-ready**. The committed-byte delta does not change the previously certified readiness disposition.
- Report: `F:\OpenScience\audits\bio-atac-seq-consensus-peakset\final3-commit-bytes-20260929\report.json`.
