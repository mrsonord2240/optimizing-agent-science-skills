> **Audit record for `bio-crispr-screens-copy-number-correction`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@9d31109](https://github.com/mrsonord2240/bioSkills/tree/9d31109159d4d490ec375d4ae88c9b77570f3840/crispr-screens/copy-number-correction) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-copy-number-correction (RE-AUDIT #3, fixed)

Generated: 2026-09-16
Source: `mrsonord2240/bioSkills@9d31109159d4d490ec375d4ae88c9b77570f3840:crispr-screens/copy-number-correction`
Round-2 report (previous audit, score 81): `F:\OpenScience\audits\bio-crispr-screens-copy-number-correction\` (this folder, now overwritten by this round)
Pre-fix report (round 1, score 73): `F:\OpenScience\audits\_pre-fix-20260916\bio-crispr-screens-copy-number-correction\`
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-crispr-screens-copy-number-correction.md` (round-3 section)

**This re-audit is fully independent execution.** The round-3 diff touched only SKILL.md
(+34/-4), fixing exactly the round-2 report's P1 (negative_control_sgrnas exception/call-site)
and two P2s (low-power floor disclosure, Reconciliation cause 5). Inputs 1-2 below are direct
regression tests of those fixes on fresh real/synthetic data. Inputs 3-7 are new — designed to
avoid measuring only the fixer's own homework, per this audit's brief.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 35 | 48 | 83 | 4/4 PASS | ✅ |
| 2 | Variant A (regression) | 36 | 49 | 85 | 4/4 PASS | ✅ |
| 3 | Edge (NEW) | 34 | 47 | 81 | 3/3 PASS | ✅ |
| 4 | Variant B (NEW) | 33 | 44 | 77 | 4/4 PASS | ✅ |
| 5 | Stress (NEW) | 29 | 37 | 66 | 2/4 PASS | ⚠️ |
| 6 | Adversarial (NEW) | 29 | 38 | 67 | 2/3 PASS | ⚠️ |
| 7 | Scope Boundary (regression) | 31 | 41 | 72 | 3/3 PASS | ⚠️ |

**Execution Average: 75.9 / 100**
**Assertion Pass Rate: 22/25**
**Static Score: 92/100 — Final Score: 82/100 — Limited Release ✅ — Deployable: true**

Round 2 was 81 (Limited Release, deployable, 1 open P1 + 2 open P2). Round 3 is 82 (Limited
Release, deployable, still) — both round-3 targeted fixes verified correct by fresh execution
(Inputs 1-2), the explicitly-required "no cry-wolf" claim confirmed (Input 3), and 2 new P2s
found by this audit's own inputs that were never in the fix log (Inputs 5, 6). The Skill remains
just below the 85 core floor.

## What actually ran

- `run/scripts_r3/01_negctrl_construction_regression.py` — Input 1 (regression) + Input 6 (NEW),
  Chronos 2.3.15, real single-line HAP1 TKOv3 planted-amplicon data.
- `run/scripts_r3/02_detect_cn_bias_fixed_regression.py` — Input 2 (regression), the round-3-fixed
  `detect_cn_bias()` verbatim on real post-CRISPRcleanR HT-29 gene-LFC+CN data already on disk
  from the round-2 audit (`run/ccr_ht29/`).
- `run/scripts_r3/03_no_cry_wolf_check.py` — Input 3 (NEW), 5 independent relabeling trials on
  real diploid HT-29 genes.
- `run/scripts_r3/04_low_power_boundary_and_nan_guard.py` — Input 4 (NEW), exact `low_power_n=8`
  boundary sweep and NaN-guard check.
- `run/scripts_r3/05_per_line_vs_pooled_reconciliation.py` — Input 5 (NEW), real 3-line
  post-`alternate_CN` gene-effect matrix already on disk from the round-2 fix pass
  (`run/chronos_3line_before.csv`, `run/chronos_3line_after.csv`).
- Input 7 — filesystem/text verification only (`git diff`, `grep`), no script file.

No new synthetic/relabeled data files were needed; all inputs reused real or honestly-labeled
data already produced and saved to disk by the round-1/round-2 audits and the round-2 fix pass,
consistent with this round's diff touching only two sections of SKILL.md.

## Detailed Outputs

### Input 1 — Canonical (REGRESSION): negative_control_sgrnas omitted

**Prompt:** "Regression-test the round-3 fix's headline claim: does omitting
`negative_control_sgrnas` really raise `ValueError` at `chronos.Chronos(...)` construction, not
`UnboundLocalError` at `train()`?"

```
=== Input 1 (regression): negative_control_sgrnas OMITTED entirely ===
Chronos(...) construction raised ValueError: excess_variance was passed as dict without key for 'screen':
{}
>>> MATCHES SKILL.md's round-3 claim verbatim.
```

Exact match. No `UnboundLocalError` escaped to the caller.

**Scores:** Basic 35/40 | Specialized 48/60 | Total 83/100
**Assertions:** 4/4 PASS

### Input 2 — Variant A (REGRESSION): low_power_floor / suspicious_despite_ns on real data

**Prompt:** "Regression-test the round-3 fix's second claim: do `low_power_floor` and
`suspicious_despite_ns` behave as SKILL.md now documents on the real HT-29 3-gene block?"

```
=== POST-correction, focused on real amplicon block (n=3 amplified) ===
  amplified_vs_diploid_gap: -0.9809479484818501
  p_amplified_more_depleted: 0.20798118187614373
  bias_present: False
  low_power_floor: True
  suspicious_despite_ns: True
```

`gap ~ -0.98? True | p ~ 0.208? True` — exact match to SKILL.md's documented numbers.

**Scores:** Basic 36/40 | Specialized 49/60 | Total 85/100
**Assertions:** 4/4 PASS

### Input 3 — Edge (NEW): does the fix cry wolf on a genuinely corrected screen?

**Prompt:** "The audit dispatch explicitly asks whether `low_power_floor`/`suspicious_despite_ns`
cry wolf on a screen that was actually corrected well. Test it."

```
trial 0: n_amplified=5 gap=0.2337  suspicious_despite_ns=False -> silent (correct)
trial 1: n_amplified=5 gap=0.1860  suspicious_despite_ns=False -> silent (correct)
trial 2: n_amplified=5 gap=-0.1632 suspicious_despite_ns=False -> silent (correct)
trial 3: n_amplified=5 gap=0.2140  suspicious_despite_ns=False -> silent (correct)
trial 4: n_amplified=5 gap=0.2004  suspicious_despite_ns=False -> silent (correct)
False-alarm rate: 0/5
```

Real diploid HT-29 genes relabeled as a small "corrected amplicon" (n=5, below `low_power_n=8`)
never trip `suspicious_despite_ns`. The fix does not cry wolf.

**Scores:** Basic 34/40 | Specialized 47/60 | Total 81/100
**Assertions:** 3/3 PASS

### Input 4 — Variant B (NEW): low_power_n=8 boundary and the NaN guard

**Prompt:** "Sweep the exact `low_power_n=8` boundary and confirm the NaN guard on
`suspicious_despite_ns` doesn't crash below the existing n>=3 floor."

```
=== (a) Boundary of low_power_n=8 at n_amplified = 7, 8, 9 ===
  n_amplified=7  low_power_floor=True   expected=True   OK
  n_amplified=8  low_power_floor=False  expected=False  OK
  n_amplified=9  low_power_floor=False  expected=False  OK

=== (b) NaN guard: fewer than 3 amplified genes ===
  n_amplified=2  gap=nan  suspicious_despite_ns=False  low_power_floor=True
  No exception raised on NaN gap; suspicious_despite_ns correctly resolves to False. OK
```

No off-by-one error; no crash on the NaN path.

**Scores:** Basic 33/40 | Specialized 44/60 | Total 77/100
**Assertions:** 4/4 PASS

### Input 5 — Stress (NEW): does pooling really mask what per-line catches?

**Prompt:** "SKILL.md's new Reconciliation cause 5 says re-run `detect_cn_bias` per cell line,
'not only pooled,' because pooling can mask a real problem. Test that specific claim on the real
3-line panel."

```
=== PER-LINE ===
  LINE_CN2  (CN=2):  gap=nan     bias_present=False
  LINE_CN8  (CN=8):  gap=-0.905  p=0.0000  bias_present=True
  LINE_CN15 (CN=15): gap=-0.898  p=0.0000  bias_present=True

=== POOLED (all 3 lines merged) ===
  pooled (n_amplified=16): gap=-0.903  p=0.0000  bias_present=True

=== Does pooling dilute a real per-line problem? ===
  NOT confirmed on this real data: pooled and per-line give the same qualitative read.
```

The underlying claim (alternate_CN leaves real residual signal) is confirmed — both
`LINE_CN8`/`LINE_CN15` independently show `bias_present=True`. But the specific justification
("pooling masks it") does not hold here: the pooled analysis caught the same bias at essentially
the same magnitude. This is a real, new finding — an overclaim in the new Reconciliation text,
not a functional defect.

**Scores:** Basic 29/40 | Specialized 37/60 | Total 66/100
**Assertions:** 2/4 PASS — 2 new FAILs (see recommendations)

### Input 6 — Adversarial (NEW): negative_control_sgrnas as an explicit empty dict

**Prompt:** "The fix log mentions, as an aside, that passing `negative_control_sgrnas={'screen':
[]}` (not omitting it) gives a different ValueError. That claim was never independently checked.
Check it, and see if SKILL.md's Common Errors table covers it."

```
=== Input 6 (NEW): negative_control_sgrnas passed as an EXPLICIT EMPTY dict {'screen': []} ===
Chronos(...) construction raised ValueError: set of negative_control_sgrnas is empty
>>> Message mentions "empty" -- consistent with the fix log's unverified aside, now independently confirmed.
```

Independently confirms the fix log's own unverified aside — but SKILL.md's Common Errors table
only documents the *omitted*-argument message (Input 1), not this distinct *empty-list* message.
A caller who builds `negative_control_sgrnas` programmatically and ends up with an empty list (a
realistic mistake, not a contrived one) hits an undocumented error text.

**Scores:** Basic 29/40 | Specialized 38/60 | Total 67/100
**Assertions:** 2/3 PASS — new P2 finding (see recommendations)

### Input 7 — Scope Boundary (REGRESSION + shipped-means-present)

**Prompt:** "Confirm the round-2 Scope paragraph and all Skill-bundled files are still present and
unbroken at the new commit, since gate 8 (shipped-means-present) applies to every re-audit."

```
**Scope:** this Skill analyses screen data. It does not support treatment, therapy or other clinical
recommendations for an individual... Decline the clinical part of such a request and answer the
computational part.
```

Present, unchanged. `usage-guide.md` and `examples/run_crispr_cleanr.R` both still exist.
`git diff` confirms the round-3 commit touched only two sections of SKILL.md (+34/-4), matching
the fix log — no incidental file removal or path breakage.

**Scores:** Basic 31/40 | Specialized 41/60 | Total 72/100
**Assertions:** 3/3 PASS

---

> **Note for reviewer:** Inputs 5, 6, and 7 are the three ⚠️ rows. Input 7 is ⚠️ only because its
> total (72) falls under the 75 status-flag cutoff for a lightweight completeness check, not
> because anything failed — all 3 of its assertions PASS. Inputs 5 and 6 are this audit's own new
> findings, not carried over from the round-2 report or the fix log: a Reconciliation-text
> overclaim and an undocumented empty-dict exception path. Neither rises to a P0 or P1 — the
> underlying fixes work exactly as intended when used the way most callers will use them; the
> gaps are narrower documentation-precision issues.
