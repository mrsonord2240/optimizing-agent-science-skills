# bio-proteomics-peptide-identification fixes (2026-09-15)

Candidate `mass-spec-proteomics-analyst`. Worktree `F:\OpenScience\external\bioSkills-wt-proteomics-b`, branch `fix/proteomics-b`, commit `e116b7a`. Runtime: pyOpenMS 3.5.0, pandas/numpy in the candidate venv; audit data `audits/bio-proteomics-peptide-identification/data` (copied to scratchpad).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Elias-Gygi 2d/(t+d) given as the separate-search estimator | P1 | Insight 2, FDR vocabulary, table Approach, failure mode (Trigger/Mechanism/Symptom/Fix) and usage-guide tip: concatenated (D+1)/T (2d/(t+d) = older whole-list form), separate pi0*D/T (Kall 2008) or mix-max; Kall et al. 2008 JPR 7:29-34 added to References | docs + audit run: Input 5 (2d/(t+d) 2.06% estimated vs 0.62% true, 2138 vs 2888 PSMs) | Method-level wording change backed by the audit's simulation |
| `peptide_ids = []` fails on pyOpenMS 3.5 | P1 | `PeptideIdentificationList()` in the search block; version header 3.5.0; Common Errors row with real TypeError text | ran: both blocks on audit `sample.mzML` + `target_decoy.fasta`, exit 0, 311 PSMs at q <= 0.01; idXML reloaded into a `PeptideIdentificationList` (381) | |
| Table snippet not rank-1, no +1 | P2 | `drop_duplicates('scan')` after sorting; `(decoys + 1) / targets.clip(lower=1)` | ran: `comet_concat.txt` 2632 PSMs, all unique scans, true FDP 0.72%; pulldown tables q floor 0.030 / 0.062 (nothing passes 1%) | |
| No SimpleSearchEngineAlgorithm parameter code | P2 | getParameters/setValue for precursor/fragment tolerance and unit, missed cleavages, fixed/variable mods; `decoys` option and built-in target/decoy annotation noted | ran: values read back (0.02 Da, 2 MC, mods) | Param names from the 3.5.0 `getParameters()` listing |
| Common Errors rows wrong; example demo has no competition | P2 | `readMzIdData` row replaced; FDR row gives real `RuntimeError: Meta value 'target_decoy' does not exist`; added all-q=0 row; `build_demo_table` draws one target + one decoy per spectrum and keeps the higher, `add_qvalues` rank-1 + (D+1) | ran: py_compile; example exit 0; realised FDP 0.21% (seed 0), 9 seeds 0-1.3%, pooled about 0.7% | Error text from audit `runs/claim_unannotated_fdr.log`; readMzIdData existence from audit `runs/r_mzid.log` |

Unfixed: none in scope. Percolator not run (no Windows build); its flags were already correct per the audit.

## Pass 2 (2026-09-15)

