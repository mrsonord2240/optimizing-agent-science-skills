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

- Final candidate audit: `audits/skills/bio-atac-seq-consensus-peakset/candidate@f370a4b24019-final2-mercury-pilot-20260929`
- Result: **91/100, Production Ready**; **15/15 assertions pass**; both vetoes pass; no open P0 or required recommendation.
- Candidate identity: `f370a4b24019a815c46f0ed9f0b2171d45a382ed277fc113a4aa77ebec2ba808`.

The provider binding record will be the canonical proof that the committed
shelf bytes match this independently audited candidate.
