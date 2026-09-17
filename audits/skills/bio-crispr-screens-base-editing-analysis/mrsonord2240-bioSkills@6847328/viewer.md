> **Audit record for `bio-crispr-screens-base-editing-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6847328](https://github.com/mrsonord2240/bioSkills/tree/684732876d2781df75d90ba35c3e9949ff4f28b2/crispr-screens/base-editing-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-base-editing-analysis (re-audit, round 2)
Generated: 2026-09-16
Source: `mrsonord2240/bioSkills@6847328:crispr-screens/base-editing-analysis`
Pre-fix report: `F:\OpenScience\audits\_pre-fix-20260916\bio-crispr-screens-base-editing-analysis\` (score 54, ❌ Reject, M4 Code Usability veto)
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-crispr-screens-base-editing-analysis.md`

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (new) — CBE library design, fresh CDS | 38 | 58 | 96 | 4/4 | ✅ |
| 2 | Variant A (new) — hand-constructed reverse-strand regression | 39 | 60 | 99 | 5/5 | ✅ |
| 3 | Edge — editing-efficiency filtering, real CRISPResso2 | 38 | 59 | 97 | 4/4 | ✅ |
| 4 | Variant B — bystander deconvolution, real CRISPResso2 | 38 | 59 | 97 | 4/4 | ✅ |
| 5 | Stress — hit-calling aggregation, real MAGeCK | 38 | 59 | 97 | 4/4 | ✅ |
| 6 | Scope Boundary — BE-Hive worked example (new code sample) | 37 | 55 | 92 | 4/4 | ✅ |
| 7 | Adversarial — schema-validation stress test | 35 | 52 | 87 | 4/5 | ⚠️ |
| 8 | Variant C (new) — clean-BE ratio, opposite direction | 38 | 57 | 95 | 4/4 | ✅ |
| 9 | Stress (new) — ABE8e window + multi-step design | 37 | 58 | 95 | 4/4 | ✅ |

**Execution Average: 95.0 / 100**
**Assertion Pass Rate: 37/38**

**Static Score: 87/100 → Static Weighted 34.8**
**Dynamic Weighted: 57.0**
**FINAL SCORE: 92/100 — ⭐ Production Ready**
**Skill Veto: PASS. Research Veto: PASS (M4 Code Usability now PASS).** `deployable: true`, `veto_override: false`

## Method note

Per `AUDIT_BRIEF.md`'s re-audit instructions: the pre-fix audit's own inputs were re-run as
regressions against real tool output (Inputs 3, 4, 5 reuse this candidate's own real CRISPResso2
2.3.4 Docker run and the sibling `bio-crispr-screens-mageck-analysis` audit's real MAGeCK 0.5.9.5
run; Input 6 reuses the same real synthetic-CBE guide sequence with the new BE-Hive code sample),
and at least two genuinely new inputs were added (Inputs 1, 2, 8, 9 are new; Input 7 extends the
pre-fix scope with a defect not in the fix log). The single most important test is **Input 2**: a
hand-constructed reverse-strand case engineered, before running any code, to trigger the OPPOSITE
failure direction from the fixer's own test case (a missed target rather than a false on-target),
to check the fix is a genuine coordinate-conversion fix rather than a patch tuned to one example.

All four of the pre-fix audit's P0 findings were re-tested by copying the four functions verbatim
from the fixed SKILL.md (`run/skill_functions.py`, one shared copy so every test imports the exact
same code) and running them against real data:

- `find_be_spacers()` — verified correct on both a fresh natural random CDS (Input 1, 2 genuine
  reverse-strand on-target hits, independently re-derived) and the hand-constructed adversarial
  case (Input 2).
- `filter_by_editing_efficiency()` — real CRISPResso2 2.3.4 `Quantification_window_nucleotide_percentage_table.txt`,
  reproduces planted ground truth exactly (50.0% target, 30.0% bystander).
- `deconvolute_bystander()` — real CRISPResso2 2.3.4 `Alleles_frequency_table.zip`, reproduces
  planted ground truth exactly (40/30/20/10 partition).
- `aggregate_variant_scores()` — real MAGeCK 0.5.9.5 `sgrna_summary.txt` (71,090 real sgRNAs from
  HAP1 TKOv3), merges cleanly and its per-variant mean matches a by-hand recomputation.

