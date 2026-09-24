> **Audit record for `bio-causal-genomics-fine-mapping`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@dfc77a6](https://github.com/mrsonord2240/bioSkills/tree/dfc77a6351c0f8af8ae6f4e1e5b38b281f4ae474/causal-genomics/fine-mapping) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-fine-mapping

## Canonical final summary

**Final:** 95/100 — ⭐ Production Ready; deployable: true.

Source: `mrsonord2240/bioSkills@dfc77a6351c0f8af8ae6f4e1e5b38b281f4ae474:causal-genomics/fine-mapping`
Auditor independent: `false`
Note: final pass: fixed and audited under one brief, see CHECKPOINT.md

Generated: 2026-09-23
Source: `mrsonord2240/bioSkills@dfc77a6351c0f8af8ae6f4e1e5b38b281f4ae474:causal-genomics/fine-mapping`
Audit context: corrective final-pass Phase 2; `auditor_independent: false` by direction.

## Verdict

**95/100 — Production Ready; deployable: true.** All vetoes pass. The former RSS M3 failure was re-executed directly from the repaired source: the default has lambda 0.0000 and credible-set outputs; two separate intentional mismatch runs have lambda 1.0000, stop before fitting/reporting, and write no result TSVs.

## Summary

| Input | Workflow | Score | Assertions | Executed | Result |
|---|---|---:|---:|---|---|
| 1 | Matched-LD summary SuSiE | 98 | 3/3 | yes | PASS |
| 2 | Individual-level SuSiE | 97 | 3/3 | yes | PASS |
| 3 | LD mismatch diagnostics | 98 | 3/3 | yes | PASS |
| 4 | coloc.susie naming guard | 99 | 3/3 | yes | PASS |
| 5 | HLA-like L stress | 97 | 3/3 | yes | PASS |
| 6 | FINEMAP 1.4.2 CLI | 88 | 3/3 | yes | PASS |
| 7 | Case-control Neff | 96 | 3/3 | yes | PASS |
| 8 | PolyFun prior integration | 99 | 3/3 | yes | PASS |
| 9 | Usage-guide/scope check | 94 | 3/3 | yes | PASS |
| 10 | SuSiEx two-ancestry CLI | 98 | 3/3 | yes | PASS |
| 11 | DAP-G summary-statistics CLI | 88 | 3/3 | yes | PASS |
| 12 | Shipped RSS default, repaired | 95 | 3/3 | yes | PASS |
| 13 | Shipped RSS intentional mismatch | 99 | 3/3 | yes | PASS |
| 14 | Clean repeated RSS mismatch | 96 | 3/3 | yes | PASS |

Execution average: **95.9/100**. Assertion pass rate: **42/42**. Static score: **94/100**.

## Corrective RSS evidence

The scripts and their full stdout are under `run/re-audit-dfc77a6/`.

- `input12_shipped_rss_default_guard.sh` executed the source snapshot whose `susie_rss_finemap.R` SHA-256 is `EE9E2B51...AC030520`. It observed `lambda = 0.0000`, a nonzero valid credible-set count, and non-empty `finemap_pips.tsv` plus `finemap_credible_sets.tsv`.
- `input13_shipped_rss_intentional_mismatch_guard.sh` set `SUSIE_RSS_DEMO_LD_MISMATCH=1`. It observed `lambda = 1.0000`, the explicit recovery/stop text, no credible-set reporting, and neither result TSV.
- `input14_shipped_rss_mismatch_is_reproducible.sh` repeated that mismatch in a clean directory with the same lambda and no outputs, excluding inherited-result leakage.

The Windows R wrapper returned 139 after materializing its output in these three checks. Each check independently asserted the required content and file state; this is retained as an open P1 runtime-status issue, not counted as a source-method failure.

## Other executed evidence

- Matched RSS: two planted signals in purity-1.0 sets; mismatch diagnostic: lambda rose above threshold while matched lambda was 0.0000.
- Individual-level SuSiE: SNP60 PIP 1.000. HLA stress: L=30 recovered 12/12 versus 10/12 at L=10.
- coloc.susie: documented named input succeeded; the old unnamed control still fails predictably rather than silently.
- FINEMAP accepted the corrected flags and emitted `locus.snp`/`locus.cred1`; SuSiEx returned `snp149` with both PIPs 1; DAP-G emitted cluster output despite its documented success exit code 1.
- PolyFun wrote real SNPVAR output and produced PIP 0.9979 with `prior_weights` versus 0.8966 with uniform or the documented wrong `prior_variance` argument.
- The shipped `susie_finemapping.R` recovered rs100 and rs350; `pip_visualization.R` wrote three non-empty PDFs.

## Gates and remaining work

- Skill veto T1–T4: PASS.
- Research veto M1–M4: PASS.
- P1: make the Windows R wrapper return 0 after successful materialized RSS runs.
- P2: verify PAINTOR in a foreground isolated build; add a sourced genotype-QC checklist for genotype routes.

The preceding rejected report/evidence is preserved at `F:\OpenScience\audits\_pre-fix-20260923\bio-causal-genomics-fine-mapping\rejected-6977f1a-final-pass\`.
