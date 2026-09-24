> **Audit record for `bio-entrez-search`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@5442c26](https://github.com/mrsonord2240/bioSkills/tree/5442c26cef8f0f9eeca84dd1eccfe00eb63d4d07/database-access/entrez-search) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-entrez-search final pass

Source: `mrsonord2240/bioSkills@5442c26cef8f0f9eeca84dd1eccfe00eb63d4d07:database-access/entrez-search`  
Date: 2026-09-24  
Result: **95/100 — Production Ready — deployable**

This is a single-brief final pass (`auditor_independent: false`). It re-executed the nine archived
logical inputs and two new source-derived inputs. All **38/38 assertions passed** using Python 3.14
and Biopython 1.88. Live NCBI values are time-stamped observations, not stable biological facts.

| Input | Coverage | Result |
|---|---|---|
| 1 | Field-qualified PubMed search and capped UID return | 4/4 pass |
| 2 | EInfo `DbInfo[0]` across four databases | 4/4 pass |
| 3 | Large history-server queue | 3/3 pass |
| 4 | MARCH1 ambiguity and qualified retry | 3/3 pass |
| 5 | WebEnv chaining and ESpell | 2/2 pass |
| 6 | EGQuery absence and shipped ESearch-loop fallback | 3/3 pass |
| 7 | XML error bodies raise rather than fabricate | 2/2 pass |
| 8 | Curated-list disclosure and all-38-db widening | 5/5 pass |
| 9 | URL encoding of adversarial-looking terms | 5/5 pass |
| 10 (new) | Local query-size / OR-clause preflight | 4/4 pass |
| 11 (new) | Exact-node taxonomy behavior | 2/2 pass |

## Final-pass changes verified

- Reduced the entrypoint to 289 lines by moving database-specific fields and recovery detail into
  `references/query-design-and-failures.md`, linked at the decision point.
- Added runnable `examples/validate_term.py`; it accepts a normal qualified query and rejects blank,
  overlong, or OR-heavy strings before a request.
- Corrected live behavior: ESearch without `usehistory='y'` does not return WebEnv; `:noexp` is the
  exact-node taxonomy modifier, while `:exp` retains expansion; an unset Entrez email emits a warning;
  and EPost batching is guidance rather than a universal 200-ID hard cap.

No open recommendations. See `eval_report_bio-entrez-search_result.json` for scores and evidence.
