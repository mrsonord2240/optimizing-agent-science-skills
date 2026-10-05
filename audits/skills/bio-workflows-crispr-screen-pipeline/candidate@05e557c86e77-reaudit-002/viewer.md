> **Audit record for `bio-workflows-crispr-screen-pipeline`**
> - Audited working candidate `05e557c86e778a8b2aded50be5391610b18ce2693750b54a662686571ec9acb5`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/workflows/crispr-screen-pipeline), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-04 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-workflows-crispr-screen-pipeline`**
> - Audited working candidate `05e557c86e778a8b2aded50be5391610b18ce2693750b54a662686571ec9acb5`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/workflows/crispr-screen-pipeline), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-04 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Re-audit: bio-workflows-crispr-screen-pipeline (final, full mode, reaudit-002)

Candidate 05e557c86e77 (uncommitted recut, 19 files; `skill_preflight --offline --shape` PASS). Changed since reaudit-001 (sha256 manifest diff): `SKILL.md`, `references/citations.md`, `routes/qc.md`, `scripts/qc.py`. Category Data Analysis, mode D, Complex, 7 inputs.

Static 88 (x0.4 = 35.2); execution average 88.3 (x0.6 = 53.0); final 88. Layer 1 35.4, Layer 2 52.9. Assertions 27/29 (93.1%).

**Decision: candidate-ready** under the canonical gate (no veto, no open P0, all floors met, 11/11 routing PASS, `--shape` PASS). One open P1 (N-01) is recommended for a localized qc.py fix before the commit.

## Routing check (routing/, model cli:claude-haiku-4-5-20251001, 3 repeats, identity 05e557c86e77...)

| Route | Result | Route | Result |
|---|---|---|---|
| count | PASS 3/3 | jacks | PASS 2/3 (r1 no route first) |
| qc | PASS 3/3 | chronos | PASS 2/3 (r1 opened qc, cn-correction, chronos) |
| cn-correction | PASS 3/3 | consensus | PASS 3/3 |
| rra | PASS 2/3 (r2 qc first) | branches | PASS 3/3 |
| bagel2 | PASS 3/3 | mle | PASS 3/3 |
| drugz | PASS 2/3 (r1 no route first) | | |

Cases file equals the audit copy in every request; data dirs for cn-correction and rra are the resampled QC-passing tables and allow_before was added for cn-correction, rra, mle, jacks (disclosed in TOOLS.md).

## Prior findings, as verified

| ID | Disposition |
|---|---|
| F-12 Gini statistic (P0) | Resolved. qc.py on real HAP1: T0 0.057, T18 0.101/0.091/0.091, identical to `mageck.mageckCount.mageckcount_gini` on ln(count+1); A375 plasmid 0.089, endpoints 0.155-0.174; count-route table 0.074 equals countsummary. |
| F-13 confirmation rule (P1) | Resolved. cn-correction 3/3, rra 2/3 (was 0/3). |
| F-14 unenforced gates (P2) | Resolved, labelled: guides>25 and skew reported, not gated. |
| F-15 case edits (P2) | Request text restored; data and allow_before differences disclosed. Residue P2. |
| F-10 drugz paired (P2) | Open, deferred. |
| F-11 LICENSE (P2) | Open, deferred. |

## New findings

- **N-01 P1** Default replicate pattern does not group `A375_C902R1_P1D14`; qc.py prints a note, then `QC PASS`, exit 0. Grouped with `pattern=R\d(?=_P1D14$)` the Pearson is 0.780 and QC FAILs.
- **F-16 P2** The Pearson gate is faithful to its source, but the route's remedy (drop the outlier) does not fit real data and "0.85 comfortable" is unsourced.

## The replicate-Pearson question

MAGeCK-VISPR (Li 2015, Table 1) lists sample correlation "at least 0.8 for replicates" and says it "calculates pairwise Pearson correlations of sample log read counts". MAGeCK's own report plots `cor(log2(normalized count+1))` over all guides. qc.py does the same on log10(raw+1), averaged over within-condition pairs. Pearson is invariant to log base and to per-sample scaling: on HAP1 and A375 log10 raw, log2 raw and log2 size-factor-normalized give the same matrix to 0.002 (scripts/replicate_corr_invariance.py). The statistic, values and samples are faithful; the real screens sit just under the guideline (HAP1 pairs 0.776/0.782/0.808; A375 0.767/0.781/0.792). Not a second Gini-type error. The residual defect is F-16.

## Execution map

| Surface | Class |
|---|---|
| qc.py: real HAP1, real A375 (default and grouped pattern), no-plasmid, bad label, two QC-passing tables, count-route table; independent Gini via MAGeCK function | executed this run |
| rra.py on QC-passing table (3,646 genes, 688 negative hits) | executed this run |
| count, bagel2, consensus, mle, drugz unpaired, jacks, chronos, cn_correction.R, rra on real HAP1, trap trips | reused from reaudit-001 (those bytes unchanged by manifest diff; environment fingerprints unchanged in TOOLS.md) |
| drugz paired, real drug screen | static-only |
| branches, install.md | not-applicable |

Evidence: `F:\OpenScience\fix-evidence\recut-crispr-pipeline\reaudit-002\` (routing.log, routing/, work/).
