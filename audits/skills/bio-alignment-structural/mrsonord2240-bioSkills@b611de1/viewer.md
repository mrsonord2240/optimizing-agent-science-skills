> **Audit record for `bio-alignment-structural`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@b611de1](https://github.com/mrsonord2240/bioSkills/tree/b611de1c303cb454f76e2e10ae39cba0db3e3c06/alignment/structural-alignment) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-alignment-structural (RE-AUDIT of the fixed Skill)
Generated: 2026-09-20 | Source: `mrsonord2240/bioSkills@b611de1c303cb454f76e2e10ae39cba0db3e3c06:alignment/structural-alignment` (copied to `run/skill/`, diff against the worktree empty)
Pre-fix: 73, Beta Only, not deployable (archived at `audits/_pre-fix-20260920/bio-alignment-structural/`). **Now: 85, Production Ready, deployable, no veto, no P0, no P1.**
Auditor: a third agent; the fix log was read but is not evidence. Category Data Analysis, mode D, Complex, N = 9 (7 regression + 2 new), executed 9/9.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical [regression] pairwise 1MBN/1A3N-A | 36 | 55 | 91 | 5/5 | ✅ |
| 2 | Variant A [regression] Foldseek 1MBN (folder, CATH50, AFDB) | 35 | 52 | 87 | 5/5 | ✅ |
| 3 | Edge [regression] Bio.PDB Superimposer | 34 | 51 | 85 | 3/4 | ✅ |
| 4 | Variant B [regression] Foldmason 19 chains | 36 | 54 | 90 | 4/5 | ✅ |
| 5 | Stress [regression + new complexes] multimer | 35 | 53 | 88 | 4/5 | ✅ |
| 6 | Scope Boundary [regression] AF model vs native | 36 | 55 | 91 | 4/4 | ✅ |
| 7 | Adversarial [regression] "homologs, give me the p-value" | 37 | 56 | 93 | 4/4 | ✅ |
| 8 | Variant B **[NEW]** kinase remote homology | 35 | 54 | 89 | 4/4 | ✅ |
| 9 | Edge **[NEW]** T4L, SeMet, AF vs crystal, degenerate inputs | 33 | 49 | 82 | 4/5 | ✅ |

**Execution average 88.4 / 100 | Assertion pass rate 37/41 (90.2%) | Layer 1 avg 35.2/40 | Layer 2 avg 53.2/60**
**Static 81 (x0.4 = 32.4) + 88.4 (x0.6 = 53.0) = 85.4 -> 85.** Floors: static >= 80 ok, execution >= 85 ok, L1 >= 32 ok, L2 >= 48 ok, assertions >= 90% ok (only just).

## What the fix changed, checked by my own runs (pre-fix P1s)

| Pre-fix finding | Verdict now | Evidence (log) |
|---|---|---|
| Foldmason not reproducible (no seed) | fixed | seed 42 twice = same md5 `9f432a6b48` (aa and 3Di); `--refine-iters 0` twice identical; unseeded x3 = 3 different md5; example `__main__` ran (`40`, `21`) |
| `per_column_lddt` is None | fixed | JSON keys `entries, scores, tree, statistics`; `len(scores)` 378 = columns; 30 columns = -1; SKILL.md snippet executed verbatim printed `SNIPPET OK 378` (`40`) |
| Foldseek-Multimer commands | fixed | `easy-multimersearch` on a folder: `_report` 9 columns, 1IRD in 1A3N qTM 0.981 / tTM 0.492; `--multimer-tm-threshold` rejected on search (rc 1, suggests `--multimer-report-mode`); cluster on a directory 9 rows, a 9-file list and a 3-file list each 1 row exit 0 (`50`) |
| `-mm 4 -byresi 0` remedy | fixed | `-mm 4` segfaults (rc -11) and is MSTA in `USalign -h`; `byresi` no longer in either doc; `-mm 1 -ter 0` gives 0.977/0.494 RMSD 0.94, numpy chain-mapping 0.9768/0.4943/0.943 (`50`) |
| Superimposer Ca2+ mis-pairing (13.38 vs 10.83) | fixed | example 10.829 A / 144 pairs; my ATOM-only numpy Kabsch 10.829 / 144; pre-fix pairing reproduced as 13.378; myoglobin 0.483 / 151 = numpy = TM-align (`30`) |
| `--alignment-type 1` E-value filter; cap hides count | fixed | type 1: old filter 0 hits, new alnTM filter 14 (folder) and 200/200 (AFDB); E 0.83-0.99; cap warning at 200 rows; help says default 1000 (`20`, `21`) |
| `tm_align()` returns None on degenerate input | fixed | `RuntimeError` with the tool's message for `one_residue` and `ligand_only`; raw TMalign rc 0, 0 rows (`90`) |
| max(TM) inflates short chains | fixed | 136 real pairs: max rule 3 false same-fold calls (1PGA vs 1ATP/1HCK/2ITZ), min rule 0; guard fires for 56 aa and the 10-residue helix (0.846) (`70`) |
| Broken `tmalign` install, `-o` wording, PDB100 | fixed | `-o sup2.pdb` -> `sup2.pdb.pdb`; install line uses `usalign`/US-align source; `foldseek databases` has no PDB100 (`10`, `91`) |
| GDT-TS and DALI without a runnable path | fixed | `TMscore -seq` 0.9853 / 0.9804 / 0.705 and default 0.508 / 0.593 as documented; DaliLite block gives `1a3n-A 20.3 1.6 141 141 26`; MUSTANG row writes `out.afasta` (3 rows) (`10`, `60`, `80`) |
| Foldmason summary counts chains as files | fixed | 11 files -> 19 chain rows named `<file>_<chain>`, single-chain files bare stem, every row ungaps to the real chain sequence (`40`) |

**Deleted claims.** `Grep` over `run/skill/` for Expresso, 3D-Coffee, T-Coffee, PROMALS3D, mTM-align, FATCAT, ChimeraX, TM-Vec, vcMSA, DEDAL, pLM, fair-esm, byresi: the only hits are the single "Not covered, because no runnable path could be verified" sentence (SKILL.md line 226) and the Hamamsy 2024 reference (line 329). The frontmatter description advertises none of them. usage-guide.md has none.
**usage-guide.md dedup (106 -> 41 lines).** I diffed against the pre-fix file. Removed: install block (now in SKILL "Install", corrected), Quick Start and "What the Agent Will Do" (repeat SKILL "When to Use", Decision Tree), Tips (each already in SKILL; the two only-in-guide facts are in the TM-score table row and the PyMOL sentence), and prompts for deleted tools. Nothing an agent needs was lost.

## Foldseek-Multimer speed claims (left unchecked by the fixer) - judged

SKILL.md line 149: "matches US-align chain-pairing in >99% of cases at 10-100x speedup pairwise and 10^3-10^4x in database mode (Kim et al 2025 benchmark)"; also "AFDB-Multimer or PDB100-Multimer scale".
- My measurement (`50`, 62 real oligomers = 60 RCSB entries + 1HBA + 2HHB, query 1A3N): US-align `-mm 1 -ter 0` 34.7 s (0.56 s/pair); `foldseek easy-multimersearch` on the folder 19.9 s (**1.7x**), createdb 9.5 s + search on the prebuilt DB 6.0 s (**5.8x**). Foldseek reported only 22 of 62 targets (prefilter); no US-align pair with max TM > 0.5 was missing from its report. Shared-target query TM differed by median 0.14 (both low-similarity pairs).
- The bioRxiv abstract (fetched) says "3-4 orders of magnitudes faster than the gold standard": supports the 10^3-10^4 database-scale figure in spirit. The 10-100x pairwise and >99% figures I could not source and did not reproduce at this scale (small complexes, startup-dominated).
- `foldseek databases` (10.941cd33) lists no multimer database and no PDB100 (0 matches, `91`); "AFDB-Multimer"/"PDB100-Multimer" and a usage-guide prompt name objects that cannot be downloaded.
- Judgement: not wrong as a scale statement, unsupported as written. Recorded as P2. Not a veto or P1: it changes no command or result.

## Detailed Outputs

### Input 1 - Canonical [regression] (91)
**Prompt:** "Align these two crystal structures with TM-align and report TM-score, RMSD and the superposition. Then tell me whether they share a fold." (1MBN vs 1A3N chain A, real, 25% id)
**Ran:** `scripts/10_input1_pairwise.py` (fixed example, US-align, numpy from TM-align's alignment, DaliLite block, PyMOL block), log `logs/10_input1.txt`.
```
EXAMPLE tm_align -> tm1 0.9 tm2 0.8356 rmsd 1.56 length1 141 length2 153 length_align 141 superposed_pdb superposed.pdb
INDEPENDENT numpy: lali 141, rmsd 1.5561, tm_by_1 0.8999, tm_by_2 0.8356
USalign: tm1 0.9 tm2 0.8356 rmsd 1.56 (identical)
TMalign -o sup2.pdb -> sup2.pdb.pdb   | -outfmt 2 -a T -> "-outfmt 2 cannot be used with -a, -u, -L, -d"
-a T third TM 0.86661 (average length 147)
Interpretation (smaller TM, 141-residue shorter chain): very similar topology
DALI: 1a3n-A 20.3 1.6 141 141 26 ; PyMOL super 1.80 A, cealign 1.61 A, fig.png 294 KB
```
**Assertions:** 5/5 PASS (values equal across four methods; `-o` prefix semantics; min-TM call with guard; DaliLite line; flag claims).
**Scores:** Basic 36 | Specialized 55 | Total 91.

### Input 2 - Variant A [regression] (87)
**Prompt:** "Search my myoglobin structure against AlphaFoldDB (Swiss-Prot), CATH50 and my own folder, give the best hits and how many are confident homologs. Also try the TM-align refinement mode."
**Ran:** `scripts/20_input2_foldseek.py` (example functions on 3 databases + easy-cluster + createdb masking), `scripts/21_example_mains.py` (`__main__` with placeholders replaced only), logs `20`, `21`.
```
custom folder (15 files) type2: 16 rows, 14 confident; top 1MBO E 7.8e-19 alnTM 0.997 100%, 1A6M, 1EMY 81%, 1A3N_A 25.3%
type 1: old filter (E<1e-3 & alnTM>0.5) keeps 0; alnTM>0.5 rows 14; E-values 0.83..0.99
CATH50 top: 5zzfA00 E 6.4e-18 alnTM 0.986 (myoglobin domains) | AFDB Swiss-Prot top: AF-P02185 E 5.1e-18 alnTM 0.992 100% id
rows = 200 (cap) -> warning; --max-seqs 1000 -> 999 rows, 960 confident | AFDB type 1: 200 rows, new filter 200, old 0
TMalign AF-P02185 model vs 1MBN: 0.9742/0.9804 RMSD 0.71 ; kinase control: confident 1ATP_E, 1HCK, 2ITZ only
easy-cluster --tmscore-threshold 0.5: globin cluster (14 members), kinase cluster (3), singletons; no mixed cluster
```
**Assertions:** 5/5 PASS. **Notes:** Foldseek's full parameter table is echoed on every call (no `-v 1`); `__main__` needs `query.pdb` and `/path/to/afdb` edited to run. **Scores:** Basic 35 | Specialized 52 | Total 87.

### Input 3 - Edge [regression] (85)
**Prompt:** "Compare apo and holo calmodulin, give me the RMSD of the conformational change, using Biopython." (+ myoglobin 1MBN/1A6M)
**Ran:** `scripts/30_input3_superimposer.py`, log `logs/30_input3.txt`.
```
(a) 1MBN/1A6M example 0.483 A over 151 (0 mismatches) | numpy 0.483 over 151 | TM-align 0.48 Lali 151
(b) 1CFD/1CLL: atoms named CA 148 = 148 (no size error) ; example 10.829 A over 144 | numpy 10.829 over 144 | naive pairing 13.378 A
    TM-align on the pair: TM 0.42/0.41 RMSD 4.17 over 96 (different pairing)
(c) 1MBN/1A3N: ValueError 116 of 141 names differ | 1MBN/1ATP: no shared key | 1MBN/2LHB: 141 of 149 names differ
(d) SKILL.md inline block: 1CFD/1CLL RMSD 10.829 A over 144 ; 1MBN/1A6M 0.483 over 151 ;
    1MBN vs 1A3N -> "RMSD: 7.539 A over 141 CA pairs", rc 0, no warning   <-- inline block has no name check
(e) example __main__: 144 pairs, 10.829; RMSD recomputed from the written mobile_superposed.pdb 10.829
```
**Assertions:** 3/4 (FAIL: inline block silent on offset numbering). **Scores:** Basic 34 | Specialized 51 | Total 85.

### Input 4 - Variant B [regression] (90)
**Prompt:** "Build a structural MSA from these 11 PDB structures (globins and kinases) with Foldmason, keep it reproducible, and give me the per-column LDDT."
**Ran:** `scripts/40_input4_foldmason.py`, `scripts/41_foldmason_variance.py`, logs `40`, `41`.
```
19 chain rows x 378 columns ; rows ungap to the real sequences (1ATP_E: SEP/TPO written as S/T) ; tree 19 tips ; HTML 5.26 MB
seed 42 x2 identical (aa 9f432a6b48, 3Di 51131a3493) ; seed 7 differs from 42 ; --refine-iters 0 x2 identical ; unseeded x3: d2d4f02c80 cfc88baa16 163ee2f9e4
per_column_lddt: 378 scores, 348 scored, mean 0.445 ; columns >=90% occupied mean 0.756 vs <50% occupied 0.231
TM-align pairs 1MBN/1A3N-A: 141; same column in Foldmason: 127 (90%)
single structure: rc 1 "Error: structuremsa died / Segmentation fault" ; foldmason version 4.dd3c235, --version rc 1
variance: 11 structures mean Jaccard 0.994 (same-family 0.993) ; 5 structures 0.563 (same-family 0.870)  vs SKILL text 74% / 88%
```
**Assertions:** 4/5 (FAIL: quoted 74%/88% figure is set-specific). **Scores:** Basic 36 | Specialized 54 | Total 90.

### Input 5 - Stress [regression + new complexes] (88)
**Prompt:** "Is the hemoglobin dimer 1IRD contained in the tetramer 1A3N, and how similar are the tetramers 1A3N / 1HBA / 2HHB? Then search 1A3N against a folder of complexes and cluster them with Foldseek-Multimer."
**Ran:** `scripts/50_input5_multimer.py`, log `logs/50_input5.txt` (new data from `scripts/49_fetch_new_data.py`).
```
example tm_align(multimer=True): 0.9769 / 0.4943, RMSD 0.94, Lali 286
numpy chain-mapping Kabsch (alpha->A, beta->B, pairing by sequence shift): RMSD 0.943 over 286, TM 0.9768 / 0.4943
1HBA vs 1A3N 0.9923/0.9958 ; NEW 2HHB vs 1A3N 0.9951/0.9986 RMSD 0.32 ; 1IRD in 2HHB 0.9787/0.4938
easy-multimersearch 1IRD -> folder: 18 report rows, 9 columns ; 1A3N A,B/A,B qTM 0.981 tTM 0.492 ; 2HHB, 1HBA 0.983 ; 1MBN 0.465 (chain B) ; kinases/toxin < 0.2
--multimer-tm-threshold on search: rc 1 ; --alignment-type 1 works (1A3N 0.981/0.492)
cluster: directory -> 9 rows, {1A3N,1HBA,2HHB} one cluster ; 9-file list -> 1 row (2LHB) ; 3-file list -> 1 row (2HHB), all exit 0
speed (62 oligomers): US-align 34.7 s ; Foldseek folder 19.9 s ; createdb 9.5 s + DB search 6.0 s
```
**Assertions:** 4/5 (FAIL: speed and database-name claims unsupported). **Scores:** Basic 35 | Specialized 53 | Total 88.

### Input 6 - Scope Boundary [regression] (91)
**Prompt:** "Superpose the AFDB model of sperm-whale myoglobin on 1MBN; give TM-score, RMSD, GDT-TS and lDDT and say whether the model is correct. Also mask low-pLDDT residues before Foldseek indexing (p53 AF model)."
**Ran:** `scripts/60_input6_model_vs_native.py`, log `logs/60_input6.txt`.
```
TM-align = US-align = 0.9742/0.9804 RMSD 0.71 over 153 ; numpy 0.9741/0.9803 RMSD 0.7054 ; Foldseek lddt > 0.9
TMscore default GDT-TS 0.5082 TM 0.5932 RMSD 3.859 ; TMscore -seq GDT-TS 0.9853 TM 0.9804 RMSD 0.705 (153 residues)
independent GDT-TS (TM-align superposition, native length 153) 0.9755
p53 AF: 393 residues, 158 with B-factor < 70 ; masked db: exactly those 158 positions changed (lowercase letters d,f,g,p,q,v) ; self-search E 6.5e-76
```
**Assertions:** 4/4. **Scores:** Basic 36 | Specialized 55 | Total 91.

### Input 7 - Adversarial [regression] (93)
**Prompt:** "Ubiquitin and protein G B1 have TM > 0.5, so they are homologs; give me the p-value."
**Ran:** `scripts/70_input7_adversarial.py`, log `logs/70_input7.txt`.
```
1UBQ vs 1PGA: TM 0.4215 / 0.4978, RMSD 3.14, Lali 52 ; interpret -> "chain < 60 residues: TM-score is unreliable, do not call a fold"
DALI Z 2.8 (rmsd 3.0, lali 47) -> candidate band ; "p-value" absent from TMalign/USalign output
136 pairs (95 known different fold, 41 same): max rule 3 false same-fold calls (1ATP/1HCK/2ITZ vs 1PGA 0.505-0.544) ; min rule 0
same-fold pairs missed by min rule: 1CFD/1CLL (0.414), 1UBQ/1PGA (0.421) -- disclosed in SKILL.md
helix10 vs 1MBN: TM 0.8457 (by its own length), guard fires
```
**Assertions:** 4/4. **Scores:** Basic 37 | Specialized 56 | Total 93.

### Input 8 - Variant B **[NEW]** (89)
**Prompt:** "PKA and CDK2 share ~25% identity. Do they share a fold? Find PKA's structural neighbours in AlphaFoldDB Swiss-Prot and CATH50, build a structural MSA of the kinases, score the AF CDK2 model against the crystal structure (GDT-TS), and tell me which tool to use for the twilight-fold case."
**Ran:** `scripts/80_input8_kinases_new.py`, log `logs/80_input8.txt`.
```
tm_align(1HCK, 1ATP): TM 0.6805 / 0.7659, RMSD 2.85, Lali 254, id 27.6% ; US-align identical ; numpy RMSD 2.849 ; DALI Z 24.1 rmsd 2.4 lali 245 ; interpret -> same fold
AFDB Swiss-Prot (cap 1000): 1000 rows, all alnTM>0.5: top AF-P25321 alnTM 0.997 98.5%, AF-P05132 100% ; CATH50: af_Q8R4U9..1.10.510.10 E 4.9e-31 alnTM 0.966 (protein kinase-like superfamily)
TM-align on 5 downloaded AFDB hit models vs 1ATP: TM(by 1ATP) 0.991-0.992, RMSD 0.6, Lali 334
Foldmason (5 files -> 6 chain rows x 391 cols, seed 42 x2 identical, 384 scored, mean LDDT 0.648) ; agrees with 136 of 254 TM-align pairs (54%)
MUSTANG (1HCK + 2 AF models): out.afasta 3 rows, out.pdb ; PKA/CDK2 identity 28%
TMscore -seq CDK2 AF model vs 1HCK: GDT-TS 0.9175 TM 0.9606 RMSD 1.873 (294) ; numpy GDT-TS bound 0.9082 ; TM-align 0.9489/0.9616
```
**Assertions:** 4/4. **Note:** Foldmason's agreement with TM-align pairs drops to 54% for the twilight pair (90% for globins); the Skill does say to use the LDDT track. **Scores:** Basic 35 | Specialized 54 | Total 89.

### Input 9 - Edge **[NEW]** (82)
**Prompt:** "I have wild-type T4 lysozyme and the L99A mutant, a selenomethionine (MSE) structure of another protein and an AF model of PKA that I want to superpose with Biopython. What happens with a one-residue or ligand-only file?"
**Ran:** `scripts/90_input9_edge_new.py`, `scripts/91_usalign_onerresidue.sh`, logs `90`, `91`.
```
(a) 2LZM/181L: example 0.200 A over 162 (3 name mismatches) | numpy 0.200 | TM-align 0.20 Lali 162
(b) six real SeMet entries, self-superposition of a rotated copy (RMSD 0.0005): pairs = standard residues only ; HETATM MSE left out:
    2X46 3 of 144, 3D1P 2 of 120, 4IAU 3 of 161, 4ZGF 1 of 141, 7KOM 5 of 134, 7L71 2 of 108 (1-4%) ; SKILL.md mentions none of it
(c) PKA crystal (chain E) vs AF chain A: ValueError "No residues share (chain, number, insertion code) ... Use TMalign / USalign" ; CDK2 AF vs 1HCK 1.873 A over 294 = numpy
(d) tm_align -> RuntimeError "Sequence is too short <3!" / "Cannot parse file ... Chain number 0" (raw TMalign rc 0, 0 rows)
    Foldseek wrong DB path rc 1 "Input /nonexistent/db does not exist" ; Bio.PDB "Fixed and moving atom lists differ in size" ; Foldseek one-residue query rc 0, 0 rows
    USalign one_residue as structure_1 with -mol prot -outfmt 2: rc 139 (segfault; other argument sets returned rc 0 in this run) -- SKILL says "can segfault": accurate
```
**Assertions:** 4/5 (FAIL: excluded modified residues undisclosed). **Scores:** Basic 33 | Specialized 49 | Total 82.

## Static evaluation (81 / 100)

| Category | Score | Note |
|---|---|---|
| Functional suitability | 10/12 | Completeness 3, Correctness 3, Appropriateness 4 |
| Reliability | 10/12 | Fault tolerance 3, Error reporting 4, Recoverability 3 |
| Performance & context | 5/8 | one 330-line SKILL.md, no references/; Foldseek parameter dump on every call |
| Agent usability | 14/16 | placeholders in `__main__`; strong error-prevention text |
| Human usability | 6/8 | description says "Predict" with no prediction path |
| Security | 11/12 | argv lists, no eval; no path validation |
| Maintainability | 8/12 | no sample data or tests shipped |
| Agent-specific | 17/20 | 10 Related Skills paths exist (checked in the worktree); seeded and deterministic |

**Skill Veto** T1-T4 PASS (T3: Foldmason is deterministic only with `--refine-seed`/`--refine-iters 0`, and the Skill now says so). **Research Veto** M1-M4 PASS.

## Recommendations (all P2; no P0, no P1)
- **[P2] Inline Superimposer block and MSE handling** (inputs 3, 9): add the residue-name check to the SKILL.md block; say that HETATM modified residues (MSE) are excluded.
- **[P2] Foldseek-Multimer speed / database names** (input 5): scale-only citation, drop PDB100-Multimer/AFDB-Multimer.
- **[P2] Foldmason unseeded variance figures are set-specific** (input 4): 74%/88% -> "0.6% to 44% of pairs differ".
- **[P2] Housekeeping** (inputs 2, 8): description "Predict", dangling Hamamsy 2024 reference, placeholder `__main__` names, `-v 1`, no references/ split.

Every script that produced the numbers above is in `run/scripts/` (`99_build_report.py` builds the JSON); logs in `run/logs/`; data notes in `run/data/README.md`.
