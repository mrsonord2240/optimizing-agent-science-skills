> **Audit record for `bio-molecular-standardization`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@5fcd1a1](https://github.com/mrsonord2240/bioSkills/tree/5fcd1a11abb2c0aad63845773334160c287a1d1a/chemoinformatics/molecular-standardization) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Re-audit Viewer — bio-molecular-standardization

Generated: 2026-09-24
Exact source: mrsonord2240/bioSkills@5fcd1a11abb2c0aad63845773334160c287a1d1a:chemoinformatics/molecular-standardization
Branch/worktree: agent/fix-bio-molecular-standardization / F:\OpenScience\worktrees\bio-molecular-standardization-fixpass
Environment: F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\python.exe — RDKit 2026.03.6, chembl_structure_pipeline 1.2.4, pandas 3.0.5
Evidence: run/reaudit_fixed_findings.py/.out and exact-current-runtime
run/input3_reaudit.out plus run/input4_reaudit.out

## Result

| Measure | Result |
|---|---:|
| Static score | 96 / 100 |
| Execution average | 96.4 / 100 |
| Assertions | 24 / 24 PASS |
| Skill veto | PASS |
| Research veto | PASS |
| Final | **96 / 100 — Production Ready** |
| Open P0/P1/P2 findings | **0** |

## Exact-commit execution

The re-audit imported the bundled examples/standardize_library.py directly from
commit 5fcd1a1, not a copied implementation. It exited 0 and passed:

~~~text
PASS commit=5fcd1a1 all 5 former P1/P2 findings closed
status_counts={'parse_failure': 1, 'excluded_by_chembl': 0,
  'multi_fragment_parent': 1, 'ok_largest_fragment_fallback': 0,
  'standardize_error': 0, 'inorganic_no_carbon': 0, 'ok': 2}
hERG rows=3966 unique=3208 replicated=379 range_flags=47 max_range=3.69
exit_code=0
~~~

The 3,966-row ChEMBL hERG fixture retained the original 3,208 standardized
identities. It now makes 47 groups spanning more than 1.0 log unit visible as
replicate_disagreement=True, rather than silently mean-aggregating them.

## Closed findings

| Former finding | Resolution | Evidence |
|---|---|---|
| P1 — ChEMBL can return an unstripped organic salt | Checks len(Chem.GetMolFrags(parent)); default returns multi_fragment_parent, while the RDKit largest-organic-fragment route is explicit opt-in. | Sodium acetate is flagged by default; fallback produces one fragment. |
| P1 — Shipped QSAR code silently discards failures | prepare_qsar_data returns (dataframe, status_counts) and the demo prints the tally. | Focused fixture records parse failure, ambiguous parent, and accepted rows exactly once. |
| P2 — Replicates lack disagreement policy | Outputs activity_range and replicate_disagreement; default review threshold is 1.0 log unit and dropping is opt-in. | hERG: 379 replicated groups, 47 range flags, maximum 3.69. |
| P2 — Isotope option is library-wide only | Complete bundled implementation accepts validated boolean keep_isotopes_col and retains the resulting decision. | One labelled and one unlabelled ethanol row remain separate; exactly one output row retains isotopes. |
| P2 — Missing columns yield raw pandas errors | Required SMILES/activity and optional isotope columns are validated at entry. | A typo raises an actionable ValueError. |

## Input results

| # | Input | Result | Assertions |
|---:|---|---:|---:|
| 1 | hERG QSAR preparation and loss accounting | 100 | 5 / 5 |
| 2 | ChEMBL parent-selection salt/co-crystal edge cases | 100 | 5 / 5 |
| 3 | Tautomer and InChIKey behavior | 91 | 4 / 4 |
| 4 | Cross-database standardized join | 91 | 5 / 5 |
| 5 | Mixed tracer policy, tautomer limits, throughput | 100 | 5 / 5 |

Inputs 3 and 4 retain their prior score deductions for the skill's intentional
scientific scope and explanatory density; neither has a failed assertion or an
open P0/P1/P2 item.

## Remaining non-blocking notes

No P0, P1, or P2 findings remain. The general skill-creator validator rejects
the repository-wide legacy frontmatter keys tool_type, primary_tool, and
author; this affects 561 skills and was deliberately not changed in this
single-skill fix pass. It is not a molecular-standardization defect and does not
affect the audit environment or executable example.
