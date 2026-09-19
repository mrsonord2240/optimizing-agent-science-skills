> **Audit record for `bio-single-cell-hashing-demultiplexing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@0de5e44](https://github.com/mrsonord2240/bioSkills/tree/0de5e44090dd0428293282bc6feff9e1389817f6/single-cell/hashing-demultiplexing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-hashing-demultiplexing (RE-AUDIT)
Generated: 2026-09-19

**RE-AUDIT of a fixed Skill.** Fresh, independent auditor — not the original auditor (score 78,
1 open P0) and not the fixer (branch `fix/sc-hashing`, commit `0de5e440`). Pre-fix report archived
to `F:\OpenScience\audits\_pre-fix-20260919\bio-single-cell-hashing-demultiplexing\`. Skill source:
`mrsonord2240/bioSkills@0de5e44090dd0428293282bc6feff9e1389817f6:single-cell/hashing-demultiplexing`,
verified from the worktree `F:\OpenScience\wt\sc-hashing`.

All 5 inputs below use **freshly generated synthetic data** (different seeds, different cell counts)
from both the original auditor's and the fixer's own test data — the point of a re-audit is to check
the fix generalizes, not just that it passes the exact case the fixer tested against.

**Scope note:** the fix diff touches only `SKILL.md`, `usage-guide.md`, and
`examples/hashsolo_scanpy.py`, all confined to the hashsolo / demuxmix / GMM-Demux sections. The
HTODemux canonical case, the modality-choice consultation, and the unequal-pooling stress case are
byte-identical to the same-day original audit (which scored them 90, 88, 92) and were **not
re-executed this round** — I do not claim to have re-run them, and their prior scores are not
included in this report's `dynamic_score`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (P0 regression) | 38 | 56 | 94 | 5/5 PASS | ✅ |
| 2 | Edge (P1 regression) | 37 | 55 | 92 | 5/5 PASS | ✅ |
| 3 | Variant A (new: GMM-Demux) | 37 | 53 | 90 | 4/5 PASS | ⚠️ |
| 4 | Variant B (new: demuxEM Windows check) | 37 | 52 | 89 | 4/4 PASS | ✅ |
| 5 | Stress (documentation-accuracy audit) | 32 | 44 | 76 | 3/4 PASS | ⚠️ |

**Execution Average: 88.2 / 100**
**Assertion Pass Rate: 21/23**

**Static Score: 93/100** | **Final Score: 90/100 — ⭐ Production Ready — deployable, no veto**

> **Note for reviewer:** the two ⚠️ rows are the same finding seen twice (Input 3 discovers it,
> Input 5 confirms it's isolated): SKILL.md's claim that GMM-Demux's SSD-mtx writer "always" fails
> did not reproduce on my run. This is a P2 documentation overclaim, not a functional defect — the
> underlying advice ("check GMM_full.csv, not exit code") remains correct regardless.

---

## Detailed Outputs

### Input 1 — Canonical (P0 regression): hashsolo 2-hashtag fix, fresh data

**Prompt:** "I have exactly 2 hashtags in my scanpy AnnData with raw HTO counts in `adata.obs`. Use
hashsolo to assign each cell to its sample."

**What ran:** `run/reaudit_20260919/gen_fresh_2tag.py` (750 cells, seed 919200226) →
`baseline_unfixed_hashsolo.py` (pre-fix pattern) → `fixed_hashsolo.py` (post-fix pattern, 2 runs for
determinism).

**Output:**
```
BASELINE (unfixed, no number_of_noise_barcodes):
  Classification: 750 Negative / 750 (100%)
  Global class agreement with ground truth: 85 / 750 = 0.113

FIXED (number_of_noise_barcodes=1):
  Classification: TAG_2 351, TAG_1 331, Doublet 44, Negative 24
  Global class agreement: 689 / 750 = 0.919
  Singlet sample-ID agreement: 621 / 621 = 1.000
  Determinism check (2 runs): classifications identical = True
```

**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100

**Assertions:**
- [PASS] Fixed pattern correctly assigns singlet samples for the large majority of true singlets — 100% singlet sample-ID agreement
- [PASS] The pre-fix pattern still reproduces the original silent 100%-Negative failure on fresh data — confirms a generalizable defect, not an artifact of the original auditor's specific dataset
- [PASS] SKILL.md documents the degeneracy with a concrete threshold check — paragraph, code guard, parameter-reference row, Common Errors row all present
- [PASS] Fixed output is deterministic across repeated runs
- [PASS] Fix generalizes beyond the fixer's own test data — independent seed/cell count

---

### Input 2 — Edge (P1 regression): demuxmix crash-guard, fresh underdispersed data

**Prompt:** "My demuxmix call is throwing an R error on underdispersed HTO background. How do I handle
this without losing the run?"

**What ran:** `demuxmix_crash_test2.R` (600 cells, near-constant background, seed 90210) →
`demuxmix_crash_test3.R` (manual `clusterInit` alone vs. the fixed `tryCatch` guard) →
`demuxmix_naive_determinism.R` (2 runs of the guard's `model='naive'` path).

**Output:**
```
Raw demuxmix() call: CAUGHT ERROR: missing value where TRUE/FALSE needed

