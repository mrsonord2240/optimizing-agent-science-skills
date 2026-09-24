> **Audit record for `bio-experimental-design-power-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@3b1beb2](https://github.com/mrsonord2240/bioSkills/tree/3b1beb228f540a2b0e5ee138bd8f6646997f4f4e/experimental-design/power-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-experimental-design-power-analysis

Source: `mrsonord2240/bioSkills@3b1beb228f540a2b0e5ee138bd8f6646997f4f4e:experimental-design/power-analysis`
Generated: 2026-09-23
Auditor independent: `false`
Note: final pass: fixed and audited under one brief, see CHECKPOINT.md

**⭐ Production Ready — 94/100; deployable true.** Static score: 95/100. Dynamic score: 93.9/100 from seven fully executed inputs and 34/34 passing assertions. The weighted total is `95 × 0.4 + 93.9 × 0.6 = 94.3`, rounded to the canonical schema score of **94/100**. Both Skill and Research vetoes passed.

## Provenance and natural exit

The source was checked out exactly at `3b1beb228f540a2b0e5ee138bd8f6646997f4f4e` in `F:\OpenScience\wt\p2-reaudit-bio-power-analysis`; it remained clean. Existing structured vectors used audit-owned child processes with no outside-process intervention.

The earlier generic pseudobulk wrapper preserved its output but not a numeric process exit. This final audit does not rely on that ambiguity: `run/closure-20260924/rerun_pseudobulk_exact.ps1` reran the exact source in an audit-owned process and persisted `pseudobulk_exact_source.execution.json` with `status=COMPLETED`, `exit_code=0`, `terminal_sentinel=true`, source SHA-256 `EF0F9E470474FCA706B447F2456C9E2BD85086A9C918E291FCAE7B35857F03F3`, and no process intervention. The sentinel is emitted only after the exact source returns.

## Vetoes

- Skill veto: **PASS** — formal vectors completed, prospective inputs are validated, pseudobulk uses a pinned seed, and no raw user code executes.
- Research veto: **PASS** — realized FDR gates power reporting, donor-level pseudobulk prevents cell pseudoreplication, and regulated clinical endpoints redirect to a sibling skill.

## Static scoring

| Category | Score | Basis |
| --- | ---: | --- |
| Functional suitability | 12/12 | Covers stated assay/design scenarios and the clinical boundary. |
| Reliability | 12/12 | Wrapper validates inputs; FDR gate rejects invalid candidates. |
| Performance/context | 7/8 | Fast closed-form path; realistic simulation is deliberately substantive. |
| Agent usability | 15/16 | Clear decision tree and prompts; no machine-readable request contract. |
| Human usability | 8/8 | Discoverable prompts, examples, and escape hatch. |
| Security | 11/12 | No secrets/raw code execution; numeric inputs checked. |
| Maintainability | 12/12 | Version guidance and executable examples. |
| Agent-specific quality | 18/20 | Precise triggers and boundaries; detailed material remains one SKILL.md. |

## Dynamic replay

| # | Vector | Basic | Specialized | Total | Assertions | Execution result |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 1 | Bulk RNA-seq sizing + FDR gate | 38/40 | 57/60 | 95 | 5/5 | exit 0 |
| 2 | Fixed-budget depth vs replicates | 36/40 | 54/60 | 90 | 5/5 | exit 0 |
| 3 | Hard target, preflight + MDE | 38/40 | 57/60 | 95 | 5/5 | exit 0 |
| 4 | scRNA-seq pseudobulk donor power | 38/40 | 57/60 | 95 | 5/5 | closure rerun: exit 0 + post-source PASS sentinel |
| 5 | Proteomics multiplicity + ATAC | 37/40 | 56/60 | 93 | 5/5 | exit 0 |
| 6 | Regulated Phase II scope boundary | 39/40 | 56/60 | 95 | 4/4 | exit 0 |
| 7 | Observed-power adversarial request | 38/40 | 56/60 | 94 | 5/5 | exit 0 |

Key observed outcomes:

- Guard probe: finite canonical power `0.286598`; FDR `0.04` accepted; `0.06` and `NaN` rejected; invalid alpha, CV, and unit effect stopped before the package call.
- Exact bulk source: Actual FDR `0.3692738`, `0.1849111`, `0.1024990`, and `0.0598908` all rejected at nominal 0.05.
- Exact pseudobulk closure rerun: 4 donors yielded FDR `0.000` / ACCEPT; 12 donors yielded FDR `0.133` / REJECT. Naive cell-level FDR remained `0.897` / `0.888` despite apparent power.
- Proteomics: raw `n=11.942258`; multiplicity-corrected `n=42.449567`; ATAC cross-check `0.219796`.
- Edge solve: required `n=6441.455943`; MDE `1.775628`.

## Recommendation

- **P2:** Keep realized-FDR tolerance at zero unless a nonzero Monte Carlo tolerance is pre-specified, paired with higher `nsims`, and shown not to change the accept/reject decision.

The canonical structured record is [eval_report_bio-experimental-design-power-analysis_result.json](eval_report_bio-experimental-design-power-analysis_result.json). Closure evidence is under `run/closure-20260924/`.

## Canonical final-pass metadata

- Source: `mrsonord2240/bioSkills@3b1beb228f540a2b0e5ee138bd8f6646997f4f4e:experimental-design/power-analysis`
- `auditor_independent: false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`
