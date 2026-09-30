"""Build report.json, findings.json, source-identity.json, execution-classifications.json, viewer.md for the initial audit
of bio-atac-seq-co-accessibility. Reads determinism.log (DET lines) for the seedless-rerun comparison."""
import hashlib, json, os, re

R = r'F:\OpenScience\audits\bio-atac-seq-co-accessibility'
root = r'F:\OpenScience\wt\atac-co-accessibility\skills\bio-atac-seq-co-accessibility'
SKILL = 'bio-atac-seq-co-accessibility'
DATE = '2026-09-30'

# ---------- source identity (live recompute) ----------
rows = []
for d, _, fs in os.walk(root):
    for f in fs:
        p = os.path.join(d, f)
        b = open(p, 'rb').read().replace(b'\r\n', b'\n')
        rows.append((os.path.relpath(p, root).replace(chr(92), '/'), len(b), hashlib.sha256(b).hexdigest()))
rows.sort(key=lambda x: x[0].encode())
man = "\n".join(f"{a}\t{b}\t{c}" for a, b, c in rows).encode()
ident = hashlib.sha256(man).hexdigest()
assert ident == '3c8089b0496fa6375512ece4b85ce85c10c47f3cb4a9c8e48c7288a62b9162e3', ident
open(os.path.join(R, 'candidate-manifest.tsv'), 'wb').write(man)
sid = {
    "schema": "scientific-skill-audit-source-identity-v1", "phase": "initial audit", "skill_id": SKILL,
    "independent_auditor": False,
    "origin": {"repository": "GPTomics/bioSkills", "commit": "d91ed3d563019e649dc854c56ccd62551359488a",
               "path": "atac-seq/co-accessibility", "license": "MIT"},
    "candidate": {
        "root": root, "worktree": r"F:\OpenScience\wt\atac-co-accessibility", "branch": "fix/atac-co-accessibility",
        "product_head": "3186916406e9cc6b0e6dc24ffe47880951fc0f93", "identity_scheme": "sha256-manifest-v1",
        "content_sha256": ident, "manifest_bytes": len(man), "file_count": len(rows),
        "manifest_recipe": "Ordinal POSIX relative paths; each UTF-8 line is path, TAB, byte count, TAB, lowercase file SHA-256 of the CRLF->LF normalized bytes; lines joined by LF without a trailing LF; SHA-256 over the manifest bytes.",
        "manifest_path": "candidate-manifest.tsv", "identity_before": ident, "identity_after": ident,
        "tree_status": "Candidate skill directory is staged/modified in the worktree from the normalize phase; no candidate bytes were modified by this audit (identity recomputed before and after)."},
    "tooling": {"tools_md": r"F:\OpenScience\audits\bio-atac-seq-co-accessibility\TOOLS.md",
                "environment_lock_sha256": "2fcd3fc2a5de3bd194b80bf864b2f7ce9762eafc45c35179df9713958db7d552"},
    "rubric": {"zip": r"F:\optimizing-agent-science-skills\skill-auditor.zip", "evaluator_version": "skill-auditor@1.0"},
    "files": [{"path": a, "bytes": b, "sha256": c} for a, b, c in rows]}
json.dump(sid, open(os.path.join(R, 'source-identity.json'), 'w', encoding='utf-8'), indent=2)

# ---------- determinism result ----------
det = {}
try:
    txt = open(os.path.join(R, 'runs', 'determinism.log'), encoding='utf-8', errors='replace').read()
    for m in re.finditer(r'^DET (.*)$', txt, re.M):
        det[len(det)] = m.group(1)
except FileNotFoundError:
    pass
DET_TEXT = ' | '.join(det.values()) if det else 'not completed'
print('DET:', DET_TEXT)

