# bio-outlier-splicing-detection fix pass — 2026-09-24

Source commit: `67bce5fe26b6ff241dd81e5efa8bfa22135919e0`

Fixed the open P1/P2 findings from the 2026-09-20 audit:

- made FRASER q selection run on both documented 2.2.0 and 2.6.1 APIs;
- made the FRASER result extraction safe when no significant rows exist;
- made Leafcutter script locations explicit and added count-correlation/PCA tissue-batch QC;
- corrected runtime/OHT observations and removed unsupported tissue-capture and disease-expectation claims; and
- shipped the deterministic synthetic cohort generator and truth contract.

Exact-commit re-audit: 95/100 Production Ready, 8/8 targeted assertions, no open P0/P1/P2. The source generator is byte-identical to the one executed in the prior full audit. See `F:\OpenScience\audits\bio-outlier-splicing-detection\` for the canonical report and viewer.
