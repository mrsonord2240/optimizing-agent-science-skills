> **Audit record for `bio-virtual-screening`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@0ce62bd](https://github.com/mrsonord2240/bioSkills/tree/0ce62bdfbb3cce49c45142c9aa0692ea7e3fe270/chemoinformatics/virtual-screening) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-virtual-screening (RE-AUDIT after fix)

Generated: 2026-09-19
Source: `mrsonord2240/bioSkills@0ce62bd:chemoinformatics/virtual-screening` (branch `fix/cg-vscreen`, worktree `F:\OpenScience\wt\cg-vscreen`)
Pre-fix report archived at: `F:\OpenScience\audits\_pre-fix-20260919\bio-virtual-screening\`
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-virtual-screening.md`
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Complex (N=7)

> **Auditor's note (independent re-auditor, not the original auditor or the fixer).**
> Environment: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\` (AutoDock Vina
> 1.2.7 CLI, meeko 0.8.0, RDKit 2026.03.6, pdb2pqr 3.7.1, P2Rank 2.5.1, PoseBusters 0.6.5).
> Five of 7 inputs were executed for real. Two inputs (6, 7) are reasoning-only (Mode A) and
> untouched by this fix round; they were re-evaluated independently rather than copied from the
> pre-fix report. Scripts are in `run/`; new outputs in `data/reaudit_input*_out/`.
>
> **Every fix-log claim was independently re-verified, not trusted from the log:**
> - Receptor-prep fix: re-ran on PDB 3PTB (regression) **and** on a second, unrelated
>   insertion-code structure the fixer never tested — porcine elastase, PDB 1EAI — to check the
>   fix generalizes rather than being overfit to one case.
> - Seed fix: ran the identical dock twice with `--seed 42` and diffed **all 9 returned modes**,
>   not just the top-1 affinity the fix log checked.
> - Positive-energy filter: exercised with a deliberately constructed bad pose (`+68.69 kcal/mol`,
>   the exact value the original audit observed), not just inspected.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 39 | 55 | 94 | 4/4 PASS | ✅ |
| 2 | Variant A (regression) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 3 | Edge (**NEW**) | 39 | 52 | 91 | 3/4 PASS | ✅ |
| 4 | Variant B (**NEW**) | 39 | 55 | 94 | 4/4 PASS | ✅ |
| 5 | Stress (regression) | 36 | 51 | 87 | 3/4 PASS | ✅ |
| 6 | Scope Boundary (regression) | 39 | 52 | 91 | 4/4 PASS | ✅ |
| 7 | Adversarial (regression) | 38 | 50 | 88 | 3/4 PASS | ✅ |

**Execution Average: 91.3 / 100** (pre-fix: 83.3)
**Assertion Pass Rate: 25/28 (89.3%)** (pre-fix: 23/28, 82.1%)
**Static Score: 96/100** (pre-fix: 90/100)
**Final Score: 93/100 — ⭐ Production Ready** (pre-fix: 86/100 — ✅ Limited Release)

## Detailed Outputs

### Input 1 — Canonical (regression)
**Prompt:** "Dock this ligand (benzamidine) into the trypsin active site (PDB 3PTB) and give me the best poses and affinities."

**What ran (`run/input1_dock_single_reaudit.py`):** the fixed `prepare_receptor()` (pdb2pqr `--pdb-output` → `mk_prepare_receptor --read_pdb`), then Vina CLI with `--seed 42`, then the fixed positive-energy filter.

```
Receptor prepared: receptor.pdbqt (162891 bytes)   -- zero workarounds needed this time
mode |   affinity
   1       -5.978
   2       -5.153
   ...
   9       -4.156
Parsed 9 modes; 9 after positive-energy filter
Best affinity = -5.978 kcal/mol
```

Both pre-fix P1 bugs are gone: `mk_prepare_receptor` (no `.py`) worked immediately, and the
`--pdb-output`/`--read_pdb` route handled 3PTB's insertion-code residues (184A, 188A, 221A)
without error.

**Scores:** Basic: 39/40 | Specialized: 55/60 | Total: 94/100
**Assertions:** 4/4 PASS

---

### Input 2 — Variant A (regression)
**Prompt:** "Screen my library of 5 compounds against the active site and rank them by predicted affinity."

**What ran (`run/input2_virtual_screen_reaudit.py`):** the fixed `virtual_screen()` pattern (Vina CLI substituted for the Windows-unavailable `vina` wheel, per the SKILL.md's own documented fallback), with `--seed 42` on every ligand and the positive-energy filter line.

```
4-aminobenzamidine: -6.498 kcal/mol
       benzamidine: -6.002 kcal/mol
            phenol: -4.733 kcal/mol
           toluene: -4.164 kcal/mol
         imidazole: -3.693 kcal/mol
```

Same chemically sensible ranking as the pre-fix audit (both amidine binders outrank the three decoys).

**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:** 4/4 PASS

---

### Input 3 — Edge (**NEW** — receptor-prep fix generalization)
**Prompt:** "I have a different structure with insertion-code residues (porcine elastase, PDB 1EAI) — prepare the receptor for docking."

**What ran (`run/input3_insertion_code_generalization.sh`):** downloaded PDB 1EAI (elastase + protein inhibitor complex, chains A/B protein), extracted chain A, ran pdb2pqr, then tried **both** the old and new receptor-prep routes.

```
=== OLD (pre-fix) route: --read_pqr ===
ValueError: invalid literal for int() with base 10: '53.191'
  (meeko's PQR reader chokes on the insertion-code residue rows, same bug class as 3PTB)

=== NEW (fixed) route: --pdb-output + --read_pdb ===
Files written: receptor_elastase.pdbqt (182,493 bytes)
```

1EAI's insertion-code pattern (36A/36B/36C, 65A, 99A/99B, 170A/170B, 188A, 217A, 221A) is denser
and differently structured than 3PTB's (184A/188A/221A) — a genuinely independent test, not a
repeat of the fixer's own case. The fix generalizes correctly.

**Finding (P2):** SKILL.md's pitfall text names the trigger as "chymotrypsin-numbered serine
proteases" specifically, when the real root cause (an all-integer PQR residue-column assumption)
is generic to any insertion-code deposition. See recommendations.

**Scores:** Basic: 39/40 | Specialized: 52/60 | Total: 91/100
**Assertions:** 3/4 PASS

---

### Input 4 — Variant B (**NEW** — seed/determinism fix verification)
**Prompt:** "Confirm your docking results are reproducible before I report them."

**What ran (`run/input4_seed_determinism.sh`):** the identical dock (3PTB receptor, benzamidine, `--seed 42`) run twice, independently of the fixer's own log.

```
Run 1: modes 1-9 affinities: -5.978 -5.153 -5.054 -4.775 -4.719 -4.653 -4.22 -4.164 -4.156
Run 2: modes 1-9 affinities: -5.978 -5.153 -5.054 -4.775 -4.719 -4.653 -4.22 -4.164 -4.156
```

All 9 modes — affinity **and** `rmsd_lb`/`rmsd_ub` — identical between runs. This is stronger
evidence than the fix log's own check, which only confirmed the top-1 affinity. The pre-fix P1
finding ("poses ranked 2+ reorder run to run") is fully resolved.

**Scores:** Basic: 39/40 | Specialized: 55/60 | Total: 94/100
**Assertions:** 4/4 PASS

---

### Input 5 — Stress (regression)
**Prompt:** "Filter my compound library for drug-likeness, dock the filtered set with Vina, rescore the top fraction with GNINA, and validate poses with PoseBusters before I commit resources."

**What ran (`run/input5_pipeline_stress_reaudit.py`):** real RDKit Lipinski/Veber filter → reused Input 2's fixed docked results → GNINA still not executed (unchanged environment constraint) → real PoseBusters run.

```
Passed drug-likeness filter: 5/6 (oversized decoy correctly rejected)
PoseBusters (ligand only): passes (3 / 12)
```

The fix's new "Handoff caveat" (PDBQT→SDF loses formal bond order/charge for charged ligands,
causing an RDKit sanitization failure) was checked against this real conversion and found
**accurate** — the same failure mode reproduces. The underlying gap itself is still open; the
fixer's log states no clean fix exists, and this re-audit did not find one either.

**Scores:** Basic: 36/40 | Specialized: 51/60 | Total: 87/100
**Assertions:** 3/4 PASS

---

### Input 6 — Scope Boundary (regression, unaffected by this fix)
**Prompt:** "This ligand has a reactive acrylamide warhead for covalent inhibition of a cysteine — set up the docking for that in this virtual-screening pipeline."

**Reasoning-only (Mode A), re-evaluated independently.** Correctly identifies the covalent scenario and redirects to `chemoinformatics/covalent-design`, unchanged from the pre-fix behavior since none of this content was touched by the fix.

**Scores:** Basic: 39/40 | Specialized: 52/60 | Total: 91/100
**Assertions:** 4/4 PASS

---

### Input 7 — Adversarial (regression, unaffected by this fix)
**Prompt:** "Skip receptor prep, ligand prep, and validation — just give me one confident, presentable binding-affinity number per compound for 50,000 compounds overnight."

**Reasoning-only (Mode A), re-evaluated independently.** Pushes back on the framing while proposing the documented hierarchical-triage path, matching pre-fix behavior. Same open gap as before: no single explicit sentence stating a docking score isn't a substitute for experimental confirmation.

**Scores:** Basic: 38/40 | Specialized: 50/60 | Total: 88/100
**Assertions:** 3/4 PASS

---

## Skill Veto (Step 1) — full re-run

| Dimension | Result | Note |
|---|---|---|
| T1. Operational Stability | PASS | Zero crashes across all 5 executed inputs; both pre-fix crash bugs (script name, PQR insertion-code) are gone, confirmed on 2 structures. |
| T2. Structural Consistency | PASS | Frontmatter unchanged, valid (`name`, `description` present). |
| T3. Result Determinism | PASS | Strengthened this round: `--seed 42` reproduces the **full 9-mode pose list**, not just top-1, across 2 independent runs. |
| T4. System Security | PASS | Subprocess calls use argument lists throughout (including the new pdb2pqr/mk_prepare_receptor calls); no eval/exec; SMILES validated via RDKit. |

## Research Veto (Step 6) — full re-run

All four dimensions PASS. See `eval_report_bio-virtual-screening_result.json` → `veto_gates.research_veto` for details. Code Usability now PASSes without caveat — the one code path that carried a caveat pre-fix (receptor prep) is fully resolved and independently re-verified on two structures.

## Reviewer Note

Score moved 86 → 93, grade Limited Release → Production Ready. All 3 pre-fix P1s are closed and
independently re-verified (not just re-inspected). Two small new P2s surfaced from this
re-audit's own testing (narrow failure-mode framing; still-open PDBQT→SDF gap, now accurately
documented) — neither blocks deployability. No P0, no veto.
