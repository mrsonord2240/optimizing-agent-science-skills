> **Audit record for `bio-single-cell-trajectory-inference`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@e8cf78a](https://github.com/mrsonord2240/bioSkills/tree/e8cf78a7ddb739b108b4a8789e042230aa09911c/single-cell/trajectory-inference) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-trajectory-inference (RE-AUDIT)
Generated: 2026-09-19

Source: `mrsonord2240/bioSkills@e8cf78a:single-cell/trajectory-inference`
Prior audit: `F:\OpenScience\audits\_pre-fix-20260919\bio-single-cell-trajectory-inference\` (84, Beta Only, not deployable)
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-single-cell-trajectory-inference.md`
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Complex (N=9 -- 7 regression + 2 new)

This is an independent re-audit: fresh scripts (not copies of the original auditor's or the
fixer's), fresh real-data runs, and an independent investigation of the fixer's central claim
that scVelo's `dynamical`/`stochastic` modes are unfixable from the call site.

Real data used: `sc.datasets.paul15()` (2730 cells, real hematopoietic progenitor data),
`scv.datasets.pancreas()`-cached real pancreatic endocrinogenesis data (3696 cells), and the
corpus's real 10x PBMC 1k v3 filtered matrix (mature/discrete cell types). See `data/README.md`
for where these cached files are preserved (not duplicated here -- see that file).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 36 | 55 | 91 | 4/4 PASS | ✅ |
| 2 | Variant A (regression) | 36 | 55 | 91 | 3/3 PASS | ✅ |
| 3 | Edge (regression) | 33 | 51 | 84 | 3/3 PASS | ✅ |
| 4 | Variant B -- scVelo (regression) | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 5 | Stress -- Slingshot/tradeSeq (regression) | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 6 | Scope Boundary -- CellRank (regression) | 35 | 53 | 88 | 3/4 PASS | ✅ |
| 7 | Adversarial (regression) | 39 | 56 | 95 | 5/5 PASS | ✅ |
| A | New -- root sensitivity (Governing Principle rule 3) | 37 | 54 | 91 | 3/3 PASS | ✅ |
| B | New -- CellRank VelocityKernel + deterministic velocity | 34 | 51 | 85 | 3/3 PASS | ✅ |

**Execution Average: 90.3 / 100**
**Assertion Pass Rate: 32/33 (97.0%)**

**Static Score: 94/100** | **Final Score: 37.6 + 54.2 = 92** (Static x 0.4 + Execution x 0.6)

**Grade: ⭐ Production Ready.** All floors met (Static ≥80, Execution ≥85, Layer1 avg 36.2 ≥32,
Layer2 avg 54.1 ≥48, assertion pass rate 97.0% ≥90%). No veto fired (Skill Veto PASS, Research
Veto PASS). `deployable: true`.

> **Note for reviewer:** Inputs 4 and 6 are where the original P1s lived -- both independently
> re-verified end-to-end. Input B is new coverage (CellRank's VelocityKernel, not exercised by
> the original audit or the fix) and surfaces a real, non-blocking observation: deterministic-
> mode velocity gives CellRank much weaker fate-probability discrimination than pseudotime-based
> kernels -- expected, given deterministic is the Skill's own "least recommended" fallback, but
> not currently called out in the CellRank section.

---

## Detailed Outputs

### Input 1 — Canonical: PAGA continuum test + DPT rooted on a known marker (regression)

Fresh script (`run/regress_1_2_3.py`), real Paul15 data, SKILL.md's PAGA + DPT blocks
(unchanged by the fix) run verbatim.

```
MEP mean pseudotime: 0.0332, mature mean: 0.3790
ASSERTION mep_lower_than_mature: True
```

Matches the original audit's numbers closely (MEP 0.033 vs mature 0.173-0.379 range).

Assertions:
- [PASS] PAGA shows Paul15 as one connected continuum, consistent with known biology.
- [PASS] Root anchored on a real MEP marker cell, not chosen by eye.
- [PASS] Mean DPT pseudotime lower in MEP progenitor pool than in mature labels (0.033 vs 0.379).
- [PASS] DPT pseudotime monotonic along the real erythroid maturation series (0.587 -> 0.099).

### Input 2 — Variant A: Palantir fate probabilities + entropy (regression)

```
Palantir entropy MEP: 0.6995, mature: 0.0599
ASSERTION entropy_falls_with_commitment: True
Terminal states auto-detected: 3
```

Matches the original (entropy 0.567->0.017 there; same direction and magnitude, small
differences from a different num_waypoints setting).

Assertions:
- [PASS] Palantir code runs exactly as documented against installed palantir 1.4.5.
- [PASS] Fate-probability entropy falls from progenitor pool to committed/mature cells.
- [PASS] Auto-detected terminal states (3) consistent with known branch structure.

### Input 3 — Edge: PAGA continuum-vs-discrete on real PBMC 1k (regression, caveat re-tested)

```
15 leiden clusters on real discrete PBMC data
Isolated at threshold=0.03: 0 / 15
Isolated at threshold=0.5: 3 / 15
Median nonzero connectivity: 0.2574
```

Independently reproduces the original finding almost exactly (original: 0/15 at 0.03, 1/15 at
0.5, median 0.29). The underlying algorithmic limitation is unchanged -- a single fixed
threshold still does not flag PBMC's known-discrete types. What changed is that SKILL.md now
explicitly warns against relying on threshold isolation alone ("Sweep the threshold and inspect
the connectivity value distribution... treat PAGA connectivity as one input... not a standalone
automatic test") and the matching Common Errors row says the same. Re-scored the assertion
against this corrected claim rather than the old (now-withdrawn) claim that a single threshold
suffices.

Assertions:
- [PASS] PAGA code executes without error on real discrete PBMC data.
- [PASS] SKILL.md no longer claims a single fixed threshold is a sufficient continuum-vs-discrete
  test; it explicitly prescribes sweeping the threshold and corroborating with marker identity,
  matching the real behavior observed (0/15 isolated at 0.03).
- [PASS] No forced trajectory ordering is asserted when continuum status is doubtful.

### Input 4 — Variant B: scVelo RNA velocity, deterministic mode, real pancreatic data (regression, P1 fix)

Fresh script (`run/regress_4_scvelo.py`) transcribes the FIXED SKILL.md's RNA Velocity block
verbatim and runs it end-to-end against real `pancreas_raw.h5ad`.

```
EXIT OK, adata shape: (3696, 2000)
mean velocity_confidence: 0.7126

Mean velocity_pseudotime per cluster:
Ductal           0.130069
Ngn3 low EP      0.186903
Ngn3 high EP     0.664244
Epsilon          0.904085
Delta            0.905012
Pre-endocrine    0.916255
Alpha            0.927412
Beta             0.959022
ASSERTION ductal_is_low: True
```

Perfectly monotone, matches the fixer's and original audit's numbers almost exactly.

**Independent verification of the "unfixable from the call site" claim (see
`run/repro_scvelo_bugs.py`, `repro2_align_dynamics.py`, `repro3_full_monkeypatch.py`):**

- Bug 1 (`mode='dynamical'` -> `recover_dynamics` -> `make_unique_list`): independently
  reproduced fresh, identical `TypeError: unique requires a Series, Index, ExtensionArray,
  np.ndarray or NumpyExtensionArray got list` -- pandas 3.x's `pandas.unique` no longer accepts
  plain lists. Confirmed real.
- Bug 2 (`align_dynamics` "assignment destination is read-only"): independently reproduced, and
  root-caused one level deeper than the fix log: `scvelo.tools._em_model_core._read_pars()` does
  `adata.var[pkey].values`, and pandas 3.x's always-on Copy-on-Write returns a **read-only**
  ndarray from that `.values` call. Confirmed real, and NOT specific to `adata.layers`
  writability (tested: forcing every layer/X writable first does not help, since the read-only
  array comes from `adata.var`, not `adata.layers`).
- New finding beyond the fix log: a **private-internals monkeypatch** (patching
  `pandas.unique` AND `scvelo.tools._em_model_core._read_pars` from the calling script, no edits
  to scvelo's shipped files) DOES get `recover_dynamics()` itself to complete
  (`repro3_full_monkeypatch.py`: "recover_dynamics SUCCEEDED with the dual monkeypatch").
  However, the actual reason to use `mode='dynamical'` -- `scv.tl.latent_time()` -- internally
  calls `velocity_graph(adata, approx=True)` -> `velocity(adata, ...)`, which re-enters the
  **default `mode='stochastic'` path** and hits the third, independent bug
  (`leastsq_generalized` -> `TypeError: only 0-dimensional arrays can be converted to Python
  scalars` -> `ValueError: setting an array element with a sequence`, inside
  `np.linalg.pinv`'s handling of a degenerate 1x1 matrix under numpy>=2). This bug lives inside
  numpy's own linear-algebra internals, not scvelo's; patching it safely from a Skill-level
  workaround is not realistic (it would mean globally monkeypatching `numpy.linalg.pinv`, which
  risks silently corrupting unrelated numeric results across the whole process).
  **Conclusion: the fixer's practical guidance is correct** -- there is no usable end-to-end path
  to `mode='dynamical'`/`latent_time` on this stack, even accounting for a more aggressive
  monkeypatch than the fix log describes. `mode='deterministic'` + `velocity_pseudotime` remains
  the only fully-working, honestly-documented path, and the compatibility note is accurate.
- Bug 3 (`mode='stochastic'`, library default): independently reproduced, identical
  `TypeError`/`ValueError` chain inside `leastsq_generalized`. Confirmed real and confirmed
  unfixable from the call site (see above).

Assertions:
- [PASS] `scv.pp.filter_and_normalize` + separate `sc.pp.highly_variable_genes` HVG step runs
  exactly as documented (no `n_top_genes` TypeError).
- [PASS] `mode='deterministic'` is clearly documented as the working path, with an accurate
  compatibility note naming the real, independently-confirmed failures in the other two modes.
- [PASS] The claim that `mode='dynamical'`/`'stochastic'` are not fixable from the call site
  holds up under independent, deeper investigation (see above) -- a defensible "document the
  limitation" fix, not a fixer giving up early.
- [PASS] Resulting pseudotime/velocity ordering matches the real known progenitor-to-terminal
  direction (Ductal 0.13 -> ... -> terminal ~0.90-0.96).

### Input 5 — Stress: Slingshot + tradeSeq (regression, P2 fix independently re-run)

Fresh R script (`run/regress_5_slingshot_tradeseq.R`) via `tools/rs.sh`.

```
number of lineages detected: 5
MEP mean pseudotime on lineage 1: 1.192463
ASSERTION mep_near_start_of_lineage1 (< 0.3 of max): TRUE
scaled/clustering matrix min value (expect negative): -8.519676
fitGAM on scaled matrix: FAILED as expected: All values of the count matrix should be non-negative
tradeSeq associationTest: 40 / 300 genes significant at p<0.05
ASSERTION tradeseq_ran_on_raw_counts: TRUE
```

The fix log noted this caveat was "not independently re-run" (textual only); this re-audit is
the first to independently confirm both halves: the scaled-matrix failure the caveat warns
about, and that raw counts fix it (40/300 here vs 46/300 in the original -- consistent, small
difference from a different random gene sample).

Assertions:
- [PASS] Slingshot runs exactly as documented, multiple lineages consistent with known branching (5 lineages, MEP near origin).
- [PASS] SKILL.md now explicitly states `fitGAM` needs raw counts, distinct from the scaled clustering matrix -- confirmed both halves of this claim hold on real data.
- [PASS] Given raw counts, tradeSeq's `associationTest` yields a sensible, non-degenerate fraction of significant genes (40/300, ~13%).
- [PASS] MEP progenitor mean pseudotime near the minimum of its lineage.

### Input 6 — Scope Boundary: CellRank 2 directed fate mapping (regression, P1 fix)

Fresh script (`run/regress_6_cellrank.py`), transcribed verbatim from the fixed SKILL.md's
CellRank block, run in the isolated `cellrank-venv` (cellrank 2.3.3) against real Paul15
branching data with `allow_overlap=True`.

```
initial_states: ['3_1']
Mean fate-probability entropy MEP: 1.7858, mature: 0.8189
ASSERTION fate_entropy_falls_with_commitment: True
SUCCESS: no RuntimeError, no ValueError
```

Matches the original's captured numbers (1.786 -> 0.819) almost exactly. No `RuntimeError`, no
`ValueError` -- both original P1 defects (overlap ValueError, Windows bootstrapping
RuntimeError) are confirmed gone.

Assertions:
- [PASS] `PseudotimeKernel`+`ConnectivityKernel`+GPCCA macrostates run exactly as documented.
- [PASS] `predict_initial_states(n_states=1, allow_overlap=True)` runs on real branching data without the original `ValueError` (30 overlapping cells) -- the fix (`allow_overlap=True`) is now inline in the code block itself, not just a note.
- [PASS] Fate-probability entropy falls from the progenitor pool to committed/mature cells (1.79 -> 0.82).
- [FAIL] The documented code *fence* is still not self-contained: it carries a comment
  instructing the agent to wrap it in `if __name__ == '__main__':`, but the fence itself is not
  wrapped, so a literal copy-paste into a bare `.py` file still crashes until the agent applies
  the guard manually. Minor -- the requirement is now correctly and clearly documented (this
  re-audit's own `regress_6_cellrank.py`, written by following that documentation, worked on the
  first try) -- but it is not a truly copy-paste-safe snippet. See P2 recommendation.

### Input 7 — Adversarial: velocity-confidence over-trust trap (regression, unchanged content)

Content unchanged by the fix (confirmed by diff: only the RNA Velocity/CellRank/PAGA/tradeSeq
sections and Installation/usage-guide changed). Original assertions re-verified by inspection
against the current SKILL.md text -- all three cited passages (Bergen 2021 mature-tissue
caution, Common Errors "high confidence, wrong arrows" row citing Zheng 2023, "clean stream plot
can manufacture coherence") are still present and unchanged.

Assertions: 5/5 PASS (unchanged from original; see prior report for full text).

### Input A — NEW: root-sensitivity test (Governing Principle rule 3)

Not in the original 7 inputs, not separately verified by the fixer. Tests the Skill's explicit
claim ("Root-cell choice flips every gene trend... the sign of every trend and which cells are
'early' invert with the root") empirically, on real Paul15 data, by running DPT from the correct
MEP-anchored root vs. a deliberately wrong root (a mature `16Neu` cell).

```
Correlation between MEP-rooted and Neu-rooted pseudotime: 0.7214
ASSERTION root_choice_materially_changes_ordering (|corr| < 0.9): True
MEP-rooted: MEP mean pt = 0.0332  Neu mean pt = 0.2920
Neu-rooted: MEP mean pt = 0.2350  Neu mean pt = 0.0775
ASSERTION early_vs_late_label_inverts_with_root: True
```

The "early"/"late" label genuinely flips (MEP goes from lowest to highest mean pseudotime when
the root changes), strongly validating the Skill's own stated rule rather than just asserting it.

Assertions:
- [PASS] Root choice materially changes the resulting pseudotime ordering (correlation 0.72, well below a same-ordering threshold).
- [PASS] The early-vs-late label assignment genuinely inverts between the two roots, exactly as the Governing Principle's rule 3 claims.
- [PASS] SKILL.md's guidance to anchor the root with orthogonal evidence (not by eye) is the correct mitigation for this real, empirically-confirmed sensitivity.

### Input B — NEW: CellRank VelocityKernel + deterministic-mode velocity (real pancreatic data)

Not in the original 7 inputs (which only exercised `PseudotimeKernel`), not separately verified
by the fixer. Tests whether the mode='deterministic' velocity graph the fix relies on is
actually usable downstream by CellRank's `VelocityKernel` -- a different, documented code path
("Velocity only when trustworthy" in the Kernel-decoupling paragraph).

```
macrostates: ['Delta', 'Epsilon', 'Ductal_1', 'Ductal_2', 'Ngn3 low EP', 'Alpha', 'Ductal_3', 'Beta']
terminal_states: ['Delta', 'Alpha', 'Beta']
initial_states: ['Ductal_2']
Mean fate-probability entropy Ductal (progenitor): 0.3601, Alpha/Beta (terminal): 0.3174
ASSERTION ductal_entropy_higher_than_terminal: True
SUCCESS: VelocityKernel + deterministic-mode velocity ran end-to-end through CellRank
```

Ran cleanly end-to-end; macrostates and terminal states are biologically correct (Delta/Alpha/
Beta are real terminal endocrine fates; Ductal is the real progenitor and is correctly identified
as an initial state). The entropy separation (0.36 vs 0.32) is real but much weaker than the
PseudotimeKernel route in Input 6 (1.79 vs 0.82) -- expected, since deterministic is the Skill's
own "least recommended... quick first pass" mode, but this is not currently called out as a
caveat in the CellRank section. See P2 recommendation.

Assertions:
- [PASS] `VelocityKernel` combined with `ConnectivityKernel` and GPCCA runs end-to-end on the fixed deterministic-mode velocity graph with no crash.
- [PASS] Terminal states (Delta, Alpha, Beta) and initial state (Ductal) are biologically correct.
- [PASS] Fate-probability entropy is higher in the progenitor pool than in terminal cells, consistent with lineage commitment, though the margin is small (documented as a finding, not a failure).