Re-audit score 79, not deployable. Worktree `F:\OpenScience\external\bioSkills-wt-prot2`, branch `fix/proteomics-2`, cut from `575ab94`. Runtime: candidate venv (pandas 2.2, numpy); real data PXD070049 Sage 0.14.6 search copied from `audits/.../rerun/sage/out/results.sage.tsv`; synthetic tables copied from `audits/.../data`. Both blocks were extracted from the worktree SKILL.md and run verbatim (only the `read_csv` line replaced by the passed frame).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| PSM-table snippet misses lowercase `rev_` decoys (Sage, the Skill's own default engine, and FragPipe) | P1 | `DECOY_PREFIXES = ('decoy_', 'rev_', 'xxx_')` compared against `protein.str.lower()`, and a `ValueError` when zero decoys are found; same change in `examples/fdr_filtering.py`; Approach sentence and two Common Errors rows | ran: FragPipe-style `rev_` table now finds 3813 decoys, keeps 2632 PSMs at true FDP 0.72% (identical to the `DECOY_` case, was 12000 kept); real Sage PXD070049 finds 222 decoys (= Sage's own 222 `label == -1`) and keeps 1406 PSMs, a set-identical match to Sage's `spectrum_q <= 0.01` list (was all 1939 kept incl. 222 decoys); a decoy-free table now raises | The auditor's P1. `REV__` (MaxQuant) is covered by the `rev_` prefix |
| Score orientation not stated | P2 | Comment says `score` must be higher-is-better, with `-log10(E-value)` for Comet e-value / MS-GF+ SpecEValue; Common Errors row for the empty 1% list | ran: `-log10(e-value)` as score keeps 2574 PSMs at true FDP 0.66% (the raw E-value gives an empty list) | |
| Picked-group FDR credited to The 2016 | P2 | Taxonomy row now `Savitski 2015; The 2022`; Savitski 2015 and The 2022 (MCP 21(12):100437) added to References | docs: same citation the fork's protein-inference SKILL.md reference list carries | |
| Redundant PeptideIndexing after SimpleSearchEngine | P2 | Approach says indexing is for idXML from other engines or after changing the FASTA; the block above is already annotated | docs + internal consistency with the search block's own "already annotates `target_decoy`" | Prose only; the code is unchanged so the block still runs standalone |

Unfixed:
- **[P2] No code for the separate-search pi0 estimator.** Added the conservative `pi0 = 1` default and the Percolator mix-max pointer to the Approach prose instead; a new estimator function is new content, out of scope per the brief.
- **[P2] Percolator, mokapot and MSFragger lack command lines.** New content, out of scope; no Windows Percolator build to verify against either.

## Pass 4 (2026-09-15) -- new executable content, not a correction pass

Re-audit score 79, Beta Only, not deployable; core Skills need 85. The re-auditor's verdict on what
remained after pass 2 was **"no DDA executor at all"**. Sam's exception to the fix brief on
2026-09-15: adding the missing executables is in scope for this pass.

Worktree `F:\OpenScience\external\bioSkills-wt-prot4a`, branch `fix/proteomics-4-dda` cut from
`fix/proteomics-3` (`e8d2cd4`). **Commit `6476b0e`**, one commit, 4 files, +327/-4.

Runtime and versions actually invoked: OpenMS 3.5.0 `DecoyDatabase`, Sage 0.14.6 (binary inside the
v0.14.7 release zip), Comet 2026.02 rev.2 (6edec91), MS-GF+ v2024.03.26 + `MzIDToTsv` (Java 17.0.19
Adoptium), Percolator 3.09.0 (build 2026-05-21), Philosopher v5.1.0, msconvert 3.0.26253 (mzML
already converted), shared venv Python 3.12 with pandas 3.0.5 / numpy 2.5.3 / pyteomics 5.0.1.
Nothing was installed and no version in the shared venv or R-lib was touched.

Data: **public CC0** `PXD070049` (Van Puyvelde et al., LFQ Benchmark Generation Beta), Orbitrap
Astral 5-min DDA, 250 pg HYE, `LFQ_Astral_DDA_5min_250pg_Condition_{A,B,C}_REP1`, FASTA
`uniprotkb_proteome_HYE_UniversalContaminants.fasta` (31,437 entries); submitter SDRF only. One
replicate per condition, so nothing below claims a within-condition CV. Plus the audit's synthetic
tables (`separate_target.tsv`, `separate_decoy.tsv`, `sample.mzML`, `target_decoy.fasta`) copied
read-only into the scratchpad.

