> **Audit record for `bio-alignment-msa-statistics`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@f3a7a62](https://github.com/mrsonord2240/bioSkills/tree/f3a7a62091e42f6e98653b5b626de94c6f7bfff7/alignment/msa-statistics) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-22 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-msa-statistics

Generated: 2026-09-22

Source: `mrsonord2240/bioSkills@f3a7a62091e42f6e98653b5b626de94c6f7bfff7:alignment/msa-statistics`

Final-pass exception: `auditor_independent: false`; fixed and audited under one brief. See `F:\OpenScience\audits\_final_pass\bio-alignment-msa-statistics\CHECKPOINT.md`.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical Pfam seed | 39 | 59 | 98 | 5/5 | ✅ |
| 2 | Variant A real aligner outputs | 39 | 58 | 97 | 5/5 | ✅ |
| 3 | Edge Pwalign PID comparison | 40 | 59 | 99 | 5/5 | ✅ |
| 4 | Variant B lowercase HBB DNA | 39 | 59 | 98 | 5/5 | ✅ |
| 5 | Stress 300x300 and 2000x300 | 38 | 58 | 96 | 5/5 | ✅ |
| 6 | Scope boundary distance handoff | 38 | 58 | 96 | 4/4 | ✅ |
| 7 | Adversarial messy/degenerate MSA | 39 | 58 | 97 | 5/5 | ✅ |
| 8 | Variant B Rfam RNA | 39 | 59 | 98 | 5/5 | ✅ |
| 9 | Edge kinase NaN ranking | 39 | 58 | 97 | 5/5 | ✅ |
| 10 | New IUPAC-rich DNA | 39 | 59 | 98 | 5/5 | ✅ |
| 11 | New format-map round trip | 39 | 59 | 98 | 5/5 | ✅ |

Execution average: **97.0/100**. Assertion pass rate: **54/54**.

## What ran

All code executed from `run/skill`, an audit-owned copy whose `SKILL.md` SHA-256 matched the worktree source before execution. The original worktree was not imported or modified.

- `phase2_pid_pwalign.R` generated 169 Pwalign ground-truth pairs. It reported 22 rows with terminal gaps and 108 with unaligned flanks.
- `phase2_pid_compare.py` compared scalar and vectorized PID1–PID4 against those pairs and six hand cases: **12/12 PASS**. The former denominator differed on 22 raw and 88 staggered-flank rows.
- `phase2_prepare.py` produced normalized HBB and aligned-globin FASTA inputs; `phase2_modeltest.sh` executed the two literal ModelTest-NG forms and emitted `MODELTEST_NT_OK` and `MODELTEST_AA_OK`.
- `phase2_regression.py` replayed archived inputs 1–10. Its final successful stages cover the 10 shipped executable examples, real Pfam/Rfam fixtures, lower/dotted forms, stress matrices, and adversarial normalization/NaN cases. Input 11 ran separately in `phase2_input11.py` after providing Biopython's required `molecule_type` annotation to write Nexus; it passed all four documented extension routes.

Selected checked output:

```text
MODELTEST_NT_OK
MODELTEST_AA_OK
SUMMARY 12 of 12 checks PASS
INPUT 11 PASS: 4 extension-mapped formats, 8 shape/row assertions plus format-count assertion
```

## Vetoes and scoring

Structural veto: PASS (stability, contract, determinism, security). Research veto: PASS (scientific integrity, practice boundaries, methodological ground, code usability).

Static score: 96/100. Dynamic score: 97.0/100. Weighted final: `96 * 0.4 + 97.0 * 0.6 = 96.6`, rounded to **97/100**.

No P0, P1, or P2 recommendation is open. The pre-fix audit was preserved at `F:\OpenScience\audits\_pre-fix-20260922\bio-alignment-msa-statistics`.
