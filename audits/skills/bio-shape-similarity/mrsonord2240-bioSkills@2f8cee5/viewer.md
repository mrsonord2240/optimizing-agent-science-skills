> **Audit record for `bio-shape-similarity`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@2f8cee5](https://github.com/mrsonord2240/bioSkills/tree/2f8cee570c21b48f08e0b15b1662c6d363bbf09b/chemoinformatics/shape-similarity) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-shape-similarity

## Canonical final summary

**Final:** 92/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@2f8cee570c21b48f08e0b15b1662c6d363bbf09b:chemoinformatics/shape-similarity`

Final-pass metadata: `auditor_independent: false` — final pass: fixed and audited under one brief, see CHECKPOINT.md.

## Summary

| Input | Type | Executed | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical USRCAT + O3A | true | 37 | 55 | 92 | 4/4 | ✅ |
| 2 | Variant A calibration | true | 33 | 50 | 83 | 3/3 | ✅ |
| 3 | Edge malformed/salt library | true | 38 | 55 | 93 | 4/4 | ✅ |
| 4 | Variant B ensemble regression | true | 38 | 56 | 94 | 4/4 | ✅ |
| 5 | Stress multi-stage pipeline | true | 36 | 55 | 91 | 3/3 | ✅ |
| 6 | Scope boundary ShaEP | true | 38 | 56 | 94 | 3/3 | ✅ |
| 7 | Adversarial score semantics | false | 36 | 52 | 88 | 4/4 | ✅ |

Execution average: **90.7 / 100**. Assertion pass rate: **25/25**.

Static score: **95 / 100**. Final score: **92 / 100 — ⭐ Production Ready**. Both veto gates passed; deployable is `true`.

## Regression execution

All current-source CLI work was run from `run/phase2_run_source_cli.ps1`, which retains its input files and assertions.

### Input 1 — Canonical

`run/input1_canonical.py` ran twice with seed 42. The identical query ranked first at USRCAT `1.0000`; top-five normalized shape scores were `1.0000, 0.7614, 0.5593, 0.3792, 0.4741`. The driver asserted the range and printed `Determinism check ... True`.

### Input 2 — Variant A calibration

`run/input2_scaffold_hop.py` produced labeled-reference shape values `0.620, 0.838` for its true hops and `0.211, 0.533, 0.575` for non-hops. Its simple derivation selected shape `0.598` and ECFP4 `0.275`, then returned zero candidates because its listed true hop had ECFP4 `0.514`. The run is valid evidence that a calibration feasibility check would help; it is not evidence for a universal replacement cutoff.

### Input 3 — Edge

The archived copied driver is not evidence for the current source. The current source CLI instead ran a library containing `C1CC(this`, `[Fe+2].[Cl-].[Cl-]`, and a valid control:

```text
WARNING: unparsable SMILES skipped: C1CC(this malformed
WARNING: 1 library molecule(s) produced no usable conformer and were dropped:
  [Cl-].[Cl-].[Fe+2]: disconnected fragments (salt/multi-component); no single shape to compare
... shape=0.656
```

### Input 4 — Variant B ensemble regression

The source CLI reran the original three-molecule library with `--n-conf 20 --seed 42`:

```text
WARNING: ...F...: 1/20 conformers failed MMFF convergence; scoring the remaining 19
WARNING: ...sulfonamide...: 4/20 conformers failed MMFF convergence; scoring the remaining 16
... shape=0.656
... shape=0.572
CCCCCCCC  shape=0.484
```

Thus 3/3 valid molecules were scored, whereas the pre-fix report documented silent omission.

### Input 5 — Stress

`run/input5_stress.py` embedded all 15 synthetic library entries, retained the top eight USRCAT candidates, aligned them with O3A, calculated ECFP4, and emitted a quadrant for each. The identical query was `close analog` at `shape=1.000, ecfp4=1.000`; the sulfonamide entry was reported as `different sampled shape` at `0.379, 0.514`.

### Input 6 — ShaEP

`run/phase2_shaep_e2e.ps1` used the current documented Open Babel conversion and exact ShaEP invocation. It created fresh mol2 files and a fresh similarity output:

```text
molecule  best_similarity  shape_similarity  ESP_similarity
UNTITLED  0.911822         0.998945          0.824699
```

The script asserts artifact existence and both named columns.

### Input 7 — Adversarial

No program execution applies (`executed: false`). The current Skill directly says the 0.7/0.5 values are repository starting defaults requiring task-relevant calibration, and its Common Errors table says normalized shape Tanimoto is 0–1. A claimed normalized score of `1.4` must therefore be a mislabeled O3A or TanimotoCombo value, not accepted as a valid shape Tanimoto.

## Fresh supplemental inputs

Every supplemental input was executed and is recorded in the JSON report.

- Fresh ordinary drug salt: current source rejected diphenhydramine hydrochloride with the disconnected-fragment reason while scoring the single-fragment control.
- Fresh disconnected query: current source rejected `[Na+].[Cl-]` before embedding with `query must be one valid connected SMILES`.
- Fresh ESPSim pair: `run/reaudit_espsim.py`, using the isolated ESPSim venv, reported shape `0.9352`, default Carbo ESP `0.8496`, and `renormalize=True` ESP `0.9052`; its range checks passed.

## Veto and recommendation

- Skill Veto T1–T4: PASS.
- Research Veto M1–M4: PASS.
- P2: add a calibration feasibility/overlap check so an inseparable labeled reference set is reported as such instead of inviting an unjustified single cutoff.

## Reproducibility artifacts

All executed drivers and input files are under [`run/`](run/), including the report arithmetic/schema validator, current-source CLI regression runner, fresh libraries, current-source example runner, and ShaEP end-to-end runner.