| addition | audit input it answers | change | run evidence |
|---|---|---|---|
| **New section "Build the Concatenated Target-Decoy Database"** + per-tool decoy-tag table (`DECOY_` OpenMS/Comet, `rev_` Sage/FragPipe/Philosopher, `XXX_` MS-GF+, `REV__` MaxQuant) | Inputs 6 and 8 (the `rev_` P1 that pass 2 fixed in code only -- the Skill never said where the tags come from); static Completeness | `DecoyDatabase -in ... -method reverse -enzyme Trypsin` | ran: 31,437 -> 62,874 entries, 31,437 `^>DECOY_`, 5.0 s wall (OpenMS 3.5.0) |
| **New section "Run a DDA Search from the Command Line"** -- Sage, Comet and MS-GF+ invoked with real Orbitrap parameters | static Functional suitability ("Percolator/mokapot/MSFragger still have no command line"); the "no DDA executor" verdict | 3 concrete command blocks, all with the decoy handling spelled out | ran, Condition A REP1 (6,135 MS2): **Sage** 10 s -> 1,939 PSMs, 222 `rev_` decoys, 1,406 targets at its own `spectrum_q <= 0.01`. **Comet** 11 s -> 6,113 PSMs, 2,168 decoy rows, raw `-log10(e-value)` TDC = **916** at 1% FDR. **MS-GF+** 83 s -> 6,806 rank-1 rows over 5,949 scans, 2,575 decoys, `-log10(SpecEValue)` TDC = **656** at 1% FDR |
| **New section "Rescore to FDR-Controlled PSMs with Percolator"**, incl. `-Y` vs `-y` read off the installed binary's own `--help` | Input 5 (Percolator was *not executed* in the audit -- "no Windows build"); static Completeness | `percolator --post-processing-tdc --results-psms ...` | ran, Percolator 3.09.0: Sage pin -> **1,398** PSMs / 1,367 peptides at q <= 0.01 (1 s); Comet pin -> **1,144** / 1,138 (0.7 s), a **+24.9%** gain over Comet's own score; three DDA runs pooled (6,864 PSMs) -> **5,006** PSMs vs Sage's own 4,961 |
| **"Which engine wins" paragraph** with the measured comparison and an explicit do-not-generalise caveat | the brief's "say which engine wins for which input" | prose | Sage 1,406 > Comet+Percolator 1,144 > MS-GF+ 656 on this input. Sage gains nothing from Percolator (1,406 -> 1,398, -0.6%) because `sage_discriminant_score` is already learned; Comet gains most. Species mix of the Sage 1% list: HUMAN 920 / YEAST 414 / ECOLI 24 / other 40, consistent with the 65:30:5 design |
| **New section "FDR from SEPARATE Target and Decoy Searches"** with `estimate_pi0` + `separate_search_qvalues` | **Input 5 FAIL**: "Skill supplies code for the separate-search estimator (pi0 estimate) -- none". Pass 2 left this unfixed as out of scope | Kall 2008 median-decoy estimator as running code, in SKILL.md and as a shipped script | ran, block extracted **verbatim** from the edited SKILL.md: pi0-hat **0.611** -> 2,888 kept, true FDP **1.04%**; pi0 = 1 -> 2,588 kept, true FDP **0.62%**; 2d/(t+d) misapplied -> 2,139 at 0.33%. Reproduces the auditor's own Input 5 numbers |
| **`examples/dda_search.sh`** (new) -- database -> search -> Percolator -> 1% list, `ENGINE=sage\|comet` | the "no DDA executor" verdict; Maintainability (an example with a stated expected output) | 130-line bash, tool paths overridable by env var | `bash -n` clean; **executed end to end from the worktree twice**: `ENGINE=sage` -> 1,398 PSMs / 1,367 peptides, 33.1 s; `ENGINE=comet` -> 1,144 / 1,138, 26.7 s; both including the DecoyDatabase step |
| **`examples/separate_search_fdr.py`** (new) | Input 5 FAIL | script form of the pi0 estimator, with a ground-truth FDP readout when the table carries `is_correct` | `py_compile` clean; ran -> `pi0-hat 0.611 / kept 2888 / true FDP 0.0104`, `pi0=1 / kept 2588 / 0.0062` |
| **Common Errors: Percolator q-value column index** | found by running, not by the audit | Percolator emits a `filename` column only when the pin has one (Sage yes, Comet no), so `q-value` sits at column 4 or 3 | ran: the first `ENGINE=comet` end-to-end returned **885** instead of 1,144 because `$4` was `posterior_error_prob`. Fixed to locate the column by header name; rerun gives 1,144, matching the standalone Percolator run byte for byte (same `Found 6113 PSMs` / `Final list yields 1138` log) |
| **Common Errors: doubled decoys** | preventive, from the two engines' flags | `-tda 1` (MS-GF+) / `generate_decoys: true` (Sage) against a DB that already holds decoys | docs + the two runs that used `-tda 0` and `generate_decoys: true` correctly |
| **Common Errors: `philosopher peptideprophet` silently models nothing** | rescoring alternative the brief offered | records the exact symptom and routes rescoring to Percolator | ran 4 times (see "Not added" below) |
| Version Compatibility header and `usage-guide.md` prerequisites | static Learnability | names the five CLI versions the route was checked on; 3 new Tips, 2 new Quick Start lines, decoy-tag warning | -- |

