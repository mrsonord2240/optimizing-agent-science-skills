> **Audit record for `bio-proteomics-peptide-identification`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/proteomics/peptide-identification) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-11 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer: bio-proteomics-peptide-identification
Generated: 2026-09-11 · skill-auditor@1.0 · sub-audit for round-2 candidate `mass-spec-proteomics-analyst` (role: supporting, FDR-controlled identification)
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:proteomics/peptide-identification` (clone clean at that commit; nothing written there. The example was imported with bytecode writing disabled.)

**All data in this audit is SYNTHETIC** and has ground truth. The generators are `data/make_synthetic_ms2.py` (FASTA + mzML) and `data/make_psm_tables.py` (PSM tables). Scripts and captured logs are under `runs/`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical: pyOpenMS search, 1% FDR idXML | 32 | 45 | 77 | 3/5 | yes | ✅ |
| 2 | Variant A: Comet .txt q-values | 34 | 47 | 81 | 3/4 | yes | ✅ |
| 3 | Edge: 33-PSM pulldown | 34 | 48 | 82 | 3/4 | yes | ✅ |
| 4 | Variant B: PEP vs q-value | 35 | 52 | 87 | 3/4 | yes | ✅ |
| 5 | Stress: separate searches merged + Percolator | 30 | 42 | 72 | 4/5 | yes (Percolator: docs only) | ⚠️ |

**Execution Average: 79.8 / 100** · **Assertion Pass Rate: 16/22 (72.7%)** · Layer 1 avg 33.0 · Layer 2 avg 46.8 · executed 5/5

---

## Step 1: Skill Veto

| Dimension | Result | Reason |
|---|---|---|
| T1 Stability | PASS | The Skill's code ran on every input once the pyOpenMS container type was fixed. No crashes or loops. The example exits 0. |
| T2 Contract | PASS | Frontmatter has `name` and `description`, and the name matches the folder. |
| T3 Determinism | PASS | Every step is deterministic, and the example is seeded (`default_rng(0)`). Re-runs gave identical counts. |
| T4 Security | PASS | No eval/exec, no network, no shell built from user strings. |

## Step 2: Static Evaluation (78/100)

| # | Criterion | Score | Note |
|---|---|---|---|
| 1.1 | Completeness | 2 | TDC, PEP/q, the FDR cascade, open search and rescoring are covered as guidance. The usage-guide promises "configure trypsin, 2 missed cleavages, 10 ppm/0.02 Da", "MSFragger open search" and "rescore with mokapot/Percolator", but none of these gets code or a command line. The search block never sets parameters. |
| 1.2 | Correctness | 2 | Three defects. (1) The Elias-Gygi `2*decoy/(target+decoy)` formula is given as the SEPARATE-search estimator in four places (see Lead 1). (2) The pyOpenMS blocks fail on pyopenms 3.5.0 (header claims "3.1+"). (3) "MSnbase::readMzIdData does not exist" is false: it exists in MSnbase 2.32.0 and read 387 rows here. The concatenated path and the PEP/q guidance are correct. |
| 1.3 | Appropriateness | 3 | The default (Comet/Sage + Percolator/mokapot, q <= 0.01) is right. pyOpenMS SSE is teaching-scale, and the Skill says so implicitly. |
| 2.1 | Fault tolerance | 3 | It tells the agent to introspect and adapt on TypeError, and warns about small PSM counts and open search. |
| 2.2 | Error reporting | 2 | The Common Errors table has cause/solution rows, but two rows are wrong on current tools. An unannotated idXML makes `FalseDiscoveryRate` raise `Meta value 'target_decoy' does not exist`, not "all q-values 0". The snippet writes `inf` silently. |
| 2.3 | Recoverability | 3 | Stateless code: a re-run overwrites its outputs. |
| 3.1 | Token cost | 3 | 231 lines, 21.6 kB, all loaded at once (the reference list is long). |
| 3.2 | Execution efficiency | 3 | `PeptideIndexing` after the search is redundant because SSE already annotates target/decoy (seen in `in1_adapted_user.log`). `removeDecoyHits` after `FalseDiscoveryRate` is redundant because decoy hits are already dropped. Both are harmless. |
| 4.1 | Learnability | 3 | Goal/Approach blocks make it easy to apply cold. |
| 4.2 | Consistency | 3 | Insight 2 says a q-value is valid "only if ... targets and decoys competed in ONE concatenated search", then gives estimators for separate searches. The usage-guide reduces this to "separate searches use the mix-max / 2x form". |
| 4.3 | Feedback design | 3 | Each block names its product, but there is no reporting template (decoy count, ID count, score at cut). |
| 4.4 | Error prevention | 4 | Covers raw-score thresholding, cross-engine scores, PEP vs q, PSM vs protein FDR, few PSMs, open search, rescoring overfitting and DIA entrapment. |
| 5.1 | Discoverability | 3 | The trigger phrase is natural, but the description is long and dense with jargon. |
| 5.2 | Forgiveness | 3 | Three decoy prefixes are accepted. The snippet silently assumes `protein`/`score` columns and one row per spectrum. |
| 6.1 | Credential safety | 4 | None needed. |
| 6.2 | Input validation | 3 | No column, rank or decoy-count checks (the same across the whole template). |
| 6.3 | Data safety | 4 | Local files only. |
| 7.1 | Modularity | 3 | Search, annotation/FDR and table FDR are separate blocks. |
| 7.2 | Modifiability | 3 | The version header is stale against the 3.5 API change. |
| 7.3 | Testability | 3 | The example is self-contained and seeded and it runs, but ships no expected output. The pyOpenMS blocks have no test data. |
| 8.1 | Trigger precision | 4 | Routes out explicitly to protein-inference, ptm-analysis, dia-analysis, quantification and data-import. |
| 8.2 | Progressive disclosure | 3 | Under 500 lines, but no references/ split. |
| 8.3 | Composability | 4 | idXML and q-value hand-offs. All 7 related Skills exist in the clone. |
| 8.4 | Idempotency | 4 | Deterministic. |
| 8.5 | Escape hatches | 3 | "Few PSMs: do NOT trust decoy FDR; inspect spectra manually" plus scope routing. No explicit stop conditions. |

Category totals: Functional 7/12 · Reliability 8/12 · Performance 6/8 · Agent usability 13/16 · Human usability 6/8 · Security 11/12 · Maintainability 9/12 · Agent-specific 18/20 = **78**.

### Gate 8 (shipped means present)
SKILL.md and usage-guide.md point at no `references/` or `scripts/` files, which confirms the lead's finding. The shipped `examples/fdr_filtering.py` exists and is not referenced from SKILL.md. All seven "Related Skills" exist: proteomics/{protein-inference, ptm-analysis, dia-analysis, quantification, spectral-libraries, data-import} and database-access/uniprot-access. **No missing file.**

### Gate 7
Research-only content. Nothing in the Skill or in any output diagnoses, prescribes or triages an individual.

## Step 3: Classification
Category 3 **Data Analysis**, execution **Mode A** (no scripts; the agent writes code from the SKILL.md patterns).
Complexity **Moderate, N = 5**. There are three task types: in-process database search with FDR (pyOpenMS), FDR from an engine's PSM table, and interpretation/rescoring guidance (PEP vs q, separate vs concatenated, Percolator). It has a decision tree with 8 scenario branches. Supporting material is one example and a usage guide, far below the 5+ reference files of a Complex Skill.

---

## Lead checks (from the lead auditor)

**Lead 1: separate-search attribution of Elias-Gygi. CONFIRMED.**
- SKILL.md insight 2, the FDR vocabulary bullet, the failure mode "Concatenated vs separate FDR formula mismatch" and usage-guide Tips all present `FDR = 2 * #decoy / (#target + #decoy)` as "the simple Elias-Gygi 2x-decoy estimator" for SEPARATE searches. The failure mode also says the factor 2 "accounts for false hits that could land in either independent database".
- Sources:
  - Elias & Gygi 2007 (*Nat Methods* 4:207; PMID 17327847). The abstract concludes that "concatenated target-decoy database searches are preferable to separate target and decoy database searches". The 2x estimator counts decoys in the accepted list of that composite search.
  - Gupta, Bandeira, Keich & Pevzner 2011 (*JASMS*, PMC3220955) write the Elias-Gygi estimate as FDR = 2·DD(Σ, T⊕R, t)/D(Σ, T⊕R, t), where T⊕R is the combined database.
  - Käll, Storey, MacCoss & Noble 2008 (*J Proteome Res* 7:29-34; PMID 18067246, "Assigning significance to peptides identified by tandem mass spectrometry using decoy databases") use separate searches with decoys/targets and a π0 correction.
  - Keich, Kertész-Farkas & Noble 2015 (mix-max) refine the separate-search case.
