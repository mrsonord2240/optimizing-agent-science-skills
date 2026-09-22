# bio-crispr-screens-crispresso-editing fixes (2026-09-16)

Worktree `F:\OpenScience\wt\crispr-b`, branch `fix/r2-crispr-b`. Runtime: CRISPResso2 2.3.4
(`pinellolab/crispresso2:latest` Docker image), invoked per `TOOLS.md` section 6 notes #10-11.
Real CRISPResso2 output generated this pass (fresh `CRISPResso` run on `FANC.Cas9.fastq`, and a
`CRISPRessoPooled` re-run with `--min_reads_to_use_region 100`) is saved at
`F:\OpenScience\wt\_fixdata\crispresso\CRISPResso_on_fixver_FANC.Cas9\` for
`base-editing-analysis` (fixed after this Skill in the same worktree) to reuse.

## Round-2 audit pass — 2026-09-16

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `parse_crispresso()` crashes on real output (`ValueError: too many values to unpack`) and reads `READS_ALIGNED_PERCENTAGE`, a column absent from the real file | P0 | Rewrote `parse_crispresso()` in SKILL.md to `pandas.read_csv(sep='\t')` the 7-column/2-row mapping-statistics file and compute `mapping_pct` as `READS ALIGNED / READS IN INPUTS * 100` instead of a nonexistent key | ran | Ran fresh against real Docker output (`CRISPResso` on `FANC.Cas9.fastq`, CRISPResso2 2.3.4): `reads_in_input=250`, `reads_aligned=235`, `mapping_pct=94.0`, `editing_quant['Modified%']['Reference']=26.38297872` (byte-identical to upstream's checked-in expected result). `py_compile` clean. |
| Same wrong column name (`READS_ALIGNED_PERCENTAGE`) repeated in the Failure Modes "Low alignment rate" row | P0 (same root cause) | Changed the Symptom line to point at `READS ALIGNED`/`READS IN INPUTS` via `parse_crispresso()` instead of the nonexistent key | ran (see above) | Third occurrence of the same defect, not separately listed in `recommendations[]` but same root cause; fixed alongside. |
| `CRISPRessoPooled` silently returns all-`NA` on a realistic pilot-scale pool (242-250 reads/amplicon); `--min_reads_to_use_region` defaults to 1000, undocumented | P0 | Added `--min_reads_to_use_region 100` to the Pooled-Amplicon Mode worked example plus a note explaining the default and telling the agent to check for `NA` rows; added the same check to usage-guide.md's "What the Agent Will Do" checklist, Tips, and a new Common Errors row | ran + help | Reran `CRISPRessoPooled -r1 Both.Cas9.fastq --amplicons_file Cas9.amplicons.txt --min_reads_to_use_region 100`: FANC 26.38297872% / HEK3 34.42622951% Modified, matching the audit's own corrected numbers and upstream's expected results exactly. `--help` confirms the flag and its default of 1000. |
| Single-Amplicon worked example's `--min_average_read_quality 30` changes the reported % (26.38%->24.89%) with no disclosure | P1 | Added a note after the worked example: the flag is a real filter, states the measured shift, and instructs reporting the retained-read fraction alongside the editing percentage | ran | Reproduced both the flagged (221/250 aligned, 24.89% Modified) and unflagged (235/250, 26.38%) runs via Docker. |
| Failure Modes table only documents a graded "<50% aligned" symptom; a badly-wrong amplicon instead hard-crashes with exit 1 and no output folder | P1 | Added a new "Total alignment failure (wrong locus / zero output)" row to Failure Modes and a matching Common Errors row | ran | Reproduced by running FANC reads against the unrelated HEK3 amplicon+guide: `CRITICAL: Alignment error... ERROR: No alignments were found`, exit 1, no output directory written. |
| Mapping-stats "Key outputs" table ("no percentage columns") contradicted the old Python snippet that read a percentage column | P2 | Resolved as a side effect of the `parse_crispresso()` fix above — the rewritten parser now computes the percentage itself instead of reading a nonexistent column, so the table and the code no longer disagree | ran (see P0 fix) | No separate change needed once the parser was corrected. |
| (Found independently, not in `recommendations[]`) shipped `examples/crispresso_analysis.sh` calls `CRISPRessoCompare --crispresso_output_folder_1/_2`, flags that do not exist | fix (shipped script that crashes, per brief) | Switched to CRISPRessoCompare's actual positional-argument syntax; added a comment explaining why | ran + help | `CRISPRessoCompare --help` (2.3.4) shows only positional `crispresso_output_folder_1 crispresso_output_folder_2` plus `-n1`/`-n2` sample-name flags. Reproduced the exact crash with the old flags (`unrecognized arguments`), then confirmed the positional form completes (exit 0) on real `CRISPResso_on_*` output directories. |
| Version Compatibility banner said "CRISPResso2 2.2.14+", untested this pass | housekeeping | Updated to "checked on CRISPResso2 2.3.4 (pinellolab/crispresso2 Docker image)" | ran | Matches the version actually used for every verification above. |

All 5 `recommendations[]` entries (2 P0, 2 P1, 1 P2) fixed, plus one additional shipped-script
defect found and fixed during verification. Nothing left unfixed.

## 2026-09-21: P2 batch, redundancy pass, split, scripts

Worktree `F:\OpenScience\wt\crispr-screens-crispresso-editing`, branch `fix/crispr-screens-crispresso-editing`
(from staging main 431aa55). Audit: score 91, Production Ready, 2 P2. Runtime: CRISPResso2 2.3.4
(`pinellolab/crispresso2` Docker, `docker cp` in/out, `crispr-screen-analyst` env). Commits: 08add3a, 9dd4ef3,
574d60a (fixes and dedup), bc45b35 (split), 205c857 (scripts). SKILL.md 391 -> 222 lines.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| CRISPRessoWGS never executed | P2 | Fetched the CRISPResso2 repo's `tests/smallGenome/smallGenome.fa`, ran WGS on `Both.Cas9.fastq.smallGenome.bam` + `Cas9.regions.txt`. The SKILL.md example used `--bam`/`--reference`; `--bam` is rejected (`ambiguous option: --bam could match --bam_output, --bam_file`). Now `--bam_file`/`--reference_file`, output layout and region-file format documented, WGS `--min_reads_to_use_region` (default 10, `NA` row + exit 0 for a 2-read region) documented | ran + help | FANCF 23 reads 26.09% Modified; HEK3 `NA` at default, 50% with `--min_reads_to_use_region 1`. Fixture not shipped: the auditor's request to cache a reference is a test-fixture matter, the Skill now cites the upstream file |
| Only Python sample has no test | P2 | `parse_crispresso()` moved verbatim to `scripts/parse_crispresso.py` with a CLI and `--selftest` (asserts on a synthetic dir in the real 2.3.4 file format) | ran | selftest OK; on fresh CRISPResso 2.3.4 output: 250 / 235 / 94.0 / 26.38297872 asserted, import form works |
| (found while running) `\  # comment` lines in the Single-amplicon and Pooled worked examples | fix | Comments moved above the command | ran (stub functions over every bash fence: before, stray " " argument and `--n_processes: command not found` / `--quantification_window_size: command not found`; after, all args received) | Would have run Pooled without `--n_processes 8`, Single without its window and output flags |
| (found while running) output-path comments wrong: `<out>/<name>/`, `3a.<ref>.Indel_size_distribution.pdf`, batch/pooled summary paths | fix | Now `CRISPResso_on_<name>/`, `3a.Indel_size_distribution.pdf`, `CRISPRessoBatch_on_<batch file>/`, `CRISPRessoPooled_on_<fastq>/` | ran (CRISPResso, Batch, Pooled on the audit data) | |
| (found) Bystander failure mode called `--quantification_window_size 10` "Default" | fix | Reworded: default is 1 | help | |