### Regression (nothing from passes 1-3 broken)

- Both pyOpenMS blocks extracted from the **edited** SKILL.md and run on the synthetic
  `sample.mzML` + `target_decoy.fasta`: 381 PSMs -> **311** at q <= 0.01, max q **0.0096** --
  identical to the audit's Input 1.
- `examples/fdr_filtering.py` unchanged, runs: Targets 2445 / Decoys 1555, **481** at q <= 0.01,
  worst PEP inside the 1% list 0.047, **289** at PEP <= 0.01 -- identical to the audit's Input 4.
- The pass-2 table snippet, unchanged, on the fresh Sage search: 222 decoys found by the lower-cased
  `rev_` prefix, **1,406** kept, scan set **identical** to Sage's own `spectrum_q <= 0.01` list.
- Input 7 reconfirmed on real data: MS-GF+ raw `SpecEValue` fed to the snippet as `score` keeps
  **0** PSMs; `-log10(SpecEValue)` keeps 656.

### Not added, and why

- **PeptideProphet.** `philosopher peptideprophet --database ... --decoy DECOY_ --ppm --accmass
  --expectscore --decoyprobs --nonparam` exits 0 on the Comet 2026.02 rev.2 pepXML, writes an
  `interact-*.pep.xml` with all 6,113 `spectrum_query` entries intact, and then logs
  `read in 0 1+, 0 2+, ... spectra` / `read in no data`; the output contains **zero**
  `peptideprophet_result` elements. Confirmed four ways: with the full semi-supervised flag set and
  with `--database` alone; with the mzML absent, present under its real name, and renamed; and from
  a 28-character working path (so not MAX_PATH). Philosopher's embedded build reports
  `PeptideProphet (TPP v5.2.1-dev Flammagenitus, Build 201906281613)`. Rescoring is therefore
  documented through Percolator only, and the symptom is in Common Errors so an agent checks the
  output rather than the exit code. TPP itself is not installed and will not be
  (`notes/tpp-installer-blocked-by-newer-vcredist-20260915`), so no TPP-only binary is referenced
  as a required step anywhere.
- **mokapot command line.** `mokapot` 0.10.0 is in the shared venv and would take the same Sage pin,
  but Percolator already covers the rescoring step end to end and a second rescorer adds surface
  without adding a pillar. Named in the taxonomy as before.
- **MSFragger / MaxQuant.** Registration-gated and absent; never routed through as a primary path.
- **Mix-max executed.** `-y` was verified from the installed Percolator 3.09.0's own `--help` text
  ("only has an effect if the input PSMs are from separate target and decoy searches"), which is a
  stronger check than pass 2's wiki lookup, but it was not *run*: doing so would need a fabricated
  pin (the synthetic separate-search tables carry no peptide sequences), and fabricated peptide
  strings have no place in a verification record.

