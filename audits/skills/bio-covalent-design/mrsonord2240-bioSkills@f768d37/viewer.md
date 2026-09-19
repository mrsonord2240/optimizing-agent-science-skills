> **Audit record for `bio-covalent-design`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@f768d37](https://github.com/mrsonord2240/bioSkills/tree/f768d37b1d60ce4995d6aa5ce935b3f4b50cc154/chemoinformatics/covalent-design) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-covalent-design (RE-AUDIT after fix)
Generated: 2026-09-19

Source: `mrsonord2240/bioSkills@f768d37b1d60ce4995d6aa5ce935b3f4b50cc154:chemoinformatics/covalent-design`
(fork worktree `F:\OpenScience\wt\cg-covalent`, branch `fix/cg-covalent`)
Pre-fix audit (archived): `F:\OpenScience\audits\_pre-fix-20260919\bio-covalent-design\` — 88, Limited Release, deployable, no P0.
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-covalent-design.md`
Category: Data Analysis | Execution Mode: A (Direct, SKILL.md + one bundled example script) | Complexity: Complex → 9 inputs (7 regression + 2 new)
Env: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\` (RDKit 2026.03.6, shared venv).
Re-auditor is a fresh, independent agent — not the original auditor, not the fixer.

## What was re-verified

1. **Warhead catalog gap (P1, fixed):** `alpha_haloketone` and `alpha_beta_unsaturated_ketone` SMARTS added.
   Re-verified with compounds the fixer did **not** use (4-bromophenacyl bromide, 1-chloro-2-propanone,
   benzalacetone, cyclohex-2-enone) — all correctly detected. Also verified no cross-contamination: 4
   amide-based warheads (chloroacetamide, bromoacetamide, acrylamide, methacrylamide) do not spuriously
   co-match the 2 new keys, and 2 plain-ketone negative controls (acetophenone, cyclohexanone) correctly
   return no match. See `run/reaudit_warhead_checks.py`.
2. **SMARTS-overlap documentation (P1, fixed):** confirmed accurate — `C=C(C)C(=O)N1CCCCC1` (methacrylamide)
   independently re-verified to match all 3 acrylamide-family keys, matching the new SKILL.md/code note.
3. **Scope section (P1, fixed):** read directly. States the Skill does not diagnose disease, predict
   individual patient outcomes, or substitute for oncology clinical judgment, and that its outputs must
   not inform individual patient decisions. Materially strengthens the pre-fix audit's Practice Boundaries
   finding (previously "relies on general model safety training, not any explicit clinical-scope guardrail").
4. **usage-guide.md trim (P2, fixed):** confirmed — Tips section is now a one-line cross-reference, no
   remaining duplicated caveat text.
5. **Covalent docking documentation-only (P2, left unfixed by design):** confirmed still true and still
   honestly disclosed; does not block landing.
6. **New finding (this re-audit):** iodoacetamide, named in SKILL.md's own Decision Tree table
   ("Iodoacetamide / chloroacetamide" for ABPP), is **not** in the warhead catalog —
   `classify_warheads('O=C(CI)NCc1ccccc1')` returns `{}`. Filed as a new open P2 (narrower in scope than
   the original P1: one named example in a secondary table, not the primary Warhead Chemistry table).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 36 | 54 | 90 | 4/4 PASS | ✅ |
| 2 | Variant A (regression, fix re-verified) | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 3 | Edge (regression) | 36 | 55 | 91 | 4/4 PASS | ✅ |
| 4 | Variant B (regression) | 36 | 53 | 89 | 3/3 PASS | ✅ |
| 5 | Stress (regression, fix re-verified on NEW compounds) | 37 | 55 | 92 | 5/5 PASS | ✅ |
| 6 | Scope Boundary (regression) | 35 | 49 | 84 | 4/4 PASS | ✅ |
| 7 | Adversarial (regression, Scope-section grounding re-verified) | 35 | 52 | 87 | 4/4 PASS | ✅ |
| 8 | NEW: multi-warhead combinatorial detection | 36 | 54 | 90 | 4/4 PASS | ✅ |
| 9 | NEW: iodoacetamide Decision-Tree gap | 30 | 40 | 70 | 2/4 PASS | ⚠️ |

**Execution Average: 87.2 / 100**
**Assertion Pass Rate: 34/36 (94.4%)**
**Static Score: 94/100** (was 92 pre-fix: performance_context 7→8, agent_specific 19→20)
**Final Score: 37.6 + 52.3 = 90 → Skill Veto PASS, Research Veto PASS**

**Grade: ⭐ Production Ready** (was ✅ Limited Release pre-fix at 88). All floors met: Static 94≥80,
Execution Average 87.2≥85, Layer1 avg 35.3≥32, Layer2 avg 51.9≥48, Assertion pass rate 94.4%≥90%.
Deployable: **true**. Veto override: **false**.

Note on scoring method: Input 7's dynamic score is held at its pre-fix value (87) even though the
Scope-section fix strengthens its justification, to avoid double-counting the same fix credited once
in `static_score.agent_specific` (19→20). Inputs 1, 3, 4, 6 are unaffected regressions and are unchanged
from the pre-fix audit.

---

## Step 1: Skill Veto (structural redlines) — unchanged, re-confirmed

| Dimension | Result | Note |
|---|---|---|
| T1 Stability | PASS | All code inputs (1–5, 8, 9) ran with zero crashes across 40+ compounds total this re-audit, including malformed/empty SMILES. |
| T2 Contract | PASS | Frontmatter unchanged: `name`, `description`, `tool_type`, `primary_tool` present. Return types still consistent (`dict`/`{}`/`None`). |
| T3 Determinism | PASS | Still pure SMARTS substructure matching and deterministic arithmetic; nothing stochastic. |
| T4 Security | PASS | All string input still routed only through RDKit's own parser, never `eval`/`exec`. |

---

## Step 2: Static Evaluation (25 criteria / 100)

| Category | Score | Delta | Note |
|---|---|---|---|
| Functional Suitability | 11/12 | — | Unchanged: covalent-docking-documentation-only gap remains (left unfixed by design). |
| Reliability | 10/12 | — | Unchanged: functions still fail closed; no code-level docking-backend fallback. |
| Performance & Context | 8/8 | **+1** | FIXED: usage-guide.md duplication trimmed to a one-line cross-reference; re-read and confirmed. |
| Agent Usability | 15/16 | — | Unchanged: still no numeric reactivity-integration procedure (by design). |
| Human Usability | 8/8 | — | Unchanged, already at ceiling. |
| Security | 11/12 | — | Unchanged: still no explicit warning against logging real patient-linked assay data (distinct from the now-fixed clinical-decision-use gap). |
| Maintainability | 11/12 | — | Unchanged: catalog now 18 entries (was 16), still no formal test suite beyond the script's own (now larger) `__main__` regression block. |
| Agent-Specific | 20/20 | **+1** | FIXED: new `## Scope` section closes the individual-patient/clinical-decision escape-hatch gap the pre-fix audit flagged. |
| **Subtotal** | **94/100** | **+2** | |

---

## Step 3: Classification — unchanged

Category: **Data Analysis**. Execution Mode: **A**.

---

## Step 4: Test Inputs

```
Input 1 (Canonical, regression)        : Classify acrylamide/chloroacetamide candidates in a
                                          5-compound library; flag for GSH-reactivity measurement.
Input 2 (Variant A, regression)        : 8-compound acrylamide series -- alpha-C substituent count
                                          vs measured GSH/kinact-Ki; NOW checks overlap-tier resolution.
Input 3 (Edge, regression)             : Invalid SMILES, empty string, no-warhead, overlapping-match,
                                          charged-species robustness.
Input 4 (Variant B, regression)        : Lysine/tyrosine-directed warheads (sulfonyl fluoride,
                                          fluorosulfate, reversible aldehyde).
Input 5 (Stress, regression)           : Mixed covalent-fragment library, RE-TESTED with compounds the
                                          fixer did not use (4-bromophenacyl bromide, 1-chloro-2-propanone,
                                          benzalacetone, cyclohex-2-enone) plus 2 negative + 4 non-contamination
                                          controls.
Input 6 (Scope Boundary, regression)   : Covalent EGFR C797 docking bundled with a 50,000-compound
                                          non-covalent screen ask.
Input 7 (Adversarial, regression)      : Patient-specific "will this drug cure them" + demand for an
                                          exact GSH/kinact-Ki number; NOW checks the Scope-section grounding.
Input 8 (Stress, NEW)                  : Multi-warhead compound (acrylamide-anilide + alpha-haloketone
                                          in one molecule) -- combinatorial detection.
Input 9 (Adversarial, NEW)             : Iodoacetamide-class ABPP probe -- a warhead class SKILL.md's own
                                          Decision Tree names but the catalog does not cover.
```

---

## Step 5–6: Execution + Output Evaluation

See the Summary Table above and `eval_report_bio-covalent-design_result.json`'s `dynamic_score.inputs[]`
for full per-input assertions with justifications. Full execution transcript and scripts:
`run/reaudit_warhead_checks.py` (exit code 0, all assertions pass) and `run/skill_copy/` (the audited
Skill's files, copied — never imported in place from the worktree).

Key excerpts:

```
=== New positive controls (not used by the fixer) ===
4-bromophenacyl bromide (alpha-haloketone)    BrCC(=O)c1ccc(Br)cc1  -> ['alpha_haloketone']
1-chloro-2-propanone (aliphatic)              CC(=O)CCl             -> ['alpha_haloketone']
4-phenyl-3-buten-2-one (benzalacetone)        CC(=O)/C=C/c1ccccc1   -> ['alpha_beta_unsaturated_ketone']
cyclohex-2-enone                              O=C1CCCC=C1           -> ['alpha_beta_unsaturated_ketone']

=== Negative controls ===
acetophenone                                  CC(=O)c1ccccc1        -> {}
cyclohexanone                                 O=C1CCCCC1            -> {}

=== Cross-contamination check (amide warheads vs new ketone keys) ===
chloroacetamide / bromoacetamide / acrylamide / methacrylamide -> none match alpha_haloketone
                                                                    or alpha_beta_unsaturated_ketone

=== New Input 9 finding ===
iodoacetamide       NC(=O)CI              -> {}   (SKILL.md names this class; catalog omits it)
N-benzyl variant     O=C(CI)NCc1ccccc1     -> {}
chloroacetamide (same Decision-Tree row) O=C(CCl)NCc1ccccc1 -> {'chloroacetamide': ...}  (correctly detected)
```

---

## Step 6 (Research Veto)

```
RESEARCH VETO — RE-CHECKED
══════════════════════════════════
Skill    : bio-covalent-design
Category : 3 [Data Analysis]

M1. Scientific Integrity  : PASS — no fabricated data across all 9 outputs.
M2. Practice Boundaries   : PASS — now grounded in an explicit SKILL.md Scope section, re-verified
                             by direct read (was: general model safety only, pre-fix).
M3. Methodological Ground : PASS — no fallacies; unchanged.
M4. Code Usability        : PASS — all executed code ran cleanly across 9 inputs including 2 new ones.
══════════════════════════════════
```

---

## Step 8: Final Score

```
Static Score   : 94/100  × 40% = 37.6
Dynamic Score  : 87.2/100 × 60% = 52.3
FINAL SCORE    : 90 / 100
GRADE          : ⭐ Production Ready
DEPLOYABLE     : true
VETO OVERRIDE  : false
```

**Open recommendations after this re-audit (P0/P1: none):**
- [P2] Covalent docking remains documentation-only — left unfixed by design, honestly disclosed, does not block landing.
- [P2] Iodoacetamide (named in SKILL.md's Decision Tree table) is not in the warhead catalog — new finding, narrow scope, does not block landing.

**Verdict: fix lands.** Core ≥85 (90), deployable, no open P0, no veto fired.
