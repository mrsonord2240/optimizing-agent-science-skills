# Fix log: bio-microbiome-amplicon-processing

> **2026-09-19, re-auditor note:** this file, the audit folder, and the pre-fix archive were all
> originally named `bio-amplicon-processing` throughout the audit/fix pipeline, but the Skill's own
> `SKILL.md` frontmatter `name:` is `bio-microbiome-amplicon-processing`. `tools/promote_skills.py`
> keys promotion off the frontmatter name (`skill_index()`), so the id mismatch silently excluded
> this Skill from every promotion run to date (it was in `idx` but never in `rep`'s matching keys).
> Renamed this file and `audits/bio-amplicon-processing/` -> `audits/bio-microbiome-amplicon-processing/`
> (and the matching pre-fix archive) to the correct id as part of landing the re-audit. Content below
> is unchanged from the fixer's original pass.

2026-09-19 — fixer pass on `fix/mb-amplicon-proc` (worktree `F:\OpenScience\wt\mb-ap`), base
`mrsonord2240/bioSkills@4ed3e17`. Source audit: `F:\OpenScience\audits\bio-microbiome-amplicon-processing\`
(87/100, Limited Release, deployable, no open P0).

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| SKILL.md's inline DADA2 example (`truncLen=c(240,160)`) and `examples/dada2_workflow.R` (`truncLen=c(240,200)`) both truncate longer than the read length that remains after correctly removing the 19bp 515F/20bp 806R primers from a 2x250 MiSeq V4 read (~231bp/~230bp) - `filterAndTrim` doesn't pad, it silently drops every read that's shorter than truncLen | P1 | Both changed to `truncLen=c(220,200)`. Added a "silent ceiling" paragraph to the `truncLen Is a Detection Budget` section explaining truncLen must respect the post-primer-trim read length, not the raw cycle count; added a matching row to the Quantitative Thresholds table; sharpened the "Few reads pass filter" Common Errors row to name this specific cause instead of only "too long (low-Q tail)" | ran | Independently reproduced from scratch (not reusing the audit's numbers as given): ran real cutadapt (515F/806R) on the audit env's real fixture reads, confirmed trimmed length is 231bp F / 230bp R; ran real `filterAndTrim` with `c(240,160)` and `c(240,200)` - both drop 1989/1989 reads with "No reads passed the filter"; `c(220,200)` passes 1989/1989. Then ran the actual fixed `examples/dada2_workflow.R` file (not a copy) end-to-end on the full 10-sample, 2-run fixture: 12 candidate ASVs -> 11 after chimera removal, 99.5% reads retained, matching the auditor's independently-run numbers. |
| (found during verification, not in the audit) `examples/dada2_workflow.R`'s `ggsave(...)` call crashes `could not find function "ggsave"` - the script only does `library(dada2)`, and `ggsave` lives in ggplot2's namespace, not re-exported by dada2 | P1 (crash, fixed inline per FIX_BRIEF's "shipped scripts that crash" rule) | Added `library(ggplot2)` to the script's imports; added `ggplot2` to usage-guide.md's Prerequisites install line | ran | The end-to-end run above only completed after this fix; before it, the script halted with `Error ... could not find function "ggsave"` right after the first run's error-learning step. |
| P2: no ITS fixture exists to verify the ITS analysis path end-to-end | P2 | Not fixed - left as documented | help | Re-confirmed the audit's own check: real installed ITSxpress 2.2.0 `--help` still lists all six documented flags (`--fastq`, `--fastq2`, `--region`, `--taxa`, `--outfile`, `--threads`) and `ITS2`/`Fungi` are valid values, so nothing is broken. Building a fixture ITSxpress can actually HMM-detect needs real conserved SSU/5.8S/LSU flanking sequence, not arbitrary synthetic reads - not a cheap fixture per FIX_BRIEF's bar, so left untested end-to-end rather than fabricating a fixture that wouldn't prove anything. |
| P2: no reproducibility/seed guidance in the DADA2 examples | P2 | Not added | docs | Checked directly rather than assumed: `?learnErrors`'s Rd docs show `randomize=FALSE` is the default (samples processed in file order, not randomly) - the Skill's examples never set `randomize=TRUE`. With the documented default parameters DADA2's error learning has no RNG step, so a `set.seed()` note would be inaccurate boilerplate, not a real fix. Not added. |
| Mandatory redundancy pass | - | none needed | inspection | usage-guide.md already held only Overview/Prerequisites/Quick Start/Example Prompts/What the Agent Will Do/Tips/Related Skills with no verbatim restatement of SKILL.md's decision tables, thresholds, or code blocks; SKILL.md remains the single home for the truncLen rule. Only change here was adding the ggplot2 prerequisite line (a real gap, not duplication). |

## Unfixed

- ITS end-to-end fixture (P2) - no cheap way to build one that ITSxpress's HMM step would meaningfully exercise; documented-but-untested status unchanged from the audit.
- DADA2 seed/reproducibility note (P2) - verified not applicable to the documented default workflow; not added rather than added incorrectly.

## Environment

Verification ran against `F:\OpenScience\audit-envs\microbiome-metagenomics-analyst\` (cutadapt 5.2,
DADA2 1.34.0 via `rr.sh`, real primer-trimmed reads independently regenerated from
`datagen\amplicon\raw_reads\` - not reused output). No packages installed or changed.
