# bio-pathway-kegg-pathways fixes (2026-09-17)

Worktree `F:\OpenScience\wt\pw-kegg`, branch `fix/pw-kegg`, based on `main` @ `49fe6d4`. Fixer:
Claude Sonnet 5. Runtime: R 4.4.3 via `F:\OpenScience\audit-envs\crispr-screen-analyst\r.sh`;
SPIA 2.58.0, graphite 1.52.0, clusterProfiler 4.14.6, org.Hs.eg.db already installed there, no
version changes made, nothing new installed. Verification: scratchpad
`.../scratchpad/pwkegg/test_fix.R` (isolated graphite+runSPIA reproduction, real synthetic data
copied from the audit's `data/SYNTHETIC_de_results.csv`, identical byte-for-byte to the audit's
own `run/gate8/de_results.csv`), and a full-script re-run of the patched
`examples/kegg_spia_topology.R` (nB lowered to 50 only for turnaround; the shipped file keeps
nB=2000).

Commits: `89fd77f` fix(pathway-analysis/kegg-pathways) — the P0/P1/P2 findings below;
`424a053` refactor(pathway-analysis/kegg-pathways) — the redundancy pass.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| graphite + runSPIA code pattern never runs as documented | P0 | SKILL.md's "Run Signed-Topology Perturbation" code block and `examples/kegg_spia_topology.R`: `prepareSPIA`/`runSPIA` now use a **relative** pathway-set name with a matching `setwd(tempdir())`/`setwd(owd)` pair (root cause 1: `runSPIA` checks `datasetName(name) %in% dir()`, and bare `dir()` only lists the current working directory's filenames — an absolute/`tempdir()`-built name can never match); `de_vec`/`universe` names get an `'ENTREZID:'` prefix to match `convertIdentifiers(db,'ENTREZID')`'s node-ID namespace before calling `runSPIA` (root cause 2: unprefixed IDs never intersect, giving 0 rows even once root cause 1 is worked around) | ran | `test_fix.R`: `runSPIA` returned 0 rows before the ID-prefix fix, 191 real rows after (real numeric `pG`/`pGFdr`, per-pathway `Status` Activated/Inhibited, non-degenerate). Full patched example script parses (`Rscript -e "parse(...)"`) and the isolated graphite-route reproduction confirms the fix end to end; the direct-`spia()` half of the script was already correct and untouched except for the P1 seed addition below. `runSPIA`'s output has no `ID`/`KEGGLINK` columns (differs from `spia()`'s), corrected in the new "Understanding Results" table |
| SPIA's own worked example omits set.seed() | P1 | `set.seed(123)` added immediately before `spia()` in SKILL.md's code block and before both `spia()` and `runSPIA()` in `examples/kegg_spia_topology.R` | ran | matches the pattern already used for `gseKEGG`; SKILL.md's Quantitative Thresholds table already required this, the worked examples just didn't do it |
| No explicit agent instruction to refuse/warn on missing background gene set | P1 | New "Agent Workflow" section in SKILL.md (moved from usage-guide.md's "What the Agent Will Do", see redundancy table) gets a new step 3: tell the user before proceeding if no measured/background gene set is available, rather than silently defaulting to whole-KEGG | docs | audit's Input 7 measured 170 vs 136 total hits (135/135 shared pathways more "significant") when `universe` was omitted — already documented as a failure mode, now also a mandatory workflow step |
| "meaningless perturbation scores" wording for SPIA on metabolic maps | P2 | Reworded in "SPIA on metabolic maps" (Per-Method Failure Modes) and the matching Common Errors row: metabolic pathways are simply **absent** from SPIA's signaling-only `hsaSPIA` output, not scored with a meaningless value | ran (audit's own Input 4 run: hsa00010 absent from `res` entirely) | |

All 4 dispatched findings fixed (1 P0, 2 P1, 1 P2). Nothing left unfixed.

## Redundancy pass (2026-09-17)

Scope: `SKILL.md` and `usage-guide.md`, per the brief's "Remove redundancy, every pass" rule.
Lines: SKILL.md 250 -> 317 (net +67: absorbed usage-guide.md's install commands, agent workflow
incl. the new P1 step, organism-code table, and results-column table, plus the P0/P1/P2 fixes
above). usage-guide.md 113 -> 35 (net -78).

**Deleted passage -> new home** (every deletion verified present at destination before commit):

| Deleted from usage-guide.md | New home in SKILL.md | Note |
|---|---|---|
| "Prerequisites" R install block (`BiocManager::install(...)` etc.) | "Version Compatibility" | verbatim, new content not previously in SKILL.md |
| "Prerequisites" conceptual bullets (ID types, universe, live-query, SPIA signaling-only) | Already stated in "Prepare the Gene IDs", "Decision Tree", "Pin the KEGG Release", "Per-Method Failure Modes" | deleted, no unique content |
| "Quick Start" one-liner prompts | Deleted — duplicated the same 5 scenarios already spelled out in "Example Prompts" | usage-guide.md keeps one prompt section, not two |
| "What the Agent Will Do" numbered workflow | New "Agent Workflow" section (after Decision Tree) | plus the new P1 refuse/warn step |
| "Common Organism Codes" table | New "Common Organism Codes" section (after Agent Workflow) | verbatim |
| "Understanding Results" column table | New "Understanding Results" section (before Per-Method Failure Modes) | verbatim, plus a note that `runSPIA()` output lacks `ID`/`KEGGLINK` (confirmed by the P0 verification run) |
| "Tips" section (8 bullets) | Already stated in "Prepare the Gene IDs", "Decision Tree", "Compare Multiple Conditions", "Run KEGG ORA", "Common Errors", "Pin the KEGG Release" | deleted, no unique content; the one non-duplicate line (pointer to enrichment-visualization/pathview) is already in the Scope paragraph and pathview section |

No disagreements found between the two files' copies before deletion.

## Fix pass on the 2026-09-17 re-audit (2026-09-21)

Worktree `F:\OpenScience\wt\pathway-kegg-pathways`, branch `fix/pathway-kegg-pathways`. Fixer: Claude
Sonnet 5. Runtime: R 4.4.3 via `mass-spec-proteomics-analyst
.sh`; SPIA 2.58.0, graphite 1.52.0,
clusterProfiler/org.Hs.eg.db from that env's `R-lib`; nothing installed. Re-audit score was 94 (Production
Ready) with one P1 and one P2 open.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| graphite route disagrees with direct `spia()` on direction, undocumented | P1 | SKILL.md: SPIA section now names two routes and states they are complementary (report Activated/Inhibited only where both agree; name the topology; prefer `spia()` when only one is run; graphite for current KEGG/Reactome); new failure-mode section "graphite and spia() disagree on SPIA direction", new Common Errors row, Decision Tree row and taxonomy wording changed from "or graphite + runSPIA" to cross-check | ran | Independent re-run on the audit's `SYNTHETIC_de_results.csv` (nB=100, seed 123): Cell cycle direct tA=+70.5 Activated vs graphite tA=-55.7 Inhibited, p53 and MAPK also split, 16 Status calls differ. From the audit's `in4b_direction_comparison.csv`: 99 matched, r=0.60, 14 strictly opposite-sign, 18 Status differ, 19 with a zero tA in one route (the audit's "30/99" counted zero-vs-nonzero as disagreement; the caveat quotes the stricter figures). Cause stated only as differing topology source: `hsaSPIA` holds 139 bundled pathways vs 319 graphite graphs (e.g. Cell cycle 233 binding/association, 269 inhibition edges); no claim which route is right beyond the planted UP/DOWN pathways |
| Shipped SPIA example has no fast-iteration nB | P2 | comment on `n_boot` in `examples/kegg_spia_topology.R` (200-500 to explore, 2000+ for reported result); same note added to the nB row of Quantitative Thresholds | ran (`parse()` OK) | default kept at 2000 |

Redundancy: the new caveat appears once in the SPIA section; the failure-mode entry and Common Errors row
point to it in one line each rather than restating the numbers. `usage-guide.md` unchanged (already only
overview, prompts and related Skills). No passages deleted.

Findings left unfixed: none.


## 2026-09-21 (structure)

Worktree `F:\OpenScience\wt\pathway-kegg-pathways`, branch `fix/pathway-kegg-pathways`. Fixer: Claude
Sonnet 5. Env `crispr-screen-analyst` (R 4.4.3 via `r.sh`; SPIA 2.58.0, graphite 1.52.0, clusterProfiler
4.14.6); nothing installed. Structure only, no behaviour or claim changed.

**Split** (commit `2bb21b0`): SKILL.md 324 -> 268 lines. Verbatim moves, checked by sorted non-blank-line
diff of old SKILL.md against new SKILL.md + references/ (only the three decision-tree rows gained a
pointer; the new files add titles, one "Read when" line each, and the Reference Files index). All three R
fences parse (`parse()` via `r.sh`).

| Section moved out of SKILL.md | New file |
|---|---|
| Run Signed-Topology Perturbation (SPIA) | `references/spia-topology.md` |
| Compare Multiple Conditions | `references/compare-conditions.md` |
| Overlay Data on the KEGG Map (pathview) | `references/pathview-overlay.md` |

Pointers added to the decision-tree rows for SPIA, compareCluster and pathview, plus a "Reference Files"
index before "Agent Workflow". Scope, decision tree, ID prep, ORA, GSEA, pinning, thresholds, failure modes
and Common Errors stay in SKILL.md.

**Scripts** (commit `2befc0b`): no file created under `scripts/`. The one block over 15 lines, the SPIA +
graphite pipeline (31 lines, `references/spia-topology.md`), duplicates `examples/kegg_spia_topology.R`, so
per the brief the copy is deleted and the reference points at the example (plus the `spia()` output-column
note and Status meaning kept in prose). Remaining blocks are 3-10 lines (ID prep, enrichKEGG/enrichMKEGG,
gseKEGG, gson pinning, compareCluster, pathview) and stay inline. ORA/pinning overlap with
`examples/kegg_enrichment.R` is partial (fragments), left as is.

Run: `examples/kegg_spia_topology.R` on the audit's `SYNTHETIC_de_results.csv` as `de_results.csv`, with
`n_boot <- 100` (sed on a scratchpad copy) plus assertions: `spia()` and `runSPIA()` both returned scored
tables (graphite 191 pathways, 180 at FDR<0.05), Status/pG/pGFdr present and finite, Cell cycle
Activated in `spia()` (tA +70.5). Whole script took 43 min wall at nB=100, so the shipped default of 2000
is impractical to run end to end; not run at 2000.

**Left inline / not run:** `enrichKEGG`, `gseKEGG`, gson-pinning, `compareCluster` and `pathview` blocks were
not re-executed (short, unchanged verbatim; not scripts). Findings left unfixed: none.
