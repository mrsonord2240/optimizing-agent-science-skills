# Fix log: bio-data-visualization-sequence-logos

## 2026-09-23 — backlog correction

Skill `data-visualization/sequence-logos`, branch
`fix/data-visualization-sequence-logos-background-correction`, commit
`2c1d7271a6bfec6c2eebf9b50914e9a3b74f60f3` from staging `8c75e1f4`.
Environment: data-visualization R 4.4.3 with ggseqlogo 0.2.2, Logomaker
0.8.7, and WSL WebLogo 3.7.12. Exact-commit evidence is under
`F:\OpenScience\audits\bio-data-visualization-sequence-logos\run\exact-commit-20260923-200710`.

| finding | priority | change | verification |
| --- | --- | --- | --- |
| `ggseqlogo(..., bg_freq=...)` is not an API and silently left figures uncorrected | P0 | Removed the invalid argument. Added `relative_entropy_logo_matrix()` to calculate `R_i = sum p_i log2(p_i/q_i)` and conventional positive custom heights `p_ia * R_i`, then plot with `method="custom"`. | Exact helper tests check pure, mixed, zero-information, uniform-background equivalence, human and GC-rich backgrounds, scale invariance, matrix orientation, invalid alphabets, and plotted layer heights; exit 0. |
| Uniform-background bias direction was reversed and the illustrative GC composition was inconsistent | P1 | Corrected the direction: uniform background understates letters rarer than 0.25 and overstates commoner letters. Standardised human background to A/T 0.29 and C/G 0.21; corrected the illustrative 72%-GC vector to A/T 0.14 and C/G 0.36 without presenting it as an independently sourced organism estimate. | Helper calibration reproduces the documented exact bit values. |
| Small-sample behaviour was treated as one method across three tools | P1 | Documented ggseqlogo sequence-input `e_n`, ggseqlogo matrix input without that correction, Logomaker's default pseudocount of 1, and WebLogo's prior weight. Added explicit `pseudocount=0` examples and an `n < 5` warning. | Exact R and Logomaker checks reproduce the documented values and boundaries. |
| Logomaker examples created an unused figure, relied on the default pseudocount, named a nonexistent `matrix_type`, used an unavailable font, and blurred signed weights with EDLogo | P1/P2 | Bound `Logo(..., ax=ax)`, made the pseudocount explicit, removed the nonexistent argument/font dependency, and labelled signed log-odds without claiming EDLogo methodology. | Exact Logomaker 0.8.7 validation exits 0 and writes two nonempty PNGs. |
| The shipped R example lacked all of its inputs and mislabeled backgrounds and sample sizes | P1 | Bundled five aligned FASTA fixtures, load every object locally, derive every displayed N, apply the actual background calculation, and write four declared PDFs. | Clean-copy exact run exits 0; the four PDFs are nonempty (32,818 / 38,994 / 24,722 / 24,749 bytes) and no `Rplots.pdf` is created. |
| RNA, matrix-orientation, low-N, and WebLogo dependency guidance was stale or incomplete | P2 | Corrected ggseqlogo matrix orientation, use `--sequence-type rna` for RNA, describe the DNA-on-RNA U-loss trap, warn against scientific interpretation below N=5, and name Ghostscript as required for WebLogo PDF/PNG/SVG on Windows. | Exact WebLogo DNA PDF and RNA PNG commands exit 0; helper rejects missing, duplicate, or extra background symbols. |
| The guide repeated claims that no longer matched the executable examples | P2 | Reconciled the guide with the tested APIs and linked the reusable helper and self-contained example. | Changed R files parse; invalid API patterns are absent; `git diff --check` passes. |

## Findings left unfixed

None of the audit recommendations. The audited Windows R environment has a
shared `cli` 3.6.6 process-teardown crash even after a minimal
`library(ggseqlogo)` load. Exact plotting runs therefore used the existing
process-local `R_PROFILE_USER` cleanup guard; separate receipts confirm
`cli_unloaded=TRUE`. No global profile or package installation was changed.
