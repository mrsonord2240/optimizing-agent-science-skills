> **Audit record for `bio-virtual-screening`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@9c76aab](https://github.com/mrsonord2240/bioSkills/tree/9c76aab55da6a7304f99b214feea6a75b5aacd8e/chemoinformatics/virtual-screening) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-virtual-screening

## Canonical final summary

**Final:** 95/100 — ✅ Production Ready; deployable: true.

Generated: 2026-09-23 · rendered from `report.json` by `tools/render_viewer.py`.

> This viewer is **generated from the audit report**, not written by the auditor. It restates the report's own recorded scores, notes and assertions and adds nothing to them. Where a hand-written viewer would argue from the runs, this one points at the scripts in [scripts/](scripts/) instead.

Source: `mrsonord2240/bioSkills@9c76aab55da6a7304f99b214feea6a75b5aacd8e:chemoinformatics/virtual-screening`

Final-pass metadata: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.
Audit type: fresh final-pass Phase 2 audit
Category: None · Execution mode: A · Complexity: Complex · N = 7 · Executed: 7/7

## What the Skill claims to do

Virtual-screening workflow for receptor preparation, binding-site prediction, ligand preparation, docking, pose review, and screening triage.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 40 | 57 | **97** | 3/3 | yes | ✅ |
| 2 | Variant A | 40 | 56 | **96** | 2/2 | yes | ✅ |
| 3 | Variant B | 39 | 56 | **95** | 2/2 | yes | ✅ |
| 4 | Adversarial | 40 | 58 | **98** | 2/2 | yes | ✅ |
| 5 | Stress | 39 | 57 | **96** | 2/2 | yes | ✅ |
| 6 | Determinism | 40 | 57 | **97** | 2/2 | yes | ✅ |
| 7 | Scope Boundary | 39 | 54 | **93** | 2/2 | yes | ✅ |

**Execution Average: 96.0 / 100** · **Assertion Pass Rate: 15/15**

**Static: 94/100** · Static weighted 37.6 + dynamic weighted 57.6 = **95/100** → ⭐ Production Ready, deployable.

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
| scientific integrity | PASS | The workflow distinguishes docking scores from experimental affinity, asks for orthogonal pose validation, and does not claim a docking pose establishes activity. Fresh receptor preparation, Vina docking, P2Rank pocket prediction, and Meeko pose reconstruction all completed from the documented local toolchain. |
| practice boundaries | PASS | SKILL.md explicitly requires visual/chemical pose validation, identifies covalent inhibitors as outside the ordinary non-covalent workflow, and treats GNINA as an optional rescoring route rather than fabricating a result. |
| methodological ground | PASS | A fresh source-level adversarial test confirmed that positive Vina energies are excluded; a seed-42 repeat produced identical source-script output; P2Rank and docking provide separable site-prediction and scoring stages. |
| code usability | PASS | The source prepare_receptor.py, dock_single.py, and example prepare_ligand helper were executed against fresh fixture copies. The source CLI fallback is runnable natively on Windows with the documented Vina executable. |

## Static score

| Category | Score | Note |
|---|---|---|
| functional suitability | 11/12 | Covers the expected receptor, pocket, ligand, docking, and pose-review stages. The optional GNINA route is documented but not bundled as a source wrapper. |
| reliability | 11/12 | Clear tool-specific handoffs and negative-energy filtering; binding-site coordinates still require scientific review rather than automatic acceptance. |
| performance context | 8/8 | The documented Vina and P2Rank local paths complete quickly on the small fixture and expose seed control. |
| agent usability | 15/16 | Commands, expected artifacts, and failure boundaries are concrete. Native Vina CLI provides a practical route when the Python API is unavailable. |
| human usability | 8/8 | The workflow is staged and gives explicit interpretation cautions instead of presenting a docking score as a conclusion. |
| security | 12/12 | No credentials, network dependency, or unsafe shell construction in the executed source paths. |
| maintainability | 11/12 | Small separable scripts with CLI arguments and local tool handoffs; the example's Python-API-only docking helper is environment-sensitive. |
| agent specific | 18/20 | Explicit validation and escape hatches are strong. The API-only example branch cannot be run natively in this Windows audit environment, although the source CLI fallback ran. |

## Input 1 — Canonical: Prepare a fresh 3PTB receptor and dock a fresh ligand with the source scripts

- Status: ✅ COMPLETED · Basic 40/40 · Specialized 57/60 · **Total 97/100**
- Execution: run/04_receptor_dock_path_repaired.execution.json: Fresh isolated execution; PID 196348 auditor-owned; no process terminated or signaled. Source prepare_receptor.py wrote fresh1/receptor.pdbqt; source dock_single.py returned 10 negative poses, best score -4.392.
- Finding: The earlier run/01_receptor_dock record is retained but excluded: its audit child PATH omitted the documented pdb2pqr tool directory. No source was changed; this fresh successful rerun used only an audit-child PATH correction.

| Assertion | Result | Evidence |
|---|---|---|
| Source receptor preparation creates a nonempty PDBQT | PASS | fresh1/receptor.pdbqt was written. |
| Source docking returns scored poses | PASS | 10 retained negative-energy poses. |
| Reported best pose is physically selected by the documented score filter | PASS | Best returned score -4.392. |

## Input 2 — Variant A: Exercise the example ligand helper on valid and invalid SMILES

- Status: ✅ COMPLETED · Basic 40/40 · Specialized 56/60 · **Total 96/100**
- Execution: run/02_virtual_helpers.execution.json: Fresh isolated execution; PID 138160 auditor-owned; no process terminated or signaled. The exact example produced a ligand PDBQT for guanidino-benzene and raised ValueError for NOT_A_SMILES.
- Finding: Confirms the example's input-validation behavior without treating an invalid molecule as a dockable input.

| Assertion | Result | Evidence |
|---|---|---|
| Valid SMILES converts to a PDBQT artifact | PASS | Fresh output exists and is nonempty. |
| Invalid SMILES is rejected explicitly | PASS | ValueError observed. |

## Input 3 — Variant B: Predict pockets with documented local P2Rank invocation

- Status: ✅ COMPLETED · Basic 39/40 · Specialized 56/60 · **Total 95/100**
- Execution: run/08_p2rank.execution.json: Fresh isolated execution; PID 148268 auditor-owned; no process terminated or signaled. P2Rank 2.5.1 Java invocation on a fresh receptor copy wrote two CSV artifacts with center fields.
- Finding: This is an independent documented preflight/site-prediction stage, not an assertion that the top site is biologically correct.

| Assertion | Result | Evidence |
|---|---|---|
| P2Rank completes on a receptor input | PASS | Java process exited 0. |
| Pocket output exposes coordinates for downstream review | PASS | CSV center columns found. |

## Input 4 — Adversarial: Ensure the exact source dock_single function excludes a positive docking energy

- Status: ✅ COMPLETED · Basic 40/40 · Specialized 58/60 · **Total 98/100**
- Execution: run/06_filter_unit.execution.json: Fresh isolated execution; PID 28640 auditor-owned; no process terminated or signaled. Exact source function parsed mock REMARK VINA RESULT values -7.0 and +68.0 and returned only [-7.0, 0.0, 0.0].
- Finding: This directly validates the repaired realized-FDR-adjacent acceptance behavior for non-favorable docked poses: they do not enter the returned candidate set.

| Assertion | Result | Evidence |
|---|---|---|
| Negative energy is retained | PASS | -7.0 returned. |
| Positive energy is excluded | PASS | +68.0 absent from returned list. |

## Input 5 — Stress: Rebuild the fresh source-docking poses to SDF using Meeko

- Status: ✅ COMPLETED · Basic 39/40 · Specialized 57/60 · **Total 96/100**
- Execution: run/05_pose_rebuild.execution.json: Fresh isolated execution; PID 39296 auditor-owned; no process terminated or signaled. Meeko rebuilt 1 molecule with 10 conformers from fresh1/poses.pdbqt and wrote poses_rebuilt.sdf.
- Finding: Verifies a concrete downstream pose-review artifact rather than stopping at a docking score.

| Assertion | Result | Evidence |
|---|---|---|
| Docked PDBQT can be reconstructed | PASS | Meeko returned a molecule. |
| Pose multiplicity survives reconstruction | PASS | 10 conformers written. |

## Input 6 — Determinism: Repeat exact source Vina CLI docking with seed 42

- Status: ✅ COMPLETED · Basic 40/40 · Specialized 57/60 · **Total 97/100**
- Execution: run/07_determinism.execution.json: Fresh isolated execution; PID 15928 auditor-owned; no process terminated or signaled. Two source CLI calls with the same inputs and --seed 42 produced identical stdout.
- Finding: Confirms deterministic score reporting for this fixture/tool version; it is not a claim of cross-version reproducibility.

| Assertion | Result | Evidence |
|---|---|---|
| Repeated seeded invocation completes | PASS | Both subprocesses exited 0. |
| Repeated seeded output is identical | PASS | Exact stdout equality asserted. |

## Input 7 — Scope Boundary: Check documented validation and special-case boundaries

- Status: ✅ COMPLETED · Basic 39/40 · Specialized 54/60 · **Total 93/100**
- Execution: run/03_scope.execution.json: Fresh isolated execution; PID 128776 auditor-owned; no process terminated or signaled. Required SKILL.md terms GNINA, validate, PoseBusters, and Covalent inhibitor were all present.
- Finding: The workflow names optional rescoring and pose validation, and does not silently apply ordinary non-covalent docking to covalent inhibitors.

| Assertion | Result | Evidence |
|---|---|---|
| Pose validation is an explicit requirement | PASS | validate and PoseBusters documented. |
| Covalent chemistry is called out as a special case | PASS | Covalent inhibitor boundary present. |

## Key strengths

- The complete local path from receptor preparation through source docking and downstream pose reconstruction executed successfully on fresh copies.
- The source correctly drops a deliberately injected positive-energy docking result rather than accepting it as a hit.
- The seeded CLI path produced identical output twice, and the workflow makes pose validation and special chemistry boundaries explicit.

## Recommendations

### P2 — Make the example docking function offer the same Vina CLI fallback as scripts/dock_single.py

- Observed in inputs: 1, 2, 6
- Problem: The example's docking helper imports the Vina Python API directly, which is unavailable in this native Windows audit environment, while the standalone source CLI path worked.
- Root cause: The example and CLI script expose different engine integration seams.
- Fix: Add an optional vina_exe/CLI branch to the example or have the example call the maintained standalone script.

### P2 — Keep a small reusable fixture and expected-artifact check with the skill

- Observed in inputs: 1, 3, 5
- Problem: The current workflow is runnable but relies on environment-provided fixtures for repeatable verification.
- Root cause: No bundled smoke-test contract accompanies the scripts.
- Fix: Ship a tiny non-proprietary receptor/ligand fixture plus assertions for nonempty receptor PDBQT, at least one negative score, and reconstructable pose output.
