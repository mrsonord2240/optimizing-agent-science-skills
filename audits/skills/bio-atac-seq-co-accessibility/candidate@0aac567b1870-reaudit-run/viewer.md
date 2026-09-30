> **Audit record for `bio-atac-seq-co-accessibility`**
> - Audited working candidate `0aac567b1870fb501220470d665c600af91f274cfa816e649bdcad81db8c8afa`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/co-accessibility), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Audit viewer: bio-atac-seq-co-accessibility (independent final re-audit, 2026-09-30)

Candidate `sha256-manifest-v1 0aac567b1870fb501220470d665c600af91f274cfa816e649bdcad81db8c8afa` (5 files, 37512 bytes), origin `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/co-accessibility`. Prior audit identity 3c8089b0... (63/100).

**Result: 85 / 100 (84.6 unrounded), Production Ready, candidate-ready.** Static 82 (x0.4 = 32.8), execution average 86.3 (x0.6 = 51.8), assertions 31/32. Layer 1 average 34.7, Layer 2 average 51.6. Skill veto PASS, research veto PASS. The margin over the 85 gate is thin; the score is the schema's integer rounding of 84.6.

## Inputs

| # | Type | Input | Status | Total | Assertions |
|---|---|---|---|---|---|
| 1 | Canonical | Shipped CLI on real 3-chromosome PBMC Multiome ATAC slice (766 peaks x 2,701 cells, pattern-format .mtx) with 4th-arg TSS BED | COMPLETED | 91 | 5/5 |
| 2 | Variant A | run_cicero_pipeline API: window=1e6 (multi-chromosome), tss_bed=NULL branch, seed reproducibility | COMPLETED | 87 | 5/5 |
| 3 | Variant B | ArchR addCoAccessibility/getCoAccessibility as documented on public PBMC 5k chr1 slice | COMPLETED | 84 | 4/4 |
| 4 | Edge | Synthetic planted-truth dataset (60 peaks, 4 latent states, 4 co-varying peak groups) plus a threshold that leaves zero strong pairs | COMPLETED | 92 | 5/5 |
| 5 | Stress | Shipped CLI on the larger real PBMC 5k chr1:1-30 Mb slice (1,726 peaks x 3,277 cells, pattern .mtx) | COMPLETED | 86 | 4/4 |
| 6 | Scope Boundary | Downstream doc snippets on the CLI output: locus arc plot (>0.5) and Hi-C concordance against a planted BEDPE | COMPLETED | 86 | 4/4 |
| 7 | Adversarial | Failure guards: dimension mismatch, colon-format peak names, missing TSS BED, BED without gene column, and a cell with zero reads | COMPLETED | 78 | 4/5 |

## Prior findings

| ID | Severity | Disposition | Independent evidence |
|---|---|---|---|
| COACC-001 | P1 | fixed | CLI on a pattern-format .mtx exits 0 (inputs 1, 5) |
| COACC-002 | P1 | fixed | enhancer column holds peak names; set equals independent recomputation (inputs 1, 5) |
| COACC-003 | P2 | fixed | genome_df from peaks; 3-chromosome and 30 Mb runs complete in 5-6 min; whole-genome run remains untested (after-action, not a finding) |
| COACC-004 | P2 | fixed | cicero 1.3.x GitHub monocle3 branch stated consistently in script header, usage-guide, method-reference; live cicero 1.3.9 |
| COACC-005 | P2 | fixed | one row per unordered pair; counts reported as unordered (inputs 1, 2, 5, 6) |
| COACC-006 | P2 | fixed | window replaces genomic_distance_max; window=1e6 executed (input 2) |
| COACC-007 | P2 | fixed | range -1..1 with negatives and NA handling verified against observed -0.48..0.96 (input 4) |
| COACC-008 | P2 | fixed | locus snippet renders a readable arc figure (input 6); arc width is not score-scaled and is not claimed |
| COACC-009 | P2 | fixed | optional TSS BED, early guards, enhancer_is_promoter flag, peak-name regex (inputs 1, 2, 7) |
| COACC-010 | P3 | fixed | SimpleList wording verified by running ArchR (input 3) |
| COACC-011 | P3 | fixed | concordance bands labelled unsourced heuristics; '>50K cells' labelled unverified (static) |
| COACC-012 | P3 | deferred-with-rationale | SCENIC+ wording corrected and labelled not executed / static review only; restricted-access, not retried |
| COACC-013 | P3 | fixed | Status column in SKILL.md quick start; LinkPeaks runtime caveat matches the 8 min 23 s / 150 gene tooling log; LinkPeaks not rerun (doc-only change, env fingerprint unchanged) |

## New findings (non-blocking)

| ID | Severity | Summary |
|---|---|---|
| COACC-014 | P2 | A cell with zero reads in the peak set halts the pipeline with 'attempt to set an attribute on NULL' |
| COACC-015 | P3 | Prompt says tssRegion=c(-2000, 500) while the script and SKILL use TSS +/- 2 kb |

Report recommendations use P2 only (schema allows P0-P2); both new findings share one P2 recommendation. Ledger: `findings.json`.

## Execution classification

Executed: CLI (pattern .mtx, 3-chromosome and 30 Mb real slices), function API (window=1e6, tss_bed=NULL, seed), planted-truth recovery, guards, arc plot, Hi-C snippet, ArchR. Reused with matching runtime: alpha block and permutation control, LinkPeaks (150 genes). Failed (loud): zero-read cell. Static-only restricted: SCENIC+ (the Skill states it was not executed). Blocked: whole-genome run. See `execution-classifications.json`.

## Coverage gaps and after-action

- Whole-genome run untested: 3 chromosomes and chr1 30 Mb complete in 5-6 min and the Skill states runtime only for chr1, so the gap is a documented limit, not a defect. Rerun with a full-genome matrix and `timeout 7200`.
- LinkPeaks not rerun after doc-only edits; the documented 8 min / 150 gene figure matches the tooling log (8 m 23 s).
- SCENIC+: needs Python <=3.11 env with conda-forge pybedtools, pip-built scenicplus, cisTarget databases, then the Snakemake route on the Multiome h5.
- Fixture note: the cached PBMC 5k scATAC is chr1-only, so the multi-chromosome run used the public 10x PBMC granulocyte-sorted 3k Multiome ATAC peaks (chr1/chr2/chr19 up to 4 Mb).

## Reproduction

Scripts in `scripts/` (ra_prep.R, ra_cli.sh, ra_cli_check.R, ra_fn.R/.sh, ra_docs.R, ra_archr.R, ra_stress.sh, build_report.py); logs in `logs/`; heavy work under `F:\OpenScience\audit-envs\bio-atac-seq-co-accessibility\work\reaudit`. Environment per `../TOOLS.md`. Run inside WSL: `bash /mnt/openscience/audits/bio-atac-seq-co-accessibility/reaudit-run/scripts/ra_cli.sh`.
