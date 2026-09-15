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