### Nothing needed from Sam

No package was installed and no shared version changed. The worktree is committed and left unpushed.

## 2026-09-21 - six P2 findings, redundancy pass, split, scripts (fixer, branch `fix/proteomics-peptide-identification`)

Audit: `eval_report_bio-proteomics-peptide-identification_result.json` (90, Production Ready, 6 P2s, none left open). Base staging `main` 431aa55. Commits: fix `4067762`, redundancy `13235eb`, split `8fdf52f`, scripts `3bc0227`. Env: `mass-spec-proteomics-analyst` (Sage 0.14.6, Comet 2026.02 rev.2, Percolator 3.09.0, OpenMS 3.5.0 DecoyDatabase, mokapot 0.10.0, pyOpenMS 3.5.0, pandas 3.0.5, numpy 2.5.3). Real data: PXD070049 Astral DDA Conditions A/B/C REP1 and the HYE FASTA; synthetic tables from the audit `data\`. No MSFragger/FragPipe jar was run.

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| dda_search.sh hides Percolator's error | P2 | pre-flight awk check that the pin's `Label` column has both 1 and -1 (prints the counts, exits 1 with the decoy-tag hint); Percolator call wrapped in `if !` that prints `tail -n 5 percolator.log` to stderr | ran: Comet with a `XXX_`-tagged database -> "6113 targets, 0 decoys", exit 1, message on console; fake failing Percolator -> exit 1 with its last line shown; Sage single run unchanged (1,717/222 pin, 1,398 PSMs, 1,367 peptides) | took the audit's second suggestion (check + trap-like tail) rather than `tee` |
| No shipped route for multi-run pooling | P2 | `MZML` accepts several space-separated paths; Sage gets them in one call, Comet is looped (`-N comet_run<n>`) and the pins merged with the header once; SKILL/cli_route note the pooling recipe | ran: Sage x3 -> 5,006 PSMs / 2,760 peptides (audit: 5,006); Comet x3 -> 20,809 pin rows, 4,120 PSMs / 2,337 peptides | paths with spaces unsupported (stated in the script header) |
| Zero-decoy stop loses the q-floor hint | P2 | ValueError message now carries the row count and `1/rows` floor (in `scripts/table_fdr.py`, moved from the SKILL.md block) | ran: `pulldown_nodecoy.tsv` -> "...smallest reachable q is 1/33 = 0.030"; `pulldown_topdecoy.tsv` -> 0 kept; rev_ variant -> 2,632 kept | wording is the audit's proposed fix |
| mokapot/MS2Rescore promised, not routed | P2 | mokapot: command and by-name q-value awk added beside Percolator (`references/cli_route.md`), single/pooled counts stated, Install line, and a Common Errors row. MS2Rescore: claim deleted from the description, decision-tree row, and the taxonomy row (now DeepLC + MS2PIP -> spectral-libraries); Declercq 2022 reference removed | ran: mokapot 0.10.0 on the Sage pins -> 1,406 (single, same as Sage) and 4,970 (pooled; Percolator 5,006, Sage 4,961). Command needs no `--decoy_prefix`; output is targets-only with column `mokapot q-value` | **mokapot 0.10.0 does not run unpatched in this env**: pandas 3.0.5 rejects `pd.to_numeric(errors="ignore")` (`mokapot/parsers/pin.py:238`) and numpy 2.5.3 has no `np.float_` (`qvalues.py:66`). The runs above used a test-only `sitecustomize.py` shim on `PYTHONPATH` (nothing installed, nothing changed in the env). The Common Errors row says so. MS2Rescore is not installed (TOOLS.md: not imported by any Skill; `psm-utils` would pin pyteomics), so "delete the claim" |
| examples/fdr_filtering.py unreferenced | P2 | cited from Insight 3 (PEP vs q-value) | ran in the audit; text change only, checked the file name against `examples/` | |
| 366-line SKILL.md, no progressive disclosure | P2 | split (below) | see below | 379 lines after the fix commit -> 200 after the split -> 202 with the scripts line |

Corrections found while moving code (not audit findings): the pyOpenMS FDR block reported 381 PSMs at 1% because `filterHitsByScore` leaves emptied identifications in the list; `scripts/pyopenms_fdr.py` adds `IDFilter().removeEmptyIdentifications` and now prints 311 (audit: 311, max q 0.0096, reloaded idXML has 0 decoy hits).

### Split (SKILL.md 379 -> 200 lines)

Moved verbatim to `references/`: Run a DDA Search + Rescore with Percolator -> `cli_route.md`; pyOpenMS search and FDR -> `pyopenms.md`; results-table and separate-search FDR -> `fdr_from_tables.md`; reference list -> `citations.md`. The database build with the decoy-tag table stays in SKILL.md (every request needs the trap). Reference Files index and two new decision-tree rows plus a pointer on the DDA row. Checked by a multiset comparison of non-blank lines before/after: only the re-pointed lines differ (DDA row, one "built above" sentence, one "code in ... above" sentence, the dropped `## References` heading); python fences `ast.parse`, bash fences `bash -n`.