- How much it matters, measured in Input 5 (synthetic separate searches of 12,000 spectra):
  - The Skill's 2d/(t+d) kept **2138** PSMs at a realised FDP of **0.33%**. At the top 2600 targets it estimates 2.06% where the truth is 0.62%.
  - π0·d/t kept **2888** (FDP 1.04%), against an oracle of 2853.
  - The error is **conservative**: it loses about 26% of identifications and claims nothing false.
  - The Skill's "most common silent FDR error" framing is also inverted. d/t on separate searches is Käll's estimator with π0 = 1 (valid, conservative). 2d/(t+d) on a concatenated search is Elias-Gygi's original usage.
  - Scored as a P1 Correctness defect (1.2 = 2), not a methodological veto.

**Lead 2: pyOpenMS path end to end. CONFIRMED (fails as written; runs after one line).**
- `runs/in1_skill_verbatim.py` (both Skill blocks verbatim) exits 1 with `TypeError: Argument 'pep_ids' has incorrect type (expected pyopenms._pyopenms_3.PeptideIdentificationList, got list)`. `IdXMLFile().load(path, [], [])` also fails (`can not handle type`).
- With `peptide_ids = PeptideIdentificationList()`, every Skill call works: `search`, `PeptideIndexing` (decoy_string 'DECOY_', prefix; return 0), `FalseDiscoveryRate().apply` (score becomes q-value, higher_better False), `IDFilter().filterHitsByScore(ids, 0.01)`, `removeDecoyHits` and `IdXMLFile().store`.
- Notes:
  - SSE already sets `target_decoy` during the search.
  - `FalseDiscoveryRate` defaults to `conservative=true`, i.e. (D+1)/T.
  - The R readers named by the Skill all ran on an mzid exported from this search: `mzID::mzID()`+`flatten()` gave 381 rows (33 decoys), `mzR::openIDfile()`+`psms()` gave 381 rows, and `MSnbase::readMzIdData()` gave 387 rows (so the Common Errors row is false). See `runs/r_mzid.log`.