### Left unfixed

None of the audit's findings. The auditor's suggestion to cache a reference FASTA beside the audit fixtures
(P2 1) is an audit-fixture action outside the Skill and was not done; the Skill's WGS claim is now backed by a run.

### Deleted passage -> new home (redundancy pass)

| deleted | new home |
|---|---|
| usage-guide Prerequisites (conda line, required inputs) | SKILL.md "Version Compatibility" (Install, Required inputs); guide keeps a pointer |
| usage-guide "What the Agent Will Do" (15 steps) | steps are SKILL.md's own sections; step 8 (`--min_average_read_quality 30`) is the Single-amplicon example and its note; step 10 (NA rows) is the Pooled/WGS text; section removed |
| usage-guide Tips | Failure Modes, Common Errors, Pooled/Batch text (each already there); BE indel >5% cause -> Quantitative Thresholds; "randomly chosen regions yield no useful comparison" -> WGS use case; UMI/primer >=3 bp advice -> Decision Tree "Fails when". "matched-tumor BAM" wording dropped (not applicable to editing amplicon/WGS runs) |
| usage-guide Mode Decision Cheat Sheet | SKILL.md Mode Decision Tree |
| usage-guide Thresholds | SKILL.md Quantitative Thresholds; added rows: substitution-vs-indel ratio (>10 clean, <3 cut-mediated), read depth 1,000+, PE intended-edit >20% at favorable sites |
| SKILL.md Common Errors rows: alignment <50%, No alignments, pooled misassignment, pooled `NA`, scaffold high | Failure Modes (low alignment, total alignment failure, scaffold), Decision Tree "Fails when" (misassignment), Pooled section (`NA`) |
| SKILL.md thresholds rows: quantification window size Cas9 1 / BE 10 | "The Quantification Window" section (the "positions 4-13" rationale was dropped; it contradicted that section's "positions 4-8") |
| SKILL.md Base Editor "Reading the output" and PE "high-quality run" sentence (numeric cutoffs) | Quantitative Thresholds |

### Split and scripts

Split (bc45b35): `references/base-editor.md` (BE section + bystander failure mode), `references/prime-editor.md`
(PE section + scaffold failure mode), `references/batch-pooled-wgs.md` (Batch, Pooled, WGS). 320 non-blank lines
before; every one is in SKILL.md or a reference file except the six decision-tree rows that gained pointers.
Scripts (205c857): SKILL.md "Parse Output in Python" block -> `scripts/parse_crispresso.py`. The other bash
fences are template commands with placeholders and stay inline; `examples/crispresso_analysis.sh` untouched.