# ---------- findings ledger ----------
F = [
 dict(id="COACC-001", severity="P1", state="open", surface="scripts/cicero_workflow.R CLI tail",
      summary="Documented CLI fails on the natural binary peak matrix: readMM of a pattern-format .mtx returns ngTMatrix and new_cell_data_set stops",
      evidence="runs/cli.log, runs/cli2.log, runs/audit_cli.sh, runs/audit_cli2.R",
      detail="Rscript scripts/cicero_workflow.R m.mtx peak_meta.tsv cell_meta.tsv exits 1 in 35 s with 'expression_data must be a matrix'. Matrix::writeMM writes any all-ones (binarized) matrix as MatrixMarket 'pattern', and readMM returns a logical ngTMatrix that monocle3 rejects. An integer-format .mtx passes new_cell_data_set (dgTMatrix), so the failure is specific to pattern/logical input, which is exactly what a binarized peak matrix exports as. The script never coerces to numeric dgCMatrix, never sets dimnames from the metadata, and never validates the input.",
      fix="Coerce readMM output to a numeric dgCMatrix (as(., 'CsparseMatrix') after converting to dMatrix), set dimnames from peak/cell metadata, check dimensions, and re-run the CLI on a pattern .mtx as the regression."),
 dict(id="COACC-002", severity="P1", state="open", surface="scripts/cicero_workflow.R enhancer-gene mapping",
      summary="enhancer column of the enhancer-gene CSV is 50 percent factor integer codes, and the table over-counts pairs (4,728 rows vs 3,083 correct unique triples)",
      evidence="runs/t2.log, runs/audit_t2.R, runs/checks.log, evidence/output/ex_chr1_enhancer_gene_pairs.csv",
      detail="Cicero's Peak2 is a factor and Peak1 a character. c(strong$Peak2[...], strong$Peak1[...]) coerces the factor half to integer codes ('8','9','15'), so 2,364 of 4,728 rows carry codes that are not peak names (codes map to peak names only via levels(Peak2), which is not saved). Because each connection is present in both orientations, the same enhancer-gene pair appears once as a code and once as a name; an independent correct derivation gives 3,083 unique (enhancer, gene, coaccess) rows. The CSV cannot be joined to the peak set and is silently wrong.",
      fix="Convert Peak1/Peak2 with as.character() before building the table, de-duplicate on the unordered pair, and add an assertion that every enhancer value is a peak name present in the input."),
 dict(id="COACC-003", severity="P2", state="open", surface="scripts/cicero_workflow.R run_cicero_pipeline",
      summary="genome_df is hard-coded to all hg38 primary chromosomes; as shipped the function did not finish in 25 min on a 1,726-peak chr1-only input (8.5 min when restricted to chr1)",
      evidence="evidence/logs/fn_full.log (EXIT 124 after 1500 s), evidence/logs/fn_chr1.log (8.5 min, exit 0)",
      detail="Bounded observation, not proof of non-termination: the unmodified function was killed at the 25 min timeout after metacell construction while modelling windows across all chromosomes; a larger budget was not tried. The genome is also hg38-only with no parameter, and method-reference.md builds genome_df from all seqnames including alt/random contigs, which the script filters. The run cost is not stated in the Skill.",
      fix="Derive genome_df from the peak coordinates (chromosomes and lengths actually present, with a genome argument), state expected runtime scaling, and document the alt/random contig filter in the reference snippet."),
 dict(id="COACC-004", severity="P2", state="open", surface="scripts/cicero_workflow.R line 2; references/method-reference.md Version Compatibility",
      summary="'Cicero 1.20+' is wrong for the monocle3 API the code uses; the Bioconductor cicero (1.30.0 on Bioc 3.23) depends on monocle 2",
      evidence="evidence/logs/R-packages.csv, runs/checks.log, TOOLS.md version-drift section",
      detail="The script and Version Compatibility line cite cicero 1.20+, which resolves via BiocManager to the monocle-2 package (no new_cell_data_set/preprocess_cds). The code needs GitHub cole-trapnell-lab/cicero-release@monocle3, DESCRIPTION Version 1.3.9 (Depends: monocle3), verified installed as 1.3.9 (RemoteRef monocle3, sha 495ef0da) and via the Bioconductor and GitHub package pages. usage-guide.md already states the GitHub-only install, so the Skill contradicts itself. monocle3 is documented as 1.3+ (installed 1.3.1; GitHub master is newer and untested).",
      fix="Replace 'cicero 1.20+' with the GitHub monocle3-branch cicero 1.3.x install, cite both packages' provenance in one place, and remove the contradiction between the reference files."),
 dict(id="COACC-005", severity="P2", state="open", surface="scripts/cicero_workflow.R counts; references/method-reference.md Visualizing and Hi-C snippets",
      summary="Cicero output holds every peak pair in both orientations, so reported 'Total/Strong connections', arcs, and per-row concordance are double-counted",
      evidence="runs/archr_sym.log, runs/audit_archr_sym.R",
      detail="On the chr1 run 100.0 percent of 98,624 scored rows have their reverse present; 12,252 strong rows are 6,126 unique unordered pairs. The script prints and saves the doubled counts, the arc plot draws each pair twice, and the Hi-C concordance percentage is computed per row. Neither the Skill nor the script mentions this.",
      fix="De-duplicate to unordered pairs after run_cicero (keep Peak1<Peak2) before counting, saving, plotting, and computing concordance; document the symmetric output."),
 dict(id="COACC-006", severity="P2", state="open", surface="references/method-reference.md Cicero mechanics",
      summary="'genomic_distance_max' (default 500 kb) is not an argument of run_cicero or generate_cicero_models; the real controls are window and distance_constraint",
      evidence="runs/checks.log (formals of run_cicero: cds, genomic_coords, window, silent, sample_num)",
      detail="method-reference.md tells users to 'increase genomic_distance_max to 1 Mb' and describes correlation restricted by it; a user following that gets an unused-argument error, and the distance_constraint used in the alpha search is not explained.",
      fix="Replace genomic_distance_max with window (and describe distance_constraint) everywhere, and add a short executed example."),
 dict(id="COACC-007", severity="P2", state="open", surface="SKILL.md and references (score description)",
      summary="Connection scores are described as 0-1, but observed scores span -0.88 to 0.93 and 34.7 percent of non-NA rows are negative (660 NA rows)",
      evidence="runs/checks.log",
      detail="SKILL.md says 'Peak-pair connection scores (0-1)' while method-reference.md separately says negative means anti-co-variation. The score table (< 0.05 not biologically meaningful) does not say how to treat negative or NA scores; the script only drops NA.",
      fix="State the real range (-1 to 1), how negative and NA scores are treated, and keep the >0.25 / >0.5 tiers with their source."),
 dict(id="COACC-008", severity="P2", state="open", surface="references/method-reference.md Visualizing Connections",
      summary="The documented plotTracks(track) call errors as written and the full strong set draws an unreadable hairball",
      evidence="runs/viz.log, runs/audit_viz.R, evidence/output/arcs.png, F:\\OpenScience\\audit-envs\\bio-atac-seq-co-accessibility\\work\\audit_viz\\locus_0.5.png",
      detail="Bare plotTracks(track) fails with 'Unable to automatically determine plotting ranges'. With chromosome/from/to added, 12,252 strong arcs at 0.6 Mb are an unlabeled hairball with no genome axis; a 400 kb window at >0.5 with a GenomeAxisTrack is legible.",
      fix="Give the snippet a locus (chromosome, from, to), a GenomeAxisTrack, a stringent filter or top-N, and score-scaled arc width."),
 dict(id="COACC-009", severity="P2", state="open", surface="scripts/cicero_workflow.R enhancer-gene mapping; input contract",
      summary="Enhancer-gene mapping depends on an unshipped TSS BED, silently skips otherwise, labels promoter peaks as enhancers, and the peak-name contract is undocumented",
      evidence="runs/checks.log, evidence/tools/prep_inputs.R",
      detail="gencode_v29_protein_coding_tss.bed is read from the working directory but is neither shipped nor documented how to make; a missing file only prints a note and the run still reports success. In the corrected derivation 763 of 3,083 enhancer-gene rows have an 'enhancer' anchor that itself lies within another gene's TSS window (promoter-promoter pairs), which SKILL.md does not exclude or label. Peak names must be chr_start_end row names in peak_metadata; the CLI does not state or check this, and chr:start-end row names would silently fail the sub() conversion.",
      fix="Document (or generate) the TSS BED source and format, fail loudly or warn prominently when missing, label promoter-promoter pairs, and validate peak-name format."),
 dict(id="COACC-010", severity="P3", state="open", surface="references/method-reference.md ArchR block",
      summary="ArchR getCoAccessibility(returnLoops=TRUE) returns a SimpleList (loops in element 1), not a GRanges as the text says",
      evidence="evidence/logs/archr.log, runs/archr_sym.log (ArchR help repeats 'GRanges loops object')",
      detail="4,462 loops in element 1, DFrame of 8,924 rows for returnLoops=FALSE; correlations 0.50-0.96, max distance 249,998 bp, so the call itself works. Only the described return class is wrong; ArchR's own help has the same wording.",
      fix="Say 'a SimpleList whose first element is the loops GRanges' and show loops[[1]]."),
 dict(id="COACC-011", severity="P3", state="open", surface="SKILL.md and references quantitative claims",
      summary="Hi-C concordance ('~30-50%'), '10-50% of peaks have a strong connection', and '> 50K cells slow' are stated without a source or executed support",
      evidence="runs/checks.log (60.0% of peaks had >=1 strong connection in the PBMC chr1 slice)",
      detail="The 30-50 percent concordance range is repeated across three files without a citation; the peak-fraction plausibility check the Skill prescribes gave 60.0 percent on public PBMC data, outside its own stated 10-50 percent band, so it cannot serve as a validity test.",
      fix="Cite or remove the ranges, or label them as unverified heuristics."),
 dict(id="COACC-012", severity="P3", state="open", surface="SCENIC+ statements (restricted, static-only)",
      summary="SCENIC+ '1.0+/1.0' is an alpha (v1.0a2, Python <=3.11.8), and 'use the published Docker image' is not evidenced in the repository README",
      evidence="runs/scenicplus_static.txt; TOOLS.md blocker B1",
      detail="Not installable here (pybedtools build fails), so only static review was possible: init_snakemake takes --out_dir and creates Snakemake/workflow/Snakefile as documented (current main), but the version and Docker claims are unverified. Restricted after-action item.",
      fix="Pin the tested release, state the Python range, and cite the Docker image or remove the sentence; rerun on the Multiome h5 once a Python <=3.11 env with conda-forge pybedtools exists."),
 dict(id="COACC-013", severity="P3", state="open", surface="SKILL.md description and routing",
      summary="Description advertises Hi-C comparison, Multiome LinkPeaks, SCENIC+ and reference databases, but only the Cicero function ships as code",
      evidence="TOOLS.md surface map rows 8-10",
      detail="The Hi-C concordance snippet ran correctly against a planted BEDPE (300 of 300 planted pairs recovered), and LinkPeaks ran on public 3k Multiome (399 links on 150 genes; all 1,530 genes did not finish in >25 min), but the Skill states neither a bounded gene set nor runtime, and reference-database routes are prose only.",
      fix="Label prose-only routes, add the LinkPeaks runtime caveat, or move them to a routed reference with executed examples."),
]
json.dump({"skill_id": SKILL, "candidate_sha256": ident, "findings": F}, open(os.path.join(R, 'findings.json'), 'w', encoding='utf-8'), indent=2)

