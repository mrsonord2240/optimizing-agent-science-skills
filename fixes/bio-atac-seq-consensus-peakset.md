# bio-atac-seq-consensus-peakset fix pass — 2026-09-29

The optimization relay resolved all three audit findings and independently
re-audited the exact final candidate bytes.

- BAP-001: the runnable shell workflow now requires ten-column narrowPeak
  records and rejects missing, `-1`, negative, and out-of-range summit offsets
  before coordinate arithmetic or output creation.
- BAP-002: the shipped script now uses Linux-compatible LF line endings and
  launches directly under Bash.
- BAP-003: the documented R and Python re-centering routes now validate summit
  offsets before coordinate arithmetic; focused base-language guard harnesses
  cover valid boundaries and invalid sentinel/missing/out-of-range cases.

- Final candidate audit: `audits/skills/bio-atac-seq-consensus-peakset/candidate@95aec81162f6-final3-commit-bytes-20260929`
- Result: **91/100, Production Ready**; **15/15 assertions pass**; both vetoes pass; no open P0 or required recommendation.
- Candidate identity: `95aec81162f6948184a6645892e40554840d8ebb5eded0ac5ec354366b7745d2`.

The provider binding record will be the canonical proof that the committed
shelf bytes match this independently audited candidate.
