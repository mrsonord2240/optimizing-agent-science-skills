# bio-similarity-searching fix pass

Source commit: `87bcd4677e0402e821a95f06f06d8400733606ae`

Fixed all findings from the 2026-09-16 audit:

- Corrected the `Tanimoto = 1.0` and activity-cliff explanation: chirality-blind Morgan fingerprints are the primary observed cause for stereoisomer conflation; hash collisions are secondary. Added chirality-aware generation, standardized identifier checks, and upstream salt-stripping guidance.
- Clarified that Tversky is a feature-overlap ranker, not proof of containment, and added SMARTS confirmation guidance plus an executable helper.
- Split MCS timeout handling on `result.canceled`; tiny uncanceled MCS results now direct users to pre-cluster rather than increase timeout.
- Added retained-pair percentile calibration for thresholds across fingerprint families.

Focused exact-commit re-audit: 9/9 executed, 36/36 assertions passed, 96/100 Production Ready. Canonical report and viewer: `F:\OpenScience\audits\bio-similarity-searching\`.