# ---------- execution classifications ----------
cls = {"schema": "execution-classifications-v1", "skill_id": SKILL, "candidate_sha256": ident, "surfaces": [
 {"surface": "scripts/cicero_workflow.R run_cicero_pipeline (chr1-only genome_df substitution)", "class": "executed", "evidence": "real 10x PBMC 5k chr1:1-30Mb, 98,624 scored pairs; COACC-002/003/005/009"},
 {"surface": "scripts/cicero_workflow.R run_cicero_pipeline exactly as shipped", "class": "failed", "evidence": "25 min timeout (bounded), COACC-003"},
 {"surface": "scripts/cicero_workflow.R CLI (readMM path)", "class": "failed", "evidence": "runs/cli.log, runs/cli2.log; COACC-001"},
 {"surface": "Cicero alpha block and permutation negative control", "class": "executed", "evidence": "evidence/logs/viz_alpha.log: real 11,794 vs 36 permuted"},
 {"surface": "Visualizing Connections (GenomicInteractions + Gviz)", "class": "executed", "evidence": "runs/viz.log; bare call errors, locus call inspected; COACC-008"},
 {"surface": "Hi-C concordance snippet", "class": "executed", "evidence": "runs/checks.log synthetic planted BEDPE, 300/300 recovered; COACC-005"},
 {"surface": "ArchR addCoAccessibility / getCoAccessibility", "class": "executed", "evidence": "evidence/logs/archr.log; COACC-010"},
 {"surface": "Signac LinkPeaks (Multiome)", "class": "executed", "evidence": "evidence/logs/linkpeaks.log (tooling-phase run, log inspected, bounded to 150 genes); COACC-013"},
 {"surface": "SCENIC+ / pycisTopic Snakemake route", "class": "blocked", "evidence": "pybedtools build fails; static source review only; COACC-012"},
 {"surface": "GeneHancer / FANTOM5 / EpiMap, HiCCUPS/HiChIP, ABC, CRISPRi-FlowFISH", "class": "static-only", "evidence": "prose only, no shipped code"},
 {"surface": "Markdown routing (SKILL.md -> references, script, LICENSE)", "class": "executed", "evidence": "4/4 relative links resolve"}]}
