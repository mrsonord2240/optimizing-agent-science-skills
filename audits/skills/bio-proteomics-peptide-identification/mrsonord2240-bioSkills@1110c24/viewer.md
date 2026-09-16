> **Audit record for `bio-proteomics-peptide-identification`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@1110c24](https://github.com/mrsonord2240/bioSkills/tree/1110c241c27760ad0127bd803e8832d54651e31c/proteomics/peptide-identification) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-peptide-identification (re-audit after pass 2 + pass 4)

Generated: 2026-09-15 · skill-auditor@1.0 · re-auditor A, final proteomics re-audit batch
Source: `mrsonord2240/bioSkills@1110c241c27760ad0127bd803e8832d54651e31c:proteomics/peptide-identification`
(fork checkout, read-only, `git status` clean, branch `openscience-fixes`; nothing was written under `F:\OpenScience\external\`)
Superseded reports: `eval_report_*` in this folder at 79/Beta Only (post-pass-2) and `_pre-fix-20260915/` at 79/Beta Only.

**Result: 90/100 · ⭐ Production Ready · deployable · no veto · 10/10 inputs executed.**
The P1 that capped both previous audits — the table snippet silently missing lowercase `rev_` decoys — is
fixed and confirmed fixed on real output from the engine the Skill recommends by default. The pass-4
command-line route was run end to end and every number the SKILL.md prose states was reproduced exactly.
Six P2s remain; no P0 or P1.

Data. SYNTHETIC with ground truth from `data/` (unchanged, reused from the first audit). PUBLIC CC0
PXD070049 (Van Puyvelde et al., *LFQ Benchmark Generation Beta*), Orbitrap Astral 5-min DDA, 250 pg HYE,
Conditions A/B/C REP1, submitter SDRF, FASTA `uniprotkb_proteome_HYE_UniversalContaminants.fasta`
(31,437 entries). One replicate per condition, so no within-condition CV is claimed anywhere below.
Scripts and outputs: `rerun4/`.

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (regression): pyOpenMS search + FDR blocks | 36 | 55 | 91 | 5/5 | yes | ✅ |
| 2 | Variant A (regression): Comet .txt q-values | 36 | 54 | 90 | 4/4 | yes | ✅ |
| 3 | Edge (regression): 33-PSM pulldown | 37 | 53 | 90 | 4/4 | yes | ✅ |
| 4 | Variant B (regression): PEP vs q-value, shipped example | 36 | 53 | 89 | 4/4 | yes | ✅ |
| 5 | Stress (regression of a prior FAIL): separate searches | 36 | 56 | 92 | 5/5 | yes | ✅ |
| 6 | Edge (regression of the P1): `rev_` decoy prefix | 36 | 56 | 92 | 4/4 | yes | ✅ |
| 7 | Adversarial (regression of a prior FAIL): E-value orientation | 35 | 53 | 88 | 4/4 | yes | ✅ |
| 8 | Variant B (regression of the P1, PUBLIC data): real Sage search | 37 | 57 | 94 | 4/4 | yes | ✅ |
| 9 | Stress (NEW, PUBLIC data): whole shipped CLI route + pooling claim | 36 | 54 | 90 | 4/5 | yes | ✅ |
| 10 | Adversarial (NEW, PUBLIC data): decoy-tag mismatch through the CLI route | 33 | 50 | 83 | 3/4 | yes | ✅ |

**Execution average 89.9 · Assertions 41/43 (95.3%) · L1 avg 35.8 · L2 avg 54.1 · Executed 10/10**

## Step 1: Skill Veto

| Dimension | Result | Reason |
|---|---|---|
| T1 Stability | PASS | Both pyOpenMS blocks, both table blocks, all three shipped scripts and all five CLI tools ran with exit 0 across 14 datasets. No crash, no hang. |
| T2 Contract | PASS | `name` and `description` present; `tool_type`/`primary_tool` consistent with the content. |
| T3 Determinism | PASS | Sage and Comet are deterministic on a fixed config. Percolator run twice on the same pin: 1,398 PSMs both times and the results files are **byte-identical** (`cmp -s` clean). Synthetic replicate counts reproduce the first audit's numbers exactly. |
| T4 Security | PASS | No `eval`/`exec` of user strings, no network, no credentials. `dda_search.sh` uses `set -euo pipefail` and `${VAR:?}` guards; its only mutation is a `sed` into its own `$OUT`. |

## Step 2: Static evaluation — 91/100 (was 82)

| Category | Score | Note |
|---|---|---|
| Functional suitability | 11/12 | Completeness 3 — end-to-end now (database build, three engines, Percolator, both estimators, two scripts), but mokapot and MS2Rescore are in the Skill's own description with no command line, and `examples/fdr_filtering.py` ships unreferenced. Correctness 4 — every estimator and every stated number reproduced. Appropriateness 4. |
| Reliability | 10/12 | Fault tolerance 4, error reporting 4 (four Common Errors rows reproduced verbatim), recoverability 3 (the script buries Percolator's error in a log). |
| Performance & context | 7/8 | 366 lines, one file, 19 references (3). Full route in 33 s (4). |
| Agent usability | 15/16 | Learnability 4, consistency 4 (The 2016 → The 2022 resolved), feedback 4, error prevention 3. |
| Human usability | 7/8 | Discoverability 3 (long description, unchanged), forgiveness 4. |
| Security | 11/12 | 4 / 3 / 4. |
| Maintainability | 11/12 | Modularity 3, modifiability 4 (env-var tool paths — this audit ran the script unchanged because of them), testability 4. |
| Agent-specific | 19/20 | Trigger 4, progressive disclosure 3, composability 4, idempotency 4, escape hatches 4. |

**Gate 8 (shipped-means-present):** every path referenced by `SKILL.md` and `usage-guide.md` exists —
`examples/dda_search.sh`, `examples/separate_search_fdr.py`. All seven Related Skills resolve in the fork,
including `database-access/uniprot-access`. No `references/`, `scripts/`, `assets/` or `templates/`
pointers. **PASS.** (The reverse direction is not a gate failure but is a P2: `examples/fdr_filtering.py`
is present and runs but nothing links to it any more.)
**Gate 7 (research scope):** research proteomics only, no individual-level claims. **PASS.**

## Step 3: Classification

Category 3 Data Analysis · Mode **D** (was A — the Skill now ships a bash pipeline and two Python scripts
alongside its prose) · Complex (7+ reference sections, branching by search mode and engine)
→ 8 regression inputs (the previous audit's set, re-run against the new commit) + 2 new = **10 inputs**.

## Detailed outputs

### Input 1 — Canonical (regression)
**Prompt:** "I have an Orbitrap HCD DDA run exported as `sample.mzML` and a concatenated target+decoy FASTA (decoys prefixed `DECOY_`). Using pyOpenMS, search it with trypsin, up to 2 missed cleavages, 10 ppm precursor, 0.02 Da fragment, carbamidomethyl C fixed, oxidation M variable, and give me the PSMs at 1% FDR saved as idXML."

**Code:** `rerun4/in1_4b.py`. Both blocks are pulled out of the current `SKILL.md` by
`rerun4/extract.py` and executed — only the two filenames are retargeted, so nothing is retyped.

```
params read back: {'precursor:mass_tolerance': 10.0, 'fragment:mass_tolerance': 0.02,
 'fragment:mass_tolerance_unit': 'Da', 'peptide:missed_cleavages': 2,
 'modifications:fixed': [b'Carbamidomethyl (C)'], 'modifications:variable': [b'Oxidation (M)']}
main: PSMs after search 381; accepted 311; correct 298; false 13; true FDP 0.0418; max q 0.009646
rep11 0.0103 | rep22 0.0034 | rep33 0.0102 | rep44 0.0000 | rep55 0.0390 | rep66 0.0036 | rep77 0.0034 | rep88 0.0035
pooled replicates: accepted 2326, false 22, FDP 0.0095
plain [] for peptide ids -> TypeError Argument 'pep_ids' has incorrect type (expected ...PeptideIdentificationList)
```

Identical to the previous audit. **Answer delivered:** 311 target PSMs at q ≤ 0.01 in `search_results.idXML`;
~300 PSMs is at the lower edge where decoy counts are noisy (single run 4.2%, pooled over 8 runs 0.95%);
protein FDR handed to protein-inference.
**Scores:** L1 36 · L2 55 (Method 18, Code 15, QC 8, Repro 9, Sec 5) · **91** · Assertions 5/5

### Input 2 — Variant A (regression)
**Prompt:** "I ran Comet against a concatenated target-decoy human DB (DECOY_ prefix) and have the .txt output. Can you compute q-values and give me the PSMs at 1% FDR? What XCorr does that correspond to?"

```
rows 60000 | after rank-1 dedup 12000 | kept 2632 | unique scans 2632 | true FDP 0.0072
XCorr at the 1% cut: 3.497
```
**Answer delivered:** 2,632 PSMs at q ≤ 0.01; XCorr ≥ 3.50 in this run only, not a reusable cut.
**Scores:** L1 36 · L2 54 · **90** · Assertions 4/4

### Input 3 — Edge (regression)
**Prompt:** "Single-bait co-IP, one gel band. Comet gave 33 PSMs and when I computed q-values every PSM came out q = 0, so I was going to write 'all identifications at 0% FDR'. Is that OK? I also attach a second export where the top hit is a DECOY_ protein."

```
pulldown_nodecoy.tsv : ValueError -> no decoy PSMs recognised: check the decoy prefix,
                       or the table was already decoy-filtered
pulldown_topdecoy.tsv: rows 33 decoys 1 kept at 1% 0 | q min 0.0625 max 0.0625 | any inf False
```
**Behaviour change worth recording.** Pre-fix, the decoy-free export returned a q floor of 0.0303, which
told the operator directly that 1% is unreachable at 33 PSMs. The pass-2 guard now raises instead. The
safety outcome is the same — no "0% FDR" or "1% FDR" claim is reachable — but the diagnostic is gone. P2.
**Answer delivered:** No. With 33 PSMs the smallest attainable q is 3–6%, so neither claim can be made;
inspect spectra manually or confirm by PRM.
**Scores:** L1 37 · L2 53 · **90** · Assertions 4/4

### Input 4 — Variant B (regression)
**Prompt:** "Percolator on our Sage search: 12,431 PSMs at q ≤ 0.01 but only 7,902 at PEP ≤ 0.01. My PI wants the PEP list because it's 'safer'. Which goes in the paper, and for the one peptide we'll validate by PRM, which number should I look at?"

Shipped `examples/fdr_filtering.py`, unchanged:
```
Targets: 2445, Decoys: 1555 (concatenated 1:1 search)
Target PSMs at q <= 0.01: 481
Worst PEP inside the 1%-FDR list: 0.047
Target PSMs at PEP <= 0.01: 289 (per-PSM cutoff is far stricter than the same q-value)
```
**Answer delivered:** report the q ≤ 0.01 list; for the PRM peptide read its PEP.
**Scores:** L1 36 · L2 53 · **89** · Assertions 4/4

### Input 5 — Stress (regression of a prior FAIL)
**Prompt:** "Our old pipeline searched X!Tandem separately against the target DB and a reversed DB (same spectra), and a student merged the two result tables. How do we get a proper 1% FDR from that? Would rescoring with Percolator help, and which options do we use?"

The previous audit **failed** this input: "Skill supplies code for the separate-search estimator (π0
estimate) — none." It now ships in `SKILL.md` and as `examples/separate_search_fdr.py`.

SKILL.md block extracted and run verbatim:
```
pi0=hat: pi0-used 0.611 kept 2888 true FDP 0.0104
pi0=1.0: pi0-used 1.000 kept 2588 true FDP 0.0062
concatenated snippet misapplied to the merged pair: kept 2632 true FDP 0.0072
```
Shipped script, independently:
```
targets 12000  decoys 12000  pi0-hat 0.611
kept at q <= 0.01: 2888
kept at q <= 0.01 with pi0 = 1 (conservative): 2588
true FDP of the pi0-hat list: 0.0104
true FDP of the pi0 = 1 list: 0.0062
```
**Fixer claim reproduced to every digit.** The π̂₀ list realises 1.04% at a nominal 1% — calibrated but
not conservative, which is what the estimator is for, and the Skill states that number itself.

Percolator's flags were checked against the **installed binary's own `--help`** (3.09.0), not
documentation:
```
 -y --post-processing-mix-max   ... only has an effect if the input PSMs are from separate
                                    target and decoy searches. This is the default setting.
 -Y --post-processing-tdc       Replace the mix-max method by target-decoy competition ...
```
Exactly what the Skill says. Mix-max itself was still not *executed* — the synthetic separate-search
tables carry no peptide sequences, so building a pin would mean fabricating them.
**Scores:** L1 36 · L2 56 (Method 19, Code 15, QC 8, Repro 9, Sec 5) · **92** · Assertions 5/5

### Input 6 — Edge (regression of the P1)
**Prompt:** "I have an MSFragger psm.tsv from FragPipe (concatenated search; its decoys are `rev_`). I renamed the hyperscore column to `score` and the spectrum column to `scan` like your snippet says. Give me the PSMs at 1% FDR."

```
decoys detected 3813 | kept 2632 | unique scans 2632 | true FDP 0.0072
MaxQuant REV__ : kept 2632 | true FDP 0.0072
decoy-free table: ValueError raised: no decoy PSMs recognised ...
```
**FIXED.** Pre-fix this kept all 12,000 spectra at 63.6% true FDP with no warning. The `rev_` result is now
bit-for-bit the `DECOY_` result, `REV__` is covered by the same lower-cased match, and a decoy-free table
stops.
**Scores:** L1 36 · L2 56 · **92** · Assertions 4/4

### Input 7 — Adversarial (regression of a prior FAIL)
**Prompt:** "MS-GF+ gave me a tsv with SpecEValue per PSM (concatenated search). Just plug SpecEValue in as `score` in your q-value code and give me the 1% list — don't bother transforming it."

```
raw E-value as score: kept 0 | true FDP nan
-log10(E-value)     : kept 2574 | true FDP 0.0066
```
Confirmed again on **real** MS-GF+ output in Input 9: raw `SpecEValue` keeps 0, `-log10(SpecEValue)` keeps
656. The prior FAIL — "Skill states the score orientation the snippet requires" — now passes: the block
carries an inline comment and there is a matching Common Errors row.
**Scores:** L1 35 · L2 53 · **88** · Assertions 4/4

### Input 8 — Variant B (regression of the P1, PUBLIC data)
**Prompt:** "I searched one Astral DDA run with Sage (the default you recommend), concatenated target-decoy with its own generated decoys. Here is results.sage.tsv. Compute q-values with your table code and give me the PSMs at 1% FDR."

Fresh Sage 0.14.6 search run by this auditor through `examples/dda_search.sh`.
```
Sage rows 1939 | label counts {1: 1717, -1: 222}
Sage's own spectrum_q <= 0.01 target PSMs: 1406
SKILL snippet: decoys detected 222 | kept 1406
  scan-set identical to Sage's own list: True
  species of the kept list: {'HUMAN': 927, 'YEAST': 416, 'other': 40, 'ECOLI': 23}
```
**FIXED on the Skill's own default engine.** Pre-fix, all 1,939 rows including 222 decoys were reported at
"1% FDR". The snippet's (D+1)/T q-values now reproduce Sage's own `spectrum_q` list scan for scan, so the
estimator and the decoy match are both right. Species proportions follow the 65:30:5 HYE design.
**Scores:** L1 37 · L2 57 · **94** · Assertions 4/4

### Input 9 — Stress (NEW, PUBLIC data)
**Prompt:** "Set the whole thing up from scratch for me: I have three 5-min Astral DDA raw files and a UniProt FASTA. Build the target-decoy database, search, rescore, and give me the 1% PSM list. Which engine should I use, and does rescoring actually buy me anything?"

`examples/dda_search.sh` executed **from the read-only fork**, twice, with tool paths passed as environment
variables and nothing else changed:

```
$ MZML=...Condition_A_REP1.mzML FASTA=...HYE...fasta OUT=... ENGINE=sage bash examples/dda_search.sh
database: 62874 entries, 31437 decoys
[sage] finished in 13s
PSMs at q <= 0.01:     1398
peptides at q <= 0.01: 1367

$ ... ENGINE=comet bash examples/dda_search.sh
Comet: Load spectra: 6135 ... Run stats: 11s
PSMs at q <= 0.01:     1144
peptides at q <= 0.01: 1138
```
The documented MS-GF+ block, run separately with its flags exactly as written
(`-tda 0 -decoy DECOY_ -t 10ppm -ti 0,1 -m 3 -inst 3 -e 1 -ntt 2 -n 1 -addFeatures 1`), then
`MzIDToTsv -showDecoy 1`:
```
rows 6806 | scans 5949 | DECOY_ rows 2575
-log10(SpecEValue) as score: decoys 2171 | kept at q<=0.01 656
raw SpecEValue as score    : kept at q<=0.01 0
```
Pooling the three conditions into one Sage search (6,864 PSMs) and rescoring:
```
Percolator PSMs at q <= 0.01: 5006   peptides: 2760
Sage's own pooled 1% list:    4961
```

**Every claim in the "Which engine wins" paragraph reproduced exactly**: 1,398/1,367, 1,144/1,138, 916
(Comet raw, see Input 10), 656 (MS-GF+), 5,006 vs 4,961 pooled, 31,437 → 62,874 for the database step.
Sage 1,406 > Comet+Percolator 1,144 > MS-GF+ 656 on this input; Sage gains nothing from Percolator on one
run and +0.9% when three runs are pooled. The Skill's tip "Percolator needs enough PSMs to train … pool
runs when you can" is therefore correct, and its "do not generalise these counts" caveat is present.

**The one gap:** `dda_search.sh` accepts a single `MZML` and the sample Sage JSON shows one mzml path, so
following the Skill's own pooling advice meant hand-writing a config. P2.
**Scores:** L1 36 · L2 54 (Code 14 — single-run script) · **90** · Assertions 4/5

### Input 10 — Adversarial (NEW, PUBLIC data)
**Prompt:** "My Comet config says `decoy_prefix = rev_` because that's what I use with FragPipe, but the database I built with your DecoyDatabase command uses `DECOY_`. I already ran the search. Is my 1% list wrong?"

This drives the Skill's self-declared silent trap through the **command-line** route rather than the table
snippet. Comet 2026.02 rev.2 on the same mzML, only `decoy_prefix` changed:

```
Label counts in the MISMATCHED pin: 1 -> 6113          (0 decoys)
Label counts in the matched pin:    1 -> 3952, -1 -> 2161
$ percolator --post-processing-tdc ... comet.pin ; echo $?
1
  Found 6113 PSMs
  Train/test set contains 6113 positives and 0 negatives, size ratio=inf and pi0=1
  Exception caught: Error: no decoy PSMs were provided.
```
And the same two searches through the Skill's table block on Comet's `.txt`:
```
decoy_prefix = DECOY_ (correct)   : rows 6113, DECOY_ rows 2168 | decoys detected 2168 | kept 916
decoy_prefix = rev_ (MISMATCHED)  : rows 6113, DECOY_ rows 2168 | decoys detected 2168 | kept 916
```

**Result: the route is safe.** Percolator refuses loudly and the table snippet is immune to this particular
mismatch, because Comet's text output names proteins from the FASTA regardless of the config. Both give
916 PSMs, which independently reproduces the Skill's own "Comet raw `-log10(e-value)` = 916" claim.

**But** `dda_search.sh` sends Percolator's stderr to `$OUT/percolator.log` and runs under `set -e`, so an
operator sees the search complete and then nothing — no error, no counts. Nothing in the script checks the
pin's `Label` column before rescoring, which is the one-line guard the Skill's own decoy-tag warning
implies. P2.
**Scores:** L1 33 · L2 50 · **83** · Assertions 3/4

## Research Veto

| Dimension | Result | Detail |
|---|---|---|
| M1 Scientific integrity | PASS | No fabricated identifiers or values. Every testable quantitative claim in the prose reproduced exactly on the same public data (see Inputs 5, 8, 9, 10). The The-2016 misattribution is corrected to Savitski 2015 / The 2022, matching protein-inference. |
| M2 Practice boundaries | PASS | Research proteomics only. |
| M3 Methodological ground | PASS | TDC, (D+1)/T, π0·D/T, mix-max routing and PEP-vs-q are correct and were confirmed calibrated against ground truth. The Skill refuses a decoy FDR claim on small lists and caveats its own engine comparison. |
| M4 Code usability | PASS | Two pyOpenMS blocks, two table blocks, three shipped scripts and five CLI tools all ran with exit 0 as written. |

## Final arithmetic

```
Static        91 x 0.4 = 36.4
Execution     (91+90+90+89+92+92+88+94+90+83)/10 = 899/10 = 89.9   x 0.6 = 53.9
Final         36.4 + 53.9 = 90.3 -> 90  (Production Ready band)
Floors (PR)   static 91>=80 ok | exec 89.9>=85 ok | L1 35.8>=32 ok | L2 54.1>=48 ok
              assertions 41/43 = 95.3% >= 90% ok  -> no downgrade
Grade         ⭐ Production Ready; deployable true; veto_override false
```

Schema and floor arithmetic checked with
`audit-envs/mass-spec-proteomics-analyst/validate_report.py` (clean apart from that script's
hard-coded `evaluated_on == '2026-09-11'` left over from the first round).

## What changed since 79

The two inputs that scored 52 and 51 in the previous audit — both instances of the silent `rev_` defect —
now score 92 and 94. Two assertions that failed then (no separate-search code, score orientation unstated)
now pass with running code behind them. The static score rose 82 → 91 on content that was executed, not
content that was described. Nothing from passes 1–3 regressed: Inputs 1, 2 and 4 reproduce the earlier
numbers digit for digit.

Both fixer claims I was asked to test directly held: **Sage + Percolator → 1,398 PSMs / 1,367 peptides**
(reproduced from the shipped script, twice, byte-identical), and **π̂₀ 0.611 → 2,888 at 1.04% true FDP**
(reproduced from both the SKILL.md block and the shipped script).

## Recommendations

- **[P2] `dda_search.sh` hides Percolator's error** (Input 10): `2>` into a log under `set -e` means a
  decoy-tag mismatch kills the script silently. `tee` the log to stderr, or add an `ERR` trap, and check the
  pin's `Label` column for both `1` and `-1` before rescoring.
- **[P2] No shipped route for multi-run pooling** (Input 9): the Skill advises pooling and proves the
  benefit, but the script takes one `MZML`. Accept several and note that Comet pins must be concatenated
  with the header once.
- **[P2] Zero-decoy stop loses the q-floor hint** (Input 3): keep the raise, but put `1/len(psms)` in the
  message so a tiny decoy-free list still tells the operator what is reachable.
- **[P2] mokapot and MS2Rescore promised but not routed** (static): both are in the frontmatter
  description; only Percolator has a command line. mokapot 0.10.0 is installed and takes the same pin.
- **[P2] `examples/fdr_filtering.py` ships but is unreferenced** (static): it is the Skill's only worked
  PEP-vs-q demonstration and it runs; cite it from Insight 3.
- **[P2] 366-line SKILL.md with no progressive disclosure** (static): move the three command-line sections
  and the 19-entry reference list into `references/`.
