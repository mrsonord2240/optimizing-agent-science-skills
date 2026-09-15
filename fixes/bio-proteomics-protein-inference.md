# bio-proteomics-protein-inference fixes (2026-09-15)

Candidate `mass-spec-proteomics-analyst`. Worktree `F:\OpenScience\external\bioSkills-wt-proteomics-b`, branch `fix/proteomics-b`, commit `3ed1d26`. Runtime: pyOpenMS 3.5.0; audit data `audits/bio-proteomics-protein-inference/data` (std idXML + truth, copied to scratchpad).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `BasicProteinInferenceAlgorithm` called parsimony; 8.6% true FDP at 1% | P1 | Described as score aggregation (taxonomy row, bullets, decision tree, default); block sets `greedy_group_resolution='true'` and applies `FalseDiscoveryRate().applyPickedProteinFDR(prot_id, String('DECOY_'), True, True)`; subsumable-before-counting stated | ran: block on `peptides_1pct_fdr_std.idXML`: 556 groups at q <= 0.01, true FDP 0.36%, 0 fragment groups | `applyPickedProteinFDR` signature from pyOpenMS 3.5.0 docstring |
| `EpifanyAlgorithm` absent; `[]` fails; bytes accessions | P1 | `BayesianProteinInferenceAlgorithm`, `PeptideIdentificationList()`, `.decode()`; version note and header 3.5.0; three Common Errors rows | ran: EPIFANY block on std idXML, exit 0, 749 groups | |
| Example drops indistinguishable proteins as subsumable; lead order-dependent | P1 | Identical-evidence proteins collapsed into nodes before the greedy loop; lead = canonical then alphabetical; isoform pair (isoform listed first) and a decoy that wins its pick added; expected output in docstring; bare `report` line removed | ran: py_compile; exit 0; same groups/leads under 3 input orders; audit Input 3 map gives one P09493+P09493-2 group, Q5VU61 subsumable | |
| Naive protein-FDR bias reversed; picked-group credited to The & Kall 2016 | P1 | Insight 2, failure mode, decision tree, thresholds and usage tip split "no protein-level FDR" (anticonservative) from classic non-picked count (conservative) and unresolved groups; The, Samaras, Kuster & Wilhelm 2022 MCP 21(12):100437 cited and added | audit run: Input 5 (no protein FDR 14.3%, naive group-level 0.57% on resolved groups); citation per audit's PubMed check | Not re-simulated |
| `picked_group_fdr` default prefix, exact-set pairing, tiny counts | P2 | Prefix now required; raises when no decoys carry it; warns below 10 decoy groups; exact-set pairing limitation stated; built-in and kusterlab package pointed to; tool prefixes listed | ran: on EPIFANY groups 586 pass; prefix `REV__` raises; 3-decoy example warns | Pairing itself not changed |
| Input contract, MaxQuant semantics, `accessions[0]` comment | P2 | Keep-decoys and score-orientation note; MaxQuant row explains `Protein IDs`, `Majority protein IDs`, group-level `Unique peptides`, REV/CON/site rows; explicit lead choice | help: column names checked against audit `proteinGroups.txt` | |
| Two-peptide effect stated as universal | P2 | Insight 3, failure mode, thresholds, usage tip: FDR effect depends on the PSM threshold | audit run: Input 5 (0.88% -> 0.40%, 365 true groups lost) | |

Unfixed: none in scope. No ProteinProphet/Philosopher commands added (new content).

## Pass 2 (2026-09-15)

No change; left byte-identical. The re-audit (85, Limited Release) reports no P1 and no demonstrated defect in what runs -- every open item is a P2 asking for new content (commands, code for a prose-only step, a report template) or a wording softening, which the brief puts out of scope.
