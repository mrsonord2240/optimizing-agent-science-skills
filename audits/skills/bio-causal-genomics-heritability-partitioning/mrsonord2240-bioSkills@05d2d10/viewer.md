> **Audit record for `bio-causal-genomics-heritability-partitioning`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@05d2d10](https://github.com/mrsonord2240/bioSkills/tree/05d2d10f902ceb158ab2a9402dc36214ca44b9a1/causal-genomics/heritability-partitioning) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Final-pass Phase 2 — bio-causal-genomics-heritability-partitioning

## Canonical final summary

**Final:** 95/100 — ⭐ Production Ready; deployable: true.

Source: `mrsonord2240/bioSkills@05d2d10f902ceb158ab2a9402dc36214ca44b9a1:causal-genomics/heritability-partitioning`
Date: 2026-09-23 · **95/100, Production Ready, deployable**
This directed final pass sets `auditor_independent: false`: `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

The preceding live audit was preserved at `F:\OpenScience\audits\_pre-fix-20260923\bio-causal-genomics-heritability-partitioning\`; the existing 2026-09-17c archive remains untouched.

## Fresh evidence

| Inputs | What ran | Checked result |
|---|---|---|
| 1 | Fresh CBIIT/ldsc `1f09cf0` munging and h2 | h2 0.3783 (0.0419), intercept 2.0926, ratio 0.1203 |
| 2 | Fresh functional S-LDSC | category/enrichment output; full baseline-LD bundle unavailable |
| 3 | Fresh cross-trait LDSC | rg 0.1117 (0.0776), p 0.1502, gcov_int -0.2577 |
| 4 | Fresh liability LDSC | h2 0.7091 (0.0786); current h2 [0,1] rule verified |
| 5 | Fresh h2-cts unpatched then patched | exact TypeError, then CellTypeB p 0.0003508 / CellTypeA p 0.9924 |
| 6–7 | Patient-PRS and fabrication boundaries | current Scope controls both; reasoning-only checks |
| 8 | Fresh LDAK 6.3 tagging + SumHer | Her_All 0.022368 (SE 0.021182) |
| 9 | Current `smoke_test_ldsc.sh` | h2, rg, and h2-cts completed under documented `ldsc-py39` |
| 10 | Current `gcta_greml.sh` | real 957-person GRM and parseable REML result |
| 11 | Impossible-h2 interpretation | current threshold requires investigation, not face-value reporting |

Artifacts are in `run/finalpass_20260923/`: `run_ldsc_ldak_smoke.sh`, `run_gcta_example.sh`, their logs, and all checked outputs. A preliminary HESS fixture harness stopped because the WSL default Python lacks pandas; it is retained as harness evidence and is not scored as a Skill defect.

No P0 or veto. Remaining P1: HDL requires its real reference panel; BOLT-REML needs a compatible host. P2: HESS step 2 needs all 22 chromosome outputs.
auditor_independent: false