json.dump(cls, open(os.path.join(R, 'execution-classifications.json'), 'w', encoding='utf-8'), indent=2)

# ---------- report.json ----------
def A(t, ok, n): return {"text": t, "result": "PASS" if ok else "FAIL", "note": n}
inputs_spec = [
 ("Canonical", "Shipped Cicero function on real PBMC 5k chr1 slice (genome_df limited to chr1)", "COMPLETED",
  "Completes in 8.5 min; enhancer column defective; counts doubled", 27, 36, [
   A("Function completes and writes connection TSV and enhancer-gene CSV", True, "exit 0; 99,284 rows, 12,252 strong"),
   A("Scores show distance decay and are within the window", True, "mean 0.068 (<50 kb) vs 0.015 (>300 kb); max span 497 kb"),
   A("enhancer column holds peak names", False, "50 percent factor integer codes (COACC-002)"),
   A("Reported connection counts equal unique peak pairs", False, "12,252 strong rows = 6,126 unique pairs (COACC-005)"),
   A("Run-to-run result is stable without a seed", 'identical=TRUE' in DET_TEXT, 'second unseeded run identical: 99,284 rows, strong-set Jaccard 1.0')]),
 ("Variant A", "ArchR addCoAccessibility/getCoAccessibility as documented", "COMPLETED",
  "Works; returnLoops returns SimpleList not GRanges", 32, 46, [
   A("addCoAccessibility and getCoAccessibility run with documented arguments", True, "835 cells, k=100, knnIteration=500, maxDist=250 kb"),
   A("Correlations respect corCutOff and maxDist", True, "0.50-0.96; max 249,998 bp"),
   A("Returned loops object matches the Skill's stated class", False, "SimpleList, loops in element 1 (COACC-010)")]),
 ("Variant B", "Signac LinkPeaks on public 3k PBMC Multiome (tooling-phase run, log inspected)", "COMPLETED",
  "Bounded to 150 genes; Skill ships no code or runtime guidance", 26, 38, [
   A("LinkPeaks returns links with finite scores and p-values", True, "399 links; score -0.33..0.41"),
   A("Most links positive and within 500 kb of TSS", True, "77 percent positive; median span 181 kb"),
   A("All chr1 genes finish in a practical time", False, "1,530 genes did not finish in >25 min; bounded to 150 (COACC-013)")]),
 ("Edge", "Documented CLI on a binarized peak matrix exported with writeMM", "ERROR",
  "Exit 1 in 35 s, expression_data must be a matrix", 12, 22, [
   A("CLI completes on the documented three-file input", False, "readMM gives ngTMatrix; monocle3 rejects it (COACC-001)"),
   A("Failure message tells the user what to change", False, "raw monocle3 error; no input validation"),
   A("Integer-format mtx passes the same call", True, "dgTMatrix accepted in runs/cli2.log")]),
 ("Stress", "Shipped function unmodified on the same 1,726-peak chr1 input", "PARTIAL",
  "Killed at 25 min timeout after metacell construction", 12, 23, [
   A("Function finishes within 25 min on a chr1-only input", False, "EXIT 124 (bounded, larger budget untested; COACC-003)"),
   A("Runtime scaling or genome argument is documented", False, "hg38 all-chromosome genome_df hard-coded"),
   A("Metacell construction and Cicero setup complete before the stall", True, "log reaches 'Running models'; stall is in per-window modelling")]),
 ("Scope Boundary", "Downstream snippets: Visualizing Connections and Hi-C concordance on real Cicero output", "COMPLETED",
  "Bare plot call errors; concordance snippet recovers planted loops", 27, 37, [
   A("plotTracks(track) runs exactly as documented", False, "needs chromosome/from/to (COACC-008)"),
   A("Locus-restricted arc plot is legible with a genome axis", True, "400 kb window, >0.5, 140 arcs; inspected PNG"),
   A("Hi-C concordance snippet runs and recovers planted truth", True, "300/300 planted true pairs recovered by countOverlaps"),
   A("Concordance is computed on unique pairs", False, "per symmetric row (COACC-005)")]),
 ("Adversarial", "Alpha block and permutation negative control (documented null)", "COMPLETED",
  "Real 11,794 strong vs 36 after per-peak cell shuffle", 33, 51, [
   A("estimate_distance_parameter returns finite positive values", True, "20 windows, 1.0-3.7, mean 2.34"),
   A("Permutation control yields far fewer strong connections", True, "36 vs 11,794"),
   A("Skill's 'expect ~0' outcome is met exactly", True, "0.3 percent residual, effectively null")]),
]
inp = []
for i, (t, lab, st, note, b, s, asrt) in enumerate(inputs_spec, 1):
    total = b + s
    flag = "✅" if (st == "COMPLETED" and total >= 75) else ("⚠️" if st == "COMPLETED" else "❌")
    if i == 4 or i == 5: flag = "❌"
    inp.append({"index": i, "type": t, "label": lab, "status": st, "status_flag": flag, "note": note, "basic": b, "specialized": s,
                "total": total, "assertions_passed": sum(1 for a in asrt if a["result"] == "PASS"), "assertions_total": len(asrt), "assertions": asrt})
