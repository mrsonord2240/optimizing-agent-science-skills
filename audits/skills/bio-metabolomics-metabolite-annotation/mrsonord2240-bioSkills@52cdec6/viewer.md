> **Audit record for `bio-metabolomics-metabolite-annotation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@52cdec6](https://github.com/mrsonord2240/bioSkills/tree/52cdec64082fb7a3bc2d84e9d7cf5c05a5fdf9f1/metabolomics/metabolite-annotation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-metabolomics-metabolite-annotation (Phase 2 final pass)

Generated: 2026-09-23
Source: mrsonord2240/bioSkills@52cdec64082fb7a3bc2d84e9d7cf5c05a5fdf9f1:metabolomics/metabolite-annotation
Branch: fix/metabolomics-metabolite-annotation
Category: Data Analysis | Mode: D | Complexity: Moderate (N=7)
Independence: auditor_independent: false — final pass: fixed and audited under one brief, see CHECKPOINT.md

The prior 2026-09-16 report, viewer, and run evidence were preserved at F:\OpenScience\audits\_pre-final-pass-20260923\bio-metabolomics-metabolite-annotation\. Fresh synthetic fixtures and all scripts/logs are under run\finalpass_20260923\. No source-tree fixture was modified.

## Final result

| Measure | Result |
|---|---:|
| Static score | 93 / 100 |
| Execution average | 91.3 / 100 |
| Final score | 92 / 100 |
| Layer 1 average | 37.1 / 40 |
| Layer 2 average | 54.1 / 60 |
| Assertion pass rate | 23 / 26 (88.5%) |
| Skill Veto / Research Veto | PASS / PASS |
| Grade | ✅ Limited Release |
| Deployable | true |

The numerical score and all structural/execution floors meet Production Ready, but the 88.5% assertion rate is below the 90% floor. The final grade is therefore downgraded one tier to Limited Release. There are no P0s or vetoes.

## Fresh execution summary

| Input | Executed | Basic /40 | Specialized /60 | Total | Assertions | Result |
|---|---|---:|---:|---:|---:|---|
| 1. Canonical matchms plus precursor regression | yes | 36 | 53 | 89 | 3/4 | single-hit label defect |
| 2. SIRIUS chain | no | 32 | 43 | 75 | 2/3 | login-gated |
| 3. MetFrag shipped data plus malformed CSV | yes | 39 | 57 | 96 | 4/4 | pass |
| 4. Evidence-to-level helper | yes | 39 | 58 | 97 | 4/4 | pass |
| 5. Genuine isomer tie | yes | 39 | 57 | 96 | 4/4 | pass |
| 6. No false tie | yes | 36 | 53 | 89 | 2/3 | single-hit label defect |
| 7. Shipped example, byte-identical | yes | 39 | 58 | 97 | 4/4 | pass |

Executed: 6/7. Input 2 is explicitly unexecuted because TOOLS.md records that SIRIUS 6 requires an academic-account login and none was authorized. The command artifact is run\finalpass_20260923\input2_sirius_chain_unexecuted.sh.

## Input 1 — canonical matchms CLI and precursor regression

Fresh MGF fixtures invoked the byte-identical audited match_library.py:

    citrate 0.9995875520642652 7
    query_no_overlap -> no confident candidate -> Level 5

This confirms the zero-overlap repair works. It also exposes a P1: the single-hit output has no "-> Level 2a", though SKILL.md and the script header promise a Level 2a call.

The fresh companion test verified the current precursor timing:

    WARNING: add_precursor_mz: No precursor_mz found in metadata.
    WARNING: _precursor_validation: Precursor_mz must be int or float.
    ASSERTIONS: add_precursor_mz returned with a warning; ModifiedCosine scoring then raised the documented Precursor_mz missing AssertionError.

Evidence: input1_library_cli_assert.py, input1_precursor_check.py, out\input1_cli.log, out\input1_precursor.log.

## Input 2 — SIRIUS chain

Not executed. The Skill correctly states the account/login prerequisite and distinguishes the ZODIAC formula from an uncalibrated structure result, but a live SIRIUS session was unavailable. This is recorded as unexecuted evidence, not a successful run.

## Input 3 — MetFrag wrapper

The exact-tip shell wrapper ran through MetFragCommandLine 2.6.1 with shipped worked data:

    Stored 3 candidate(s)
    candidates in .../citrate_test.csv: 3
    ASSERTIONS: 3 rows; citrate/isocitrate tie at Score=1.0; glucose below tie.

A fresh malformed CSV demonstrated the guard:

    Stored 0 candidate(s)
    ERROR: 0 candidates stored in .../bad_csv.csv (check CSV quoting)
    ASSERTIONS: malformed unquoted InChI CSV triggers wrapper exit 1 instead of silent success.

Evidence: input3_metfrag_assert.ps1, run_metfrag.sh, out\input3.log.

## Inputs 4–7

Input 4 ran every confidence helper branch: Level 1 standard, Level 2a library hit, Level 2b diagnostic evidence, Level 3 candidate set, Level 4 formula, and Level 5 bare feature. The high-score two-peak case correctly did not promote.

Input 5 executed a genuine matchms isomer tie:

    ['citrate', 'isocitrate'] tied -> Level 3 (isomer wall)

Input 6 used related malate and succinate references. Citrate was the only passing candidate at 0.9997151582503054 and seven matches, proving no false tie; it also repeated the P1 missing-Level-2a output.

Input 7 was byte-compared to the exact-tip shipped example before it ran:

    query_strong -> hippuric_acid score=1.00 matches=7 level=2a
    query_promiscuous -> hippuric_acid score=0.78 matches=2 level=3

Its shipped assertions passed. Evidence is in input4_assign_level.py, input5_tie_cli_assert.py, input6_no_false_tie_cli_assert.py, input7_shipped_example_assert.py and their out logs.

## Veto review

- T1 stability: PASS — six runnable paths completed with expected assertions.
- T2 contract: PASS — no fixed JSON API is claimed. The CLI single-hit omission is a P1 feedback defect, not malformed required schema.
- T3 determinism: PASS — deterministic synthetic fixtures yielded expected matching, tie, and level results.
- T4 security: PASS — no secrets, raw code execution, or unsafe shell expansion.
- M1 scientific integrity: PASS — outputs preserve confidence limits.
- M2 practice boundaries: PASS — no individual diagnosis or prescription.
- M3 methodological ground: PASS — ties are capped at Level 3 and ambiguous results are not presented as identifications.
- M4 code usability: PASS — Python compiled, shell passed bash -n, and all runnable paths executed.

## Recommendation

### P1 — emit Level 2a in the CLI single-hit branch

scripts/match_library.py advertises a confidence call, but its len(passing) == 1 branch prints only compound, score, and matched-peak count. Change that print statement to include "-> Level 2a" and add a shipped CLI assertion checking it. This closes both failed assertions and restores the Production Ready assertion-rate floor.
