> **Audit record for `bio-conformer-generation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@82ca4e9](https://github.com/mrsonord2240/bioSkills/tree/82ca4e996c8149725569183a338cdd28f44f8268/chemoinformatics/conformer-generation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-conformer-generation (final pass)

Evaluated 2026-09-24 with `skill-auditor@1.0`.

Source: `mrsonord2240/bioSkills@82ca4e996c8149725569183a338cdd28f44f8268:chemoinformatics/conformer-generation`.

This is a final-pass combined fix and audit. `auditor_independent: false`; final-pass note: `fixed and audited under one brief, see CHECKPOINT.md`.
It supersedes the 2026-09-19 c4e2ccd re-audit (90/100, Limited Release), which is preserved at
`F:\OpenScience\audits\_pre-fix-20260924\bio-conformer-generation`.

## What changed before this audit

- Empty-string SMILES now follows the same explicit `Invalid SMILES` validation path as malformed SMILES.
- Empty/mismatched energy vectors and invalid Boltzmann inputs have clear contracts rather than raw `min()` errors or silent truncation.
- The macrocycle statement now reflects RDKit 2026.03.6: `ETKDGv3()` already sets `useMacrocycleTorsions=True`; a new packaged comparison reports default versus explicit opt-out for a chosen molecule without asserting universal benefit.
- `examples/gen_conformers.py` now uses the same validation and `(mol, ids)` macrocycle return contract as the inline workflow.

## Runtime and evidence

Environment: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\python.exe`, Python 3.12, RDKit 2026.03.6, NumPy 2.5.3, xTB 6.7.1.

Every Python fence in `SKILL.md` was extracted, compiled, and executed in documented order by
[`run/final_regression_audit.py`](run/final_regression_audit.py). The script reran all nine logical
inputs from the archived c4e2ccd audit and added two fresh packaged-example/edge inputs. Its machine-readable
output is [`run/final_regression_result.json`](run/final_regression_result.json).

| # | Input | Evidence checked | Result |
|---|---|---|---|
| 1 | Aspirin canonical ensemble (regression) | 20/20 embedded and MMFF94s-converged; 18.9098–20.8331 kcal/mol | PASS |
| 2 | Ibuprofen single docking conformer (regression) | Optimized SDF round-trip retained non-planar 3D coordinates | PASS |
| 3 | Phenylboronic acid MMFF gap (regression) | 10/10 UFF fallback results; 11.4524–11.4747 kcal/mol | PASS |
| 4 | 14-membered macrocycle (regression) | Ring size 14; 10/10 macrocycle path conformers; current default flag verified true | PASS |
| 5 | Flexible imatinib pipeline (regression) | 7 rotors -> 45 conformers -> 43 RMSD-pruned -> 38 energy-windowed; Boltzmann asphericity 0.43156 | PASS |
| 6 | Windows CREST boundary (regression) | Expected `FileNotFoundError`; standalone xTB returned 0 and wrote `xtbopt.xyz` | PASS |
| 7 | Malformed/empty SMILES and determinism (regression) | Three explicit ValueErrors; seed 7 repeats; seed 99 differs | PASS |
| 8 | Fe-containing disconnected input (regression) | 5 conformers; actual MMFF94s selection recorded; no coordination-validity overclaim | PASS |
| 9 | Empty/mismatched helper inputs (regression) | Empty filter `[]`; clear mismatch/non-finite errors; uniform equal-energy weights | PASS |
| 10 | Packaged `gen_conformers.py` (fresh) | Valid ensemble, `(mol, ids)` macrocycle return, empty-SMILES ValueError | PASS |
| 11 | Packaged macrocycle comparison (fresh) | Parseable JSON for both settings; invalid `--n-conf 0` rejected | PASS |

### Selected output from the final harness

```text
passed=11/11
input 5: rotatable_bonds=7, requested=45, embedded=45,
         rmsd_kept=43, energy_window_kept=38, boltzmann_asphericity=0.4315623505
input 6: crest_exception=[WinError 2] The system cannot find the file specified,
         xtb_returncode=0, xtbopt=run/xtbopt.xyz
input 7: Invalid SMILES: 'Xyz[[[invalid'; Invalid SMILES: 'c1ccccc1((('; Invalid SMILES: ''
input 11: default embedded/scored=5/5; opt-out embedded/scored=5/5
```

The macrocycle comparison is intentionally not scored as evidence that either setting is universally superior:
it is a runnable applicability diagnostic. The default and opt-out lactam ensembles each embedded and scored
five conformers, with respectively 43.3680–48.7216 and 44.1178–47.4689 kcal/mol MMFF94s ranges.

## Vetoes and scoring

- Skill veto: PASS — stable, contract-consistent, seeded/deterministic, and no shell injection or credential path.
- Research veto: PASS — all values are live RDKit/xTB outputs; no clinical scope; caveats prohibit treating force-field ensembles as definitive populations or coordination validation.
- Static: 97/100.
- Execution: 93.9/100; assertions 44/44.
- Final: `97 × 0.4 + 93.9 × 0.6 = 95.1`, rounded to **95/100**.

**Grade: ⭐ Production Ready.** `deployable: true`; no veto and no open P0, P1, or P2 recommendations.

## Reproducibility commands

```powershell
$py = 'F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\python.exe'
& $py F:\OpenScience\audits\bio-conformer-generation\run\final_regression_audit.py `
  --skill-dir F:\OpenScience\worktrees\bio-conformer-generation-finalpass\chemoinformatics\conformer-generation `
  --out F:\OpenScience\audits\bio-conformer-generation\run\final_regression_result.json
```

The command checks output content and fails nonzero unless every input passes; it is not an exit-code-only audit.
