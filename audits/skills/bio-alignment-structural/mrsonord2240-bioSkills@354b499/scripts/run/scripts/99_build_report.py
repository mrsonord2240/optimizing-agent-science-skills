"""Build eval_report_bio-alignment-structural_result.json and eval_viewer_bio-alignment-structural.md from the
scores/assertions recorded below, and run the schema pre-emit checklist. Run with the Windows venv python:
  PYTHONIOENCODING=utf-8 F:/OpenScience/audit-envs/alignment/Scripts/python.exe run/scripts/99_build_report.py
Every number here was produced by the scripts in run/scripts and logged in run/logs (see execution_note per input)."""
import json, os, sys
OUT = r'F:\OpenScience\audits\bio-alignment-structural'
P, F = 'PASS', 'FAIL'

meta = {
    "skill_name": "bio-alignment-structural",
    "description": "Align protein structures using Foldseek 3Di, TM-align, US-align, DALI, or Foldmason for structural MSA. Predict, score, and superpose backbone coordinates when sequence identity is below the twilight zone or remote-homology detection is required.",
    "evaluated_on": "2026-09-20",
    "evaluator_version": "skill-auditor@1.0",
    "category": "Data Analysis",
    "execution_mode": "D",
    "complexity": "Complex",
    "n_inputs": 7,
    "source": "mrsonord2240/bioSkills@354b4992cd8d2f1bee039510af618da0333821f1:alignment/structural-alignment",
    "env": "F:/OpenScience/audit-envs/alignment (WSL science env alignment: TM-align 20240303, US-align 20241108, Foldseek 10.941cd33, Foldmason 4.dd3c235, DaliLite v5, PyMOL 3.1.0, Biopython 1.88)",
}

veto = {
    "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
    "research_veto": {
        "applicable": True, "gate": "PASS",
        "scientific_integrity": {"result": "PASS", "detail": "No fabricated numbers or identifiers in any output; every TM-score/RMSD/Z quoted was reproduced by a second tool (US-align, DaliLite, PyMOL, Foldseek). Literature citations (e.g. Gilchrist 2026 Science 391:485) could not be checked offline and are not treated as evidence."},
        "practice_boundaries": {"result": "PASS", "detail": "Structural-bioinformatics scope only; no diagnostic or prescriptive content in SKILL.md or any of the 7 outputs."},
        "methodological_ground": {"result": "PASS", "detail": "No principled fallacy that inverts a conclusion. Weaknesses recorded as P1/P2: the 'larger TM (shorter chain)' headline metric plus the 0.5 cut gives false same-fold calls for chains <60 aa (3/38 known-different-fold pairs, all with 1PGA, 56 aa; a synthetic 10-residue helix scores 0.846 vs myoglobin); the '>0.8 = homologous' row conflates fold with homology."},
        "code_usability": {"result": "PASS", "detail": "All 4 shipped examples/*.py run from a clean copy on real data and were asserted against ground truth (Biopython 1.88 OK, no removed-API calls). Defects are in documented patterns, not in a script that will not run: easy-multimersearch --multimer-tm-threshold is rejected (rc=1), USalign -mm 4 -byresi 0 segfaults (rc=-11), easy-multimercluster with a file list silently returns one row (exit 0), report.get('per_column_lddt') is None, tm_align() returns None with exit 0 on a too-short chain. Recorded as P1; core pairwise/search/MSA code paths are runnable."},
    },
}