**Lead 3: table snippet guard, +1 and demo competition. PARTLY CONFIRMED.**
- Division by zero: when rank 1 is a decoy, `decoys/targets` gives `inf`. There is no exception or warning, and the running minimum masks it (q = 0.031). This is benign in pandas.
- Missing +1: material. With 33 PSMs and no decoys every q is 0 while 11 PSMs are false.
- Rank handling: the snippet never keeps one hit per spectrum. On a Comet .txt with 5 rows per scan, 4 scans entered the list twice and it kept 57 fewer PSMs.
- Example demo: 1000 null targets and 2000 decoys are scored as independent rows, with no competition. Its "1%" list has a realised FDP of 0.60%.

**Lead 4: Percolator and R claims. CONFIRMED against documentation; Percolator not executed.**
- Percolator wiki (Command-line options):
  - `-y/--post-processing-mix-max` "only has an effect if the input PSMs are from separate target and decoy searches. This is the default setting".
  - `-Y/--post-processing-tdc` "Replace the mix-max method by target-decoy competition"; this is turned on automatically for concatenated input.
  - `--picked-protein` takes the FASTA.
- The Skill's statements match.
- The R functions exist and ran (above); this was execution, not documentation.

---

## Detailed Outputs

### Input 1: Canonical
**Prompt:** "I have an Orbitrap HCD DDA run exported as `sample.mzML` and a concatenated target+decoy FASTA (decoys prefixed `DECOY_`). Using pyOpenMS, search it with trypsin, up to 2 missed cleavages, 10 ppm precursor, 0.02 Da fragment, carbamidomethyl C fixed, oxidation M variable, and give me the PSMs at 1% FDR saved as idXML."
**Data (SYNTHETIC):**
- `data/target_decoy.fasta`: 50 random targets plus 50 reversed `DECOY_` proteins.
- `data/sample.mzML`: 600 MS2 spectra. 300 are b/y spectra from `TheoreticalSpectrumGenerator` for target peptides (15-70% of peaks kept, 50-200 noise peaks, 3 ppm jitter). 300 are pure-noise spectra whose precursor comes 50/50 from target and decoy peptides.
**Code:**
- `runs/in1_skill_verbatim.py`: Skill blocks verbatim.
- `runs/in1_adapted.py`: two changes. The `PeptideIdentificationList` fix, and user settings applied via `getParameters()/setValue()`, because the Skill shows no search-parameter code.
**What ran and printed:**
```
verbatim: TypeError: Argument 'pep_ids' has incorrect type (expected ...PeptideIdentificationList, got list)   exit 1
adapted (user settings):
SSE params: {precursor 10.0 ppm, fragment 0.02 Da, missed_cleavages 2}
[after search]   pep_ids=381 hits=381 target_decoy={'target': 348, 'decoy': 33} score_type=ln(hyperscore)
[after FDR]      hits=348 target only, score_type=q-value higher_better=False
[after filterHitsByScore(0.01)] hits=311
accepted target PSMs=311 correct=298 false(noise spectra)=13 true FDP=0.0418 max q=0.0096   sensitivity 0.993
(defaults, 10 ppm fragment / 1 missed cleavage: 303 accepted, 5 false, FDP 0.0165)
replicates, 8 further seeds (runs/in1_replicates.log): FDP 0.0103 0.0034 0.0102 0.0000 0.0390 0.0036 0.0034 0.0035
  pooled: accepted 2326, false 22, FDP 0.0095
null check, 2000 noise spectra (runs/null_check.log): target hits 274 vs decoy 272 (symmetric null)
```
**Response delivered:**
- `psms_1pct.idXML` with 311 target PSMs at q <= 0.01 and decoys removed.
- The response says that about 300 PSMs sits at the lower edge of where decoy counts are stable. This run's realised error (4.2%) is the variance the Skill warns about, and the pooled replicates are calibrated.
- Protein grouping and protein FDR go to protein-inference.

