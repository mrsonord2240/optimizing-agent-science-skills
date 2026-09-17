# bio-causal-genomics-heritability-partitioning fixes (2026-09-17)

Worktree `F:\OpenScience\wt\cg-hp`, branch `fix/cg-heritability-partitioning`, based on fork main
`49fe6d4`. Fixer: Claude Sonnet 5. Audit scored 75, Reject on a Research Veto (M4, Code Usability):
the Skill's recommended `abdenlab/ldsc-python3` v2.0.0 was unconditionally broken on `--h2`, `--rg`,
and `--h2-cts`.

**Working route found and verified end to end** (not a source patch to the broken fork): the
Skill's own claim that `bulik/ldsc` is "unmaintained since 2019" is stale. `bulik/ldsc`'s README was
updated 2026-01-16 to point at `CBIIT/ldsc` (NIH CBIIT), a maintained Python 3 port with a
2026-08-10 commit. Cloned it fresh (`tools/ldsc-cbiit/`, commit `1f09cf0c`), built a new Python 3.9
env (`ldsc-py39`, WSL `science` seat, never touching `venv-ldsc`/`bio`/`R-lib`), and ran `--h2`,
`--rg`, `--h2-cts` against the audit's own `ldsc_test_fixtures/` (real regression output, not exit
codes): `--h2` and `--rg` ran unmodified and reproduced the audit's numbers exactly (h2=0.7642,
rg=0.0058); `--h2-cts` needed one real, minimal, documented one-line patch
(`ldscore/sumstats.py`: `.loc[:,1:]` -> `.iloc[:,1:]`, a leftover from replacing pandas' removed
`.ix[:,1:]` with the label-based accessor instead of the positional one) and then produced a real
differentiated two-tissue result (p=3.5e-4 vs p=0.99). Full install steps, exact versions, and the
smoke test are recorded in `F:\OpenScience\audit-envs\mendelian-randomization-analyst\TOOLS.md`
("Added 2026-09-17 by the `heritability-partitioning` fixer").

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Primary tool's `--h2`/`--rg` CLI broken in the exact recommended fork/version | P0 | SKILL.md Version Compatibility + Tool Install Notes: replaced `abdenlab/ldsc-python3` recommendation with `CBIIT/ldsc` (bulik/ldsc's own README now points there); examples/ldsc_partitioned_h2.sh header updated to match | ran | `--h2` and `--rg` run against `CBIIT/ldsc` commit `1f09cf0c` with zero patches, reproducing the audit's own numbers on the same fixtures (h2=0.7642 (0.0538), rg=0.0058 (0.0572)) |
| Finucane 2018 `--h2-cts` unconditionally broken | P0 | Tool Install Notes: documented the one-line `.loc[:,1:]` -> `.iloc[:,1:]` patch (`ldscore/sumstats.py`); SKILL.md's Cell-Type Prioritization section gained the `.ldcts` row format + chromosome-split requirement (previously only in usage-guide.md, and incomplete there) | ran | Patched clone produces real `cell_type_results.txt`: CellTypeB Coefficient=3.18e-06 p=3.5e-04 (passes Bonferroni 0.025/2), CellTypeA p=0.99 (does not) -- a differentiated, checkable result |
| No scope/escape-hatch guidance for patient-facing PRS misuse | P1 | New "## Scope" section: h2/PRS are population-level statistics, not an individual diagnostic/prescriptive tool; redirect to a clinician | docs | Matches the audit's Input 6 finding (the refusal it saw came from Claude's general safety training, not the Skill) |
| No fabrication guard for "give me numbers without real data" requests | P1 | Same "## Scope" section: do not invent a heritability/enrichment number; run the real pipeline or offer a clearly-cited literature estimate labeled as external | docs | Matches the audit's Input 7 finding |
| `ldsc.py`'s own exception handler is broken (`traceback.format_exc(ex)`), compounding every crash | P1 | Not applicable after the tool switch: `CBIIT/ldsc`'s exception handling was exercised directly during verification (the `--h2-cts` pre-patch run) and printed a normal traceback, no second `TypeError`. Noted this in the Version Compatibility "LDSC fork history" paragraph instead of adding a separate caveat | ran | Confirmed while reproducing the pre-patch `--h2-cts` crash: a clean traceback, not a masked one |
| SKILL.md is a 452-line monolith with no `references/` split | P2 | Not fixed -- time-boxed behind the P0/P1 tool fix and the mandatory redundancy pass; left for a future pass | -- | Left unfixed, reason given |
| No bundled example/test data | P2 | Added `examples/smoke_test_ldsc.sh` exercising `--h2`, `--rg`, `--h2-cts` on the simulated fixtures in the user's own CBIIT/ldsc clone (`test/`); not bundled, since they are GPL-3 and the Skill is MIT | ran | `bash examples/smoke_test_ldsc.sh` (via the same env) exits 0 and prints the same real, differentiated `--h2`/`--rg`/`--h2-cts` output as the ad hoc verification above |