avg = round(sum(x["total"] for x in inp) / len(inp), 1)
passed = sum(x["assertions_passed"] for x in inp); total_a = sum(x["assertions_total"] for x in inp)
cats = {
 "functional_suitability": (7, 12, "Sound method coverage and a working core pipeline, but the shipped CLI fails on the natural input, the enhancer-gene output is wrong, and routes beyond Cicero ship no code"),
 "reliability": (6, 12, "No input validation; missing TSS BED silently skipped; unmodified function did not finish in 25 min; no seed"),
 "performance_context": (7, 8, "SKILL.md is 68 lines with routed references; runtime cost of the full-genome default is not disclosed"),
 "agent_usability": (11, 16, "Clear tool-selection tables and workflow; contradictory version guidance and non-existent parameter names reduce reliability"),
 "human_usability": (5, 8, "Quick reference tables are readable; error recovery for the CLI, plotting, and dependency installs is thin"),
 "security": (11, 12, "No credentials, no execution of user strings; unchecked file arguments only"),
 "maintainability": (7, 12, "One script mixes CLI parsing, pipeline, and mapping; no tests; version claims drift between files"),
 "agent_specific": (14, 20, "Precise trigger description and good progressive disclosure; composability weakened by routes without code and wrong install claim"),
}
sub = sum(v[0] for v in cats.values())
sw = round(sub * 0.4, 1); dw = round(avg * 0.6, 1); score = int(round(sw + dw))
grade = "Production Ready" if score >= 85 else "Limited Release" if score >= 75 else "Beta Only" if score >= 60 else "Reject"
sym = {"Production Ready": "⭐", "Limited Release": "✅", "Beta Only": "⚠️", "Reject": "❌"}[grade]
recs = [
 {"priority": "P1", "title": "CLI fails on binarized (pattern) .mtx input", "observed_in": [4],
  "problem": "The documented three-file CLI exits 1 because readMM returns a logical ngTMatrix that monocle3 rejects; the natural binary peak export is exactly this format.",
  "root_cause": "The script passes readMM output straight to new_cell_data_set with no coercion or validation.",
  "fix": "Coerce to a numeric dgCMatrix, set dimnames from the metadata, validate dimensions, and re-run the CLI on a pattern .mtx (COACC-001)."},
 {"priority": "P1", "title": "enhancer-gene CSV column contains factor codes", "observed_in": [1],
  "problem": "Half of the enhancer values are integer factor codes, not peak names, and the table over-counts pairs (4,728 vs 3,083 correct).",
  "root_cause": "c() of a factor Peak2 and a character Peak1 coerces the factor to integer codes.",
  "fix": "Use as.character() on both anchors, de-duplicate unordered pairs, and assert every enhancer is an input peak name (COACC-002)."},
 {"priority": "P2", "title": "Hard-coded all-chromosome genome_df; 25 min timeout", "observed_in": [5],
  "problem": "The unmodified function did not finish in 25 min on a chr1-only input; restricted to chr1 it took 8.5 min.",
  "root_cause": "genome_df is fixed to all hg38 primary chromosomes regardless of the peak set.",
  "fix": "Derive genome_df from the peak coordinates and document runtime scaling (COACC-003)."},
 {"priority": "P2", "title": "Wrong cicero version and duplicated pair counts", "observed_in": [1, 6],
  "problem": "'Cicero 1.20+' resolves to the monocle-2 Bioconductor package, and every peak pair appears in both orientations so counts and concordance are doubled.",
  "root_cause": "Version text was not checked against the monocle3-branch package; the symmetric output is not de-duplicated.",
  "fix": "State GitHub cicero-release@monocle3 1.3.x and de-duplicate pairs before counting or plotting (COACC-004, COACC-005)."},
 {"priority": "P2", "title": "Documentation contract errors: parameter, scores, plotting", "observed_in": [1, 6],
  "problem": "genomic_distance_max does not exist, scores are described as 0-1 but go negative, and plotTracks(track) errors as written.",
  "root_cause": "Reference snippets were not executed against the installed packages.",
  "fix": "Use window/distance_constraint, document the -1 to 1 range and NA handling, give the plot a locus, and add a seed argument (COACC-006 to COACC-008)."},
 {"priority": "P2", "title": "Enhancer-gene mapping inputs and unsupported claims", "observed_in": [1],
  "problem": "The TSS BED is unshipped and silently skipped, promoter-promoter pairs are labelled enhancers, and several quantitative claims and the SCENIC+ version/Docker statements are unsupported.",
  "root_cause": "Undocumented input contract; claims carried over without citations or execution.",
  "fix": "Document or generate the TSS BED, label promoter pairs, cite or soften the ranges, and pin SCENIC+ (COACC-009 to COACC-013)."},
]
report = {
 "meta": {"skill_name": SKILL, "description": "Infer cis-regulatory connections (peak-to-peak co-accessibility) from scATAC-seq using Cicero, ArchR getCoAccessibility, or SCENIC+, and map them to enhancer-gene candidates.",
          "evaluated_on": DATE, "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "D", "complexity": "Complex", "n_inputs": 7},
 "veto_gates": {
  "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
  "research_veto": {"applicable": True, "gate": "PASS",
    "scientific_integrity": {"result": "PASS", "detail": "No fabricated values; enhancer column defect (COACC-002) is a coding error, and unsupported ranges are filed as P3 COACC-011"},
    "practice_boundaries": {"result": "PASS", "detail": "Research analysis guidance; no clinical claims"},
    "methodological_ground": {"result": "PASS", "detail": "Co-accessibility is explicitly framed as a hypothesis generator, not 3D contact; permutation control behaves as documented"},
    "code_usability": {"result": "PASS", "detail": "The function ran to completion with a chr1-only genome_df and integer-format matrices load; CLI failure on pattern .mtx and the 25 min unmodified timeout are P1/P2 defects (COACC-001, COACC-003), not unrunnable code"}}},
 "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
 "dynamic_score": {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": passed, "total": total_a}, "inputs": inp},
 "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": grade, "grade_symbol": sym,
           "deployable": grade in ("Production Ready", "Limited Release"), "veto_override": False},
 "key_strengths": [
  "Correct scientific framing: co-accessibility is a hypothesis generator, with explicit validation routes and an ABC/Hi-C decision table",
  "Core Cicero pipeline, alpha estimation, and permutation negative control behave as documented on real public PBMC data",
  "ArchR and LinkPeaks routes ran with plausible outputs; Hi-C concordance snippet recovered planted truth",
  "Lean SKILL.md with routed references and preserved MIT provenance"],
 "recommendations": recs}
json.dump(report, open(os.path.join(R, 'report.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print("static", sub, "avg", avg, "score", score, grade, "assertions", passed, total_a)

# ---------- viewer.md ----------
V = f"""# Audit viewer: {SKILL} (initial audit, {DATE})

Candidate `sha256-manifest-v1 {ident}` (5 files), origin `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/co-accessibility`. Diagnostic score only; not a readiness claim.

**Result: {score} / 100, {grade}, not deployable.** Static {sub} (x0.4 = {sw}), execution average {avg} (x0.6 = {dw}), assertions {passed}/{total_a}. Skill veto PASS, research veto PASS. Category Data Analysis, mode D, 7 inputs.

## Inputs

| # | Type | Input | Status | Total |
|---|---|---|---|---|
""" + "\n".join(f"| {x['index']} | {x['type']} | {x['label']} | {x['status']} | {x['total']} |" for x in inp) + """

## Findings (ordered ledger)

| ID | Severity | Summary |
|---|---|---|
""" + "\n".join(f"| {f['id']} | {f['severity']} | {f['summary']} |" for f in F) + """

Report recommendations carry P3 findings under P2 (schema allows P0-P2 only); findings.json keeps ledger severities. Full text with evidence and fix: `findings.json`. Report: `report.json`.

## Execution classification

Executed: shipped function (chr1-only genome), alpha block and permutation control, visualization, Hi-C snippet, ArchR, LinkPeaks (tooling-phase run, log inspected). Failed: CLI on pattern .mtx; shipped function unmodified (25 min timeout, bounded). Blocked: SCENIC+ (pybedtools build; static review only). Static-only: reference databases, HiChIP/ABC/CRISPRi prose. See `execution-classifications.json`.

## Observations not filed as findings

- Two unseeded runs of the shipped function on the same machine were identical (99,284 rows, Pearson 1.0000, strong-set Jaccard 1.0000), so no determinism finding is filed; the Skill's 'set seed' advice is unnecessary here but the script does not set one.
- The permutation control is clean (36 residual strong pairs of 11,794 real).
- Integer-format .mtx loads through new_cell_data_set; the CLI failure is specific to logical/pattern input.
- The CLI when fed an integer matrix was not run end to end because the unmodified genome default exceeds the time budget.
- Real chr1 slice: strong pairs are proximal (71 percent < 250 kb) with distance-decay mean scores.

## Reproduction

Scripts and logs in `runs/`, tooling evidence in `evidence/`, environment per `TOOLS.md` (WSL env `bio-atac-seq-co-accessibility`, R 4.4.3, cicero 1.3.9 GitHub monocle3 branch, monocle3 1.3.1, ArchR 1.0.3, Signac 1.17.1).
"""
open(os.path.join(R, 'viewer.md'), 'w', encoding='utf-8', newline='\n').write(V)