### Redundancy pass (usage-guide.md 80 -> 47 lines)

| deleted passage | new home |
| --- | --- |
| Prerequisites: `pip install pyopenms pandas numpy`, CLI engine list, DecoyDatabase, msconvert/ThermoRawFileParser, BiocManager line | SKILL.md Version Compatibility "Install" line |
| "Command-line route checked on Sage 0.14.6 ..." + example script sentence | SKILL.md Version Compatibility and the DDA section of `references/cli_route.md` |
| What the Agent Will Do (7 steps) | SKILL.md Default-when-uncertain line, Insights 1-3, decoy-tag table, Scope |
| Tips: q vs PEP; raw score; concatenated vs separate; decoys at protein level; decoy tags; rescoring gains; Percolator needs PSMs; few PSMs; open search; PSM vs protein FDR | SKILL.md Insights 1-3, decoy-tag table, `references/cli_route.md` rescoring paragraph, Per-Method Failure Modes, Decision Tree |
| Tips: "no blanket 2 unique peptides rule" | protein-inference SKILL.md Insight 3 (grep-verified); this Skill's Scope routes protein-level questions there |

### Runnable code to scripts/

| old location | script |
| --- | --- |
| `references/pyopenms.md` search block (was SKILL.md "Database Search with pyOpenMS") | `scripts/pyopenms_search.py` |
| `references/pyopenms.md` FDR block | `scripts/pyopenms_fdr.py` (loads the idXML; `--decoy-string`, `--fdr`) |
| `references/fdr_from_tables.md` results-table block | `scripts/table_fdr.py` (`--scan/--score/--protein/--out`) |
| `references/fdr_from_tables.md` separate-search block | deleted; duplicates `examples/separate_search_fdr.py`, which the reference now points to (ran: pi0-hat 0.611, 2,888 kept, true FDP 1.04%) |

Each script run exactly as the reference invokes it: 381 PSMs written / 311 at q <= 0.01; 12,000 spectra, 3,813 decoy hits, 2,632 kept (true FDP 0.72%, unique scans); the `rev_` rewrite gives the same 2,632. The three-line Sage/Comet/MS-GF+ block and the DecoyDatabase block stay inline (config sketches and one-liners; `dda_search.sh` is the runnable form).

### Left unfixed

- None of the six findings. Two caveats: mokapot cannot run unpatched on this env's pandas 3 / numpy 2 (documented, not fixable without changing versions); MS2Rescore was removed rather than routed (not installed).
- Noticed, not a finding: MSFragger, MaxQuant, MetaMorpheus, X!Tandem and pFind appear in the taxonomy and decision tree without commands. MSFragger's jars are licence-gated here; the others are named for choice guidance only.
