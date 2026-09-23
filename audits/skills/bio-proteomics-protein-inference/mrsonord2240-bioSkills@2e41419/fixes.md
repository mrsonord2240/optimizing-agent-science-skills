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

## Pass 5 — 2026-09-15 (re-audit at 83, below the CORE floor of 85)

Branch `fix/proteomics-5` (worktree `F:\OpenScience\external\bioSkills-wt-prot5`), branched from
`openscience-fixes` @ `1110c24`. Commit `22fc3f8`. Evidence: the batch-C re-audit at
`F:\OpenScience\audits\bio-proteomics-protein-inference\` (18:57/18:59), run after Percolator 3.09.0
and Philosopher 5.1.0 were installed, which made two previously untestable routes testable. Runtime:
Percolator 3.09.0, Philosopher 5.1.0, pyOpenMS 3.5.0, Comet 2026.02 rev.2. Data: PXD070049 (CC0) DDA
Condition_A REP1 Comet pepXML/pin against a 31,437-protein target + `DECOY_` FASTA, and the audit's
synthetic `peptides_1pct_fdr_std.idXML` + `truth_std.csv`, both copied to scratchpad.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Fido row documents `percolator --protein`, which does not exist in 3.09.0 | P1 | Taxonomy row records Fido as removed and warns not to script it; a NEW row documents `-f` / `--picked-protein`; a decision-tree row and a runnable CLI block added; Version Compatibility gains a CLI-flag introspection bullet; Serang 2010 cited | ran (two independent methods): `--protein` and `-A` absent from the full `--help`, and each exits 1 with `ERROR: the option --protein is invalid.`; `--picked-protein` present in `--help`. Then ran the new block: `percolator -f target_decoy.fasta -P DECOY_ -z trypsin -l prot.target.tsv ... -S 1 comet.pin` -> "Performing picked protein strategy", 2339 target / 1760 decoy proteins after picking, **458 groups at q<=0.01**, and the block's own `awk` check counts the same 458 | reproduces the auditor's 458 exactly |
| FragPipe/TPP route named with no commands, and no "check output, not exit code" rule anywhere | P1 | New **Output contract (CLI)** paragraph; new `philosopher workspace -> database -> peptideprophet -> proteinprophet -> filter -> report` block with an output assertion after every step; decision-tree row rewritten to end in "COUNT THE ROWS in `protein.tsv`"; header bullet and usage-guide tip; two Common Errors rows | ran: `philosopher filter --pepxml comet.pep.xml --tag DECOY_ --picked --razor` (after `workspace --init` + `database --annotate`) exits **0**, logs `Database search results ions=0 peptides=0 psms=0`, `Converged to 0.00 % FDR with 0 PSMs`, `Final report ... proteins=0`, and writes **no** `protein.tsv`. `philosopher peptideprophet` exits **0** writing an `interact-comet.pep.xml` with 6113 `<spectrum_query` and **0** `peptideprophet_result`. The whole shipped block was then run verbatim: `bash -n` clean, Percolator leg -> 458 groups, Philosopher leg stops at the first guard with `PeptideProphet modelled 0 PSMs` | Philosopher's pepXML ingestion is broken in this environment (the auditor confirmed with an OpenMS-re-serialised pepXML); that is environmental. The Skill's defect was the missing verification, and the added guards demonstrably catch it |
| Wrong decoy prefix described as silent ("silently counts decoys as targets") | P2 | Prose corrected: both implementations raise; prefixes listed per tool; a Common Errors row replaces the MaxQuant-only row | ran: `applyPickedProteinFDR(..., String('rev_'), True, True)` on DECOY_ data raises `IndexError: invalid unordered_map<K, T> key`; with `'DECOY_'` it returns 556 groups at 1% (pyOpenMS 3.5.0) | |
| EPIFANY listed first for standard DDA and called "strong at controlled protein-group FDR"; third positional argument undocumented in effect | P2 | Decision tree puts Basic + `greedy_group_resolution` first with the measured comparison; taxonomy row states the numbers; block comment says the third positional argument is `greedy_group_resolution` and that flipping it changed nothing here | ran: on `peptides_1pct_fdr_std.idXML` + picked FDR, EPIFANY = 583 groups / 3.43% true FDP with `False` **and** with `True`; Basic + greedy = 556 / 0.36% | the flag genuinely does not move this dataset, so the comment states that rather than recommending a flip |
| "10-30% false with no protein-level FDR" quoted with no dataset or PSM-threshold condition | P2 | Qualified in all three places (Insight 2, decision tree, failure-mode symptom) with the measured figure | audit run: 113k-PSM synthetic deep benchmark at 1% PSM FDR -> 7.0% true FDP, 14.8% estimated | not re-simulated; taken from the audit's Input 5 |
| No research-use / clinical boundary statement | P2 | One Scope sentence routing patient-level "protein X is present" claims to a validated targeted assay (PRM/MRM) | n/a (text) | |

Also: Version Compatibility line now names Percolator 3.09.0 and Philosopher 5.1.0; usage-guide
prerequisites replaced "ProteinProphet (TPP)" with the Philosopher subcommands (TPP itself is
permanently skipped on this machine) and the Percolator route. All three python blocks re-extracted
from the edited SKILL.md and run (556 and 583 groups); the new bash block passes `bash -n`; file is
pure ASCII with CRLF preserved.

## Left unfixed (pass 5)

- **P2 — "the wrong-prefix failure is described as silent".** Fixed above; listed here only because the
  audit phrased it as two items (built-in and sketch) and both are covered by one row.
- Nothing else from the recommendations list is open. The two ⚠️/low inputs (3 and 6) were both P1/P2
  items addressed above.
- Not a Skill defect, noted only: Philosopher 5.1.0 reads 0 PSMs from **any** pepXML in this
  environment (Comet's and OpenMS `IDFileConverter`'s alike), so the FragPipe route cannot be shown
  producing protein groups here. The block is written so that this fails loudly instead of reporting
  `Converged to 0.00 % FDR`.

## Pass 6 -- 2026-09-21 (fix of the latest re-audit: 1 P1, 3 P2)

Worktree `F:\OpenScience\wt\proteomics-protein-inference`, branch `fix/proteomics-protein-inference`.
Runtime: pyOpenMS 3.5.0, Percolator 3.09.0. Data: audit `peptides_1pct_fdr_std.idXML` + `truth_std.csv`,
and the PXD070049 `comet.pin` + `target_decoy.fasta`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Percolator route emits a flat list; "one row per group representative" | P1 | CLI block comment now says partners are ELIMINATED, not listed, and never to report `prot.target.tsv` as a group list without `--protein-report-duplicates --protein-report-fragments` (`-g -c`); same caveat added to the taxonomy row and the decision-tree row | ran: default run -> 2,339 rows, 0 with a comma; with both flags -> 28 rows list several accessions (e.g. HS71A,HS71B), 458 groups at q<=0.01 either way; flags checked in `--help` | reproduces the auditor's 2,339 / 0 |
| Entrapment advice omits its precondition | P2 | Naive-FDR Fix line now requires a proteome absent from the sample and says a HYE-style multi-species mix does not provide one | text | |
| `DECOY_` hard-coded in shipped code | P2 | `DECOY_PREFIX` constant at the top of the pyOpenMS block; shell variable `DECOY_PREFIX` in the CLI block (Percolator `-P`, Philosopher `--prefix`, `--decoy`, `--tag`) | ran: pyOpenMS block -> 556 groups; Percolator leg verbatim -> 458; `bash -n` clean | |
| pyOpenMS route has no output schema | P2 | Approach names the group record (`leading_protein`, `accessions`, `n_peptides`, `n_unique_peptides`, `is_decoy`, `qvalue`); the default block now builds it, matching `examples/protein_groups.py` | ran: 556 groups pass, 2 false vs truth = 0.36% FDP (same as pass 1); multi-member isoform groups carry both accessions | |

Redundancy pass (each fact once):

| deleted | now lives in |
|---|---|
| Version Compatibility Fido error text; taxonomy Fido row error text | Common Errors `ERROR: the option --protein is invalid.` row |
| Output contract's philosopher reproduction detail | Common Errors philosopher `filter` / `peptideprophet` rows |
| Thresholds rows "Two-peptide rule", "Single-peptide IDs" | Insight 3 and the Two-peptide failure mode |
| Common Errors rows: protein FDR higher than nominal; low-abundance proteins missing; spurious DE on paralogs; unique count changed with DB | Naive-FDR, Two-peptide and Razor failure modes; Vocabulary ("Unique" is DATABASE-RELATIVE) |
| usage-guide Tips (7 bullets), Prerequisites CLI comment, What-the-Agent-Will-Do steps | SKILL.md Insights 1-3, Vocabulary, decision tree, Output contract, Version Compatibility (new Install line carries the pip/CLI/no-TPP note) |

Unfixed: none.

## 2026-09-21 (structure)

Worktree `F:\OpenScience\wt\proteomics-protein-inference`, branch `fix/proteomics-protein-inference`. Behaviour and claims unchanged. Env `mass-spec-proteomics-analyst`, pyOpenMS 3.5.0.

**Split** (commit `549e28b`): `SKILL.md` 318 -> 167 lines; four sections moved verbatim into `references/` (0 non-blank lines lost, checked by multiset comparison; python fences `ast.parse`, bash fence `bash -n`).

| old location | new file |
|---|---|
| "Group Proteins with pyOpenMS" (lines 87-143) | `references/pyopenms-basic-inference.md` |
| "Bayesian Inference + Group FDR with EPIFANY" | `references/epifany-bayesian-inference.md` |
| "Picked Protein-Group FDR" | `references/picked-group-fdr.md` |
| "Protein Groups from the CLI: Percolator and Philosopher" | `references/percolator-philosopher-cli.md` |

Added: "Reference Files" index, pointers in four decision-tree rows, the Percolator taxonomy row and the default-when-uncertain line. Two dangling cross-references retargeted ("shown above" -> `pyopenms-basic-inference.md`; "Output contract above" -> "in `SKILL.md`").

**Scripts** (commit `2e41419`):

| old location | script | how run |
|---|---|---|
| pyOpenMS block (`references/pyopenms-basic-inference.md`) | `scripts/group_proteins_pyopenms.py` (args: idXML, `--decoy-prefix`, `--fdr`, `--out`) | on audit `peptides_1pct_fdr_std.idXML`: 556 groups at 1%; vs `truth_std.csv` 2 false (0.36% FDP), multi-member groups present; `--decoy-prefix rev_` raises as documented |
| EPIFANY block | `scripts/epifany_inference.py` (`--greedy-group-resolution`, `--out`) | same idXML: 749 groups, posteriors in [0,1] (assertions); flag runs too |
| `picked_group_fdr` sketch | `scripts/picked_group_fdr.py` (importable function + CLI on a TSV) | on the EPIFANY table: 586 target groups at q<=0.01 (20 false vs truth = 3.4%, matches the 3.43% already logged); `--decoy-prefix REV__` raises `ValueError`; toy pairing case returns the expected two groups |

Kept as a script, not deleted for `examples/protein_groups.py`: the sketch's wrong-prefix guard (raises when no accession carries the prefix) differs from the example's (raises only when `is_decoy` marks none), so it is not a duplicate. SKILL.md Common Errors row now names `scripts/picked_group_fdr.py`.

**Stayed inline:** the Percolator / Philosopher CLI block (`references/percolator-philosopher-cli.md`). The Percolator leg is under 15 lines, and the Philosopher leg cannot produce output on this machine (Philosopher 5.1.0 reads 0 PSMs from any pepXML, see pass 5), so no script could be run to a real result.

## Final pass Phase 1 — 2026-09-22

Worktree `F:\OpenScience\wt\proteomics-protein-inference`, branch `fix/proteomics-protein-inference`,
tip `2e41419be0f5d52378d18ce545c162a611006a93`. Runtime: pyOpenMS 3.5.0, Percolator 3.09.0,
Philosopher 5.1.0. No source edit was warranted: every runnable block and shipped script was executable
as documented, and the one known unable-to-produce route trips its explicit output guard.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Previously unverified whole-Skill runnable-block sweep | P1 | No Skill change; added final-pass execution evidence and checkpoint | ran: Basic+greedy 556 passing groups, EPIFANY 749 posteriors in [0,1], picked-group script 586 groups and rejects `REV__`, Percolator 458 groups, example 2 target groups; every shipped Python script compiled | Audit fixture and PXD070049 Comet artifacts preserved outside the worktree |
| Percolator/Philosopher CLI block after structure move | P1 | No Skill change; ran the Percolator leg and the staged-name Philosopher guard exactly | ran: Percolator `prot.target.tsv` 458 q<=0.01; Philosopher processes 6,135 results but writes zero `peptideprophet_result`, so `grep` guard exits 1; `bash -n` clean | This confirms the Skill refuses the known silent-empty result rather than accepting exit 0 |
| CLI flags after structure move | P2 | No Skill change | help: Percolator `--picked-protein`; Philosopher `--maxppmdiff`, `--psm`, `--pepxml`, `--protxml`, `--picked`, `--razor` | No missing or renamed option found |

## Left unfixed (final pass Phase 1)

- **Positive Philosopher / ProteinProphet output path:** blocked by Philosopher 5.1.0's local pepXML
  ingestion failure (it reports `read in no data` for this Comet input and the earlier OpenMS-reserialised
  input). It needs a functioning compatible Philosopher/TPP environment or compatible pepXML fixture.
  The Skill's current guard is tested and correct; a separate TPP-install retry is explicitly excluded by
  Sam's 2026-09-15 decision.
