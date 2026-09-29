> **Audit record for `bio-atac-seq-consensus-peakset`**
> - Audited working candidate `f370a4b24019a815c46f0ed9f0b2171d45a382ed277fc113a4aa77ebec2ba808`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/consensus-peakset), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-29 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Independent re-audit: bio-atac-seq-consensus-peakset

**Date:** 2026-09-29  
**Candidate:** `F:\OpenScience\wt\mercury-pilot-consensus-peakset\skills\bio-atac-seq-consensus-peakset`  
**Exact identity:** `sha256-manifest-v1 f370a4b24019a815c46f0ed9f0b2171d45a382ed277fc113a4aa77ebec2ba808`  
**Result:** Candidate-ready — **91/100, Production Ready**

## Score and readiness

| Measure | Result | Gate |
|---|---:|---:|
| Static | 85/100 | ≥80 — pass |
| Dynamic execution average | 94.3/100 | ≥85 — pass |
| Layer 1 | 38/40 | ≥32 — pass |
| Layer 2 | 56/60 | ≥48 — pass |
| Assertions | 15/15 (100%) | ≥90% — pass |
| Veto gates | None | No veto/open P0 — pass |

The schema record is `report.json`; exact manifest and provenance are in `source-identity.json`.

## Evidence and dispositions

- Canonical public shell run and two-file run were reused only after confirming the exact shell-script SHA-256, cached input hashes, and runtime fingerprint are unchanged. Public output: 3,000 pooled → 2,927 iterative → 2,886 final 501 bp peaks and 2,886 SAF rows. Two-file output: 400 pooled → 393 iterative → 388 final peaks and SAF rows. Both output families passed recorded schema, coordinate, width, ordering, bounds, blacklist, and BED/SAF correspondence checks.
- BAP-003 is resolved on the exact candidate bytes. The complete R block parsed; its guard was tested using base R mocks before summit arithmetic. The connected Python function was parsed and guard-tested with a mocked BedTool sink; valid endpoint offsets yielded 501 bp intervals and invalid rows were rejected before output construction. See `evidence/r-guard.log` and `evidence/python-guard.log`.
- Reused shell malformed-row and negative-summit evidence rejected both cases before output directory creation; see `evidence/shell-evidence-reuse.md`.
- Full optional R/pybedtools workflows were not executed because `GenomicRanges`, `rtracklayer`, and `pybedtools` are absent. They are not counted as executed. No packages, tools, or data were installed or downloaded. This does not block readiness for the required core Bash workflow and the independently exercised corrected guards.
- Mercury's earlier post-fix `set -e` control-flow claim was treated as advisory and checked against the saved shell rejection evidence: both invalid direct runs exit nonzero, emit one file/line diagnostic, and create no output directory. No unresolved finding remains.

## Handoff

The exact fixed working bytes are **candidate-ready**. The orchestrator may commit and route the candidate through intake; this audit itself did not commit, publish, push, release, or perform Marketplace actions. Canonical seven-section handoff: `F:\optimizing-agent-science-skills\handoff\bio-atac-seq-consensus-peakset-handoff.md`.
