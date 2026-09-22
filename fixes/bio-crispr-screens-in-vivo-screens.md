# Fix log: bio-crispr-screens-in-vivo-screens (2026-09-19)

Source: `crispr-screens/in-vivo-screens`, fork branch `fix/cs-invivo` (worktree
`F:\OpenScience\wt\cs-invivo`), commit `f649395`. Audit: 88/100, Production
Ready, deployable, no P0, 2 P1 + 2 P2 open.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| Compound hit-calling threshold (meta-FDR<0.05 AND >=50% animals at per-animal FDR<0.05) called 0/5 planted hits on the audit's synthetic data despite meta-FDR reaching 3e-6 | P1 | Changed the consistency arm to per-animal **nominal** p<0.05 (not FDR<0.05) in SKILL.md's `meta_analyze_animals()` and `examples/per_animal_meta_analysis.py`; added a "Compound hit-calling threshold" doc section with the rationale (per-animal FDR needs more power than typical in vivo cohorts have) and a "flag for manual review" path for genes that clear meta-FDR but fail consistency | ran — copied audit's `run/mageck_out/*.gene_summary.txt` (6 animals, 60 genes, 5 planted hits) to scratchpad; extracted+`py_compile`'d SKILL.md's snippet and ran it, and ran the updated shipped example script, against that data. New rule: 4/5 recovered, 0 false positives among 55 noise genes. 5th planted hit (Gene004, meta-FDR 0.0013, nominal-p in 1/6 animals) now surfaced as "flag for review" instead of silently dropped by either rule | Old rule genuinely gives 0/5 on this data (`animals_at_fdr_05`=0 for every one of 60 genes) — confirmed independently before changing anything |
| SKILL.md/usage-guide.md never mention IACUC / ethical review anywhere, despite describing live-animal tumor implantation throughout | P1 | Added "Ethical & Regulatory Requirements" section to SKILL.md (IACUC approval before starting, protocol citation in publications, 3Rs framing), placed right after front matter; added a one-line pointer in usage-guide.md's Prerequisites section per the dedup rule (full text lives once, in SKILL.md) | docs — matches audit's own recommended fix text and standard practice (IACUC approval, ARRIVE-style citation, 3Rs) | n/a |
| `mageck mle`'s permutation-derived FDR values drift run-to-run, no seed control, undocumented | P2 | Added a determinism note to the MLE section: no `--seed` option exists; report Wald p-values as the stable primary metric; `--permutation-round` (default 2, suggested 10) improves stability but isn't deterministic | ran `mageck mle --help` (MAGeCK 0.5.9.5, this env) — confirmed no seed/random flag anywhere in the option list, `--permutation-round` exists with default 2 | matches audit's own re-run diff finding |
| CRISPR-StAR section has no worked numeric example (unlike the Manguso 2017 focused-library section) | P2 | Added a worked numeric example (30,000 sgRNAs / 4 guides per gene, 1000x transduction representation, 50,000 cells/uL x 200uL = 10M cells/mouse -> 333x pre-bottleneck coverage, 75mg/kg tamoxifen x2 days, 28-day harvest, 118-tumor cohort with a 30-tumor sufficiency finding relevant to 3Rs) | WebSearch + WebFetch against the real paper, not invented | The original Uijttewaal 2025 *Nat Biotechnol* paper does not itself publish a cell-number/MOI recipe (confirmed by the audit's own Input-2 finding). The numbers above are from **Fenoglio et al. 2026, *Cell Rep Methods* 6(7):101470** — a CRISPR-StAR application/validation study co-authored by Uijttewaal, found via WebSearch and read via WebFetch. Cited as a separate reference to avoid misattributing these numbers to the 2025 paper. |

## Incidental fix (found while verifying the P1 above)

`examples/per_animal_meta_analysis.py` had a bare `≥` (U+2265) character inside
an f-string `print()`. On this Windows machine's default `cp1252` console
codec that raises `UnicodeEncodeError` and crashes the script before it can
print any hits — only visible after `PYTHONIOENCODING=utf-8` is forced.
Replaced with ASCII `>=`. Re-verified the script now runs to completion
without any environment workaround.

## Left unfixed

Nothing from the audit's `recommendations[]` list is left open — all 2 P1s
and 2 P2s addressed (4/4).

Not attempted: broader dedup of `usage-guide.md`'s Prerequisites
section (bash install block, required-inputs list) into SKILL.md. That
content exists only in usage-guide.md and arguably belongs in SKILL.md per
the "every pass" dedup rule, but it isn't duplicated (no fact stated twice)
and isn't part of any of the 4 assigned findings — left alone to keep the
diff minimal, flagging here in case a future pass wants it.

## 2026-09-21 (P2 batch fix, commit 7a32183 on fix/crispr-screens-in-vivo-screens)

Env: crispr-screen-analyst (Python venv, pandas 3.0.5, scipy 1.18.1). SKILL.md 266 -> 263 lines (under 300, no split).

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| Ethics requirement not tied to the steps that recommend new animal work | P2 | Pointers to "Ethical & Regulatory Requirements" added at the "increase animals per condition" fix, the arrayed-validation fix, the arrayed-validation threshold row, and a new Validation Checklist section (moved from usage-guide.md, first item is IACUC coverage of follow-up cohorts). The audit named usage-guide.md's steps; those steps now live in SKILL.md, the guide points at SKILL.md. | read + grep (5 references to the section in SKILL.md) | Guide's "What the Agent Will Do" list collapsed to one line naming SKILL.md. |

Also (redundancy pass, no audit finding): the inline `meta_analyze_animals` block duplicated `examples/per_animal_meta_analysis.py`; deleted and pointed at the example. Example run on the audit's 6-animal / 60-gene data (`_pre-fix-20260919/.../mageck_out/animal_1..6.gene_summary.txt`): 4 hits (Gene000-003), Gene004 flagged for review, matching SKILL.md's stated 4/5 + 1 flagged.

### Left unfixed

- Nothing from the audit's single P2 is left open (1/1).
- `mageck mle` design-matrix heredoc in "Hit Calling for In Vivo" stays inline: a 6-row illustrative matrix, not a runnable script (needs the user's own count table). No `scripts/` move.
- Disagreement logged: usage-guide.md's checklist said per-animal depth >=100 reads/sgRNA; SKILL.md says >=500 reads/sgRNA at endpoint and >=50x coverage. Kept SKILL.md's, did not carry the 100 figure over.

### Deleted passage -> new home

| deleted (usage-guide.md) | now |
| --- | --- |
| Prerequisites install block (`conda install -c bioconda mageck`, pip) | SKILL.md "Version Compatibility" (Install line; added statsmodels, which the example imports) |
| Required inputs numbers (n=10+, 3,000-15,000 sgRNAs) | guide names SKILL.md "Quantitative Thresholds" / "Focused Library Design" |
| "What the Agent Will Do" 14-step list | SKILL.md decision flow, Hit Calling, Validation Checklist |
| Tips: genome-wide library failure, syngeneic for immune screens, n=10+ animals, Cas9 selection, CEGv2 calibration, CRISPR-StAR, heterogeneity | already in SKILL.md (bottleneck math, Syngeneic decision rule, Failure Modes, CRISPR-StAR section) |
| Tips: n=10 at 100x beats n=3 at 500x | SKILL.md Quantitative Thresholds ("Depth vs breadth") |
| Tips: metastasis screens per-site | SKILL.md Failure Modes, "Tumor heterogeneity" fix |
| Decision Cheat Sheet, Thresholds tables | SKILL.md "Syngeneic vs Xenograft vs PDX" and "Quantitative Thresholds" |
| Validation Checklist | SKILL.md "Validation Checklist" (100 reads/sgRNA item dropped, see above) |
