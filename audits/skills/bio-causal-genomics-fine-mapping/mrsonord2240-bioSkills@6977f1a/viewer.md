> **Audit record for `bio-causal-genomics-fine-mapping`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6977f1a](https://github.com/mrsonord2240/bioSkills/tree/6977f1aea2dfa42d1b1a937517e70659c5801e8a/causal-genomics/fine-mapping) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-fine-mapping

Generated: 2026-09-23  
Source: `mrsonord2240/bioSkills@6977f1aea2dfa42d1b1a937517e70659c5801e8a:causal-genomics/fine-mapping`  
Audit context: final pass; `auditor_independent: false` by direction (see final-pass checkpoint).

## Verdict

**92/100 before veto; ❌ Reject; deployable: false.** The Research Veto M3 fails because the shipped `examples/susie_rss_finemap.R` reports credible sets after its own severe LD-mismatch diagnostic (`lambda=0.8314`). The full structured report is `eval_report_bio-causal-genomics-fine-mapping_result.json`.

## Summary

| Input | Type | Basic | Specialized | Total | Assertions | Executed | Status |
|---|---|---:|---:|---:|---|---|---|
| 1 | Canonical matched-LD RSS | 39 | 59 | 98 | 3/3 | yes | ✅ |
| 2 | Individual-level SuSiE | 39 | 58 | 97 | 3/3 | yes | ✅ |
| 3 | LD mismatch edge | 39 | 59 | 98 | 3/3 | yes | ✅ |
| 4 | coloc.susie regression | 40 | 59 | 99 | 3/3 | yes | ✅ |
| 5 | HLA-like stress | 39 | 58 | 97 | 3/3 | yes | ✅ |
| 6 | FINEMAP CLI | 36 | 53 | 89 | 3/3 | yes | ✅ |
| 7 | Neff / causal-claim boundary | 38 | 58 | 96 | 3/3 | yes | ✅ |
| 8 | PolyFun functional priors | 40 | 59 | 99 | 3/3 | yes | ✅ |
| 9 | Usage-guide Tip recall | 37 | 57 | 94 | 3/3 | yes | ✅ |
| 10 | Fresh SuSiEx two-ancestry | 39 | 59 | 98 | 3/3 | yes | ✅ |
| 11 | Fresh DAP-G | 36 | 56 | 92 | 3/3 | yes | ✅ |
| 12 | Fresh shipped RSS self-consistency | 20 | 25 | 45 | 1/3 | yes | ❌ |

Execution average: **91.8/100**. Assertion pass rate: **34/36**.

## Executed evidence

All scripts and stdout are retained in `run/final-pass-20260923/`. The archived prior audit is at `F:\OpenScience\audits\_pre-fix-20260923\bio-causal-genomics-fine-mapping\`.

- Inputs 1–5 and 7 used `mendelian-randomization-analyst/r.sh`. They re-ran the prior regression inputs: matched-LD lambda 0.0246 with two planted hits; individual-level SNP60 PIP 1.000; mismatch lambda 0.7517 versus 0.0000 matched; named coloc PP.H4 1.000 with the old unnamed error still reproducible; and L=30 recovered 12/12 high-signal planted variants versus 10/12 at L=10.
- Input 6 ran FINEMAP 1.4.2 in WSL `cg-finemap`: documented current flags and space-delimited LD parsed, and it emitted `locus.snp` and `locus.cred1`.
- Input 8 ran `polyfun.py --compute-h2-L2` on 182,454 bundled real summary-statistic rows. Its R integration then showed `prior_weights` PIP 0.9979 versus 0.8966 under uniform or the wrong `prior_variance` argument.
- Input 10 initially exposed coordinate mistakes in this **new audit fixture**, not the Skill: the retained first two logs show the bad fixture attempts. The coordinate-consistent rerun completed SuSiEx and recovered `snp149` with `CS_PIP=1`.
- Input 11 confirmed DAP-G's documented status-1-on-success behavior while producing clusters and a `snp149` row.

## New P0: shipped RSS example breaks its own diagnostic contract

Input 12 executed the supplied code, not a reimplementation:

```text
estimate_s_rss lambda = 0.8314
Lambda > 0.10: LD reference likely mismatches the GWAS sample.
Effective L used (credible sets returned): 3 / requested 10
Valid credible sets after purity filter: 3
Wrote finemap_pips.tsv and finemap_credible_sets.tsv
```

This violates the Skill's own Critical LD Diagnostic Block: a diagnostic must precede reporting credible sets, and a failed diagnostic needs refitting or a changed reference. The self-contained simulation instead creates z-scores by adding hand-made bumps to an unrelated banded LD matrix. The P0 repair is to simulate `z ~ N(R %*% true_z, R)` and hard-stop reporting when `lambda > 0.10`.

## Static checks

`run/final-pass-20260923/static_checks.ps1` checked that `SKILL.md` is exactly 300 lines, all locally referenced files exist, all three shell examples pass `bash -n`, and all three R examples parse. The actual `susie_finemapping.R` and `pip_visualization.R` also ran; the former recovered rs100 and rs350 at PIP approximately 1, and the latter wrote three non-empty PDFs.

## Gates and score

- Skill Veto T1–T4: PASS.
- Research Veto: M1 PASS, M2 PASS, **M3 FAIL**, M4 PASS.
- Static: 91/100. Dynamic: 91.8/100. Weighted diagnostic score: 92/100.
- Veto overrides the numeric score: **Reject, not deployable**.
