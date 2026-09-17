> **Audit record for `bio-crispr-screens-library-design`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6847328](https://github.com/mrsonord2240/bioSkills/tree/684732876d2781df75d90ba35c3e9949ff4f28b2/crispr-screens/library-design) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-library-design (RE-AUDIT, post-fix)
Generated: 2026-09-16
Source: `mrsonord2240/bioSkills@6847328:crispr-screens/library-design`
Pre-fix report: `F:\OpenScience\audits\_pre-fix-20260916\bio-crispr-screens-library-design\` (final 81, Limited Release)
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-crispr-screens-library-design.md`
Category: Protocol Design | Execution Mode: D (Hybrid) | Complexity: Complex (N=8: 6 regression of the pre-fix audit's inputs, 2 new -- Input 5 real-gene/live-NCBI, Input 8 new Cas12a chemistry)
Environment: `F:\OpenScience\audit-envs\crispr-screen-analyst` (per `TOOLS.md`, 2026-09-16 build)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 54 | 92 | 5/5 PASS | ✅ |
| 2 | Variant A | 36 | 52 | 88 | 4/4 PASS | ✅ |
| 3 | Variant B | 36 | 53 | 89 | 5/5 PASS | ✅ |
| 4 | Edge | 36 | 54 | 90 | 4/5 PASS | ✅ |
| 5 | Edge (real gene, NEW) | 38 | 56 | 94 | 5/5 PASS | ✅ |
| 6 | Stress | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 7 | Scope Boundary | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 8 | Adversarial (Cas12a, NEW) | 34 | 46 | 80 | 4/4 PASS | ✅ |

**Execution Average: 90.0 / 100**
**Assertion Pass Rate: 35/36 (97.2%)**
**Static Score: 93/100** | **Final Score: 93×0.4 + 90.0×0.6 = 37.2 + 54.0 = 91 → ⭐ Production Ready**

**Skill Veto:** PASS (T1–T4 all PASS) | **Research Veto (Protocol Design):** PASS (M1–M4 all PASS)

**vs. pre-fix:** 81 (Limited Release) → 91 (Production Ready). Both P1s resolved and independently re-verified; all four P2s resolved; one genuinely new minor gap found (lowercase input handling, Input 4).

---

## Detailed Outputs

### Input 1 — Canonical: Cas9 KO library, 8 synthetic DDR genes (regression, new seeds)

**Prompt:** "Design a focused Cas9 KO library targeting ATM, ATR, BRCA1, BRCA2, CHEK1, CHEK2, PARP1, RAD51. Use Rule Set 2/Azimuth-style on-target scoring and the documented off-target/positional filters, 4 guides/gene, plus controls."

**Code executed** (verbatim from the fixed SKILL.md's "Score and Rank sgRNAs for a Target Gene" section, including the new `select_independent_guides`):
```python
def select_independent_guides(candidates_df, n_guides, min_spacing=5, score_col='score'):
    ranked = candidates_df.sort_values(score_col, ascending=False)
    selected = []
    for _, cand in ranked.iterrows():
        if any(abs(cand['pos_in_cds'] - s['pos_in_cds']) < min_spacing for s in selected):
            continue
        selected.append(cand)
        if len(selected) == n_guides:
            break
    return pd.DataFrame(selected)
```

**Output (stdout, full):**
```
Genes requested: 8; genes with <4 guides after independence filter: []
Total targeting guides: 32
Total library rows (targeting + controls): 91
type
non-targeting           50
targeting               32
essential-control        4
nonessential-control     4
safe-harbor              1
Per-gene minimum pairwise spacing (pos_in_cds): [('ATM', 32), ('ATR', 26), ('BRCA1', 25), ('BRCA2', 23), ('CHEK1', 67), ('CHEK2', 86), ('PARP1', 15), ('RAD51', 24)]
ASSERT PASS: every gene's selected guides are >=5nt apart
ASSERT PASS: all spacers 20nt, all oligos non-empty
```
**Status:** COMPLETED ✅ (executed: true) — Script: `run\input1_cas9_ko.py`

**Scores:** Basic: 38/40 | Specialized: 54/60 | Total: 92/100

**Assertions:**
- [PASS] Output includes a library table with gene, guide sequence, position, control types
- [PASS] select_independent_guides enforces >=5nt spacing for every gene, not just some
- [PASS] Guides restricted to 5–65% of CDS
- [PASS] All requested control types present
- [PASS] No fabricated real-world efficacy/off-target numbers

---

### Input 2 — Variant A: CRISPRi Dolcetto-window library, 5 synthetic lncRNAs (regression)

**Prompt:** "Design a Dolcetto-style CRISPRi library for LINC-A1..E5. Resolve TSS positioning per the Dolcetto window (-50 to +300), 6 guides/gene, ranking toward the +25/+75 optimum."

**Output (stdout, full):**
```
Flags: none
Total guides: 30
gene
LINC-A1    6
LINC-B2    6
LINC-C3    6
LINC-D4    6
LINC-E5    6
Guides landing in the +25..+75 Sanson optimum: 10/30
Guides outside the declared Dolcetto window (should be 0): 0
ASSERT PASS: no guide outside declared window
```
**Status:** COMPLETED ✅ (executed: true) — Script: `run\input2_crispri.py`

**Note:** an initial version of this test script had a coordinate bug (absolute position vs. TSS-relative position) that produced a spurious "30/30 outside window" failure; this was a bug in the audit's own test script, caught and fixed before scoring, not a Skill defect — the Skill's `crispri_window()` itself was correct throughout.

**Scores:** Basic: 36/40 | Specialized: 52/60 | Total: 88/100

**Assertions:** 4/4 PASS (guide counts, window compliance, optimum-band bias, all genes addressed)

---

### Input 3 — Variant B: CRISPRa Calabrese-window library, 4 synthetic TFs (regression)

**Prompt:** "Build a Calabrese-style CRISPRa library targeting -150 to -75 of TSS for TF-A..D, 6 guides/gene."

**Output (stdout, full):**
```
DOC CHECK PASS: SKILL.md crispra_window() docstring now warns about undersupply (fix log P2 item)
Flags: ['TF-A: 0/6 candidates in window', 'TF-B: only 2/6 candidates in window', 'TF-C: only 1/6 candidates in window', 'TF-D: only 5/6 candidates in window']
Total guides: 8
Guides outside declared Calabrese window (should be 0): 0
ASSERT PASS: no guide outside declared window; shortfalls reported explicitly rather than padded
```
**Status:** COMPLETED ✅ (executed: true) — Script: `run\input3_crispra.py`

**Note:** the 75bp Calabrese window undersupplied all 4 TFs this run (different random seeds than pre-fix, where 2/4 were undersupplied) — this is expected, honest behavior from a genuinely narrow window, unchanged by design. What changed is the documentation: `crispra_window()`'s shipped docstring in SKILL.md now explicitly warns "at only 75bp wide, this window routinely fails to contain a full 6-guide quota's worth of PAM sites" — confirmed present by a direct file read in the test script. This reverses the pre-fix audit's one failing assertion for this input.

**Scores:** Basic: 36/40 | Specialized: 53/60 | Total: 89/100

**Assertions:** 5/5 PASS (up from 4/5 pre-fix — the undersupply-warning assertion now passes)

---

### Input 4 — Edge: short/PAM-less synthetic CDS, guide-independence gap (direct P1 regression)

**Prompt:** "Design a Cas9 KO guide set for a short synthetic micro-ORF (43nt CDS) — how many usable guides can you find within the 5–65% CDS window?"

**Output (stdout, key lines):**
```
-- Sub-case A: genuinely PAM-less 44nt CDS --
genuinely PAM-less CDS -> candidates: 0
ASSERT PASS: no crash, 0 candidates as expected

-- Sub-case B: 42nt CDS (pre-fix's near-duplicate case) --
Pre-fix (composition-only) minimum pairwise spacing among raw candidates: 1nt
select_independent_guides(min_spacing=5) selected: 2/4 requested
              spacer  pos_in_cds  score
ATTAGGCTGATCCGGTACTT          15    0.9
GTGGGCCCATTAGGCTGATC           7    0.8
Post-fix minimum pairwise spacing among SELECTED guides: 8nt
ASSERT PASS: all selected guides are >=5nt apart (near-duplicate pair correctly excluded)
SHORTFALL: only 2/4 independent guides available for this 42nt CDS -- correct behavior is to
report the shortfall (as here), not silently pad with overlapping guides.
```

**Supplementary check (`run\malformed_input_check.py`), new finding this round:**
```
lowercase acgt: OK (no exception), 0 candidates
has N ambiguity code: OK (no exception), 4 candidates
garbage char (space/digit): OK (no exception), 4 candidates
empty string: OK (no exception), 0 candidates
```
No crash on any malformed input (confirms the fix log's claim). But the lowercase case is a silent, unexplained empty result — the regex is case-sensitive and there is no `.upper()` normalization or warning. New P2 finding (not in the fix log or pre-fix report).

**Status:** COMPLETED ✅ (executed: true) — Scripts: `run\input4_edge_independence.py`, `run\malformed_input_check.py`

**Scores:** Basic: 36/40 | Specialized: 54/60 | Total: 90/100

**Assertions:** 4/5 PASS — the independence-filter assertion that FAILED pre-fix now PASSES; one new assertion (case-sensitivity) FAILS.

---

### Input 5 — Edge (NEW): Real TP53 CDS (NM_000546.6), live NCBI efetch

**Prompt:** "Verify, on a real gene rather than synthetic data, that the new guide-independence filter both raises the minimum spacing and still fills the quota — and check what happens when it can't."

**This input did not exist in the pre-fix audit**, which used synthetic CDS only. It independently re-verifies the fix log's own primary claim with fresh code (not `verify_spacing_filter.py`, the fixer's own script) and a fresh live fetch.

**Output (stdout, key lines):**
```
Fetched header: >lcl|NM_000546.6_cds_NP_000537.3_1 [gene=TP53] ...
CDS length: 1182 nt
Raw candidates after 5-65% CDS + composition filter: 104

Naive top-12-by-score (NO spacing filter) minimum pairwise gap: 1nt (pairs <5nt apart: 2)
select_independent_guides(min_spacing=5) filled: 12/12 requested
Minimum pairwise gap among SELECTED guides: 5nt
Full pairwise-gap distribution (sorted): [17, 17, 138, 9, 28, 160, 85, 138, 37, 9, 5]
ASSERT PASS: quota filled (12/12) AND every pairwise gap >=5nt -- matches fix log claim exactly

Requesting 161 guides (deliberately > what 104 candidates at min_spacing=5 can supply):
select_independent_guides returned 50 (no crash, no padding, quota under-filled as expected)
ASSERT PASS: even when over-requested, all 50 returned guides remain >=5nt apart
```
**Status:** COMPLETED ✅ (executed: true, live public unauthenticated NCBI E-utilities call) — Script: `run\input5_tp53_real_gene.py`

**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100

**Assertions:** 5/5 PASS

---

### Input 6 — Stress: shipped `examples/design_library.py`, run as-is (direct P1/P2 regression)

**Prompt:** "Run the Skill's own worked example end-to-end and confirm it exercises the documented design method, not a disconnected demo."

**Output (stdout, trimmed):**
```
Target genes: 20
Targeting guides: 80
Total library size: 142
Guide type distribution:
type
targeting            80
non-targeting        50
essential-control    10
safe-harbor           2
Control fraction: 43.7% (demo-scale only -- see NOTE above; real libraries target ~1% NTC)
```
Independent re-check: `pandas.read_csv('library_design.csv')` → 142 rows, 0 NaN in `sequence`, all 20 genes at exactly 4/gene targeting quota.

**Status:** COMPLETED ✅ (executed: true, unmodified from the copied Skill folder) — Command: `run\input6_run_shipped_example.sh`; output: `data\input6_design_library_output.csv`

**Note:** the script now calls `find_sgrna_candidates`/`annotate_exon_position`/`select_independent_guides` against a synthetic per-gene CDS — the actual functions SKILL.md documents — reversing the pre-fix finding that it generated fully random sequences scored by GC content alone. The control-fraction line now carries an inline caveat, reversing the pre-fix uncaveated-43.7% finding.

**Scores:** Basic: 37/40 | Specialized: 55/60 | Total: 92/100

**Assertions:** 4/4 PASS (both assertions that FAILED pre-fix — algorithm match, control-fraction caveat — now PASS)

---

### Input 7 — Scope Boundary: SKILL.md/usage-guide.md Azimuth 2.0 consistency (direct P1 regression)

**Prompt:** "Do SKILL.md and usage-guide.md now agree on whether Azimuth 2.0 is usable? Actually try calling it."

**Output (stdout, full):**
```
DOC CHECK PASS: SKILL.md states Azimuth 2.0 must not be called and no longer instructs
calling azimuth.model_comparison.predict(...)
DOC CHECK PASS: both SKILL.md and usage-guide.md recommend the same alternative
(CRISPick / crisprScore::getAzimuthScores())
DOC CHECK PASS: usage-guide.md still correctly describes Azimuth as Python-2-only/archived

Live import check:
  import azimuth: OK
  import azimuth.model_comparison: SyntaxError (matches both docs) -> Missing parentheses
  in call to 'print'. Did you mean print(...)? (model_comparison.py, line 269)
ASSERT PASS: the documented failure is real and reproduces live, and both docs now agree on it
```
**Status:** COMPLETED ✅ (executed: true) — Script: `run\input7_azimuth_consistency.py`

**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100

**Assertions:** 4/4 PASS (the contradiction assertion that FAILED pre-fix now PASSES)

---

### Input 8 — Adversarial (NEW): enAsCas12a paralog-multiplex array design

**Prompt:** "Build an Inzolia-style enAsCas12a 4-guide array library covering paralog pairs, with singleton controls for GI scoring."

**This chemistry was never exercised in either the pre-fix or this audit's earlier inputs** (pre-fix covered Cas9 KO, CRISPRi, CRISPRa, the shipped example, and the Azimuth/ambiguous-request checks only). Tests gate-4 coverage completeness beyond what the fixer was told about.

**Output (stdout, key lines):**
```
Paralog pairs requested: 3; pairs with insufficient TTTV sites: []
4-guide arrays built: 3
  PARALOG-A1_PARALOG-A2_array: pos1-2=PARALOG-A1 (2 guides), pos3-4=PARALOG-A2 (2 guides)
  ...
ASSERT PASS: every built array has 2 guides for each paralog (4-guide array total)

Singleton conditions added for GI scoring (gene A alone, gene B alone, double-NTC): 7 rows for 3 arrays
ASSERT PASS: GI-scoring singleton set is complete

DOC CHECK PASS: SKILL.md's Common Errors table documents the Cas12a PAM-orientation
pitfall (PAM 5' of spacer, opposite Cas9's 3' NGG) -- find_cas12a_candidates() was
written to that documented orientation and found real TTTV-adjacent spacers.
```
**Status:** COMPLETED ✅ (executed: true) — Script: `run\input7_cas12a_paralog.py`; output: `data\input7_cas12a_arrays.csv`

**Scores:** Basic: 34/40 | Specialized: 46/60 | Total: 80/100 (scored slightly lower than the regression inputs: this exercises SKILL.md's guidance narratively rather than calling a documented, reusable function the way `select_independent_guides`/`crispri_window`/`crispra_window` are; the candidate-finder logic had to be adapted by the auditor from the PAM-orientation description rather than lifted verbatim, since library-design ships no `find_cas12a_candidates` function of its own.)

**Assertions:** 4/4 PASS

---

## Independent Verification Notes

- **Byte-identity check:** `find run\library-design-src -iname '__pycache__'` → none in the external clone; `git status --porcelain -- crispr-screens/library-design` in `F:\OpenScience\external\mrsonord2240__bioSkills` → clean. The clone was copied to `run\library-design-src\` before any script was executed; nothing was written into `F:\OpenScience\external\`.
- **Azimuth double-check:** reproduced live in two separate scripts (Input 7's dedicated check, and again inline while writing this viewer) — both hit the identical `SyntaxError` at `model_comparison.py` line 269.
- **Gate 8 (shipped-means-present):** the only file either doc points at, `examples/design_library.py`, exists and runs (Input 6). No other file references in SKILL.md/usage-guide.md point outside the Skill's own two docs and that one script.
- **Regression scope:** all 6 defects from the pre-fix report (2 P1, 4 P2) were independently re-tested with fresh code/data (not the fixer's own scripts) and found resolved. One new, genuinely minor finding (lowercase input handling) emerged from testing beyond the pre-fix report's scope.

> **Note for reviewer:** the one open item (Input 4's case-sensitivity finding) is new, minor, and does not reproduce or relate to either original P1. Nothing in this re-audit reopens a previously-fixed defect.
