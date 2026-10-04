# bio-splicing-quantification fix pass - 2026-10-03

The documented rMATS code did not run on real output: the inline mean-PSI snippet raised `TypeError`, `parse_rmats_output` raised `KeyError` for every event type except skipped exons, and its `mean_PSI` averaged in the `IncLevelDifference` column, so 310 of 958 skipped-exon rows were wrong by up to 0.5. The parser now handles all five event types for JC and JCEC counts, pools only the two IncLevel columns, and requires read support in every replicate of both groups. The Skill now states the XS-tag prerequisite for leafcutter (untagged STAR BAMs gave zero clusters with exit 0), uses the working `IRFinder -m FastQ` invocation with the reference-build command, states the SUPPA2 TPM header format and `statsmodels<0.15` pin, and labels MAJIQ V3 and VAST-TOOLS as not executed. Later text-only passes corrected the JC effective-length statement and reduced the frontmatter description to its trigger.

- Final candidate audit: `audits/skills/bio-splicing-quantification/candidate@1010225625de-reaudit-delta2-20261003`
- Result: **85/100, Production Ready**; open P2s SQ-12 (raw KeyError on a header-only rMATS file) and SQ-14 (an inexact clause about when the maximum JC lengths are reached).
- Candidate identity: `1010225625de8bd6106b0c187dd8b1459d3ae84e91abeb44a7df95a8bdef792d`.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
