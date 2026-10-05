> **Audit record for `bio-workflows-crispr-screen-pipeline`**
> - Audited working candidate `e242270b6fc053d495f12c86df5d2d8eb96f9b42fd3971d6435796c9bae5a71d`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/workflows/crispr-screen-pipeline), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-04 by audit-scientific-skill worker (Claude Sonnet 5.5), initial audit run-002, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Audit: bio-workflows-crispr-screen-pipeline (initial, run-002)

Candidate e242270b6fc053d495f12c86df5d2d8eb96f9b42fd3971d6435796c9bae5a71d (uncommitted recut, 19 files). Category Data Analysis, mode D, Complex, 7 inputs.

Static 78/100 (x0.4 = 31.2); execution average 75.6 (x0.6 = 45.4); final 77 -> diagnostic grade Reject by research-veto M4. Assertions 25/32.

This is a diagnostic score, not a readiness decision.

## Routing check (routing/routing.json, rerun after Docker was up; 3 repeats per route)

| Route | Result |
|---|---|
| count | PASS 3/3 |
| qc | PASS 3/3 |
| cn-correction | FAIL 1/3 |
| rra | FAIL 0/3 |
| bagel2 | PASS 3/3 |
| mle | FAIL 0/3 |
| drugz | PASS 3/3 |
| jacks | FAIL 0/3 |
| chronos | PASS 3/3 |
| consensus | PASS 3/3 |
| branches | PASS 3/3 |

First attempt (routing-attempt1-402/) had four routes errored by OpenRouter HTTP 402; its other results differed on noisy routes (bagel2 1/3, qc 2/3, drugz 2/3). The clean rerun is the record.

## Findings (ordered)

- **F-01 P0** chronos.md snippet cannot run (research-veto M4). The Chronos snippet fails on the first sequence_map assertion; fixing the column name then fails on a missing pDNA row and missing negative_control_sgrnas. Fix: Replace the snippet with the tested construction: sequence_map columns sequence_ID, cell_line_name, days, pDNA_batch with a cell_line_name==pDNA row; negative_control_sgrnas per library; counts with sequence_ID rows. Execute it on the staged panel.
- **F-02 P1** jacks.md command fails: wrong script path and map columns. python run_JACKS.py at the clone root exits 2; the script lives in JACKS/jacks/. replicatemap needs a Control column and guidemap the same sgRNA/Gene headers. Fix: Give the real path (JACKS/jacks/run_JACKS.py) and the required map columns; run the command as written.
- **F-03 P1** count.md library column order gives 0% mapped, exit 0. Route says library.csv columns are sgRNA, Gene, Sequence; mageck count reads id, sequence, gene by position. Following the text gives an all-zero table with exit 0. Fix: State the order id, sequence, gene and make the 65-70% mapping check a stop, not a hint.
- **F-04 P1** rra route fails routing 0/3: agent opens qc.md first. For a two-condition dropout request the agent opens qc.md (and often cn-correction and bagel2) before rra.md and never runs rra.py within the step budget. Fix: Reword the order line as the analysis order the answer must respect (QC reported, not read first), and have the rra row name the case: counts in hand, baseline and endpoint known.
- **F-05 P1** cn-correction route fails routing 1/3. Agent opens qc.md first and in two of three runs never issues the Rscript command. Fix: Phrase the row as the action (cancer line, count table in hand, remove amplicon bias) and fix the ordering line.
- **F-06 P1** mle route fails routing 0/3: row does not describe the request. A two-cell-line initial/final design with a design matrix leads the agent to read every route file; none of three runs reaches mle.md first. Fix: Name the design-matrix case in the row (design matrix, several cell lines or time points, beta scores).
- **F-07 P1** jacks route fails routing 0/3: panel request goes to chronos. Five cell lines with one library, a replicate map and a guide map: the agent opens chronos.md first, then reads most routes. Fix: Differentiate the two rows (JACKS: replicate map and guide map, no copy-number input; Chronos: needs plasmid, days, negative controls).
- **F-08 P2** cn-correction.md omits non-integer output and dropped guides. Corrected table has 86,881 of 90,709 guides and non-integer counts; qc.py refuses it. Tested-with line and cn_correction.R header still say CRISPRcleanR was not run, but it ran unchanged. Fix: State both properties and the qc-before-correction order; replace the stale UNEXECUTED header and the not-run clause in SKILL.md with the tested CRISPRcleanR 3.0.1 / R 4.4.3 versions.
- **F-09 P2** qc.py silently skips the plasmid gate when plasmid= is omitted. Without plasmid= the plasmid sample is held to the endpoint Gini 0.3 gate; HAP1_T0 (0.288) passes where the 0.1 gate would fail it. Fix: Print a one-line warning (or exit) when plasmid= is absent.
- **F-10 P2** drugz paired mode and a real drug screen not exercised. Only the -unpaired variant ran, on HAP1 columns relabelled as a drug screen; the paired -c/-x two-replicate command and the vehicle-vs-drug biology are unverified. Fix: Tooling-delta pass: stage a real public drug screen; static-only until then.
- **F-11 P2** no Skill-root LICENSE or provenance note. skill_preflight warns: frontmatter says MIT, author GPTomics, but the Skill carries no LICENSE file and no origin statement. Fix: Cite the repository license evidence in the manifest or restore a LICENSE at the Skill root.

## Execution map

| Surface | Class |
|---|---|
| count, qc, rra, bagel2, consensus, mle, drugz (unpaired), jacks, chronos, cn-correction | executed (route text defects above) |
| drugz paired mode | static-only (no staged data) |
| branches (reference route), references/install.md | not-applicable (no runnable surface) |

## Per-input scores

| # | Type | Label | Status | Basic | Spec | Total |
|---|---|---|---|---|---|---|
| 1 | Canonical | HAP1 TKOv3 table: qc.py then rra.py (route commands) | COMPLETED | 34 | 54 | 88 |
| 2 | Variant A | HAP1: BAGEL2 fc/bf/pr with --seed 42, then consensus.py | COMPLETED | 33 | 53 | 86 |
| 3 | Edge | count route: FASTQ to guide counts, library.csv columns as route text states | PARTIAL | 24 | 32 | 56 |
| 4 | Variant B | A375 cancer line: cn_correction.R (WSL crispr-ccr) then rra.py on the corrected table | COMPLETED | 33 | 52 | 85 |
| 5 | Variant B | mle on MAGeCK demo leukemia table; drugz on HAP1 relabelled as a drug screen | COMPLETED | 31 | 48 | 79 |
| 6 | Stress | Five-line panel: jacks and chronos, route text as written then tooled variants | PARTIAL | 22 | 30 | 52 |
| 7 | Adversarial | Trap trips: normalized table, missing baseline, one method, no plasmid label | COMPLETED | 33 | 50 | 83 |

Assertions and notes per input are in report.json. Scripts, logs and outputs: run root scripts/, work/.