static = {
    "functional_suitability": (8, 12, "Completeness 3 (pairwise, search, multimer, MSA, hybrid all present; no DALI command, no runnable pLM aligner, no p-value/GDT-TS tool, Expresso not runnable offline). Correctness 2 (thresholds and TM-align/US-align/Foldseek/PyMOL patterns verified, but -mm 4 claim, --multimer-tm-threshold on multimersearch, per_column_lddt key, -o output name, evalue filter under alignment-type 1 are wrong). Appropriateness 3."),
    "reliability": (7, 12, "Fault tolerance 2 (examples use check=True and warn on unequal CA counts, but TM-align exits 0 with no row for degenerate input so tm_align() returns None and the example then raises TypeError; Superimposer silently pairs Ca2+ ions). Error reporting 2 (Common Errors table present but two rows unverified/odd). Recoverability 3."),
    "performance_context": (5, 8, "Token cost 2 (24 KB single SKILL.md, no references/ split; several long tables of tools that have no runnable pattern). Execution efficiency 3."),
    "agent_usability": (12, 16, "Learnability 3, Consistency 3, Feedback design 3 (examples print checked values), Error prevention 3 (good twilight-zone, RMSD, pLDDT and TM-caveat warnings; misses hetero-atom/numbering and multimer-flag traps)."),
    "human_usability": (5, 8, "Discoverability 3 (natural prompts in usage-guide). Forgiveness 2 (examples hard-code placeholder filenames reference.pdb/query.pdb//path/to/afdb; no CLI arguments)."),
    "security": (11, 12, "subprocess called with argv lists, no shell, no eval; no secrets. No path validation on user filenames (3 on input validation)."),
    "maintainability": (8, 12, "Modularity 3, Modifiability 3, Testability 2 (no sample data, no asserts in any example, output field meaning only in docstrings)."),
    "agent_specific": (14, 20, "Trigger precision 3, Progressive disclosure 3 (332 lines but no references/), Composability 3 (all 10 cross-skill paths exist), Idempotency 2 (Foldmason --refine-iters 100 is not reproducible run to run, TM-align -o name is not the name given), Escape hatches 3."),
}
static_cats = {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in static.items()}
static_sub = sum(v[0] for v in static.values())