**Scores:**
- Layer 1 = 32. FC 7 (delivered only after an API fix and self-sourced parameter code) · R&C 8 · Eff 8 · Scope 9.
- Layer 2 = 45. Method 17 (per-spectrum TDC, (D+1)/T, decoys by protein reversal) · Code 9 (fails as written; one-line fix; no parameter code) · QC 7 (no decoy-count or PSM-count check in the code) · Repro 7 (deterministic; version header wrong) · Security 5.
- **Total 77.**

**Assertions:**
- [FAIL] The Skill's pyOpenMS code runs as written on pyopenms 3.5.0. TypeError at `search()`; `IdXMLFile().load` with a list fails too.
- [PASS] Output filters on the q-value (not ln(hyperscore)) at 0.01 and removes decoys.
- [PASS] The delivered 1%-FDR list is calibrated against ground truth: pooled FDP 0.95% over 8 seeds.
- [PASS] Scope: protein-level FDR and grouping are handed to protein-inference.
- [FAIL] The Skill supplies code to apply the user's search settings. Defaults are 10 ppm fragment and 1 missed cleavage.

### Input 2: Variant A
**Prompt:** "I ran Comet against a concatenated target-decoy human DB (DECOY_ prefix) and have the .txt output (scan, num, charge, xcorr, delta_cn, e-value, plain_peptide, protein). Can you compute q-values and give me the PSMs at 1% FDR? What XCorr does that correspond to?"
**Data (SYNTHETIC):** `data/comet_concat.txt`. 12,000 scans (40% with a correct target), 40 null candidates per scan split half target and half decoy, 5 rows per scan (Comet's default `num_output_lines`), plus ground-truth columns.
**Code:** `runs/in2_comet_table.py`. The Skill's snippet is verbatim; `xcorr` is mapped to `score`.
**What ran and printed:**
```
as written -> KeyError: 'score'          (generic column name; mapped xcorr -> score)
(a) Skill snippet, all Comet rows (ranks 1-5)    kept= 2602  unique scans= 2598  true FDP=0.0077
(b) Skill snippet, rank-1 only (proper TDC)      kept= 2659  unique scans= 2659  true FDP=0.0083
(c) rank-1, (D+1)/T                              kept= 2632                     true FDP=0.0072
(d) rank-1, ranked on -log10(E-value)            kept= 2706                     true FDP=0.0085
XCorr at the 1% cut (b): 3.484
```
**Response delivered:**
- Keep rank 1 per scan, because "one best hit per spectrum" resolves the competition. The agent had to infer this; the snippet does not do it.
- Result: 2659 PSMs at q <= 0.01, which corresponds to XCorr >= 3.48 in this run only. Do not reuse that as a fixed cut.
- Recommend Percolator/mokapot per the Skill's default.

**Scores:**
- Layer 1 = 34. FC 8 · R&C 8 · Eff 9 · Scope 9.
- Layer 2 = 47. Method 16 (no rank-1 rule, no +1) · Code 11 (runs after the column map) · QC 7 · Repro 8 · Security 5.
- **Total 81.**

**Assertions:**
- [PASS] Snippet yields monotone q-values and a 1% list with realised FDP <= 1% (0.83%).
- [FAIL] The Skill says to keep only the rank-1 hit per spectrum. Run on all rows, it counted 4 scans twice and kept 57 fewer PSMs.
- [PASS] Output does not threshold on raw XCorr or compare engines.
- [PASS] Scope: PSM level only; protein FDR goes to protein-inference.

### Input 3: Edge
**Prompt:** "Single-bait co-IP, one gel band. Comet gave 33 PSMs and when I computed q-values every PSM came out q = 0, so I was going to write 'all identifications at 0% FDR'. Is that OK? I also attach a second export where the top hit is a DECOY_ protein."
**Data (SYNTHETIC):** `data/pulldown_nodecoy.tsv` has 33 top-1 target PSMs, 11 of them false. `pulldown_topdecoy.tsv` is the same list with the best row relabelled as a decoy.
**Code:** `runs/in3_pulldown.py`, the Skill's snippet verbatim.
**What ran and printed:**
```
pulldown_nodecoy:  decoys=0 false targets=11   warnings: none   kept at q<=0.01: 33 (false among kept: 11)  q min/max 0/0
pulldown_topdecoy: decoys=1   row1 fdr=inf qvalue=0.03125   warnings: none   kept: 0   q = 0.0312 everywhere
smallest q attainable with (D+1)/T at T=33: 0.030
```
**Response delivered:**
- No. Zero decoys does not mean zero false targets, per the Skill's "Decoy FDR on too few PSMs".
- With 33 PSMs the smallest defensible q is about 1/33 = 3%, so a 1% claim is impossible.
- Inspect the spectra manually (fragment coverage) and confirm key peptides by synthetic standards or PRM.
- Do not quote an FDR figure.

**Scores:**
- Layer 1 = 34. FC 8 · R&C 8 · Eff 9 · Scope 9.
- Layer 2 = 48. Method 16 (the right verdict comes from the prose, not the code) · Code 11 (runs; silent `inf`) · QC 8 · Repro 8 · Security 5.
- **Total 82.**

**Assertions:**
- [PASS] Safety: output refuses to report the 33-PSM list as "0% FDR" or as 1%-FDR controlled.
- [PASS] Snippet survives a decoy at rank 1 without crashing (`inf` is masked by the running minimum).
- [FAIL] Snippet q-values reveal that the list is too small: q = 0 on all 33 rows while 11 are false.
- [PASS] Output recommends manual spectrum inspection or orthogonal validation.

### Input 4: Variant B
**Prompt:** "Percolator on our Sage search: 12,431 PSMs at q <= 0.01 but only 7,902 at PEP <= 0.01. My PI wants the PEP <= 0.01 list because it's 'safer'. Which goes in the paper, and for the one peptide we'll validate by PRM, which number should I look at?"
**Code:**
- `examples/fdr_filtering.py` smoke test, run as-is.
- `runs/in4_pep_vs_q.py` applies the example's `add_qvalues` and `add_pep` to the synthetic rank-1 Comet table (a stand-in for the user's run) and restores the demo's hidden truth.

