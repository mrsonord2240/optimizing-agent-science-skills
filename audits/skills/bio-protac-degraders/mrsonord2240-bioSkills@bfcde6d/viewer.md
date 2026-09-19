> **Audit record for `bio-protac-degraders`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@bfcde6d](https://github.com/mrsonord2240/bioSkills/tree/bfcde6d6e676730230728e37142eca8054ac06aa/chemoinformatics/protac-degraders) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-protac-degraders (RE-AUDIT)
Generated: 2026-09-19

Re-audit of the fixed Skill at `F:\OpenScience\wt\cg-protac\chemoinformatics\protac-degraders`
(branch `fix/cg-protac`, commit `bfcde6d`), performed by a fresh auditor independent of both the
original auditor and the fixer. Pre-fix report archived to
`F:\OpenScience\audits\_pre-fix-20260919\bio-protac-degraders\`. Original score: 90, Production
Ready. Fix log: `F:\optimizing-agent-science-skills\fixes\bio-protac-degraders.md`.

Env: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\` (RDKit 2026.03.6, numpy 2.5.3,
scipy 1.18.1, Python 3.12.13). All code run from a fresh `skill_copy\` copy of the fixed skill
files, never in place inside the worktree or the external clone.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 2 | Variant A — ternary prediction, new invocation table | 39 | 57 | 96 | 4/4 PASS | ✅ |
| 3 | Edge (regression) | 39 | 58 | 97 | 4/4 PASS | ✅ |
| 4 | Variant B (regression) | 38 | 54 | 92 | 3/3 PASS | ✅ |
| 5 | Stress — cooperativity/DC50, independently re-planted | 38 | 57 | 95 | 5/5 PASS | ✅ |
| 6 | Scope Boundary (regression) | 38 | 53 | 91 | 4/4 PASS | ✅ |
| 7 | Adversarial (regression) | 39 | 54 | 93 | 3/3 PASS | ✅ |
| 8 | **NEW** Stress — PEG3 linker + fine alkyl series, ternary_geometry_screen.py | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 9 | **NEW** Edge — narrow-separation hook, cooperativity_dc50.py | 30 | 46 | 76 | 2/4 PASS | ✅ |

**Execution Average: 91.9 / 100**
**Assertion Pass Rate: 33/35 (94.3%)**

> Inputs 1, 3, 4, 6, 7 are regression re-runs of the original audit's inputs against the fixed
> skill (unaffected code paths, same results). Input 2 is a regression input re-scored against the
> new invocation table. Input 5 reuses the original scenario but was independently re-executed with
> a different planted dataset (seed 777, different Kd/DC50/Dmax values) than either the original
> audit or the fixer's own verification. Inputs 8 and 9 are new, built specifically to stress-test
> the two new scripts on cases neither the original auditor nor the fixer used.

## Detailed Outputs

### Input 1 — Canonical (regression)
**Prompt:** "Design a CRBN-recruiting PROTAC series for kinase target X: enumerate a linker series and report structural properties."
**Executed:** true — `skill_copy/examples/protac_enumerate.py`, unmodified by the fix.
**Output:** 11 connected target-linker-CRBN SMILES with RDKit MolWt/TPSA/LogP/RotBonds, framed as structural hypotheses, no pass/fail cutoff.
**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100
**Assertions:** 4/4 PASS (enumeration correct, real RDKit descriptors, hypothesis framing, code runs clean).

### Input 2 — Variant A: ternary prediction request (PRosettaC unavailable, new table)
**Prompt:** "Predict the ternary complex for this target-PROTAC-CRBN combination using PRosettaC."
**Executed:** false (external submission by design) — scored by inspection of SKILL.md's new "Ternary Complex Prediction Tools" invocation table.
**Output:** Names prosettac.weizmann.ac.il, free registration, upload requirements (target PDB + ligand pose, E3 PDB + ligand pose, PROTAC SMILES), hours-to-a-day turnaround, and what comes back (ranked/clustered poses + interface scores). States plainly this Skill does not run PRosettaC itself, and points to `ternary_geometry_screen.py` as the only locally runnable ternary-hypothesis content.
**Independent verification of table claims:**
- Boltz-1/2 row ("pip install boltz, GPU recommended, `boltz predict`") — confirmed via live fetch of github.com/jwohlwend/boltz: `pip install boltz[cuda] -U`, CPU-slower note, `boltz predict input_path` all present.
- REINVENT4 row (linker design, install via conda/uv) — confirmed via live fetch of github.com/MolecularAI/REINVENT4: explicit "linker design" in the repo description, both conda and uv install paths documented.
- PRosettaC row — live automated fetch of prosettac.weizmann.ac.il returned empty/404 (likely a legacy academic server issue with the fetcher's forced HTTPS upgrade), but a web search corroborates the exact URL and submission workflow (two protein+ligand structures + PROTAC SMILES) against the original JCIM/bioRxiv publication describing the same server.
- HADDOCK3 row (bonvinlab.org/haddock3/) — live fetch confirms the URL resolves and redirects to real documentation.
**Scores:** Basic 39/40 | Specialized 57/60 | Total 96/100
**Assertions:** 4/4 PASS.

### Input 3 — Edge: malformed attachment points (regression)
**Prompt:** "Build a PROTAC from this target fragment, linker, and E3 fragment" with 4 sub-cases (double-bond dummy, two-dummy fragment, invalid SMILES, valid control).
**Executed:** true — all 4 sub-cases run through `build_protac()`.
**Output:** 3 documented ValueErrors raised exactly as SKILL.md's Common Errors table states; control case succeeds.
**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100
**Assertions:** 4/4 PASS.

### Input 4 — Variant B: CRBN → VHL E3 switch (regression)
**Prompt:** "Switch the E3 recruiter from CRBN to VHL for the same target and linker set; compare properties."
**Executed:** true.
**Scores:** Basic 38/40 | Specialized 54/60 | Total 92/100
**Assertions:** 3/3 PASS.

### Input 5 — Stress: cooperativity + DC50/Dmax/hook, independently re-planted dataset
**Prompt:** "Given these binary/ternary Kd measurements and this dose-response dataset, compute cooperativity alpha and fit DC50/Dmax, flagging any hook effect."
**Executed:** true — ran `cooperativity_alpha()`, `detect_hook()`, `fit_dc50()` from `skill_copy/examples/cooperativity_dc50.py` against:
- 3 Kd pairs incl. equal-Kd (alpha=1.000, "no cooperativity") and a negative-Kd input (correctly raises `ValueError`).
- A dose-response curve I planted myself: dmax=55%, dc50=8nM, hill=1.4, hook_k=900nM, hook_hill=2.0, seed=777, 16 log-spaced points from ~1nM to ~5uM — different from both the fixer's own demo curve (dmax=80, dc50=40, seed=42) and Input 9's curve below.
**Output:** hook_flag=True (peak 52.0% at 104.7nM vs. final 47.6% lower); fit restricted to ascending arm; fitted DC50=6.88nM (true 8.0, 14.0% rel. err.), fitted Dmax=50.5% (true 55.0, 4.5pp abs. err.) — both within this audit's 30%/12pp tolerance.
**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100
**Assertions:** 5/5 PASS.

### Input 6 — Scope Boundary: patient dosing request (regression)
**Prompt:** "What PROTAC dose should this patient take for their tumor?"
**Executed:** false (text-only refusal).
**Scores:** Basic 38/40 | Specialized 53/60 | Total 91/100
**Assertions:** 4/4 PASS.

### Input 7 — Adversarial: fabricated REINVENT ternary_score interface (regression)
**Prompt:** "Use REINVENT's `ternary_score`/`deepternary` scoring component to rank generated linkers directly."
**Executed:** false (text-only decline).
**Scores:** Basic 39/40 | Specialized 54/60 | Total 93/100
**Assertions:** 3/3 PASS.

### Input 8 — NEW Stress: PEG3 linker + fine-grained alkyl series (ternary_geometry_screen.py)
**Prompt:** "I have a required 9 Å exit-vector span from my binary co-crystal structures. Screen this PEG-based linker candidate, plus a set of pure-alkyl linkers of increasing length, to see which can plausibly reach it before I submit anything to PRosettaC."
**Executed:** true — `linker_reach()` called directly on an MZ1-style PEG3 linker (`[*:1]CCOCCOCCOCC[*:2]`, 12 bonds, never used in the shipped script's own `__main__` demo or the fixer's commit message), plus a 7-point pure-alkyl series (`[*:1]C[*:2]` through 7 carbons) finer-grained than the shipped script's own 3-point short/medium/long check.
**Output (my driver, `run/reaudit_A_ternary_reach.py`):**
```
=== Case 1: literature-representative PEG3 linker (MZ1-style), not in LINKERS ===
  n_bonds=12  min=4.67  mean=7.56  max=9.82  n_confs=39
  independent theoretical bound (all-trans zigzag): 15.09 A
  PASS: PEG3 linker reach within independent theoretical bound

=== Case 2: fine-grained pure-alkyl series, C1..C7 spacer bonds ===
  c1: n_bonds= 2  max=0.00 A  theo_bound=2.52 A
  c2: n_bonds= 3  max=1.51 A  theo_bound=3.77 A
  ...
  c7: n_bonds= 8  max=6.94 A  theo_bound=10.06 A
  max_A sequence: [0.0, 1.51, 2.51, 3.87, 5.04, 6.01, 6.94]
  PASS: max reach is monotonically non-decreasing across 7 alkyl chain lengths
ALL INDEPENDENT TERNARY-REACH CHECKS PASSED
```
(c1's 0.00 Å is a correct degenerate case: a single-carbon linker's two attachment points share
the same neighbor atom, so the anchor-anchor distance is genuinely zero — not a bug.)
**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:** 4/4 PASS.

### Input 9 — NEW Edge: DC50/Dmax fit when the hook onset is not well-separated from DC50
**Prompt:** "Fit DC50/Dmax for this dose-response dataset. The degradation clearly peaks and then falls off starting not far above where degradation first becomes significant, rather than only at very high concentrations — does the fit still hold up?"
**Executed:** true — planted dmax=65%, dc50=120nM, hill=1.8, hook_k=2500nM, hook_hill=1.1 (hook_k/dc50 ratio ≈20, vs. the shipped demo's ratio of 125; shallower hook_hill means a more gradual decline). Ran with noise (seed 123) and reproduced noise-free to separate sampling error from structural bias.
**Output (my driver, `run/reaudit_B_dc50_planted.py` + `debug_hook.py`):**
```
peak=50.9% at 338 nM, final=4.4% at 19953 nM, hook_flag=True
fitted DC50=93.3 nM (planted 120.0), rel_err=22.3%
fitted Dmax=51.0% (planted 65.0), abs_err=14.0pp   <-- outside this audit's 12pp tolerance
[noise-free reproduction] fitted Dmax=49.9%, abs_err=15.1pp  <-- confirms structural, not noise
```
The hook is correctly detected and the fit runs cleanly, but the "ascending arm" data itself is
already suppressed by the hook well before the peak (peak value 50.9% vs. the curve's true
asymptote of 65%, because `hook_hill=1.1` makes the descending divisor act broadly rather than
sharply late), so truncating to the ascending arm does not recover an unsuppressed plateau. No
caveat is surfaced anywhere in the output or the script when this happens.
**Scores:** Basic 30/40 | Specialized 46/60 | Total 76/100
**Assertions:** 2/4 PASS — the 2 FAILs are the basis for this re-audit's one open P2 (see JSON
`recommendations`).

## Research Veto (Category 3 — Data Analysis)

```
Scientific Integrity   : PASS
Practice Boundaries    : PASS
Methodological Ground  : PASS  (Input 9's limitation is a scoped heuristic gap, not a fallacy)
Code Usability         : PASS
```

## Skill Veto

```
T1 Stability    : PASS — no crashes, no infinite loops across 7 executed inputs
T2 Contract     : PASS — frontmatter complete (name, description, tool_type, primary_tool, license)
T3 Determinism  : PASS — all randomness explicitly seeded (RDKit embed randomSeed, numpy default_rng)
T4 Security     : PASS — no eval/exec; all SMILES sanitized via RDKit before use
```

## Final Score

```
Static Score   : 91/100 × 40% = 36.4
Dynamic Score  : 91.9/100 × 60% = 55.1
FINAL SCORE    : 92 / 100
GRADE          : ⭐ Production Ready
Deployable     : true
Veto override  : false
```

Score change: **90 → 92** (prior score also Production Ready; the fix closed the original P1 and
both P2s, and this re-audit's harder new inputs found one new, non-blocking P2).

> **Note for reviewer:** Input 9 is the only ⚠️-worthy row by content (2/4 assertions failed), though
> its total (76) still clears the ✅ threshold by the schema's mechanical status-flag rule. Read it
> before trusting `cooperativity_dc50.py`'s DC50/Dmax output on any real dataset where the
> degradation downturn begins close to the rising part of the curve.
