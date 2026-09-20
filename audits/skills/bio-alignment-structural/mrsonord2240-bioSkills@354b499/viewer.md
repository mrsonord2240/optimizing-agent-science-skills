> **Audit record for `bio-alignment-structural`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@354b499](https://github.com/mrsonord2240/bioSkills/tree/354b4992cd8d2f1bee039510af618da0333821f1/alignment/structural-alignment) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-alignment-structural

Generated: 2026-09-20  |  Source: `mrsonord2240/bioSkills@354b4992cd8d2f1bee039510af618da0333821f1:alignment/structural-alignment`

Category: Data Analysis (3) | Mode D (scripts + CLI + reasoning) | Complexity: Complex -> 7 inputs | Env: F:/OpenScience/audit-envs/alignment (WSL science env alignment: TM-align 20240303, US-align 20241108, Foldseek 10.941cd33, Foldmason 4.dd3c235, DaliLite v5, PyMOL 3.1.0, Biopython 1.88)

All 7 inputs were executed on real structures (RCSB/AFDB downloads + Foldseek CATH50 and AFDB Swiss-Prot). The only synthetic files are three hand-made degenerate PDBs in `run/data/synthetic/`. Scripts are in `run/scripts/`, raw output in `run/logs/`.

## Step 1 - Skill Veto: PASS

| Dim | Result | Evidence |
|---|---|---|
| T1 Stability | PASS | 4/4 shipped examples run; TM-align, US-align, Foldseek, Foldmason, PyMOL and local DaliLite each ran on real inputs |
| T2 Contract | PASS | frontmatter has name, description, tool_type, primary_tool, license |
| T3 Determinism | PASS (with P1) | TM-align, US-align, Foldseek byte-identical over 2 runs (logs/41). Foldmason `--refine-iters 100` is NOT reproducible (3 md5s, aligned-pair Jaccard 0.74; logs/42, 43); `--refine-seed 42` is. Optional MSA path only, one flag fixes it, recorded as P1 rather than a veto |
| T4 Security | PASS | subprocess with argv lists, no shell/eval, no secrets |

## Step 2 - Static score: 70 / 100

| Category | Score | Note |
|---|---|---|
| functional_suitability | 8/12 | Completeness 3 (pairwise, search, multimer, MSA, hybrid all present; no DALI command, no runnable pLM aligner, no p-value/GDT-TS tool, Expresso not runnable offline). Correctness 2 (thresholds and TM-align/US-align/Foldseek/PyMOL patterns verified, but -mm 4 claim, --multimer-tm-threshold on multimersearch, per_column_lddt key, -o output name, evalue filter under alignment-type 1 are wrong). Appropriateness 3. |
| reliability | 7/12 | Fault tolerance 2 (examples use check=True and warn on unequal CA counts, but TM-align exits 0 with no row for degenerate input so tm_align() returns None and the example then raises TypeError; Superimposer silently pairs Ca2+ ions). Error reporting 2 (Common Errors table present but two rows unverified/odd). Recoverability 3. |
| performance_context | 5/8 | Token cost 2 (24 KB single SKILL.md, no references/ split; several long tables of tools that have no runnable pattern). Execution efficiency 3. |
| agent_usability | 12/16 | Learnability 3, Consistency 3, Feedback design 3 (examples print checked values), Error prevention 3 (good twilight-zone, RMSD, pLDDT and TM-caveat warnings; misses hetero-atom/numbering and multimer-flag traps). |
| human_usability | 5/8 | Discoverability 3 (natural prompts in usage-guide). Forgiveness 2 (examples hard-code placeholder filenames reference.pdb/query.pdb//path/to/afdb; no CLI arguments). |
| security | 11/12 | subprocess called with argv lists, no shell, no eval; no secrets. No path validation on user filenames (3 on input validation). |
| maintainability | 8/12 | Modularity 3, Modifiability 3, Testability 2 (no sample data, no asserts in any example, output field meaning only in docstrings). |
| agent_specific | 14/20 | Trigger precision 3, Progressive disclosure 3 (332 lines but no references/), Composability 3 (all 10 cross-skill paths exist), Idempotency 2 (Foldmason --refine-iters 100 is not reproducible run to run, TM-align -o name is not the name given), Escape hatches 3. |

## Steps 4-6 - Inputs, outputs, scores

| # | Type | Basic /40 | Spec /60 | Total | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 35 | 52 | 87 | 4/5 | yes | COMPLETED ✅ |
| 2 | Variant A | 33 | 50 | 83 | 3/5 | yes | COMPLETED ✅ |
| 3 | Edge | 28 | 38 | 66 | 3/5 | yes | COMPLETED ⚠️ |
| 4 | Variant B | 30 | 44 | 74 | 3/5 | yes | COMPLETED ⚠️ |
| 5 | Stress | 24 | 34 | 58 | 2/5 | yes | PARTIAL ❌ |
| 6 | Scope Boundary | 31 | 46 | 77 | 3/4 | yes | COMPLETED ✅ |
| 7 | Adversarial | 30 | 44 | 74 | 3/5 | yes | COMPLETED ⚠️ |

**Execution average: 74.1 / 100** (Layer 1 avg 30.1/40, Layer 2 avg 44.0/60)  |  **Assertion pass rate: 21/34 (62%)**

### Input 1 - Canonical: TM-score/RMSD myoglobin 1MBN vs hemoglobin alpha 1A3N-A (25% id) with examples/tm_align_pairwise.py, cross-checked

**Executed:** True. Ran in WSL (scripts/10_input1_tmalign.py, 11_dali_pymol_crosscheck.sh). Prompt: 'Compute the TM-score and RMSD between myoglobin 1MBN and hemoglobin alpha 1A3N chain A; is it the same fold?'

**What it produced:** TM 0.900/0.8356, RMSD 1.56, Lali 141 equal in TM-align and US-align; DALI Z 20.3; PyMOL super 1.80/cealign 1.61. -o superposed.pdb wrote superposed.pdb.pdb, not the named file.

**Scores:** Basic 35/40 | Specialized 52/60 | Total 87/100

**Assertions:**
- [PASS] TM-score, RMSD and aligned length agree between TM-align and an independent tool - US-align gives identical 0.9000/0.8356/1.56/141; DaliLite Z 20.3 (Skill's >20 band); PyMOL cealign 1.61 A over 136
- [PASS] Output reports both TM normalisations, RMSD and aligned length as SKILL.md requires - example prints tm1, tm2, RMSD, identity; length_align in the dict
- [PASS] Fold interpretation matches ground truth (globin fold conserved; globin vs kinase 1ATP is a different fold) - interpret_tmscore: 0.90 -> equivalent topology; 1MBN vs 1ATP max TM 0.385 -> weak; PKA vs CDK2 0.77 -> same fold
- [FAIL] The superposed-structure file named by output_pdb exists after the call - TM-align 20240303 wrote superposed.pdb.pdb plus five .pml files; superposed.pdb does not exist
- [PASS] No diagnostic/prescriptive content; scope stays structural - no clinical statements

### Input 2 - Variant A: Foldseek homolog search of 1MBN: custom 13-PDB DB, real CATH50, real AFDB Swiss-Prot

**Executed:** True. Ran (scripts/20_input2_foldseek.py) with the example's foldseek_search()/parse_results() on three real databases. Prompt: 'Search myoglobin 1MBN against a structure database and list confident structural homologs.'

**What it produced:** Top hits correct (AFDB: AF-P02185 100% id alnTM 0.992; CATH50 sperm-whale myoglobin domains; custom DB myoglobins then hemoglobins). With --alignment-type 1 the E-value column is 0.88-0.99 so the example's evalue<1e-3 filter returns 0 confident hits; default max_seqs=200 silently caps the hit list.

**Scores:** Basic 33/40 | Specialized 50/60 | Total 83/100

**Assertions:**
- [PASS] Top-ranked hits are the query's own family (ground truth: myoglobins, then globins; no kinase/toxin passes alnTM>0.5,E<1e-3) - custom DB: 1MBO, 1A6M, 1EMY first, 14 confident, 0 non-globin; AFDB: AF-P02185 first (100.0% id)
- [PASS] Every result row parses into the 10 documented columns - 16/16, 200/200, 200/200 rows parsed; no skipped-row warning
- [PASS] Foldseek alignment TM-scores agree with TM-align on the same pair - --alignment-type 1 qTM 0.856/tTM 0.924 vs TM-align 0.8356/0.9000 for 1MBN/1A3N-A (<0.05); AF model TM-align 0.980
- [FAIL] The example's 'confident homologs' filter works for every alignment_type the function accepts - alignment_type=1 gives evalue 0.88-0.99 for true globins -> 0 confident hits; the SKILL recommends type 1 for refinement
- [FAIL] Reported hit count reflects the database, not a silent cap - max_seqs=200 default: 200 rows printed as '200 confident' for AFDB (tooling run with default 1000 gave 999 rows)

### Input 3 - Edge: Bio.PDB Superimposer: myoglobin 1MBN/1A6M (153 vs 151 CA) and apo/holo calmodulin 1CFD/1CLL

**Executed:** True. Ran the unmodified examples/biopython_superimposer.py from copies (scripts/30_input3_superimposer.py). Prompt: 'Compare apo and holo calmodulin and quantify the conformational change' (usage-guide's own prompt).

**What it produced:** Myoglobin pair: 0.483 A, identical to residue-matched truth and TM-align 0.48. Calmodulin: 148 vs 148 'CA' atoms so no warning, but 4 of the holo 'CA' atoms are Ca2+ ions; example prints 13.38 A vs 10.83 A residue-matched truth over 144 pairs.

**Scores:** Basic 28/40 | Specialized 38/60 | Total 66/100

**Assertions:**
- [PASS] Example RMSD equals residue-matched ground truth for a co-numbered pair (1MBN/1A6M) - 0.483 vs 0.483 (151 pairs); TM-align 0.48
- [FAIL] Example RMSD equals residue-matched ground truth for apo/holo calmodulin - 13.378 A (148 pairs incl. 4 Ca2+ ions named 'CA') vs 10.829 A (144 residue-matched pairs)
- [FAIL] The example warns whenever its atom pairing is unsafe - warns only when the two CA counts differ; 148==148 here so no warning although 4 pairs are ion-vs-residue and offsets follow
- [PASS] Output points to TM-align/US-align for unknown correspondence - warning text in the example and SKILL.md 'Approach' sentence do so
- [PASS] No out-of-scope claims - purely geometric

### Input 4 - Variant B: Foldmason structural MSA of 8 globin + 3 kinase structures; per-column LDDT via report-mode 2

**Executed:** True. Ran unmodified examples/foldmason_msa.py from a copy (scripts/40_input4_foldmason.py), then the SKILL.md report-mode-2 recipe, then reproducibility (41/42/43). Prompt: 'Build a structural MSA from these structures with Foldmason and give me per-column LDDT.'

**What it produced:** Output files match the documented names; 19 chain rows x 378 columns for 11 files (example prints 'MSA: 19 sequences'). 90% of TM-align's 1MBN/1A3N-A residue pairs recovered. report.get('per_column_lddt') is None (key is 'scores'). Three unseeded --refine-iters 100 runs give 377/378/378 columns, mean Jaccard of aligned pairs 0.74 (homolog pairs ~0.88); --refine-seed 42 is byte-identical x3.

**Scores:** Basic 30/40 | Specialized 44/60 | Total 74/100

**Assertions:**
- [PASS] All four documented outputs exist (result_aa.fa, result_3di.fa, guide tree .nw, .html report) - family_msa_aa.fa, _3di.fa, .nw, .html present and non-empty
- [PASS] Every MSA row's ungapped length equals the residue count of its PDB chain - 19/19 rows match CA counts (1ATP 336 includes SEP/TPO hetero residues)
- [PASS] MSA agrees with an independent structural aligner on a homologous pair - 127/141 TM-align residue pairs (90%) for 1MBN vs 1A3N-A are aligned pairs in the MSA; globin-globin id 0.48 vs globin-kinase 0.09
- [FAIL] The Skill's per-column LDDT recipe returns per-column values - report.get('per_column_lddt') -> None; values live in report['scores'] (378 values, min -1.0, max 0.81)
- [FAIL] The documented command is reproducible run to run - 3 unseeded runs -> 3 md5s; 28 of 36 pairwise alignments differ; SKILL never mentions --refine-seed (default -1 = random); --refine-iters 0 is deterministic

### Input 5 - Stress: Multi-part: multimer TM (US-align), Foldseek-Multimer search/cluster, easy-cluster on 14 PDBs

**Executed:** True. Ran (scripts/50_input5_multimer.py, 51_multimercluster_probe.sh) with every command copied from SKILL.md. Prompt: 'Compare hemoglobin tetramer 1A3N with the dimer 1IRD and mutant 1HBA, search the complex against a multimer DB above TM 0.5, and cluster all my structures at TM>0.5.'

**What it produced:** US-align -mm 1 -ter 0 correct (1IRD in 1A3N 0.977/0.494; 1HBA vs 1A3N 0.992/0.996). easy-cluster at 0.5 gives globin/kinase/toxin-pure clusters. Three documented multimer commands fail: -mm 4 -byresi 0 segfaults; easy-multimersearch --multimer-tm-threshold -> 'Unrecognized parameter'; easy-multimercluster *.pdb returns one row (last file) with exit 0.

**Scores:** Basic 24/40 | Specialized 34/60 | Total 58/100

**Assertions:**
- [PASS] US-align -mm 1 -ter 0 gives correct whole-complex TM for known pairs - tetramer vs Trp37Arg mutant 0.992/0.996 RMSD 0.55; dimer vs tetramer 0.977/0.494 matches the tooling agent
- [FAIL] The stated remedy for different stoichiometry (-mm 4 -byresi 0) runs and returns a pairwise complex score - US-align 20241108: segmentation fault (rc -11), 'structure_2 is ignored for -mm 4'; -mm 4 is multiple-structure alignment; -mm 1 already handles unequal stoichiometry
- [FAIL] easy-multimersearch accepts --multimer-tm-threshold as printed in SKILL.md - rc=1: Unrecognized parameter '--multimer-tm-threshold' (the flag exists only on easy-multimercluster)
- [FAIL] easy-multimercluster *.pdb ... clusters all supplied structures - 3, 9 and 9 input files gave 1 row (only the last file); a directory argument clustered all 7 correctly; exit code 0 both ways
- [PASS] easy-cluster --tmscore-threshold 0.5 gives fold-pure clusters - 4 clusters: 15 globin chains, 3 kinase chains, PKI peptide, tetanus toxin; no mixing

### Input 6 - Scope Boundary: Evaluate an AlphaFold model against its crystal structure (TM, RMSD, lDDT, GDT-TS) and mask low-pLDDT residues

**Executed:** True. Ran (scripts/60_input6_model_vs_native.py) on the real AFDB model AF-P02185-F1 v6 and 1MBN, plus AF-P04637 (p53) for masking. Prompt: 'Superpose my AlphaFold model of myoglobin on 1MBN, give TM-score, RMSD, GDT-TS and lDDT, and tell me whether it is correctly modelled.'

**What it produced:** TM 0.980, RMSD 0.71 over 153 (TM-align == US-align); Foldseek lddt 0.941 (>0.6 cutoff). Masking verified: 158 of 393 p53 residues (pLDDT<70) masked, alignments unchanged (seeding only). GDT-TS not obtainable from a tool the Skill names: TMscore (extra tool) printed 0.508 for a 0.98-TM model because of an off-by-one residue numbering, 0.985 after renumbering.

**Scores:** Basic 31/40 | Specialized 46/60 | Total 77/100

**Assertions:**
- [PASS] TM-score and RMSD for the model are the same in TM-align and US-align and indicate a near-native model - 0.9742/0.9804, RMSD 0.71, Lali 153 in both
- [PASS] Foldseek lddt for the near-native model exceeds the SKILL's 0.6 'correctly modelled' cutoff - 0.941
- [PASS] --mask-bfactor-threshold 70 masks exactly the low-pLDDT residues - 158 masked 3Di positions = 158 CA with B<70 in AF-P04637; self-search bits/alnTM unchanged (masking affects seeding only)
- [FAIL] The Skill provides a usable path to the GDT-TS it lists as a 'correct fold' criterion - names LGA/MaxCluster/OpenStructure only, none installed and no command; naive TMscore run gave 0.508 vs true 0.985 (numbering trap) and the Skill warns about none of this

### Input 7 - Adversarial: 'Ubiquitin and protein G B1 have TM>0.5, so they are homologs; give me the p-value'

**Executed:** True. Ran (scripts/70_input7_adversarial.py, 71_maxTM_false_positive_matrix.py, 82/83 synthetic probes, 11 DALI). Prompt as the label; ground truth: both are beta-grasp folds in different SCOP superfamilies, not homologs.

**What it produced:** TM-align/US-align: 0.498/0.4215 RMSD 3.14 (borderline), DALI Z 2.8 ('candidate', not homology), Foldseek E 0.029. Skill does not call them homologs. But with its headline metric max(TM1,TM2) a 56-aa chain vs unrelated kinases scores 0.505-0.544 ('same fold'), and a synthetic 10-residue helix vs myoglobin scores 0.846 ('equivalent topology (homologous)'). No shipped tool prints the length-aware p-value the Skill recommends.

**Scores:** Basic 30/40 | Specialized 44/60 | Total 74/100

**Assertions:**
- [PASS] The Skill's guidance does not conclude the pair are homologs - TM 0.498 (<0.5) and DALI Z 2.8 fall in 'weak'/'candidate: verify with biology'
- [FAIL] The recommended larger-TM rule with the 0.5 cut yields no false same-fold call on known-different folds - 3 of 38 known-different-fold pairs >0.5 (1PGA 56 aa vs 1ATP 0.505, 2ITZ 0.538, 1HCK 0.544); normalising by the longer chain gives 0
- [FAIL] The requested length-aware TM p-value (Xu & Zhang 2010) can be produced with the Skill - no formula, command or script; TM-align and US-align print no p-value
- [PASS] Foldseek/DALI corroborating evidence is consistent with the TM-score conclusion - Foldseek E 2.9e-2 alnTM 0.435 (weak); DALI Z 2.8
- [PASS] No fabricated statistics or references - all values traced to tool output

## Research Veto: PASS

- **scientific_integrity**: PASS - No fabricated numbers or identifiers in any output; every TM-score/RMSD/Z quoted was reproduced by a second tool (US-align, DaliLite, PyMOL, Foldseek). Literature citations (e.g. Gilchrist 2026 Science 391:485) could not be checked offline and are not treated as evidence.
- **practice_boundaries**: PASS - Structural-bioinformatics scope only; no diagnostic or prescriptive content in SKILL.md or any of the 7 outputs.
- **methodological_ground**: PASS - No principled fallacy that inverts a conclusion. Weaknesses recorded as P1/P2: the 'larger TM (shorter chain)' headline metric plus the 0.5 cut gives false same-fold calls for chains <60 aa (3/38 known-different-fold pairs, all with 1PGA, 56 aa; a synthetic 10-residue helix scores 0.846 vs myoglobin); the '>0.8 = homologous' row conflates fold with homology.
- **code_usability**: PASS - All 4 shipped examples/*.py run from a clean copy on real data and were asserted against ground truth (Biopython 1.88 OK, no removed-API calls). Defects are in documented patterns, not in a script that will not run: easy-multimersearch --multimer-tm-threshold is rejected (rc=1), USalign -mm 4 -byresi 0 segfaults (rc=-11), easy-multimercluster with a file list silently returns one row (exit 0), report.get('per_column_lddt') is None, tm_align() returns None with exit 0 on a too-short chain. Recorded as P1; core pairwise/search/MSA code paths are runnable.

## Extra checks outside the 7 inputs (also executed)

- Flags verified against `--help` of the installed tools: `TMalign -a T` OK but `-outfmt 2` cannot be combined with `-a/-u/-L/-d`; `foldseek easy-search --alignment-type/--max-seqs/--format-output` OK; `easy-cluster --tmscore-threshold` OK; `createdb --mask-bfactor-threshold` OK (seeding only); `easy-multimersearch --multimer-tm-threshold` does NOT exist; `foldmason easy-msa --refine-iters/--report-mode` OK, `--refine-seed` exists and is undocumented.
- PyMOL `pymol -cq -d "load ..; super ..; ray; png"`: ran, fig.png written (228 KB), super RMSD cycles printed.
- bioconda `tmalign` (usage-guide install line): binary dies with `libgfortran.so.3` (logs/80).
- T-Coffee `-mode expresso`: fails (BLAST/FTP). 3D-Coffee (SKILL form and explicit `-method TMalign_pair,mafft_msa`): both hit the 120 s timeout (rc 124) while T-Coffee retried retired ftp.wwpdb.org/rcsb REST endpoints, no alignment written (logs/81); the template-file format is not documented in the Skill. Not counted as executed inputs.
- MUSTANG (table row only): ran on 3 myoglobins, wrote .afasta/.pdb. DALI web server: gated, not used; DaliLite v5 run locally instead.
- ChimeraX `matchmaker`: not installed (licence-gated download), not executed. pLM aligners (TM-Vec, vcMSA, DEDAL, pLM-BLAST): prose only, no command in the Skill, not executed.
- Common Errors rows: TM-align 'atoms not enough' is really 'Sequence is too short <3' with exit 0; Foldseek wrong DB path -> rc 1 'does not exist'; Foldmason with one structure -> 'structuremsa died'.
- Sibling-skill Biopython 1.88 breakage: none here (Bio.PDB PDBParser/Superimposer/PDBIO unchanged). `git status` and `find` of the staging clone show no `__pycache__`.

## Step 8 - Final

Static 70 x 0.4 = 28.0 | Dynamic 74.1 x 0.6 = 44.5 | **FINAL 73 / 100 - ⚠️ Beta Only** | deployable: False | veto_override: False

Floors: static 70 (<80 for Production Ready), execution avg 74.1, Layer 1 30.1, Layer 2 44.0, assertion rate 62% (<80% for Limited Release).

### Recommendations

**[P1] Foldmason example is not reproducible (no seed)** (inputs [4])
- Problem: foldmason_msa.py defaults to --refine-iters 100; three identical runs give three different MSAs (377/378 columns, aligned-pair Jaccard 0.74, homolog pairs 0.88). --refine-seed is never mentioned.
- Root cause: Random refinement default (--refine-seed -1) shipped without a seed or a note.
- Fix: Add --refine-seed <N> to the example and SKILL.md command, state that --refine-iters 0 is deterministic, and say unseeded runs are not comparable.

**[P1] Foldseek-Multimer commands are wrong or silently lossy** (inputs [5])
- Problem: easy-multimersearch --multimer-tm-threshold is rejected (flag only exists on easy-multimercluster); easy-multimercluster with a file list/glob clusters only the last file and exits 0; 'Foldseek-MM-TM' has no command (it is --alignment-type 1) and the complex-level TM is in the separate <out>_report file, which is not mentioned.
- Root cause: Commands written from the paper/README rather than run against a release; Skill-level flag list not checked against --help.
- Fix: Use a directory argument for easy-multimercluster, drop the threshold flag from multimersearch (or use --tmscore-threshold), document --alignment-type 1 as the -TM mode and the _report file columns, and add a run-and-check line.

**[P1] '-mm 4 -byresi 0' remedy for unequal stoichiometry is wrong** (inputs [5])
- Problem: USalign -mm 4 is multiple-structure alignment (structure_2 ignored) and segfaulted on two complexes; -byresi 0 is unrelated. US-align -mm 1 -ter 0 already handles dimer vs tetramer (0.977/0.494).
- Root cause: Mode taxonomy taken from memory.
- Fix: Replace with: -mm 1 -ter 0 handles unequal stoichiometry; report both normalisations; -mm 2 for chains into an oligomer.

**[P1] Per-column LDDT recipe returns None** (inputs [4])
- Problem: report.get('per_column_lddt') is None on Foldmason 4.dd3c235; the JSON keys are entries, scores, tree, statistics and the per-column values are in 'scores' (-1 for uncomputed columns).
- Root cause: Key name guessed; the Skill hedges ('may evolve') but ships a broken line.
- Fix: Use report['scores'] and note -1 = no LDDT; assert len(scores) equals the MSA column count.

**[P1] Superimposer example silently mis-pairs atoms** (inputs [3])
- Problem: Selecting every atom whose id is 'CA' pulls in Ca2+ ions and all models; positional truncation then pairs ions with residues. Apo/holo calmodulin printed 13.38 A instead of 10.83 A and no warning because the CA counts happened to be equal.
- Root cause: Atom selection by name only; correspondence assumed positional.
- Fix: Select ATOM-record CA of one model (residue.id[0]==' '), pair by (chain, resseq, icode), print the pair count and refuse when the pairing is empty or offset.

**[P1] alignment_type=1 breaks the example's confidence filter** (inputs [2])
- Problem: With --alignment-type 1 Foldseek reports E-values of 0.88-0.99 for true homologs, so 'evalue < 1e-3' returns 0 hits although alnTM is 0.93; the default max_seqs=200 also caps the printed count.
- Root cause: E-value is not meaningful for TM-align re-alignment; filter written for type 2 only.
- Fix: Filter on alntmscore (and lddt) when alignment_type=1, and raise or state the max_seqs cap in the printed summary.

**[P1] Guard tm_align() against degenerate input** (inputs [7])
- Problem: TM-align exits 0 with no data row for a <3-residue or ligand-only file, so tm_align() returns None and the example crashes on result['tm1'].
- Root cause: Exit code trusted; parse result not checked.
- Fix: Raise a clear error when parse_outfmt2 returns None and include TM-align's stdout message.

**[P2] 'Larger TM' headline metric inflates small-chain scores** (inputs [7])
- Problem: max(TM1,TM2) called 'the standard fold-similarity metric' contradicts TM-align's own printed advice (normalise by the reference); 3/38 known-different-fold pairs exceed 0.5 and a synthetic 10-residue helix scores 0.846; interpret_tmscore ignores the <60-residue caveat given in prose and labels >0.8 'homologous'.
- Root cause: Length-asymmetry handled only in prose.
- Fix: Report both normalisations, add a length guard in interpret_tmscore, say fold similarity is not homology, and name a source for the Xu-Zhang p-value or drop the reference.

**[P2] usage-guide installs a broken tmalign package** (inputs static)
- Problem: conda install -c bioconda tmalign gives a 2018 Fortran binary that dies with libgfortran.so.3; -o writes <name>.pdb (superposed.pdb.pdb) not the named file; Expresso needs BLAST/FTP and 3D-Coffee (`-mode 3dcoffee` and an explicit TMalign_pair method) both timed out at 120 s retrying retired RCSB/wwPDB endpoints (rc 124) with no alignment written; ChimeraX not executed.
- Root cause: Install line and outputs not run on a clean machine.
- Fix: Point to the US-align source build or the zhanggroup binary, fix the -o wording, and give the T-Coffee template-file format with a working command.

**[P2] GDT-TS and DALI have no runnable path** (inputs [6])
- Problem: SKILL lists GDT-TS >50 and DALI Z bands but names no installed tool or command for either; the Zhang-lab TMscore binary prints GDT-TS but pairs by residue number (0.508 vs 0.985 for an off-by-one model).
- Root cause: Reference tables without procedures.
- Fix: Add a one-line DaliLite (dali.pl) or web-server step and a TMscore/renumbering note, or remove the bands the Skill cannot help compute.

**[P2] Summary counts chains as structures** (inputs [4])
- Problem: foldmason_msa.py prints 'MSA: 19 sequences' for 11 input files because Foldmason emits one row per chain (<file>_<chain>).
- Root cause: Row count reported as structure count.
- Fix: Print files vs chains, or say so in the docstring.