**What ran and printed:**
```
smoke: Targets 2000, Decoys 2000 | q<=0.01: 666 | worst PEP in 1% list 0.102 | PEP<=0.01: 371     exit 0
q<=0.01 : 2659 PSMs, true FDP 0.0083, mean PEP of accepted 0.0170, worst PEP 0.077
PEP<=0.01: 1406 PSMs, true FDP 0.0007
   accepted with PEP in [0.01,0.05): n=991 observed wrong 0.010 | [0.05,0.2): n=262 observed wrong 0.042
lowest-scoring 100 accepted PSMs: mean PEP 0.070, observed wrong fraction 0.070
example demo: kept 666 at q<=0.01, true FDP 0.0060 (1000 null targets vs 2000 decoys, no competition)
```
**Response delivered:**
- Report the q <= 0.01 list. It is a list-level 1% error.
- The PEP <= 0.01 list is a list at roughly 0.1% FDP: half the IDs, with no statistical gain for a discovery table.
- For the single PRM peptide, look at its PEP. The worst PSM inside a 1% list can have a PEP near 8% (here 0.077), which is why per-ID decisions use PEP.
- The example's kernel PEP runs high (mean 1.7% against a 0.83% realised FDP) but is well calibrated at the list boundary.

**Scores:**
- Layer 1 = 35. FC 9 · R&C 9 · Eff 8 · Scope 9.
- Layer 2 = 52. Method 17 · Code 13 (example runs out of the box; crude PEP estimator) · QC 8 · Repro 9 · Security 5.
- **Total 87.**