A = lambda text, res, note: {"text": text, "result": res, "note": note}
inputs = [
 dict(index=1, type="Canonical", label="TM-score/RMSD myoglobin 1MBN vs hemoglobin alpha 1A3N-A (25% id) with examples/tm_align_pairwise.py, cross-checked", status="COMPLETED", status_flag="✅",
  executed=True, execution_note="Ran in WSL (scripts/10_input1_tmalign.py, 11_dali_pymol_crosscheck.sh). Prompt: 'Compute the TM-score and RMSD between myoglobin 1MBN and hemoglobin alpha 1A3N chain A; is it the same fold?'",
  note="TM 0.900/0.8356, RMSD 1.56, Lali 141 equal in TM-align and US-align; DALI Z 20.3; PyMOL super 1.80/cealign 1.61. -o superposed.pdb wrote superposed.pdb.pdb, not the named file.",
  basic=35, specialized=52, assertions=[
   A("TM-score, RMSD and aligned length agree between TM-align and an independent tool", P, "US-align gives identical 0.9000/0.8356/1.56/141; DaliLite Z 20.3 (Skill's >20 band); PyMOL cealign 1.61 A over 136"),
   A("Output reports both TM normalisations, RMSD and aligned length as SKILL.md requires", P, "example prints tm1, tm2, RMSD, identity; length_align in the dict"),
   A("Fold interpretation matches ground truth (globin fold conserved; globin vs kinase 1ATP is a different fold)", P, "interpret_tmscore: 0.90 -> equivalent topology; 1MBN vs 1ATP max TM 0.385 -> weak; PKA vs CDK2 0.77 -> same fold"),
   A("The superposed-structure file named by output_pdb exists after the call", F, "TM-align 20240303 wrote superposed.pdb.pdb plus five .pml files; superposed.pdb does not exist"),
   A("No diagnostic/prescriptive content; scope stays structural", P, "no clinical statements")]),
 dict(index=2, type="Variant A", label="Foldseek homolog search of 1MBN: custom 13-PDB DB, real CATH50, real AFDB Swiss-Prot", status="COMPLETED", status_flag="✅",
  executed=True, execution_note="Ran (scripts/20_input2_foldseek.py) with the example's foldseek_search()/parse_results() on three real databases. Prompt: 'Search myoglobin 1MBN against a structure database and list confident structural homologs.'",
  note="Top hits correct (AFDB: AF-P02185 100% id alnTM 0.992; CATH50 sperm-whale myoglobin domains; custom DB myoglobins then hemoglobins). With --alignment-type 1 the E-value column is 0.88-0.99 so the example's evalue<1e-3 filter returns 0 confident hits; default max_seqs=200 silently caps the hit list.",
  basic=33, specialized=50, assertions=[
   A("Top-ranked hits are the query's own family (ground truth: myoglobins, then globins; no kinase/toxin passes alnTM>0.5,E<1e-3)", P, "custom DB: 1MBO, 1A6M, 1EMY first, 14 confident, 0 non-globin; AFDB: AF-P02185 first (100.0% id)"),
   A("Every result row parses into the 10 documented columns", P, "16/16, 200/200, 200/200 rows parsed; no skipped-row warning"),
   A("Foldseek alignment TM-scores agree with TM-align on the same pair", P, "--alignment-type 1 qTM 0.856/tTM 0.924 vs TM-align 0.8356/0.9000 for 1MBN/1A3N-A (<0.05); AF model TM-align 0.980"),
   A("The example's 'confident homologs' filter works for every alignment_type the function accepts", F, "alignment_type=1 gives evalue 0.88-0.99 for true globins -> 0 confident hits; the SKILL recommends type 1 for refinement"),
   A("Reported hit count reflects the database, not a silent cap", F, "max_seqs=200 default: 200 rows printed as '200 confident' for AFDB (tooling run with default 1000 gave 999 rows)")]),
 dict(index=3, type="Edge", label="Bio.PDB Superimposer: myoglobin 1MBN/1A6M (153 vs 151 CA) and apo/holo calmodulin 1CFD/1CLL", status="COMPLETED", status_flag="⚠️",
  executed=True, execution_note="Ran the unmodified examples/biopython_superimposer.py from copies (scripts/30_input3_superimposer.py). Prompt: 'Compare apo and holo calmodulin and quantify the conformational change' (usage-guide's own prompt).",
  note="Myoglobin pair: 0.483 A, identical to residue-matched truth and TM-align 0.48. Calmodulin: 148 vs 148 'CA' atoms so no warning, but 4 of the holo 'CA' atoms are Ca2+ ions; example prints 13.38 A vs 10.83 A residue-matched truth over 144 pairs.",
  basic=28, specialized=38, assertions=[
   A("Example RMSD equals residue-matched ground truth for a co-numbered pair (1MBN/1A6M)", P, "0.483 vs 0.483 (151 pairs); TM-align 0.48"),
   A("Example RMSD equals residue-matched ground truth for apo/holo calmodulin", F, "13.378 A (148 pairs incl. 4 Ca2+ ions named 'CA') vs 10.829 A (144 residue-matched pairs)"),
   A("The example warns whenever its atom pairing is unsafe", F, "warns only when the two CA counts differ; 148==148 here so no warning although 4 pairs are ion-vs-residue and offsets follow"),
   A("Output points to TM-align/US-align for unknown correspondence", P, "warning text in the example and SKILL.md 'Approach' sentence do so"),
   A("No out-of-scope claims", P, "purely geometric")]),
 dict(index=4, type="Variant B", label="Foldmason structural MSA of 8 globin + 3 kinase structures; per-column LDDT via report-mode 2", status="COMPLETED", status_flag="⚠️",
  executed=True, execution_note="Ran unmodified examples/foldmason_msa.py from a copy (scripts/40_input4_foldmason.py), then the SKILL.md report-mode-2 recipe, then reproducibility (41/42/43). Prompt: 'Build a structural MSA from these structures with Foldmason and give me per-column LDDT.'",
  note="Output files match the documented names; 19 chain rows x 378 columns for 11 files (example prints 'MSA: 19 sequences'). 90% of TM-align's 1MBN/1A3N-A residue pairs recovered. report.get('per_column_lddt') is None (key is 'scores'). Three unseeded --refine-iters 100 runs give 377/378/378 columns, mean Jaccard of aligned pairs 0.74 (homolog pairs ~0.88); --refine-seed 42 is byte-identical x3.",
  basic=30, specialized=44, assertions=[
   A("All four documented outputs exist (result_aa.fa, result_3di.fa, guide tree .nw, .html report)", P, "family_msa_aa.fa, _3di.fa, .nw, .html present and non-empty"),
   A("Every MSA row's ungapped length equals the residue count of its PDB chain", P, "19/19 rows match CA counts (1ATP 336 includes SEP/TPO hetero residues)"),
   A("MSA agrees with an independent structural aligner on a homologous pair", P, "127/141 TM-align residue pairs (90%) for 1MBN vs 1A3N-A are aligned pairs in the MSA; globin-globin id 0.48 vs globin-kinase 0.09"),
   A("The Skill's per-column LDDT recipe returns per-column values", F, "report.get('per_column_lddt') -> None; values live in report['scores'] (378 values, min -1.0, max 0.81)"),
   A("The documented command is reproducible run to run", F, "3 unseeded runs -> 3 md5s; 28 of 36 pairwise alignments differ; SKILL never mentions --refine-seed (default -1 = random); --refine-iters 0 is deterministic")]),
 dict(index=5, type="Stress", label="Multi-part: multimer TM (US-align), Foldseek-Multimer search/cluster, easy-cluster on 14 PDBs", status="PARTIAL", status_flag="❌",
  executed=True, execution_note="Ran (scripts/50_input5_multimer.py, 51_multimercluster_probe.sh) with every command copied from SKILL.md. Prompt: 'Compare hemoglobin tetramer 1A3N with the dimer 1IRD and mutant 1HBA, search the complex against a multimer DB above TM 0.5, and cluster all my structures at TM>0.5.'",
  note="US-align -mm 1 -ter 0 correct (1IRD in 1A3N 0.977/0.494; 1HBA vs 1A3N 0.992/0.996). easy-cluster at 0.5 gives globin/kinase/toxin-pure clusters. Three documented multimer commands fail: -mm 4 -byresi 0 segfaults; easy-multimersearch --multimer-tm-threshold -> 'Unrecognized parameter'; easy-multimercluster *.pdb returns one row (last file) with exit 0.",
  basic=24, specialized=34, assertions=[
   A("US-align -mm 1 -ter 0 gives correct whole-complex TM for known pairs", P, "tetramer vs Trp37Arg mutant 0.992/0.996 RMSD 0.55; dimer vs tetramer 0.977/0.494 matches the tooling agent"),
   A("The stated remedy for different stoichiometry (-mm 4 -byresi 0) runs and returns a pairwise complex score", F, "US-align 20241108: segmentation fault (rc -11), 'structure_2 is ignored for -mm 4'; -mm 4 is multiple-structure alignment; -mm 1 already handles unequal stoichiometry"),
   A("easy-multimersearch accepts --multimer-tm-threshold as printed in SKILL.md", F, "rc=1: Unrecognized parameter '--multimer-tm-threshold' (the flag exists only on easy-multimercluster)"),
   A("easy-multimercluster *.pdb ... clusters all supplied structures", F, "3, 9 and 9 input files gave 1 row (only the last file); a directory argument clustered all 7 correctly; exit code 0 both ways"),
   A("easy-cluster --tmscore-threshold 0.5 gives fold-pure clusters", P, "4 clusters: 15 globin chains, 3 kinase chains, PKI peptide, tetanus toxin; no mixing")]),
 dict(index=6, type="Scope Boundary", label="Evaluate an AlphaFold model against its crystal structure (TM, RMSD, lDDT, GDT-TS) and mask low-pLDDT residues", status="COMPLETED", status_flag="✅",
  executed=True, execution_note="Ran (scripts/60_input6_model_vs_native.py) on the real AFDB model AF-P02185-F1 v6 and 1MBN, plus AF-P04637 (p53) for masking. Prompt: 'Superpose my AlphaFold model of myoglobin on 1MBN, give TM-score, RMSD, GDT-TS and lDDT, and tell me whether it is correctly modelled.'",
  note="TM 0.980, RMSD 0.71 over 153 (TM-align == US-align); Foldseek lddt 0.941 (>0.6 cutoff). Masking verified: 158 of 393 p53 residues (pLDDT<70) masked, alignments unchanged (seeding only). GDT-TS not obtainable from a tool the Skill names: TMscore (extra tool) printed 0.508 for a 0.98-TM model because of an off-by-one residue numbering, 0.985 after renumbering.",
  basic=31, specialized=46, assertions=[
   A("TM-score and RMSD for the model are the same in TM-align and US-align and indicate a near-native model", P, "0.9742/0.9804, RMSD 0.71, Lali 153 in both"),
   A("Foldseek lddt for the near-native model exceeds the SKILL's 0.6 'correctly modelled' cutoff", P, "0.941"),
   A("--mask-bfactor-threshold 70 masks exactly the low-pLDDT residues", P, "158 masked 3Di positions = 158 CA with B<70 in AF-P04637; self-search bits/alnTM unchanged (masking affects seeding only)"),
   A("The Skill provides a usable path to the GDT-TS it lists as a 'correct fold' criterion", F, "names LGA/MaxCluster/OpenStructure only, none installed and no command; naive TMscore run gave 0.508 vs true 0.985 (numbering trap) and the Skill warns about none of this")]),
 dict(index=7, type="Adversarial", label="'Ubiquitin and protein G B1 have TM>0.5, so they are homologs; give me the p-value'", status="COMPLETED", status_flag="⚠️",
  executed=True, execution_note="Ran (scripts/70_input7_adversarial.py, 71_maxTM_false_positive_matrix.py, 82/83 synthetic probes, 11 DALI). Prompt as the label; ground truth: both are beta-grasp folds in different SCOP superfamilies, not homologs.",
  note="TM-align/US-align: 0.498/0.4215 RMSD 3.14 (borderline), DALI Z 2.8 ('candidate', not homology), Foldseek E 0.029. Skill does not call them homologs. But with its headline metric max(TM1,TM2) a 56-aa chain vs unrelated kinases scores 0.505-0.544 ('same fold'), and a synthetic 10-residue helix vs myoglobin scores 0.846 ('equivalent topology (homologous)'). No shipped tool prints the length-aware p-value the Skill recommends.",
  basic=30, specialized=44, assertions=[
   A("The Skill's guidance does not conclude the pair are homologs", P, "TM 0.498 (<0.5) and DALI Z 2.8 fall in 'weak'/'candidate: verify with biology'"),
   A("The recommended larger-TM rule with the 0.5 cut yields no false same-fold call on known-different folds", F, "3 of 38 known-different-fold pairs >0.5 (1PGA 56 aa vs 1ATP 0.505, 2ITZ 0.538, 1HCK 0.544); normalising by the longer chain gives 0"),
   A("The requested length-aware TM p-value (Xu & Zhang 2010) can be produced with the Skill", F, "no formula, command or script; TM-align and US-align print no p-value"),
   A("Foldseek/DALI corroborating evidence is consistent with the TM-score conclusion", P, "Foldseek E 2.9e-2 alnTM 0.435 (weak); DALI Z 2.8"),
   A("No fabricated statistics or references", P, "all values traced to tool output")]),
]
for i in inputs:
    i["total"] = i["basic"] + i["specialized"]
    i["assertions_passed"] = sum(a["result"] == P for a in i["assertions"])
    i["assertions_total"] = len(i["assertions"])

avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
ap, at = sum(i["assertions_passed"] for i in inputs), sum(i["assertions_total"] for i in inputs)
sw, dw = round(static_sub * 0.4, 1), round(avg * 0.6, 1)
score = int(sw + dw + 0.5)
grade, sym = ("Production Ready", "⭐") if score >= 85 else ("Limited Release", "✅") if score >= 75 else ("Beta Only", "⚠️") if score >= 60 else ("Reject", "❌")
gate_fail = any(v == "FAIL" for v in veto["skill_veto"].values()) or veto["research_veto"]["gate"] == "FAIL"
final = {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": grade, "grade_symbol": sym,
         "deployable": (grade in ("Production Ready", "Limited Release")) and not gate_fail, "veto_override": gate_fail}

recs = [
 dict(priority="P1", title="Foldmason example is not reproducible (no seed)", observed_in=[4],
  problem="foldmason_msa.py defaults to --refine-iters 100; three identical runs give three different MSAs (377/378 columns, aligned-pair Jaccard 0.74, homolog pairs 0.88). --refine-seed is never mentioned.",
  root_cause="Random refinement default (--refine-seed -1) shipped without a seed or a note.",
  fix="Add --refine-seed <N> to the example and SKILL.md command, state that --refine-iters 0 is deterministic, and say unseeded runs are not comparable."),
 dict(priority="P1", title="Foldseek-Multimer commands are wrong or silently lossy", observed_in=[5],
  problem="easy-multimersearch --multimer-tm-threshold is rejected (flag only exists on easy-multimercluster); easy-multimercluster with a file list/glob clusters only the last file and exits 0; 'Foldseek-MM-TM' has no command (it is --alignment-type 1) and the complex-level TM is in the separate <out>_report file, which is not mentioned.",
  root_cause="Commands written from the paper/README rather than run against a release; Skill-level flag list not checked against --help.",
  fix="Use a directory argument for easy-multimercluster, drop the threshold flag from multimersearch (or use --tmscore-threshold), document --alignment-type 1 as the -TM mode and the _report file columns, and add a run-and-check line."),
 dict(priority="P1", title="'-mm 4 -byresi 0' remedy for unequal stoichiometry is wrong", observed_in=[5],
  problem="USalign -mm 4 is multiple-structure alignment (structure_2 ignored) and segfaulted on two complexes; -byresi 0 is unrelated. US-align -mm 1 -ter 0 already handles dimer vs tetramer (0.977/0.494).",
  root_cause="Mode taxonomy taken from memory.",
  fix="Replace with: -mm 1 -ter 0 handles unequal stoichiometry; report both normalisations; -mm 2 for chains into an oligomer."),
 dict(priority="P1", title="Per-column LDDT recipe returns None", observed_in=[4],
  problem="report.get('per_column_lddt') is None on Foldmason 4.dd3c235; the JSON keys are entries, scores, tree, statistics and the per-column values are in 'scores' (-1 for uncomputed columns).",
  root_cause="Key name guessed; the Skill hedges ('may evolve') but ships a broken line.",
  fix="Use report['scores'] and note -1 = no LDDT; assert len(scores) equals the MSA column count."),
 dict(priority="P1", title="Superimposer example silently mis-pairs atoms", observed_in=[3],
  problem="Selecting every atom whose id is 'CA' pulls in Ca2+ ions and all models; positional truncation then pairs ions with residues. Apo/holo calmodulin printed 13.38 A instead of 10.83 A and no warning because the CA counts happened to be equal.",
  root_cause="Atom selection by name only; correspondence assumed positional.",
  fix="Select ATOM-record CA of one model (residue.id[0]==' '), pair by (chain, resseq, icode), print the pair count and refuse when the pairing is empty or offset."),
 dict(priority="P1", title="alignment_type=1 breaks the example's confidence filter", observed_in=[2],
  problem="With --alignment-type 1 Foldseek reports E-values of 0.88-0.99 for true homologs, so 'evalue < 1e-3' returns 0 hits although alnTM is 0.93; the default max_seqs=200 also caps the printed count.",
  root_cause="E-value is not meaningful for TM-align re-alignment; filter written for type 2 only.",
  fix="Filter on alntmscore (and lddt) when alignment_type=1, and raise or state the max_seqs cap in the printed summary."),
 dict(priority="P1", title="Guard tm_align() against degenerate input", observed_in=[7],
  problem="TM-align exits 0 with no data row for a <3-residue or ligand-only file, so tm_align() returns None and the example crashes on result['tm1'].",
  root_cause="Exit code trusted; parse result not checked.",
  fix="Raise a clear error when parse_outfmt2 returns None and include TM-align's stdout message."),
 dict(priority="P2", title="'Larger TM' headline metric inflates small-chain scores", observed_in=[7],
  problem="max(TM1,TM2) called 'the standard fold-similarity metric' contradicts TM-align's own printed advice (normalise by the reference); 3/38 known-different-fold pairs exceed 0.5 and a synthetic 10-residue helix scores 0.846; interpret_tmscore ignores the <60-residue caveat given in prose and labels >0.8 'homologous'.",
  root_cause="Length-asymmetry handled only in prose.",
  fix="Report both normalisations, add a length guard in interpret_tmscore, say fold similarity is not homology, and name a source for the Xu-Zhang p-value or drop the reference."),
 dict(priority="P2", title="usage-guide installs a broken tmalign package", observed_in=[],
  problem="conda install -c bioconda tmalign gives a 2018 Fortran binary that dies with libgfortran.so.3; -o writes <name>.pdb (superposed.pdb.pdb) not the named file; Expresso needs BLAST/FTP and 3D-Coffee (`-mode 3dcoffee` and an explicit TMalign_pair method) both timed out at 120 s retrying retired RCSB/wwPDB endpoints (rc 124) with no alignment written; ChimeraX not executed.",
  root_cause="Install line and outputs not run on a clean machine.",
  fix="Point to the US-align source build or the zhanggroup binary, fix the -o wording, and give the T-Coffee template-file format with a working command."),
 dict(priority="P2", title="GDT-TS and DALI have no runnable path", observed_in=[6],
  problem="SKILL lists GDT-TS >50 and DALI Z bands but names no installed tool or command for either; the Zhang-lab TMscore binary prints GDT-TS but pairs by residue number (0.508 vs 0.985 for an off-by-one model).",
  root_cause="Reference tables without procedures.",
  fix="Add a one-line DaliLite (dali.pl) or web-server step and a TMscore/renumbering note, or remove the bands the Skill cannot help compute."),
 dict(priority="P2", title="Summary counts chains as structures", observed_in=[4],
  problem="foldmason_msa.py prints 'MSA: 19 sequences' for 11 input files because Foldmason emits one row per chain (<file>_<chain>).",
  root_cause="Row count reported as structure count.",
  fix="Print files vs chains, or say so in the docstring."),
]
report = {
 "meta": meta, "veto_gates": veto,
 "static_score": {"subtotal": static_sub, "max": 100, "categories": static_cats},
 "dynamic_score": {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": ap, "total": at}, "inputs": inputs},
 "final": final,
 "key_strengths": [
  "Core tool guidance is accurate and reproducible: TM-align, US-align, DaliLite and PyMOL agreed on TM 0.90/0.8356, RMSD 1.56, Z 20.3; Foldseek alnTM matched TM-align within 0.05",
  "All four shipped examples run from a clean copy on Biopython 1.88 and Foldseek 10.941 / Foldmason 4.dd3c235 and print usable results",
  "Thresholds and decision guidance (twilight zone, RMSD misuse, pLDDT masking, DALI Z bands) matched real-data ground truth: 158/158 low-pLDDT residues masked, DALI Z 2.8 for the ubiquitin/protein G pair",
  "Shipped-means-present holds: examples/tm_align_pairwise.py exists and all 10 cross-skill paths resolve",
 ],
 "recommendations": recs,
}

# ---- pre-emit checklist
assert len(report["static_score"]["categories"]) == 8
assert static_sub == sum(c["score"] for c in static_cats.values())
for k, c in static_cats.items(): assert 0 <= c["score"] <= c["max"] and c["note"]
assert len(inputs) == meta["n_inputs"] == 7
for i in inputs:
    assert 3 <= len(i["assertions"]) <= 5 and i["basic"] + i["specialized"] == i["total"] and i["basic"] <= 40 and i["specialized"] <= 60
    exp = "✅" if (i["status"] == "COMPLETED" and i["total"] >= 75) else "⚠️" if i["status"] == "COMPLETED" else "❌"
    assert i["status_flag"] == exp, (i["index"], i["status_flag"], exp, i["total"])
assert 2 <= len(report["key_strengths"]) <= 5
assert [r["priority"] for r in recs] == sorted(r["priority"] for r in recs)
print('static', static_sub, 'exec_avg', avg, 'final', score, grade, 'assertions', ap, '/', at, 'deployable', final["deployable"])
L1 = sum(i["basic"] for i in inputs) / 7; L2 = sum(i["specialized"] for i in inputs) / 7
print('L1 avg %.1f  L2 avg %.1f  assertion rate %.0f%%' % (L1, L2, 100 * ap / at))

json.dump(report, open(os.path.join(OUT, 'eval_report_bio-alignment-structural_result.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# ---- viewer
md = ["# Eval Viewer - bio-alignment-structural", "", "Generated: 2026-09-20  |  Source: `%s`" % meta["source"], "",
      "Category: Data Analysis (3) | Mode D (scripts + CLI + reasoning) | Complexity: Complex -> 7 inputs | Env: %s" % meta["env"], "",
      "All 7 inputs were executed on real structures (RCSB/AFDB downloads + Foldseek CATH50 and AFDB Swiss-Prot). The only synthetic files are three hand-made degenerate PDBs in `run/data/synthetic/`. Scripts are in `run/scripts/`, raw output in `run/logs/`.", "",
      "## Step 1 - Skill Veto: PASS", "",
      "| Dim | Result | Evidence |", "|---|---|---|",
      "| T1 Stability | PASS | 4/4 shipped examples run; TM-align, US-align, Foldseek, Foldmason, PyMOL and local DaliLite each ran on real inputs |",
      "| T2 Contract | PASS | frontmatter has name, description, tool_type, primary_tool, license |",
      "| T3 Determinism | PASS (with P1) | TM-align, US-align, Foldseek byte-identical over 2 runs (logs/41). Foldmason `--refine-iters 100` is NOT reproducible (3 md5s, aligned-pair Jaccard 0.74; logs/42, 43); `--refine-seed 42` is. Optional MSA path only, one flag fixes it, recorded as P1 rather than a veto |",
      "| T4 Security | PASS | subprocess with argv lists, no shell/eval, no secrets |", "",
      "## Step 2 - Static score: %d / 100" % static_sub, "", "| Category | Score | Note |", "|---|---|---|"]
for k, c in static_cats.items(): md.append("| %s | %d/%d | %s |" % (k, c["score"], c["max"], c["note"]))
md += ["", "## Steps 4-6 - Inputs, outputs, scores", "", "| # | Type | Basic /40 | Spec /60 | Total | Assertions | Executed | Status |", "|---|---|---|---|---|---|---|---|"]
for i in inputs: md.append("| %d | %s | %d | %d | %d | %d/%d | %s | %s %s |" % (i["index"], i["type"], i["basic"], i["specialized"], i["total"], i["assertions_passed"], i["assertions_total"], "yes", i["status"], i["status_flag"]))
md += ["", "**Execution average: %.1f / 100** (Layer 1 avg %.1f/40, Layer 2 avg %.1f/60)  |  **Assertion pass rate: %d/%d (%.0f%%)**" % (avg, L1, L2, ap, at, 100 * ap / at), ""]
for i in inputs:
    md += ["### Input %d - %s: %s" % (i["index"], i["type"], i["label"]), "", "**Executed:** %s. %s" % (i["executed"], i["execution_note"]), "", "**What it produced:** %s" % i["note"], "",
           "**Scores:** Basic %d/40 | Specialized %d/60 | Total %d/100" % (i["basic"], i["specialized"], i["total"]), "", "**Assertions:**"]
    md += ["- [%s] %s - %s" % (a["result"], a["text"], a["note"]) for a in i["assertions"]] + [""]
md += ["## Research Veto: PASS", ""] + ["- **%s**: %s - %s" % (k, v["result"], v["detail"]) for k, v in veto["research_veto"].items() if isinstance(v, dict)]
md += ["", "## Extra checks outside the 7 inputs (also executed)", "",
       "- Flags verified against `--help` of the installed tools: `TMalign -a T` OK but `-outfmt 2` cannot be combined with `-a/-u/-L/-d`; `foldseek easy-search --alignment-type/--max-seqs/--format-output` OK; `easy-cluster --tmscore-threshold` OK; `createdb --mask-bfactor-threshold` OK (seeding only); `easy-multimersearch --multimer-tm-threshold` does NOT exist; `foldmason easy-msa --refine-iters/--report-mode` OK, `--refine-seed` exists and is undocumented.",
       "- PyMOL `pymol -cq -d \"load ..; super ..; ray; png\"`: ran, fig.png written (228 KB), super RMSD cycles printed.",
       "- bioconda `tmalign` (usage-guide install line): binary dies with `libgfortran.so.3` (logs/80).",
       "- T-Coffee `-mode expresso`: fails (BLAST/FTP). 3D-Coffee (SKILL form and explicit `-method TMalign_pair,mafft_msa`): both hit the 120 s timeout (rc 124) while T-Coffee retried retired ftp.wwpdb.org/rcsb REST endpoints, no alignment written (logs/81); the template-file format is not documented in the Skill. Not counted as executed inputs.",
       "- MUSTANG (table row only): ran on 3 myoglobins, wrote .afasta/.pdb. DALI web server: gated, not used; DaliLite v5 run locally instead.",
       "- ChimeraX `matchmaker`: not installed (licence-gated download), not executed. pLM aligners (TM-Vec, vcMSA, DEDAL, pLM-BLAST): prose only, no command in the Skill, not executed.",
       "- Common Errors rows: TM-align 'atoms not enough' is really 'Sequence is too short <3' with exit 0; Foldseek wrong DB path -> rc 1 'does not exist'; Foldmason with one structure -> 'structuremsa died'.",
       "- Sibling-skill Biopython 1.88 breakage: none here (Bio.PDB PDBParser/Superimposer/PDBIO unchanged). `git status` and `find` of the staging clone show no `__pycache__`.", "",
       "## Step 8 - Final", "", "Static %d x 0.4 = %.1f | Dynamic %.1f x 0.6 = %.1f | **FINAL %d / 100 - %s %s** | deployable: %s | veto_override: %s" % (static_sub, sw, avg, dw, score, sym, grade, final["deployable"], final["veto_override"]),
       "", "Floors: static 70 (<80 for Production Ready), execution avg %.1f, Layer 1 %.1f, Layer 2 %.1f, assertion rate %.0f%% (<80%% for Limited Release)." % (avg, L1, L2, 100 * ap / at), "",
       "### Recommendations", ""]
for r in recs: md += ["**[%s] %s** (inputs %s)" % (r["priority"], r["title"], r["observed_in"] or "static"), "- Problem: %s" % r["problem"], "- Root cause: %s" % r["root_cause"], "- Fix: %s" % r["fix"], ""]
open(os.path.join(OUT, 'eval_viewer_bio-alignment-structural.md'), 'w', encoding='utf-8').write("\n".join(md) + "\n")
print('written')
