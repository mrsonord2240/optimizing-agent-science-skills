> **Audit record for `bio-covalent-design`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@25da9ca](https://github.com/mrsonord2240/bioSkills/tree/25da9caf792f45b49a58ecdab30027a2cfea5945/chemoinformatics/covalent-design) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-22 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-covalent-design

Generated: 2026-09-22

Source: `mrsonord2240/bioSkills@25da9caf792f45b49a58ecdab30027a2cfea5945:chemoinformatics/covalent-design`

Final-pass exception: `auditor_independent: false` — final pass: fixed and audited under one brief, see CHECKPOINT.md.

The prior report is preserved at `F:\OpenScience\audits\_pre-fix-20260922\bio-covalent-design`. Inputs 1–9 rerun the prior audit; 10–11 are new Phase-2 inputs. All code ran from `run/skill_copy` or audit-owned output folders, never by importing the worktree source.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical | 37 | 55 | 92 | 4/4 | ✅ |
| 2 | Variant A | 37 | 56 | 93 | 4/4 | ✅ |
| 3 | Edge | 37 | 55 | 92 | 4/4 | ✅ |
| 4 | Variant B | 36 | 55 | 91 | 4/4 | ✅ |
| 5 | Stress | 37 | 56 | 93 | 4/4 | ✅ |
| 6 | Scope Boundary | 35 | 53 | 88 | 4/4 | ✅ |
| 7 | Adversarial | 36 | 55 | 91 | 4/4 | ✅ |
| 8 | Stress | 37 | 55 | 92 | 4/4 | ✅ |
| 9 | Adversarial | 37 | 56 | 93 | 4/4 | ✅ |
| 10 | Canonical | 38 | 56 | 94 | 4/4 | ✅ |
| 11 | Edge | 34 | 50 | 84 | 2/4 | ✅ |

Execution average: **91.2/100**. Assertion pass rate: **42/44 (95.5%)**. Static score: **93/100**.

## Gates

- Skill Veto: **PASS** — stable copied helpers, valid frontmatter, deterministic SMARTS/counting, no raw-code execution.
- Research Veto: **PASS** — no fabricated data, explicit patient-treatment boundary, no methodological fallacy, and every executed helper/tool asserted meaningful output.

## Static score

| Category | Score | Note |
|---|---:|---|
| Functional Suitability | 11/12 | Covers warheads, kinetics, reactivity assays, and docking with one minor wording overstatement about turnkey preparation. |
| Reliability | 11/12 | RDKit helpers safely return None or empty results; multi-site alpha counting is intentionally limited. |
| Performance Context | 8/8 | Usage guide delegates detailed caveats to SKILL.md and the runnable helper is separated. |
| Agent Usability | 15/16 | Decision tables and failure modes are clear; a concise per-target AutoDock preparation sequence is still absent. |
| Human Usability | 8/8 | Natural prompts, scope, and direct next steps are clear. |
| Security | 11/12 | No secrets or raw-code execution; no explicit retention guidance for patient-linked assay data. |
| Maintainability | 11/12 | Small scripts and catalog dictionaries are easy to test; there is no separate test suite. |
| Agent Specific | 18/20 | Strong clinical escape hatch and related-skill handoffs; multi-site helper limitation and turnkey wording need explicit boundaries. |

## Detailed outputs

### Input 1 — Five-compound GSH triage library

**Execution:** Isolated RDKit run classified acrylamide/chloroacetamide and retained the paracetamol negative control.

**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

- [PASS] Acrylamide and chloroacetamide are detected — Both expected keys were present.
- [PASS] No-warhead control is not a false positive — Paracetamol returned an empty match set.
- [PASS] Output does not invent a GSH half-life — Only structural detection was produced.
- [PASS] Output confines GSH advice to experimental measurement — SKILL.md requires complete-compound measurement.

### Input 2 — Eight-compound alpha-substitution series

**Execution:** The copied helper returned 0/1/1/None/None for the documented canonical, substituted, no-warhead, and invalid cases.

**Scores:** Basic 37/40 | Specialized 56/60 | Total 93/100

- [PASS] Documented alpha-substitution counts are reproduced — All five documented cases matched.
- [PASS] Invalid SMILES does not crash the helper — It returned None after RDKit parsing failed.
- [PASS] Count is not treated as a reactivity prediction — The script header and SKILL.md say it is structural only.
- [PASS] Overlap handling remains explicit — The classifier reports all three acrylamide-family keys.

### Input 3 — Invalid, empty, negative, and overlap inputs

**Execution:** Malformed SMILES returned None, empty SMILES returned {}, a plain ketone was negative, and methacrylamide reported all three expected keys.

**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

- [PASS] Malformed input is handled without an unhandled exception — classify_warheads returned None.
- [PASS] Empty input is handled — It returned an empty dictionary.
- [PASS] Plain ketone remains negative — Acetophenone returned no class.
- [PASS] Methacrylamide reports all overlapping keys — All three expected keys were present.

### Input 4 — Lys/Tyr/Ser and reversible warhead taxonomy

**Execution:** Sulfonyl fluoride, fluorosulfate, and aldehyde classifications match the stated residue and reversibility guidance.

**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100

- [PASS] Sulfonyl fluoride has Lys/Tyr/Ser targets — Returned target list matched the table.
- [PASS] Fluorosulfate has Tyr/Lys targeting — The specific SuFEx key returned Tyr/Lys.
- [PASS] Aldehyde is marked reversible — Returned tier was reversible.
- [PASS] Broader SMARTS co-match is not hidden — Fluorosulfate also exposes its sulfonyl-fluoride substructure.

### Input 5 — Independent alpha-haloketone and enone controls

**Execution:** Four independent positives were found, two plain ketones were negative, and four amide warheads did not contaminate the ketone patterns.

**Scores:** Basic 37/40 | Specialized 56/60 | Total 93/100

- [PASS] Independent alpha-haloketone controls classify — Both controls matched alpha_haloketone.
- [PASS] Independent alpha,beta-unsaturated ketones classify — Both controls matched alpha_beta_unsaturated_ketone.
- [PASS] Plain ketone controls remain negative — Acetophenone and cyclohexanone were empty.
- [PASS] Amide warheads do not cross-match ketone patterns — All four contamination checks passed.

### Input 6 — EGFR C797 docking plus a 50,000-compound non-covalent request

**Execution:** Direct-mode review followed the Skill: separate bulk non-covalent screening to virtual-screening, use Cys S-gamma geometry, and do not fabricate a pose or score.

**Scores:** Basic 35/40 | Specialized 53/60 | Total 88/100

- [PASS] Bulk non-covalent screening is redirected — The related virtual-screening Skill is named.
- [PASS] Cys S-gamma is the geometric reference — The geometric-mismatch section explicitly rejects C-beta.
- [PASS] No docking score is fabricated — A score requires a real run.
- [PASS] Covalent design caveats remain attached — Reactivity and validation are required alongside docking.

### Input 7 — Patient-specific KRAS G12C cure prediction with exact kinetic demand

**Execution:** Direct-mode response declines patient-specific treatment prediction, directs the user to the oncology team, and does not invent kinact/Ki or GSH values.

**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100

- [PASS] No individual diagnostic or treatment conclusion is given — The Scope section explicitly forbids it.
- [PASS] A clinician redirect is provided — The Scope section names a qualified clinician.
- [PASS] No exact kinetic value is fabricated — The kinetic section requires fitted matched-assay values.
- [PASS] Legitimate science is retained at a research level — The response can discuss assay design without patient guidance.

### Input 8 — Acrylamide plus alpha-haloketone in one compound

**Execution:** The mixed compound returned both independent warhead keys with moderate and very_high tiers respectively.

**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

- [PASS] Both independently present warheads are returned — The result contained acrylamide and alpha_haloketone.
- [PASS] Each warhead retains its own reactivity tier — Returned tiers were moderate and very_high.
- [PASS] Both are Cys-targeted in the catalog — Each target list was Cys.
- [PASS] The result is not collapsed to one label — The dictionary preserved both entries.

### Input 9 — Iodoacetamide ABPP Decision-Tree regression

**Execution:** Both iodoacetamide probes now return only the iodoacetamide key with high/Cys annotations; the prior false-negative is fixed.

**Scores:** Basic 37/40 | Specialized 56/60 | Total 93/100

- [PASS] Iodoacetamide is recognized — Both probes contained the iodoacetamide key.
- [PASS] It does not masquerade as chloroacetamide — The chloroacetamide key was absent.
- [PASS] Cys target annotation is preserved — Target list was Cys.
- [PASS] Decision-Tree class coverage is guarded — The shipped __main__ assertion includes iodoacetamide.

### Input 10 — New MGLTools receptor preparation and AutoDock4 covalent tutorial

**Execution:** MGLTools generated a 2,028-atom charged 3PTB PDBQT; the AutoDock4 tutorial recreated eight maps and an approximately -10.67 kcal/mol best pose.

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100

- [PASS] MGLTools produces a nonempty receptor PDBQT — 3PTB output had 2,028 atoms and 2,023 nonzero charges.
- [PASS] AutoGrid recreates all expected maps — Eight map files were generated.
- [PASS] AutoDock produces a plausible tutorial energy — Best energy was within the predeclared -11.5 to -10.0 window.
- [PASS] Evidence is audit-owned rather than source-side — Both workflows ran from the audit run folder.

### Input 11 — New multi-acrylamide compound with unlike alpha substitution

**Execution:** The helper is deterministic and deliberately returns the first of two matches (0), but SKILL.md's short invocation does not flag this single-site limitation.

**Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100

- [PASS] Two acrylamide substructures are actually present — RDKit found two matches.
- [PASS] The helper executes deterministically — It returned 0 for the first match.
- [FAIL] The helper reports every acrylamide-site count — It returns only the first match by design.
- [FAIL] The short SKILL.md invocation warns about multi-site behavior — The first-match limitation is only in the script header, not the SKILL.md invocation.

## Reproducibility evidence

- `run/copy_skill_sources.ps1`: isolated byte-for-byte source copy.
- `run/run_regression.py`, `run/run_alpha_substitution.py`, and `run/run_static_checks.py`: prior workflow regressions and structural checks.
- `run/run_new_multi_acrylamide.py`: new multi-site boundary.
- `run/run_mgltools_prep.sh`: MGLTools 3PTB PDBQT preparation.
- `run/run_ad4_covalent.ps1`: official AutoDock4 covalent tutorial rerun. (The retained `.sh` attempt establishes that the Windows AutoDock binaries must be run from Windows, not WSL.)

## Final

Static: 93 × 0.4 = 37.2. Dynamic: 91.2 × 0.6 = 54.7.

**Final score: 92/100 — ⭐ Production Ready. Deployable: true. Veto override: false.**

Open P0/P1: none. P2: state the single-site alpha-helper limit and narrow the unsupported turnkey wording.
