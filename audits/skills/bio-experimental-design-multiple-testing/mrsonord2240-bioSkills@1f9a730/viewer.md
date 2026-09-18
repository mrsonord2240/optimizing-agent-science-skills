> **Audit record for `bio-experimental-design-multiple-testing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@1f9a730](https://github.com/mrsonord2240/bioSkills/tree/1f9a7307f1ea83733cc63c66e46ce697c05a7069/experimental-design/multiple-testing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-18 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-experimental-design-multiple-testing (RE-AUDIT of a fixed Skill)

Generated: 2026-09-18
Source: `mrsonord2240/bioSkills@1f9a730:experimental-design/multiple-testing` (fork worktree `F:\OpenScience\wt\ed-mtc`, branch `fix/ed-mtc`)
Prior audit (pre-fix, archived): `F:\OpenScience\audits\_pre-fix-20260918\bio-experimental-design-multiple-testing\` — score **82, Beta Only, not deployable** (assertion pass rate 21/33 = 63.6%, below the 80% Limited-Release floor; no P0s, 4 open P1s)
Fix log (claims, verified independently below, not taken on faith): `F:\optimizing-agent-science-skills\fixes\bio-experimental-design-multiple-testing.md`

I am a different agent from both the original auditor and the fixer, with no stake in this Skill
passing. Every number below comes from a script in `runs/`, run in this session against the
fixed Skill copied out of the fork worktree into a scratch execution area (never executed
in-place inside the worktree or `F:\OpenScience\external\`). All synthetic data
(`data/make_synthetic.py`, seed 20260918) was regenerated fresh for this re-audit — different
seed, and for two inputs a different simulation construction, than either the pre-fix audit's
or the fixer's own data — specifically so this score is not just re-measuring what the fixer was
told about.

Category: **3 — Data Analysis** · Execution mode: **A (Direct)** · Complexity: **Complex → N = 7** · Executed: **7 / 7**

## Environment

| | |
|---|---|
| R | 4.4.3 / Bioconductor 3.20 — qvalue **2.38.0**, IHW **1.34.0** — via `F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\r.sh` (never bare Rscript) |
| Python | 3.12.13 (venv in the same shared env) — statsmodels **0.15.0**, scipy 1.18.1, numpy 2.5.3, pandas 3.0.5 |

No package versions changed in the shared env; nothing was installed for this re-audit.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical — BH + q-value, fresh 18k-gene table | 38 | 55 | **93** | 4/5 | ✅ |
| 2 | Variant A — BH vs BY dependence, independent re-run | 37 | 54 | **91** | 5/5 | ✅ |
| 3 | Edge — small-family q-value: default vs bootstrap vs lambda=0 fix | 37 | 53 | **90** | 5/5 | ✅ |
| 4 | Variant B — IHW crash-rate regression + retry/fallback pattern | 34 | 46 | **80** | 4/5 | ⚠️ |
| 5 | Stress — FCR-adjusted CIs, verbatim code, fresh selected set | 37 | 54 | **91** | 4/4 | ✅ |
| 6 | Scope Boundary (NEW) — IHW nbins=1 literally collapses to BH | 36 | 50 | **86** | 3/3 | ✅ |
| 7 | Adversarial (NEW) — user proposes bootstrap; does guidance hold? | 35 | 50 | **85** | 4/4 | ✅ |

**Execution Average: 88.0 / 100** · Layer 1 avg 36.3/40 · Layer 2 avg 51.7/60
**Assertion Pass Rate: 29 / 31 (93.5%)**

## Veto gates

**Skill Veto — PASS.** Stability PASS (every code block runs; the IHW one-liner's crash is a
known, documented, mitigated probabilistic risk in an external LP solver, not the Skill's own
logic looping or crashing uncontrollably — same judgment call the pre-fix audit made). Contract
PASS (frontmatter unchanged and complete: `name`, `description` ~1000 chars ending in a "Use
when" trigger, `tool_type: mixed`, `primary_tool: qvalue`, `goal_approach_exempt: true`). 261
lines, well under the 500-line cap (up from 192 pre-fix — entirely new failure-mode and FCR
content). Determinism PASS (pure functions of the p-value vector; the shipped example sets a
seed). Security PASS — grep for `eval(`, `exec(`, `system(`, `rm -rf`, credentials, tokens and
URLs across all three files returns one hit, `unlink()` (R tempfile cleanup, benign); the new
`system2()` child-process call passes a fixed, non-user-controlled expression string, not raw
user input.

**Research Veto (Category 3, applicable) — PASS** on all four dimensions, detailed in the JSON.
The biggest change from the pre-fix audit: **Methodological Ground** was PASS-with-a-flagged-
miscalibration before (the BH/BY dependence claim didn't match simulation); it is now a clean
PASS because the rewritten section is independently reproduced as accurate (Input 2).

**Gate 8 (shipped-means-present) — PASS.** All seven qualified sibling-skill paths re-verified to
exist in the fork at commit `1f9a730`; `examples/multiple_testing_correction.R` still exists but
is still never referenced by `SKILL.md` or `usage-guide.md` (unchanged progressive-disclosure gap).

## Static Evaluation — 90 / 100 (pre-fix: 84)

| Category | Score | Driver |
|---|---|---|
| Functional Suitability | 10/12 | FCR gap closed with real code; local FDR and IDR still underspecified relative to the description |
| Reliability | 11/12 | The three previously-undocumented failure modes (q-value, IHW, BH/BY) are now accurate and tested; IHW's residual crash risk is the one open weakness |
| Performance & Context | 7/8 | 261 dense lines, growth is all substantive |
| Agent Usability | 15/16 | Decision tree/taxonomy now internally consistent with corrected claims; `de_table` still undefined in the IHW snippet |
| Human Usability | 7/8 | q-value section now states its own family-size floor with a working fallback in the same block |
| Security | 10/12 | New child-process pattern introduces no injection surface; no independence diagnostic shipped, unchanged |
| Maintainability | 11/12 | IHW section now genuinely testable via the shipped retry pattern; the shipped example's misleading BH seed (P2) remains untouched by design |
| Agent-Specific | 19/20 | Routing unchanged and excellent; progressive-disclosure gap for examples/ persists |

## Synthetic data (independently regenerated for this re-audit)

`data/make_synthetic.py`, seed 20260918. All SYNTHETIC; gene/term IDs prefixed `REGENE`/`REGO` so
nothing can be mistaken for real data. Deliberately different generator from both the pre-fix
audit's `make_synthetic.py` and the fixer's own scripts.

```
REAUDIT SYNTHETIC DE table: (18000, 4) | true alternatives: 1500 | pi0(true) = 0.9167
raw p<0.05: 2185 | null p<0.05 (expect ~825): 812
corr(mean_expression, pvalue | null) = 0.0103
REAUDIT all-null GO set: 40 terms, min p = 0.0134
```

---

## Detailed Outputs

### Input 1 — Canonical (regression of pre-fix Input 1, independent data)

**Prompt:** "I've got p-values for 18,000 genes from a knockout RNA-seq experiment
(`de_pvalues_reaudit.csv`, column `pvalue`). Apply Benjamini-Hochberg at FDR 0.05, and also give
me Storey q-values with pi0 so I can see whether it's worth switching."

**Code** (`runs/input1_bh_qvalue.R`, following SKILL.md's "FDR — Benjamini-Hochberg and the
q-value" verbatim):

```r
padj <- p.adjust(pvalues, method = 'BH')
library(qvalue)
qobj <- qvalue(pvalues)
q <- qobj$qvalues
lfdr <- qobj$lfdr
```

**Output** (`runs/input1_bh_qvalue.log`, exit 0):

```
true pi0 = 0.9167
BH discoveries at FDR 0.05: 1006
qvalue estimated pi0: 0.9351
Storey q-value discoveries q<0.05: 1023
BH q<=0.05             R= 1006 true+=  966 false+=   40 realized FDP=0.0398 power=0.6440
Storey q<0.05          R= 1023 true+=  982 false+=   41 realized FDP=0.0401 power=0.6547
local FDR < 0.20       R=  987 true+=  950 false+=   37 realized FDP=0.0375 power=0.6333
Bonferroni 0.05        R=  117 true+=  117 false+=    0 realized FDP=0.0000 power=0.0780
```

Everything held on fresh, independently generated data. The lfdr-thresholding gap from the
pre-fix audit is unchanged and unaddressed by this fix pass (it wasn't one of the 4 P1s).

**Scores:** Basic 38/40 | Specialized 55/60 | **Total 93/100**

**Assertions:** 4/5 PASS — the one FAIL is the same as pre-fix (no lfdr threshold rule given).

---

### Input 2 — Variant A (regression of pre-fix Input 2, independent seed and construction)

**Prompt:** "My genes sit in co-regulated modules so test statistics aren't independent. Is BH
still valid or do I need BY? I'd rather not lose power if I don't have to."

**Code** (`runs/input2_dependence.py`): 300 replicates per dependence structure (independent,
positive-block rho=0.8, negative-pair rho=-0.95), m=5000, 500 alternatives, BH and BY via
`multipletests`. Uses a z-score-based p-value generator, deliberately different from both the
pre-fix audit's and the fixer's own beta-distribution constructions.

**Output** (`runs/input2_dependence.log`, exit 0):

```
structure       method    meanFDP   sdFDP  P(FDP>0.10)   power   meanR
independent     fdr_bh     0.0446  0.0114        0.000  0.5974   312.7
independent     fdr_by     0.0048  0.0061        0.000  0.2830   142.2
positive_block  fdr_bh     0.0382  0.0516        0.130  0.5976   312.0
positive_block  fdr_by     0.0050  0.0199        0.017  0.2771   139.3
negative_pair   fdr_bh     0.0446  0.0151        0.000  0.5963   312.1
negative_pair   fdr_by     0.0052  0.0076        0.000  0.2812   141.4

statsmodels 0.15.0 default rejections: 60 vs explicit fdr_bh: 297
```

This is the clearest before/after: the pre-fix audit's two assertion FAILs on this input were
both testing the OLD, now-corrected claim ("realized FDR exceeds nominal under negative
dependence"). The rewritten SKILL.md text states the true finding — mean holds, variance widens,
BY costs ~50% power — and this independent run (different seed, different p-value generator,
different rep count) reproduces it: mean FDP never exceeds ~0.045, SD(FDP) rises 0.0114→0.0516
under positive dependence, and BY's power drops from ~0.597 to 0.283 (52.6% loss, matching "~50%").

**Scores:** Basic 37/40 | Specialized 54/60 | **Total 91/100**

**Assertions:** 5/5 PASS — up from 3/5 pre-fix.

---

### Input 3 — Edge (regression of pre-fix Input 3, extended to m=10, independent replication)

**Prompt:** "This is small: 30-40 GO terms, and I don't think any are real. What's the right
correction, and can I get q-values? A labmate said if qvalue() errors I should just switch to
`pi0.method='bootstrap'`."

**Code** (`runs/input3_small_family_qvalue.R`, `runs/input3b_stored_table_check.R`): 200 all-null
replicates at m=10, 20, 50, comparing default `qvalue(p)`, `qvalue(p, pi0.method='bootstrap')`,
and the fix's `qvalue(p, lambda=0)`.

**Output** (`runs/input3_small_family_qvalue.log`, exit 0):

```
=== m = 10 ===  default: 120/200 (60.0%) errors | bootstrap: 120/200 (60.0%) errors | lambda=0: 0/200
=== m = 20 ===  default:  67/200 (33.5%) errors | bootstrap:  67/200 (33.5%) errors | lambda=0: 0/200
=== m = 50 ===  default:  21/200 (10.5%) errors | bootstrap:  21/200 (10.5%) errors | lambda=0: 0/200
sample default error:   missing or infinite values in inputs are not allowed
sample bootstrap error: missing values and NaN's not allowed if 'na.rm' is FALSE
```

On the stored 40-term all-null table (`runs/input3b_stored_table_check.log`): BH gives 0
discoveries, `qvalue(lambda=0)` gives pi0=1.0000 and 0 discoveries.

This is the strongest single confirmation in the re-audit of a claim the fix log makes that
sounds almost too clean to be true: bootstrap fails at the **exact same count** as the broken
default at every size tested, just on a different error message — independently reproduced here,
not just re-measured from the fixer's own numbers. The shipped fallback (`lambda=0`) had zero
errors across 600 replicates and always recovered the planted pi0=1.0 exactly.

**Scores:** Basic 37/40 | Specialized 53/60 | **Total 90/100**

**Assertions:** 5/5 PASS — up from 2/4 pre-fix.

---

### Input 4 — Variant B (regression of pre-fix Input 4 — the highest-stakes fix to verify)

**Prompt:** "I have mean expression for all 18,000 genes. Use IHW to weight hypotheses and tell
me how many more discoveries I get than plain BH."

**Regression test 1 — raw crash rate at pinned nbins=5** (`runs/input4a_ihw_single_attempt.R`,
run 12 times as 12 separate R processes since a segfault kills the process outright;
`runs/ihw_crash_rate_nbins5.log`):

```
attempt  1: exit=139   attempt  2: exit=139   attempt  3: exit=0 (OK, 1018 rej)
attempt  4: exit=0     attempt  5: exit=139    attempt  6: exit=0
attempt  7: exit=0     attempt  8: exit=0      attempt  9: exit=139
attempt 10: exit=139   attempt 11: exit=139    attempt 12: exit=0
```

**6/12 = 50% crash rate** — lands exactly inside the SKILL.md's stated 50-75% range and matches
the fix log's own 6/12 check. This independently confirms the crash is real, probabilistic, and
NOT eliminated by pinning nbins low — vindicating the SKILL.md's (and the corrected
`mass-spec-proteomics-analyst/TOOLS.md`'s) weaker, honest claim over the disproven "nbins<=5 is
stable" claim the pre-fix environment doc used to make.

**Regression test 2 — the shipped retry+fallback pattern, run end-to-end multiple times**
(`runs/shipped_example_repeats.log`, `runs/shipped_example_copy.R`): of the completed runs, one
succeeded with IHW on the first or second retry (95 vs BH=93), one exhausted all 3 retries and
printed `IHW did not complete after 3 attempts (solver crash); falling back to BH = 93
discoveries` (exit 0), and a third again succeeded with IHW (95 vs 93). **In every completed run
the parent R session exited 0 — the retry+fallback pattern never let a segfault escape the child
process**, including the run where the solver failed all 3 times.

**What the fix does NOT close:** the bare formula call printed as the primary code example,
`ihw(pvalue ~ mean_expression, data = de_table, alpha = 0.05, nbins = 5)`, still crashes at
~50% if run directly — the safety only exists if the analyst reads the caution comment
immediately above it and uses the wrapped version from `examples/`. This is flagged as a P1 in
the recommendations below (not a veto — the mitigation that exists works, and is documented,
just not made the path of least resistance).

**Scores:** Basic 34/40 | Specialized 46/60 | **Total 80/100**

**Assertions:** 4/5 PASS (one deliberate FAIL: "the bare one-liner is safe to run directly" —
it is not, by design of the assertion, to keep this residual risk visible in the score).

---

### Input 5 — Stress (dedicated regression of the FCR half of pre-fix Input 7)

**Prompt:** "I selected my hits at BH-FDR 0.05. Can I just report the usual 95% CIs for those, or
does selecting on significance mess with the intervals?"

**Code** (`runs/input5_fcr_ci.R`) — the SKILL.md "False Coverage Rate" block, copied verbatim,
against a freshly simulated selected set (m=4000, 400 alternatives, independent of both the
pre-fix audit's and the fixer's own selected sets):

```r
q <- 0.05; R <- sum(padj < q); m <- length(pvalues)
fcr_level <- 1 - q * R / m; alpha_fcr <- 1 - fcr_level
z <- qnorm(1 - alpha_fcr / 2)
ci_lower <- estimate[padj < q] - z * se[padj < q]
ci_upper <- estimate[padj < q] + z * se[padj < q]
```

**Output** (`runs/input5_fcr_ci.log`, exit 0):

```
Selected set R = 45 out of m = 4000
FCR-adjusted level = 0.9994 (z = 3.449) vs naive z = 1.960
naive 95% CI coverage on selected set : 0.6889
FCR-adjusted CI coverage on selected set: 0.9556
```

The P1 that was "named four times, shipped nowhere" now has real, runnable code, and it works:
naive coverage 68.9% → FCR-adjusted 95.6%, close to the 95% nominal target, on data this re-audit
generated independently.

**Scores:** Basic 37/40 | Specialized 54/60 | **Total 91/100**

**Assertions:** 4/4 PASS.

---

### Input 6 — Scope Boundary (NEW — not in the pre-fix audit)

**Prompt (self-directed technical probe, not a user request):** does IHW's nbins formula
literally collapse to a single bin below m~1500, and does IHW then produce numerically identical
output to plain BH, as SKILL.md's Quantitative Thresholds table and IHW failure mode both claim?

**Code** (`runs/input6_nbins1_collapse.R`): m=800 (< 1500 → floor(800/1500)=0), a uniform,
null-independent covariate.

**Output** (`runs/input6_nbins1_collapse.log`, exit 0):

```
Only 1 bin; IHW reduces to Benjamini Hochberg (uniform weights)
nbins used: 1
IHW rejections: 25 | BH rejections: 25 | identical sets: TRUE
max abs diff IHW padj vs BH padj: 0.0000000000
```

The pre-fix audit inferred this behavior by reading IHW's R source; this re-audit triggers it
directly on live data. IHW's own message matches SKILL.md's quote verbatim, and its adjusted
p-values are bit-identical to BH's — the SKILL.md's specific mechanistic claim, not just its
general caution, is literally true.

**Scores:** Basic 36/40 | Specialized 50/60 | **Total 86/100**

**Assertions:** 3/3 PASS.

---

### Input 7 — Adversarial (NEW — not in the pre-fix audit)

**Prompt:** "qvalue(pvalues) keeps erroring on my 30-term GO list. A labmate said
`pi0.method='bootstrap'` is more robust, so I should switch to that instead of BH. Should I?"

**What the fixed SKILL.md tells an agent to say** (see `runs/input7_bootstrap_adversarial.md`
for the full write-up): no — bootstrap is documented in the "q-value fails on small families"
failure mode as failing at a comparable rate to the default, just on a different error; the
Skill recommends `qvalue(p, lambda=0)` or plain BH instead.

**Verification:** this is exactly what Input 3's independent execution found — bootstrap failed
at the identical count to the default estimator (120/200, 67/200, 21/200) on a different error
message, at every family size tested. A response following the PRE-FIX Skill would have had
nothing to say here (no q-value failure mode existed at all) and likely would have let the
labmate's bad advice stand.

**Scores:** Basic 35/40 | Specialized 50/60 | **Total 85/100**

**Assertions:** 4/4 PASS.

---

## Verdict

**Final Score: 89/100 — ⭐ Production Ready — Deployable: true — Veto: none.**

All floors clear: static 90 ≥ 80, execution average 88.0 ≥ 85, Layer 1 average 36.3/40 ≥ 32,
Layer 2 average 51.7/60 ≥ 48, assertion pass rate 29/31 = 93.5% ≥ 90%. This is a genuine,
independently-verified jump from the pre-fix 82 (Beta Only, not deployable) — the pre-fix
downgrade was driven entirely by the assertion pass rate falling below the 80% floor, and this
fix pass closed exactly the gaps that were failing those assertions. All 4 P1s are resolved, two
(IHW crash reduction, q-value bootstrap) honestly and correctly disclosed as partial rather than
complete fixes. Two genuinely new probes (Input 6, Input 7) confirm the fix holds up under
scrutiny the fixer was never given. One new P1 is raised (the bare IHW one-liner is still the
primary code example despite being unsafe to copy directly) and two P2s carry over unfixed by
design (misleading shipped-example seed; local FDR/IDR under-specification).