**Assertions:**
- [PASS] Recommends the q-value for the list and PEP for the single-peptide decision.
- [PASS] Every number comes from executed code.
- [PASS] The shipped example runs as a smoke test.
- [FAIL] The example demo is a faithful concatenated-competition simulation (it uses independent rows; realised FDP 0.60% at nominal 1%).

### Input 5: Stress
**Prompt:** "Our old pipeline searched X!Tandem separately against the target DB and a reversed DB (same spectra), and a student merged the two result tables. How do we get a proper 1% FDR from that? Would rescoring with Percolator help, and which options do we use?"
**Data (SYNTHETIC):** `data/separate_target.tsv` and `data/separate_decoy.tsv`. These are the same 12,000 spectra as Input 2, with the best target hit and best decoy hit per spectrum.
**Code:** `runs/in5_separate_search.py`.
**What ran and printed:**
```
(1) Skill: "Elias-Gygi 2x-decoy" 2d/(t+d), separate        kept= 2138  true FDP=0.0033
(2) Kall 2008 separate, pi0=1: d/t                         kept= 2588  true FDP=0.0062
(3) Kall 2008 separate, pi0-hat=0.611: pi0*d/t             kept= 2888  true FDP=0.0104
(4) per-scan competition (TDC) then d/t                    kept= 2659  true FDP=0.0083
(5) Skill concatenated snippet on the merged file          kept= 2588  true FDP=0.0062
oracle: largest list with true FDP <= 1%                   kept= 2853
   top 2600 targets: true FDP 0.0062 | 2d/(t+d) 0.0206 | d/t 0.0104 | pi0*d/t 0.0063
```
**Response delivered (as the Skill directs):**
- The search mode is separate, so do not use the concatenated d/t snippet as-is.
- For separate searches, use the Skill's "Elias-Gygi 2x-decoy" estimator (result: 2138 PSMs) or mix-max.
- Better: rescore with Percolator. For separate input, mix-max is the default; `-Y/--post-processing-tdc` switches to target-decoy competition (which gave 2659 here). Use cross-validated training.
- `--picked-protein <fasta>` belongs to protein-inference.
- Percolator was **not executed**: there is no Windows build. Flags were checked against the Percolator wiki.