**One genuinely new defect was found** (Input 7): `find_be_spacers()` crashes with a bare,
unrelated `KeyError('n_bystanders')` when it finds zero candidate spacers (e.g. a short CDS, or a
lowercase-masked CDS against the case-sensitive `[ACGT]GG` PAM regex), instead of the clear
`ValueError` pattern the fix pass added to the other three functions. This is reported as P1, not a
veto trigger, since the core (non-empty, real-data) path is confirmed correct across Inputs 1, 2, 3,
4, 5, 6, 8, and 9.

## Detailed Outputs

### Input 1 — Canonical (new): CBE library design on a fresh synthetic CDS

**Prompt:** "Design a CBE saturation library tiling a target region of a synthetic CDS, minimize
bystanders, annotate target + bystander for amino acid 25."

**Code:** `run/input1_find_be_spacers_forward.py` (imports `find_be_spacers` verbatim from
`run/skill_functions.py`, itself copied by hand from the fixed SKILL.md).

Fresh CDS (seed=7, 180nt), different from the pre-fix audit's seed-1 CDS. 15 candidates found for
target_aa=25; 2 genuine on-target hits, both reverse-strand:

```
strand=- spacer_start=102 i=6 -> true_forward_index=72 in_target_codon=True
strand=- spacer_start=101 i=7 -> true_forward_index=72 in_target_codon=True
```

Both independently re-derived from raw `spacer_start`/`strand`/`i` fields (not the function's own
`target_positions` output) and confirmed inside the true codon `[72,75)`.

**Scores:** Basic 38/40 | Specialized 58/60 | Total 96/100 | Assertions 4/4

---

### Input 2 — Variant A (new, critical regression): hand-constructed reverse-strand case

**Prompt:** "Install a C>T variant at a specific codon; find me the CBE spacer."

**Code:** `run/input2_find_be_spacers_reverse_hand_check.py`

The pre-fix defect: `genomic_pos` computed in reverse-complement coordinate space, compared
directly against forward-strand codon bounds. The fix log's own test found a case where this
produced a **false on-target** (a real off-target call misattributed as target). To check the fix
is a general coordinate conversion rather than tuned to that one example, this test was engineered
— by hand, before running any code — to trigger the **opposite** failure: a true on-target edit
that the unconverted math would call a **bystander** (false negative).

Derivation: 100nt CDS, target codon = aa 30 → forward range `[87,90)`. Forced the true edited base
to forward index 88 (`cds[88]='G'`), which lands at reverse-complement index 11. Unconverted math:
`genomic_pos=11`, not in `[87,90)` → would be called bystander. Converted math: `genomic_pos =
100-1-11 = 88`, in `[87,90)` → correctly target.

```
Engineered candidate row (strand='-', spacer_start=7):
  target_positions: [5]
  bystander_positions: []
PASS: fixed code correctly classifies the hand-verified true on-target C as TARGET.

For reference -- unconverted (pre-fix) genomic_pos = 11 (in [87,90)? False) -> pre-fix code
would have called this a BYSTANDER (false negative).
Converted (fixed) genomic_pos = 88 (in [87,90)? True) -> fixed code calls this TARGET,
matching the hand-derived ground truth.
```

**Scores:** Basic 39/40 | Specialized 60/60 | Total 99/100 | Assertions 5/5

---

### Input 3 — Edge: editing-efficiency filtering on real CRISPResso2 output

**Prompt:** "Run CRISPResso2 on my pilot timepoint samples. Compute target editing % per sgRNA. Keep
sgRNAs >30% target editing for the primary screen."

**Code:** `run/input3_filter_by_editing_efficiency.py`, against real CRISPResso2 2.3.4 output at
`F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\base-editing-synthetic\results\CRISPResso_on_synth_cbe\`
(planted ground truth: 50.00% target editing, 30.00% bystander editing).

Identified the two real reference-C window positions (5 and 7) directly from the table's own column
headers (`'C'` and `'C.1'`, pandas' dedup suffix for the real file's duplicated headers) rather than
trusting the ground-truth file blindly:

```
target_pos=5: {'sgrna_id': 'synth_cbe', 'editing_pct': 0.5, 'pass_filter': True}
target_pos=7: {'sgrna_id': 'synth_cbe', 'editing_pct': 0.30000000000000004, 'pass_filter': True}
```

Exact match to planted ground truth (50.00% / 30.00%).

**Scores:** Basic 38/40 | Specialized 59/60 | Total 97/100 | Assertions 4/4

---

### Input 4 — Variant B: bystander deconvolution on real allele table

**Prompt:** "From CRISPResso2 allele tables, separate reads by edit pattern: target only,
target+bystander. Compute per-pattern fitness contribution."

**Code:** `run/input4_deconvolute_bystander.py`, against the real `Alleles_frequency_table.zip` from
the same CRISPResso2 run.

```
   target_edited  bystander_69_edited  %Reads