All 7 `recommendations[]` entries addressed (2 P0 fixed, 2 P1 fixed, 1 P1 resolved by the tool switch
and noted, 1 P2 fixed, 1 P2 left unfixed with reason).

## Redundancy pass (2026-09-17, same session)

Scope: `SKILL.md` and `usage-guide.md` only, per the brief's "Remove redundancy, every pass" rule.
Lines: SKILL.md 452 -> ~475 (net +23: absorbed the `.ldcts` row-format detail, the finer
intercept/ratio table, and the Computational Footprint table, all previously only in
usage-guide.md or duplicated); usage-guide.md 187 -> 83 (net -104).

**Deleted passage -> new home** (checked present at destination before commit):

| Deleted from usage-guide.md | New home | Note |
|---|---|---|
| "Prerequisites" full install command blocks (LDSC/LDAK/reference downloads/HDL) | SKILL.md "Tool Install Notes" (already there, now corrected) | Replaced with a one-line pointer; kept the "Inputs: columns..." paragraph, which has no SKILL.md equivalent |
| "What the Agent Will Do" 10-step list | Restates SKILL.md's workflow sections 1:1 | Deleted outright, no unique content -- Overview + Quick Start already orient a human reader |
| "Method Selection Quick Reference" table | SKILL.md "Decision Tree by Scenario" (already there, same 12 decisions) | Deleted, pointer added |
| "Cell-Type / Tissue Prioritization Workflow" section | SKILL.md "Cell-Type Prioritization (Finucane 2018)" (already there) | The `.ldcts` row-format sentence (`<name> <ldscore_prefix>,<control_ldscore_prefix>`) was the one genuinely new detail -- moved into SKILL.md's section (not just deleted) before removing this one |
| "LDSC vs LDAK Decision Matrix" table | SKILL.md "LDSC vs LDAK Reconciliation" + Decision Tree row (already there) | Deleted, no unique content |
| "Computational Footprint" table | New SKILL.md "## Computational Footprint" section | Moved verbatim -- runtime/hardware expectations are agent-actionable, not just human-planning color |
| "Intercept Diagnostic Quick Reference" table (finer 5-bin intercept/ratio table) | SKILL.md "LDSC Intercept Interpretation" | Moved in; SKILL.md's own coarser 2-row intercept thresholds in "Quantitative Thresholds" collapsed to a pointer at the finer table so the fact lives once |
| "Tips" (9 of 10 bullets) | Each bullet's fact already lives in a named SKILL.md section (Intercept Interpretation, LDSC vs LDAK Reconciliation, HDL bias failure mode, non-EUR failure mode, liability-scale failure mode, Cell-Type Prioritization, HESS failure mode, Decision Tree, and the now-corrected Version Compatibility) | Deleted; only the one bullet with no SKILL.md home (pre-computing/reusing LD scores, ~3GB one-time download) was kept |
| "Related Skills" | Kept only in usage-guide.md; SKILL.md's identical 12-item copy deleted | Per the brief's own text: "usage-guide.md keeps... related Skills" is usage-guide's designated home, not SKILL.md's -- the two files had carried a byte-for-byte duplicate list |

Examples/ scripts are exempt from this rule and were not touched for dedup (only for the tool-route
fix above).

## Not fixed

- SKILL.md/`references/` progressive-disclosure split (P2) -- time-boxed; the file is now ~475
  lines after the redundancy pass added the moved-in tables, slightly larger than the audited
  452. A future pass should do this split rather than growing SKILL.md further.

## Nothing needs Sam.

## 2026-09-17, integration (orchestrator)

- Merged to fork main at `10ac5b0`, including `c3dff65`, which replaced the fixer's bundled copy of CBIIT's GPL-3 fixtures with staging from the user's clone. Re-run: identical numbers.
- `285e2b0` (merged `c602f2a`): genetic-correlation, genomic-sem, `causal-genomics/README.md` and `workflows/causal-genomics-pipeline/usage-guide.md` still recommended abdenlab/ldsc-python3; all now give the CBIIT route. Verified from a fresh GitHub clone with the documented install in a throwaway WSL env: h2 0.3783 (0.0419), rg 0.1117 (0.0776), h2-cts CellTypeB P=3.5e-4 / CellTypeA P=0.99.
