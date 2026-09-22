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

## 2026-09-21 fixer pass on `fix/microbiome-amplicon-processing`

Worktree `F:\OpenScience\wt\microbiome-amplicon-processing`, base staging `431aa55`. Commits: `8effd26` (fix),
`d926a64` (redundancy), `0e9a568` (scripts step). Audit: 92/100 Production Ready, 3 open P2s. Env
`microbiome-metagenomics-analyst` (DADA2 1.34.0, cutadapt 5.2, ITSxpress 2.2.0 and QIIME2 2024.10 in WSL).
SKILL.md 260 -> 267 lines: under 300, no split.

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| removeBimeraDenovo low-abundance recall undocumented | P2 | Added a caution paragraph to "Combine Runs, Then Remove Chimeras". The audit's suggested `method='pooled'` workaround was **not** adopted. | ran | Re-ran the shipped workflow on the fixture, then `removeBimeraDenovo` with consensus, pooled and per-sample, and `minFoldParentOverAbundance` 0.5/1/1.5: CHIMERA_2 (115 reads, 0.58% of reads) survives every one. |
| abundance-cutoff shortcut not pre-empted by name | P2 | Added a paragraph to the decontam section naming a flat relative-abundance cutoff and why it fails. | ran | Fixture: Ralstonia (kit contaminant) 5.11% of reads, Escherichia-Shigella (real) 4.28%. Cutoffs 1/5/10/12%: none removes Ralstonia without removing a real taxon at 10%+ (Roseburia, E. coli); `isContaminant(method='combined')` flags only Ralstonia. |
| ITS path never run end to end | P2 | No fixture shipped (would be new content). The Skill's ITS commands were run instead, see the defect row below. | ran | Real yeast ITS region (NCBI KT459474.1), 200 simulated read pairs, three ITS2 lengths (202/217/232 bp). ITSxpress 2.2.0 `--region ITS2 --taxa Fungi`: 200 pairs in, 200 merged and trimmed reads out. `filterAndTrim(truncLen=0, minLen=50)`: 200/200 kept. Fixed truncLen at the longest length: 100/200 kept, so the "never fixed-truncate" claim holds. `learnErrors` could not fit on 200 constant-Q reads, so `dada()` on ITS was not exercised. |
| (found during the work) ITSxpress and Deblur bash blocks put `# comment` after a trailing `\` | P1-class (broken command) | Comments moved above the command in both blocks. | ran | Bash treats `\ #` as an escaped space then a comment, so the command ended early and `--outfile ...` ran as its own command ("command not found"). Extracted both fixed blocks from SKILL.md and ran them against stub functions: one call each with all arguments. Deblur `denoise-16S`, `dada2 denoise-ccs`, `cutadapt trim-paired` flags confirmed in QIIME2 2024.10 `--help`. |
| Redundancy pass (mandatory) | - | See table below. | grep | |
| Scripts step (Sam, 2026-09-21) | - | Nothing moved. No inline block is a unique runnable block of 15+ lines (per-run pipeline is a 14-line excerpt of `examples/dada2_workflow.R`, the others 4-9). Added pointers to the two shipped examples, which SKILL.md never mentioned. | ran | `examples/remove_primers.sh` run on fixture reads: 1989 pairs kept, 231 bp after trim. |

### Left unfixed

- ITS end-to-end fixture as a shipped example: would be new content (a script plus data), and `dada()` cannot be
  exercised on reads this small with constant quality. The trim and filter steps were run and pass.
- Chimera survivor: the cause is not diagnosed and no method found that recovers it (all three methods tested and
  the fold threshold fail), so the Skill now says so rather than offering a workaround.
- Two other things not run: Deblur and `dada2 denoise-*` (help-only, no QIIME2 artifacts in the fixture).

### Deleted passage -> new home

| deleted | now |
| --- | --- |
| usage-guide Prerequisites install lines (conda, R, QIIME2 note) | SKILL.md "Install" block under the title |
| usage-guide Prerequisites conceptual bullets (demultiplexed input, primers known, region known, per-run, controls) | SKILL.md Scope, Remove Primers, truncLen section, Per-Run pipeline, Decontamination |
| usage-guide "What the Agent Will Do" (9 steps) | SKILL.md Per-Run pipeline / Combine / Decontamination sections |
| usage-guide Tips (9 bullets) | ASV insight corollaries, Remove Primers, truncLen section, ITS section, Failure Modes, Decision Tree (`pool='pseudo'`), Decontamination; "save chimera-free table as RDS" -> Combine section |
| SKILL.md Version Compatibility paragraph on per-run error model | corollary 2 and Per-Run pipeline; the defaults-drift sentence stays |
| Failure Mode "Merge cliff from over-truncation" | truncLen section, Quantitative Thresholds, Common Errors ("near-zero `merged`, not low diversity" added to truncLen section) |
| Failure Mode "Fixed-truncating ITS" | ITS section (ITS1 ~200-600 bp mechanism sentence added), Common Errors |
| Failure Mode "ASV count read as species richness" | corollary 3 (copy number 1-15+ added), ASV vs OTU "Defensible practice" |
| Failure Mode "Low-biomass contamination ignored" | Decontamination section (kitome signatures and "report what was removed" added) |
| truncLen V4 bullet re-stating the post-cutadapt length; closing "OTHER end of the budget" sentence | truncLen "silent ceiling" paragraph and Thresholds row |
| Combine section "large READ fraction chimeric = leftover primers" | Failure Mode "Primers left on", Thresholds row, Common Errors |

Kept on purpose: the Quantitative Thresholds table rows for the truncLen budget and ceiling. They index numbers
whose mechanism is in the truncLen section, and the re-audit checked them.