0          False                False    40.0
1          False                 True    10.0
2           True                False    30.0
3           True                 True    20.0
```

Exact match to planted ground truth (unmodified 40%, target-only 30%, target+bystander 20%,
bystander-only 10%; sums to 100.0).

**Scores:** Basic 38/40 | Specialized 59/60 | Total 97/100 | Assertions 4/4

---

### Input 5 — Stress: hit-calling aggregation on real MAGeCK output

**Prompt:** "Apply MAGeCK MLE to the BE screen counts. Aggregate per-sgRNA LFC to per-variant
scores."

**Code:** `run/input5_aggregate_variant_scores.py`, merging against the real MAGeCK 0.5.9.5
`sgrna_summary.txt` reused from the sibling `bio-crispr-screens-mageck-analysis` audit's own
verified real HAP1 TKOv3 run (71,090 real sgRNAs, lowercase `sgrna` column).

```
Real LFC values for V1's 3 sgRNAs: [6.1648, 4.3083, 4.8304]
Hand-computed mean: 5.101166666666667
Function's reported mean for V1: 5.101166666666667
```

Merge succeeds on the real lowercase column; per-variant aggregation matches an independent
by-hand mean exactly.

**Scores:** Basic 38/40 | Specialized 59/60 | Total 97/100 | Assertions 4/4

---

### Input 6 — Scope Boundary: BE-Hive worked example (P1 fix)

**Prompt:** "Predict editing efficiency and bystander outcomes for my designed CBE guide using
BE-Hive."

**Code:** `run/input6_behive_predict.py` — runs the new "BE-Hive Editing-Efficiency Prediction"
section's code sample verbatim from the fixed SKILL.md, using the real `guide_seq` from this
candidate's own synthetic CBE fixture (`TGATCACGTAGCATGCACGT`).

```
Total predicted probability = 0.9795059113130233
C-prefixed numeric columns found in pred_df: ['C4', 'C6', 'C11', 'C15', 'C17']
All editable C positions in the spacer (1-indexed): [5, 7, 12, 16, 18]
```

Unlike the pre-fix audit (which needed a corrective second attempt after a 1nt frameshift building
the substrate by hand from the README alone), the new SKILL.md example's own substrate/spacer
offset assertion passed on the first attempt. Independently verified the documented `C<n> = spacer
position n+1` naming convention against **all 5** editable Cs in the spacer (not just the 2
SKILL.md's own text checks) — held exactly, including the planted target (C4=pos5) and bystander
(C6=pos7).

**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100 | Assertions 4/4

---

### Input 7 — Adversarial: schema-validation stress test (finds one new defect)

**Prompt (implicit):** an agent following the Skill hits malformed/drifted real-world data.

**Code:** `run/input7_schema_validation_adversarial.py`

Five deliberately malformed inputs against the three newly-schema-checked functions, all raised a
specific, actionable `ValueError`:

```
[filter_by_editing_efficiency: target_base not in table rows] PASS -- ValueError: target_base='C'
  not in table rows ['A', 'G', 'T', 'N'] (...); unexpected CRISPResso2 ... schema
[filter_by_editing_efficiency: target_pos out of range] PASS -- ValueError: target_pos=99 out of
  range for a 2-position quantification window in (...)
[deconvolute_bystander: missing '%Reads' column (old wrong schema)] PASS -- ValueError: Unexpected
  Alleles_frequency_table schema: missing {'%Reads'}; got columns [...]
