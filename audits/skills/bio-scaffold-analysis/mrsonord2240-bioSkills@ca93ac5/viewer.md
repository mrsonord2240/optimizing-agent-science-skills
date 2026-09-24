> **Audit record for `bio-scaffold-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@ca93ac5](https://github.com/mrsonord2240/bioSkills/tree/ca93ac599c17ee0c898c2a443777a60ebcd96177/chemoinformatics/scaffold-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0 exact-commit focused re-audit.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-scaffold-analysis

Re-audited 2026-09-24 against exact clean commit `ca93ac599c17ee0c898c2a443777a60ebcd96177` in `agent/fix-bio-scaffold-analysis`, based on `main` at `80118b2aa7a282506e2661ce9c8bc8a810d0a1fb`.

The pre-fix report and viewer are preserved under `re-audit-20260924/pre-fix/`. This viewer replaces the former canonical release assessment.

## Result

| Measure | Pre-fix | Re-audit |
|---|---:|---:|
| Static score | 91.0 | 95.0 |
| Execution average | 86.9 | 92.1 |
| Assertions | 24/30 | 30/30 |
| Final score | 88/100 | **93/100** |
| Grade | Limited Release | **Production Ready** |
| Open P0 / P1 / P2 | 0 / 2 / 2 | **0 / 0 / 0** |

Structural vetoes remain clear: stability, contract, determinism, and security all pass. The source worktree was clean and at the exact commit named above during focused execution.

## Re-executed assertions

The 24 assertions that passed in the earlier audit concern unchanged code or instructions and remain carried forward. The six prior failures were checked against the exact final commit; all now pass.

### Scaffold split

The splitter now assigns each next scaffold group to the less-filled partition, then uses singleton groups to reach an exact requested size where possible. It never splits a scaffold and exposes diagnostics only when requested (`return_diagnostics=True`).

| Requested train fraction | Train / test | Achieved | Scaffold overlap | Test singleton fraction |
|---:|---:|---:|---:|---:|
| 0.8 | 1200 / 300 | 0.800 | 0 | 0.407 |
| 0.7 | 1050 / 450 | 0.700 | 0 | 0.407 |
| 0.9 | 1350 / 150 | 0.900 | 0 | 0.400 |

These checks used the audited 1,500-compound MMPA fixture. A same-seed rerun produced identical partitions. This closes the prior all-singleton test-set pathology without claiming label balance; the Skill still directs users to audit endpoint balance or use a validated group-aware stratification approach when required.

### MMPA recipe and output contract

The documented sequence now includes:

```bash
mmpdb fragment data.smi -o data.fragments
mmpdb index data.fragments -o data.mmpdb
mmpdb loadprops -p props.tsv data.mmpdb
mmpdb transform --smiles 'COc1ccccc1' --property pIC50 data.mmpdb
```

The focused mmpdb 3.1.4 check loaded 1,064 pIC50 records and returned 135 transform rows. Its header contains `pIC50_count`, `pIC50_avg`, `pIC50_std`, `pIC50_paired_t`, and `pIC50_p_value`; the Skill correctly says results are tool-ordered, must be sorted explicitly, and contain no confidence column.

### Worked representation example and scope warning

The published worked strings now exactly match RDKit 2026.03.6 output:

```text
Bemis-Murcko: O=C(NCC1CCCC1)c1ccccc1
Generic:      CC(CCC1CCCC1)C1CCCCC1
```

The taxonomy also makes the generic-framework loss concrete without universalizing it: the reference 1,500-compound hERG library collapsed from 857 Bemis-Murcko scaffolds to 583 generic frameworks (1.47-fold fewer groups), and its largest generic framework covered four Bemis-Murcko scaffolds.

## Evidence

- Split, determinism, and canonical-string assertions: `re-audit-20260924/run-focused/scaffold_validation.out`
- MMPA property import: `re-audit-20260924/run-focused/loadprops.out`
- MMPA transform header and rows: `re-audit-20260924/run-focused/transform.out`
- Exact-commit documentation and output cross-check: `re-audit-20260924/run-focused/mmpdb_validation.out`

No P0, P1, or P2 findings remain.