Manual clusterInit alone (correct list format per ?demuxmix):
  CAUGHT ERROR with manual clusterInit: missing value where TRUE/FALSE needed
  -> clusterInit alone does NOT avoid the crash (matches the fixer's claim)

Fixed guard (tryCatch -> model='naive'):
  demuxmix regression fit failed (...); retrying with model="naive"
  Warning: Not all models converged. Do not use the classification results.
  HTO call table: HX 127, HX,HY 15, HX,HZ 12, HY 117, HY,HZ 3, HZ 133, negative 293

Naive-fallback determinism (2 runs): identical = TRUE
```

**Scores:** Basic: 37/40 | Specialized: 55/60 | Total: 92/100

**Assertions:**
- [PASS] Underdispersion crash reproduces on fresh, independently-generated data
- [PASS] Fixed `tryCatch` guard recovers via `model='naive'` instead of crashing
- [PASS] Manual `clusterInit` alone does NOT avoid this crash, as the fixer's log specifically claims — independently verified with the documented `clusterInit` format
- [PASS] `dmmClassify()`'s convergence warning is surfaced and the Skill tells the agent to check it
- [PASS] Naive-fallback output is deterministic across repeated runs

---

### Input 3 — Variant A (new tool coverage): GMM-Demux CLI, end to end

**Prompt:** "I want explicit multi-sample-multiplet accounting from my 4-tag HTO CSV, independent of
Seurat/scanpy. Run GMM-Demux."

**What ran:** `gen_fresh_4tag.py` (1000 cells, seed 31337) → float-cast per the Skill's caveat →
`GMM-demux.exe -c hto_4tag_fresh_gmm_input.csv G_A,G_B,G_C,G_D -f gmm_out` (2 runs for determinism).

**Output:**
```
Run: exit 0, GMM_full.csv (15067 bytes) + GMM_full.config + SSD_mtx/{barcodes,features,matrix} all
written successfully (no failure on the mtx-writer step this run).
Global class agreement: 1000/1000 = 1.000
Singlet sample-ID agreement: 840/840 = 1.000
2-run determinism: identical Cluster_id column
```

**Scores:** Basic: 37/40 | Specialized: 53/60 | Total: 90/100

**Assertions:**
- [PASS] CLI runs end-to-end per the Skill's documented pattern
- [PASS] Classification matches ground truth (global + singlet sample-ID)
- [PASS] The float-dtype CSV caveat is accurate and necessary
- [PASS] Output is deterministic across repeated runs
- [FAIL] The SSD-mtx writer "always" fails after classification, as SKILL.md states — my run exited 0 and wrote it successfully; "always" overclaims (P2)

---

### Input 4 — Variant B (P1 verification): demuxEM/pegasus Windows build-failure claim

**Prompt:** "Is the demuxEM/pegasus example in this Skill actually runnable here, or should I expect
it to fail?"

**What ran:** `pip install --no-cache-dir pegasusio` inside the fixer's own
`tools/demuxem-venv/`, a fresh install attempt (no cached artifacts reused).

**Output:**
```
io_funcs.c
ext_modules/io_funcs.c(21781): warning C4013: 'getline' undefined; assuming extern returning int
...
io_funcs.obj : error LNK2001: unresolved external symbol getline
... : fatal error LNK1120: 1 unresolved externals
error: Command '[...link.exe...]' returned non-zero exit status 1120.
Failed to build pegasusio
```
Post-attempt `pip list` confirmed numpy 1.26.4 / scipy 1.13.1 / scikit-learn 1.5.2 / GMM-Demux 0.2.2.3
unchanged.

**Scores:** Basic: 37/40 | Specialized: 52/60 | Total: 89/100

**Assertions:**
- [PASS] pegasusio genuinely fails to build on Windows with the documented error
- [PASS] The failure is a platform incompatibility (POSIX-only `getline`, no MSVC equivalent), not a missed install step
- [PASS] The failed build attempt did not corrupt the shared GMM-Demux venv
- [PASS] SKILL.md accurately discloses this limitation inline rather than shipping a broken example

---

### Input 5 — Stress: documentation-accuracy audit across the fix

**Prompt (self-directed review):** cross-check every claim the fix added against Inputs 1-4's real
execution evidence.

**Output:** hashsolo and demuxmix claims (thresholds, error messages, remedies, warnings) all matched
exactly. `usage-guide.md`'s Tips section points to `SKILL.md` rather than restating it — no redundant
duplication introduced. One inaccuracy found: GMM-Demux's "always fails" mtx-writer claim (Input 3).

**Scores:** Basic: 32/40 | Specialized: 44/60 | Total: 76/100

**Assertions:**
- [PASS] hashsolo and demuxmix Common Errors / threshold-reference entries accurately reflect verified behavior
- [FAIL] GMM-Demux Common Errors / prose entry accurately reflects verified behavior — see Input 3
- [PASS] `usage-guide.md` avoids restating `SKILL.md` content added by the fix
- [PASS] The fix introduces no new scope violations or fabricated claims

---

## Veto Gates

**Skill Veto:** PASS on all four (T1 Stability, T2 Contract, T3 Determinism — independently verified
for all 3 fixed code paths, T4 Security).

**Research Veto (Category 3 — Data Analysis):** PASS on all four (M1 Scientific Integrity, M2 Practice
Boundaries, M3 Methodological Ground, M4 Code Usability — all executed code ran to completion on fresh
data).

## Final

```
Static Score   : 93/100 x 40% = 37.2
Dynamic Score  : 88.2/100 x 60% = 52.9
FINAL SCORE    : 90 / 100
GRADE          : ⭐ Production Ready
Deployable     : true
Veto override  : false
```

P0 status: **the P0 is resolved.** No open P0 or P1. Two P2s recorded (GMM-Demux "always fails"
overclaim; no bundled example dataset) — neither blocks promotion.