[aggregate_variant_scores: mageck_sgrna_summary missing lowercase 'sgrna'] PASS -- ValueError: ...
[aggregate_variant_scores: variant_annotation_df missing lowercase 'sgrna'] PASS -- ValueError: ...
```

Then tested `find_be_spacers()` with a zero-candidate input (a too-short CDS, and separately a
lowercase-masked CDS against the case-sensitive `[ACGT]GG` PAM regex — both hit the same root
cause):

```
[find_be_spacers: zero-candidate case] NEW FINDING (P1, not in the fix log): raises a bare,
unrelated-looking KeyError: KeyError('n_bystanders') from an internal
'.sort_values("n_bystanders")' call on an empty DataFrame with no columns at all -- not the
specific, actionable ValueError pattern the other three functions now use.
[find_be_spacers: lowercase CDS] confirms the same root cause: KeyError('n_bystanders')
```

This is a genuinely new, previously-unreported defect (see Recommendations, P1). It is a boundary
condition, not a break in the core happy path already confirmed correct in Inputs 1, 2, and 9.

**Scores:** Basic 35/40 | Specialized 52/60 | Total 87/100 | Assertions 4/5

---

### Input 8 — Variant C (new): clean-BE ratio, opposite direction from the pre-fix audit

**Prompt:** "My BE sample shows 60% editing and looks clean — confirm this isn't Cas9
contamination."

**Code:** `run/input8_clean_be_ratio.py`

The pre-fix audit tested the substitution-vs-indel diagnostic in only one direction (a real Cas9
sample, correctly called Cas9-like). This tests the other direction, on this candidate's own real,
independently-known-clean synthetic-CBE CRISPResso2 2.3.4 run:

```
Insertions=0  Deletions=0  Substitutions=120
Substitution-vs-indel ratio = 120/0 = inf
Classifies as clean BE: True
Classifies as Cas9-like: False
```

Correctly classified as clean BE, not Cas9-like — confirming the diagnostic discriminates in both
directions.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100 | Assertions 4/4

---

### Input 9 — Stress (new): ABE8e window + multi-step zero-bystander design

**Prompt:** "I want the highest-activity ABE for installing an A>G variant with minimal bystanders.
Design ABE8e sgRNAs for this CDS and tell me which are zero-bystander."

Note on target selection: the script first swept every amino acid in the CDS to find one with a
real zero-bystander on-target candidate (aa=42), rather than picking a codon at random and reporting
"0 candidates" as if that were the interesting result — a researcher would do the same before
committing to a design. The sweep itself is informative: several codons genuinely have no viable
ABE8e candidate, which the function correctly reports as an empty result rather than a false
positive.

**Code:** `run/input9_abe8e_multistep.py`

The pre-fix audit only exercised ABE7.10's window `(4,7)`. This checks ABE8e's window `(4,8)`, read
directly from the **executed** source via `inspect.getsource()` (not just SKILL.md's prose table):

```
'ABE7.10': (4, 7),   'ABE8.20': (4, 8),   'ABE8e': (4, 8),     # SpABE8e matches CBE window (Richter 2020)
```

Found 2 genuine zero-bystander on-target candidates for target_aa=42; both independently
re-verified (true forward index 123, inside codon `[123,126)`; window re-scanned directly for `A`
characters, confirming only the reported position is editable in-window).

**Scores:** Basic 37/40 | Specialized 58/60 | Total 95/100 | Assertions 4/4

---

## Research Veto

| Dimension | Result |
|---|---|
| M1 Scientific Integrity | PASS |
| M2 Practice Boundaries | PASS |
| M3 Methodological Ground | PASS |
| M4 Code Usability | **PASS** — all 4 bundled functions now run correctly and reproduce planted ground truth against real CRISPResso2 2.3.4 and real MAGeCK 0.5.9.5 output; the reverse-strand fix independently re-verified on a hand-constructed case in the opposite bug direction from the fixer's own test. One new, narrower defect found (find_be_spacers() crash on zero candidates) is a P1 robustness gap on a boundary condition, not a break in the confirmed-correct core path. |

## Note for reviewer

All four pre-fix P0s are now closed, independently re-verified against real tool output rather than
by re-running the fixer's own scripts. The audit's one new finding (Input 7, find_be_spacers()
crashing on zero candidates) is exactly the kind of gap this re-audit was designed to surface: it
falls in the one function the fix pass did not add schema validation to, and it is the same class of
defect (missing edge-case guard) as the three P0s that were fixed — worth closing in the same pass
rather than treating this Skill's hardening as complete.