**Scores:**
- Layer 1 = 30. FC 6 (a valid but under-powered answer that passes the wrong citation on to the user) · R&C 7 · Eff 8 · Scope 9.
- Layer 2 = 42. Method 12 (mis-attributed estimator, no π0, inverted failure-mode mechanism) · Code 11 (the Skill gives no separate-search code; Percolator not runnable here) · QC 7 · Repro 7 · Security 5.
- **Total 72.**

**Assertions:**
- [PASS] Identifies the search mode as separate and does not apply the concatenated snippet blindly.
- [FAIL] The separate-search estimator the Skill prescribes is correctly attributed and calibrated. It reported 2.06% against a true 0.62%, and kept 2138 PSMs where π0·d/t kept 2888.
- [PASS] Percolator guidance matches the documentation.
- [PASS] Warns about rescoring overfitting and cross-validation.
- [PASS] Scope: picked protein FDR goes to protein-inference.

---

## Research Veto (Category 3)
| Dimension | Result | Detail |
|---|---|---|
| M1 Scientific integrity | PASS | Nothing fabricated. The Elias-Gygi issue is a real paper cited for the wrong setting. It is recorded as a correctness defect (P1). |
| M2 Practice boundaries | PASS | Research proteomics only. |
| M3 Methodological ground | PASS | Core TDC, q-value and PEP doctrine is sound. The separate-search prescription over-estimates FDR (conservative) and does not invert conclusions. |
| M4 Code usability | PASS | Positive evidence: the pyOpenMS pipeline runs after the one-line adaptation the Skill's version rule directs. The table snippet, the example, and the three R readers ran. The Percolator flags exist in its documentation. |

## Final Arithmetic
- Static 78 × 0.4 = **31.2**
- Execution average = (77 + 81 + 82 + 87 + 72) / 5 = 399 / 5 = **79.8**, × 0.6 = **47.9**
- Final = 31.2 + 47.9 = 79.1, which rounds to **79**. That is the Limited Release band.
- Floors for Limited Release: static 78 ≥ 70 ✓ · execution 79.8 ≥ 75 ✓ · L1 33.0 ≥ 28 ✓ · L2 46.8 ≥ 42 ✓ · assertions 16/22 = 72.7% ≥ 80% ✗. One floor is missed, so the grade drops one tier to **⚠️ Beta Only**.
- **Deployable: false**. No veto fired (veto_override false).

For the candidate spec (supporting role needs ≥ 75, deployable, no open P0), the Skill does not qualify as it stands. The two P1 fixes would clear it: correct the separate-search estimator, and the PeptideIdentificationList change.

## Recommendations
- **[P1] Correct the separate-search FDR estimator and citation** (Input 5).
  - SKILL.md insight 2, the FDR vocabulary, the failure mode (Trigger, Mechanism and Fix) and the usage-guide tip all need changing.
  - Replace with: concatenated TDC uses (decoy+1)/target (Elias-Gygi's 2d/(t+d) is the older, conservative whole-list form); separate searches use π0·decoy/target (Käll et al. 2008, *J Proteome Res* 7:29) or mix-max (Keich 2015).
- **[P1] Update the pyOpenMS code to `PeptideIdentificationList`** (Input 1).
  - Use `peptide_ids = PeptideIdentificationList()` in both blocks and in the IdXMLFile Common Errors row.
  - Correct the version header.
- **[P2] Make the table snippet rank-1 and +1 corrected** (Inputs 2, 3): `drop_duplicates('scan')` after sorting, and `(decoys + 1) / targets.clip(lower=1)`.
- **[P2] Show SimpleSearchEngineAlgorithm parameter setting** (Input 1): tolerances, missed cleavages and mods. Also note the `decoys` option and that the search already annotates target/decoy.
- **[P2] Fix two Common Errors rows and the example demo** (Input 4).
  - `MSnbase::readMzIdData` exists.
  - An unannotated idXML raises a RuntimeError rather than returning zero q-values.
  - The demo should draw one target and one decoy score per null spectrum and keep the higher.

**Unverified:** Percolator and mokapot were not executed. The page numbers of the Skill's reference list were not checked individually, apart from Elias & Gygi 2007, Käll 2008 and Keich 2015.
