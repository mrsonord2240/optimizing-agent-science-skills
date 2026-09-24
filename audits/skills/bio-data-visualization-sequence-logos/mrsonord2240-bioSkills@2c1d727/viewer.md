> **Audit record for `bio-data-visualization-sequence-logos`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@2c1d727](https://github.com/mrsonord2240/bioSkills/tree/2c1d7271a6bfec6c2eebf9b50914e9a3b74f60f3/data-visualization/sequence-logos) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-sequence-logos

Generated: 2026-09-23 · rendered from `report.json` by `tools/render_viewer.py`.

> This viewer is **generated from the audit report**, not written by the auditor. It restates the report's own recorded scores, notes and assertions and adds nothing to them. Where a hand-written viewer would argue from the runs, this one points at the scripts in [scripts/](scripts/) instead.

Source: `mrsonord2240/bioSkills@2c1d7271a6bfec6c2eebf9b50914e9a3b74f60f3:data-visualization/sequence-logos`
Audit type: final-pass backlog remediation
Category: Data Analysis · Execution mode: A · Complexity: Complex · N = 9 · Executed: 9/9 exact-commit vectors

## What the Skill claims to do

Build sequence logos from aligned DNA, RNA, or protein motifs using ggseqlogo (R), Logomaker (Python), or WebLogo with explicit bits vs probability encoding, correctly computed non-uniform-background relative entropy, custom alphabets, and multi-logo stacking.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical regression | 37 | 56 | **93** | 3/3 | yes | ✅ |
| 2 | Canonical regression | 38 | 58 | **96** | 7/7 | yes | ✅ |
| 3 | Variant A regression | 38 | 58 | **96** | 5/5 | yes | ✅ |
| 4 | Variant B regression | 38 | 58 | **96** | 3/3 | yes | ✅ |
| 5 | Edge regression | 36 | 55 | **91** | 4/4 | yes | ✅ |
| 6 | Edge regression | 37 | 56 | **93** | 4/4 | yes | ✅ |
| 7 | Adversarial regression | 38 | 58 | **96** | 3/3 | yes | ✅ |
| 8 | New end-to-end input | 39 | 58 | **97** | 5/5 | yes | ✅ |
| 9 | New environment boundary | 38 | 58 | **96** | 3/3 | yes | ✅ |

**Execution Average: 94.9 / 100** · **Assertion Pass Rate: 37/37**

**Static: 93/100** · Static weighted 37.2 + dynamic weighted 56.9 = **94/100** → ⭐ Production Ready, deployable.

---

## Veto gates

### Skill veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| stability | PASS |  |
| contract | PASS |  |
| determinism | PASS |  |
| security | PASS |  |

### Research veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| scientific integrity | PASS | The claimed non-uniform-background route now computes relative entropy instead of passing an ignored parameter. The 72% GC Streptomyces composition is presented as illustrative, not independently sourced. |
| practice boundaries | PASS | Motif visualization only; no diagnostic or prescriptive claim. |
| methodological ground | PASS | Uniform bits, background relative entropy, signed log-odds, and non-equivalent low-N tool defaults are explicitly separated. |
| code usability | PASS | The exact checkout helper, complete example, Logomaker snippet, and WebLogo DNA/RNA commands completed with the recorded outputs. |

## Static score

| Category | Score | Note |
|---|---|---|
| functional suitability | 12/12 | All three routes distinguish uniform bits from non-uniform-background relative entropy. |
| reliability | 11/12 | Alphabet/background validation and low-N/RNA/dependency limits are explicit. |
| performance context | 7/8 | Reusable helper and small bundled fixtures make the central workflow reproducible. |
| agent usability | 15/16 | Tool choice, current API signatures, and labels agree with the calculation. |
| human usability | 8/8 | Direct prompts, decision table, and concise boundaries are clear. |
| security | 11/12 | No credentials, network operation, or destructive cleanup; outputs are local PDFs. |
| maintainability | 11/12 | The calculation is separately testable and shipped fixture data remove undefined inputs. |
| agent specific | 18/20 | Precise trigger and hand-offs; external package APIs still require version inspection. |

## Input 1 — Canonical regression: Uniform-background ggseqlogo bits route and matrix orientation

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 56/60 · **Total 93/100**
- Execution: run/exact-commit-20260923-200710/uniform_small_n_exact.R; guarded exit 0 with cli_unloaded=TRUE receipt.
- Finding: Exact source preserves letters-as-rows/positions-as-columns and no longer claims a nonexistent background argument.

| Assertion | Result | Evidence |
|---|---|---|
| PWM orientation is stated correctly | PASS | Transposed positions-by-letters input rejects with the expected row-name error. |
| Uniform route remains method='bits' | PASS | Exact n=5 sequence route rendered 1.567191488 bits; matrix route rendered 2.000000000 bits. |
| No functional bg_freq call remains | PASS | Exact-source search. |

## Input 2 — Canonical regression: Custom relative-entropy ggseqlogo route

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 58/60 · **Total 96/100**
- Execution: run/exact-commit-20260923-200710/examples/test_relative_entropy_logo.R; exit 0 with process-local guard.
- Finding: Exact helper checks passed, including numerical calibration, malformed backgrounds, and the rendered custom-stack height.

| Assertion | Result | Evidence |
|---|---|---|
| Human-background pure C totals -log2(.21) | PASS | 2.251538767 bits. |
| Background-matched column totals zero | PASS | No NaN or invented height. |
| Mixed letters use p_i D_KL | PASS | Exact helper comparison. |
| Uniform background equivalence holds | PASS | Exact helper comparison. |
| GC calibration and scale invariance hold | PASS | Pure G 1.643856190; pure A 2.473931188. |
| Missing, duplicate, and extra symbols reject | PASS | Expected errors. |
| ggseqlogo stack reaches calculated custom height | PASS | ggplot build comparison. |

## Input 3 — Variant A regression: Logomaker information and signed-weight snippets

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 58/60 · **Total 96/100**
- Execution: run/exact-commit-20260923-200710/logomaker_exact.py; exit 0.
- Finding: Exact current-code checks passed under Logomaker 0.8.7 and produced both PNGs.

| Assertion | Result | Evidence |
|---|---|---|
| Information matrix matches relative entropy | PASS | Exact checker assertion. |
| Pseudocount is explicitly zero | PASS | Exact checker assertion. |
| Logo binds to supplied axes | PASS | Exact checker assertion. |
| Signed weight route is valid | PASS | Exact checker assertion. |
| Information and weight PNGs render | PASS | Both files present. |

## Input 4 — Variant B regression: WebLogo DNA and RNA commands

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 58/60 · **Total 96/100**
- Execution: run/exact-commit-20260923-200710/weblogo_exact.sh; exit 0.
- Finding: Exact commands passed under WebLogo 3.7.12; both declared artifacts are non-empty.

| Assertion | Result | Evidence |
|---|---|---|
| DNA command writes PDF | PASS | weblogo_dna.pdf, 5,535 B. |
| RNA command selects RNA mode and writes PNG | PASS | weblogo_rna.png, 3,624 B. |
| Windows Ghostscript boundary remains disclosed | PASS | Exact-source inspection. |

## Input 5 — Edge regression: Tool-specific small-N behavior

- Status: ✅ COMPLETED · Basic 36/40 · Specialized 55/60 · **Total 91/100**
- Execution: run/exact-commit-20260923-200710/uniform_small_n_exact.R, logomaker_exact.py, and weblogo_exact.sh; all exact-commit checks exit 0.
- Finding: The exact source now distinguishes ggseqlogo sequence/matrix behavior, Logomaker pseudocounts, and WebLogo priors rather than calling them one correction.

| Assertion | Result | Evidence |
|---|---|---|
| ggseqlogo sequence and matrix paths are distinguished | PASS | Exact n=5 heights were 1.567191488 for sequences and 2.000000000 for a counts matrix. |
| Logomaker default is identified as pseudocount, not Schneider | PASS | Exact n=5 default was 0.553383332 bits versus 2.000000000 with pseudocount=0. |
| WebLogo prior/weight is disclosed | PASS | Exact n=5 default and --weight 0 logodata outputs differed. |
| N<5 is exploratory rather than authoritative | PASS | Exact-source failure-mode guidance. |

## Input 6 — Edge regression: Alphabet and malformed-input boundaries

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 56/60 · **Total 93/100**
- Execution: Helper checks in input 2 plus exact WebLogo RNA execution in input 4.
- Finding: Exact helper validation rejects incompatible symbols/backgrounds; exact WebLogo evidence covers the RNA route.

| Assertion | Result | Evidence |
|---|---|---|
| Unknown sequence symbols reject | PASS | Helper validation. |
| Missing/duplicate/extra background names reject | PASS | Helper test. |
| RNA WebLogo path renders | PASS | Input 4 exact PNG. |
| Matrix orientation is explicit for both R and Python | PASS | Exact-source inspection. |

## Input 7 — Adversarial regression: Non-uniform-background bias direction

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 58/60 · **Total 96/100**
- Execution: Exact helper calibration plus exact-source inspection.
- Finding: The exact helper calibration and corrected prose agree: uniform bits understate rare true-background letters and overstate common ones.

| Assertion | Result | Evidence |
|---|---|---|
| Human C=.21 is taller than 2 uniform bits | PASS | 2.251538767 bits. |
| Human A=.29 is lower than 2 uniform bits | PASS | Documented 1.786 bits. |
| Streptomyces composition is illustrative, not independently sourced | PASS | Exact-source wording. |

## Input 8 — New end-to-end input: Self-contained shipped-example execution

- Status: ✅ COMPLETED · Basic 39/40 · Specialized 58/60 · **Total 97/100**
- Execution: run/exact-commit-20260923-200710/examples/seqlogo_phd.R; exit 0 with process-local guard.
- Finding: The formerly incomplete example ran from a clean exact checkout using bundled fixtures and produced exactly its four stated PDFs.

| Assertion | Result | Evidence |
|---|---|---|
| All required FASTA fixtures are bundled | PASS | DNA, three multi-logo, and protein inputs. |
| N labels are derived from loaded data | PASS | Exact-source inspection. |
| Four declared PDFs are non-empty | PASS | 32,818 / 38,993 / 24,722 / 24,749 B. |
| No Rplots.pdf is emitted | PASS | Artifact check False. |
| Custom and uniform panels are truthfully distinguished | PASS | Exact-source inspection plus successful render. |

## Input 9 — New environment boundary: Windows ggseqlogo CLI teardown containment

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 58/60 · **Total 96/100**
- Execution: run/exact-commit-20260923-200710 exit-codes.txt and guard receipts.
- Finding: The process-local guard yields clean helper and example exits and receipts prove the cli package was unloaded; no global profile was changed.

| Assertion | Result | Evidence |
|---|---|---|
| Helper test exits zero under the process-local profile | PASS | helper_exit=0; cli_unloaded=TRUE. |
| Example exits zero under the process-local profile | PASS | example_exit=0; cli_unloaded=TRUE. |
| Guard is not a shipped/global skill requirement | PASS | Exact checkpoint and source inspection. |

## Key strengths

- The silent ggseqlogo background-correction defect is replaced by an executable and numerically tested relative-entropy route.
- The exact checkout's self-contained example emitted all declared PDFs without a stray device output.
- Exact current-code Logomaker and WebLogo regressions cover the corrected API and RNA paths.
