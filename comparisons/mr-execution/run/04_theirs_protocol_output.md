# Response an agent loaded with `mendelian-randomization-protocol-designer` / `two-sample-mr-exposure-screening-reference-grounded` gives to the shared requests

Request given: "I have two-sample summary statistics for exposure X (exposure_gwas.tsv, ~400 SNPs, N=200k) and
outcome Y (outcome_gwas.tsv, N=100k). Estimate the causal effect of X on Y and tell me whether pleiotropy is a problem."

Both SKILL.md files say the task is to "generate a complete, structured research design", not run anything; there is
no script, and their references list tools (TwoSampleMR, MRPRESSO, ...) but no code or call signatures. An agent
following them does what the prose says: it emits the A-J protocol. Written below as that agent would (abridged only in length, not in section coverage).

## A. Study framing
Causal question: does genetically proxied X affect Y (one-way, two-sample, IVW primary). Assumptions stated: EUR ancestry
matched, non-overlapping samples, genome-wide-significant instruments.

## B. Workload configurations
| Config | Modules | Workload |
|---|---|---|
| Lite | IVW + Egger + weighted median | 2-4 wk |
| Standard | + heterogeneity (Q), pleiotropy (Egger intercept, MR-PRESSO), leave-one-out, Steiger | 4-8 wk |
| Advanced | + reverse MR / MVMR, replication GWAS | 8-12 wk |
| Publication+ | + reviewer downgrade map, triangulation | 12+ wk |

## C. Recommended primary plan: Standard, pattern A + C (single-exposure + robustness)

## D. Step-by-step workflow
> **Dataset Disclaimer:** Any datasets mentioned below are provided for reference only. (...)
1. Instruments: p < 5e-8, LD clump (r2 and window declared), F-statistic screen.
2. Harmonise alleles; drop/handle palindromic SNPs conservatively.
3. IVW primary. 4. Weighted median, MR-Egger. 5. Cochran Q, Egger intercept, MR-PRESSO "when justified". 6. Leave-one-out. 7. Steiger.

## E-F. Data architecture, methods (necessary / recommended / optional table)
Per method-library.md defaults: IVW default primary; sensitivity set = Egger + weighted median + leave-one-out at minimum.

## G-I. Validation tiers, bias review, claim boundaries
Tiers: nominal -> sensitivity-qualified -> robust prioritized -> follow-up priority. Downgrade if "evidence of directional
pleiotropy or unresolved outliers". Language: "genetically predicted X was associated with Y".

## J-K. Figures; literature plan (no verified references without browsing -> search strategy + evidence gap)

## L. Minimal executable version: one exposure, one outcome, IVW + basic sensitivity.

# What this response contains about the data
Nothing. No instrument count, no F statistics, no estimate, no Q, no intercept. It cannot say whether pleiotropy is present in these files.
