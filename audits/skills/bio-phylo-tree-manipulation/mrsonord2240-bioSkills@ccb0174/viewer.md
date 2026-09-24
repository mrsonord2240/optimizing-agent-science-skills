> **Audit record for `bio-phylo-tree-manipulation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@ccb0174](https://github.com/mrsonord2240/bioSkills/tree/ccb01746cf23973cdd265786bf90b84ceddb2528/phylogenetics/tree-manipulation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-phylo-tree-manipulation

Generated: 2026-09-24 · rendered from `report.json` by `tools/render_viewer.py`.

> This viewer is **generated from the audit report**, not written by the auditor. It restates the report's own recorded scores, notes and assertions and adds nothing to them. Where a hand-written viewer would argue from the runs, this one points at the scripts in [scripts/](scripts/) instead.

Source: `mrsonord2240/bioSkills@ccb01746cf23973cdd265786bf90b84ceddb2528:phylogenetics/tree-manipulation`
Audit type: final pass regression of all eight archived scenario areas plus two fresh inputs
Category: Data Analysis · Execution mode: A · Complexity: Complex · N = 10 · Executed: 9/10

## What the Skill claims to do

Edit phylogenetic tree structure with Biopython Bio.Phylo, treating rooting as a separate statistical inference rather than a display choice.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 56 | **94** | 3/3 | yes | ✅ |
| 2 | Variant A | 38 | 56 | **94** | 2/2 | yes | ✅ |
| 3 | Edge | 38 | 57 | **95** | 3/3 | yes | ✅ |
| 4 | Variant B | 38 | 56 | **94** | 2/2 | yes | ✅ |
| 5 | Stress | 38 | 56 | **94** | 3/3 | yes | ✅ |
| 6 | Scope Boundary | 38 | 56 | **94** | 3/3 | no | ✅ |
| 7 | Adversarial | 38 | 56 | **94** | 3/3 | yes | ✅ |
| 8 | Regression edge | 38 | 57 | **95** | 4/4 | yes | ✅ |
| 9 | Fresh adversarial input | 39 | 56 | **95** | 4/4 | yes | ✅ |
| 10 | Fresh edge input | 39 | 57 | **96** | 4/4 | yes | ✅ |

**Execution Average: 94.4 / 100** · **Assertion Pass Rate: 31/31**

**Static: 93/100** · Static weighted 37.2 + dynamic weighted 56.6 = **94/100** → ⭐ Production Ready, deployable.

---

## Veto gates

### Skill veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| stability | PASS |  |
| contract | PASS |  |
| determinism | PASS |  |
| security | PASS |  |

### Research veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| scientific integrity | PASS | All empirical claims in this pass use archived synthetic trees or explicitly labelled tool output; the Skill refuses unsupported basal and dated claims. |
| practice boundaries | PASS | Research tree editing only; no clinical or individual diagnostic claim. |
| methodological ground | PASS | The separate a-priori ingroup check is executable in both the documented snippet and the shipped root example, preventing an outgroup-complement tautology. |
| code usability | PASS | All five shipped examples compile and run from a clean working directory under Biopython 1.88. |

## Static score

| Category | Score | Note |
|---|---|---|
| functional suitability | 12/12 | Rooting, pruning, collapse, induced-subtree, and distance examples have executable coverage. |
| reliability | 12/12 | Outgroup and ingroup checks, dual-label support parsing, and no-readable-support guard cover prior silent failures. |
| performance context | 7/8 | The 247-line main Skill keeps structural edits local and directs heavyweight inference to dedicated tools. |
| agent usability | 15/16 | Rooting decision table and explicit routes distinguish editing from inference and dating. |
| human usability | 8/8 | Failure modes state the consequence and recovery for LBA, rate variation, branch lengths, and polytomies. |
| security | 12/12 | Examples use local files and no credential, network, or shell-evaluation path. |
| maintainability | 12/12 | Five small runnable examples align with the core instructions and version checks. |
| agent specific | 15/20 | Trigger, scope boundaries, and tool routing are precise; specialised command availability still needs environment verification. |

## Input 1 — Canonical: Archived close IQ-TREE outgroups

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Execution: final_pass_verify.py assertions 1-3.
- Finding: Temporary ingroup root, outgroup stem root, and separately declared ingroup all pass.

## Input 2 — Variant A: Archived induced subtree and distance preservation

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Execution: final_pass_verify.py assertions 4-5.
- Finding: Pruning retains the requested tips and preserves I1-I2 patristic distance.

## Input 3 — Edge: Archived UFBoot and zero-length collapse

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Execution: final_pass_verify.py assertions 6-8.
- Finding: IQ-TREE dual labels parse and low support / writer-floor branches collapse.

## Input 4 — Variant B: Archived rate-shifted MAD and MinVar

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Execution: final_pass_verify.py assertions 11-14.
- Finding: MAD reports AI 0.880 and MinVar writes its rooted tree; agreement remains explicitly non-confident.

## Input 5 — Stress: Archived IQ-TREE non-reversible root confidence

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Execution: run/nr/rootnr.stdout; rootstrap and AU output files present.
- Finding: IQ-TREE 3 command wrote rootnr.rootstrap.nex and rootnr.roottest.csv on the archived alignment.

## Input 6 — Scope Boundary: Clock/root-to-tip dating request

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Execution: Routing answer evaluated against Skill scope.
- Finding: Correctly routed to divergence-dating rather than converting a structural edit into a tMRCA claim.

## Input 7 — Adversarial: Archived lonely distant outgroup

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Execution: final_pass_verify.py assertion 9 and documented failure-mode checks.
- Finding: LBA warning path remains represented; no basal claim is licensed.

## Input 8 — Regression edge: Archived FarOut plus I13 misassignment

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Execution: final_pass_verify.py assertions 9-10.
- Finding: Outgroup-only monophyly passes but the separate a-priori ingroup check fails, exactly as required.

## Input 9 — Fresh adversarial input: Malformed a-priori ingroup

- Status: ✅ COMPLETED · Basic 39/40 · Specialized 56/60 · **Total 95/100**
- Execution: final_pass_verify.py assertion 30.
- Finding: A focal list that wrongly includes an outgroup is detected instead of being replaced by an outgroup complement.

## Input 10 — Fresh edge input: Label-free support tree and shipped example

- Status: ✅ COMPLETED · Basic 39/40 · Specialized 57/60 · **Total 96/100**
- Execution: final_pass_verify.py assertions 17-31.
- Finding: Label-free tree reaches the guard condition; root_tree.py executes its new ingroup validation from a clean cwd.

## Key strengths

- The shipped outgroup example now executes the a-priori ingroup-monophyly check that its scientific safety guidance requires.
- Archived synthetic regressions cover actual LBA misassignment, dual IQ-TREE support labels, writer-floor zero lengths, MAD, MinVar, and non-reversible IQ-TREE rooting.
- All shipped examples compile and run from a clean working directory under Biopython 1.88.
