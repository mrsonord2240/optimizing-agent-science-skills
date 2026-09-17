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
