"""Build findings.json, report.json, source-identity.json, out/manifest.json for the initial audit of bio-atac-seq-footprinting."""
import hashlib, json, os, pathlib, subprocess

H = pathlib.Path(__file__).resolve().parent.parent
CAND = pathlib.Path(r"F:\OpenScience\wt\atac-footprinting\skills\bio-atac-seq-footprinting")


def w(name, obj):
    (H / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


# ---------------- findings (single ordered ledger) ----------------
F = []
def f(id, sev, title, obs, problem, cause, fix, ev):
    F.append({"id": id, "severity": sev, "state": "open", "title": title, "observed_in": obs, "problem": problem,
              "root_cause": cause, "fix": fix, "evidence": ev})

f("FOOT-001", "P1", "CTCF validation step vanishes silently when no CTCF motif dir matches", [3],
  "run_tobias.sh gates its only QC step (CTCF PlotAggregate) on the glob CTCF_*/beds/CTCF_*_bound.bed. With a motif file lacking CTCF (GATA1, IRF4, EBF1 only) the script exits 0, writes an empty out/validation/, prints no warning and still prints the differential table; SKILL.md calls the CTCF dip the required check before trusting calls.",
  "The if [ -f ... ] guard has no else branch.",
  "Add an else branch that prints a clear warning (or exits non-zero unless a flag opts out) naming the missing CTCF motif, and say in SKILL.md that non-CTCF or non-JASPAR-named motif sets need another positive control.",
  "logs/a2_no_ctcf_and_spaces.log (rerun a2r: rc=0, validation files: 0); scripts/a2_no_ctcf_and_spaces.sh")
f("FOOT-002", "P1", "scPrinter route is not runnable as documented", [5],
  "usage-guide.md installs scPrinter with pip install ./ from a clone and lists scATAC-cluster and 80M-read requests, but the bundle has no scPrinter command or API. The v1.2.0 install imports tangermeme.tools.tomtom, which exists in tangermeme 0.4.4 but not in 1.5.0 (verified by wheel listing); import_fragments needs snapatac2==2.8.0 (2.9.0 lacks pp.import_data); first import downloads models from the internet; the stated scprinter 0.1+ floor is stale (1.2.0). With those pins the classic path worked: 400x99x200 finite scores, CTCF bound>unbound at modes 10/20/30 (p 1e-15 to 2e-8), profile peak at -2 bp.",
  "scPrinter is named as a first-class tool but only its name and a clone-install line are shipped.",
  "Add a tested scPrinter recipe (env pins tangermeme 0.4.4 and snapatac2 2.8.0, SCPRINTER_DATA and network note, bias prediction, import_fragments, get_footprint_score with an interpretation of the mode/scale argument) or narrow the description and usage requests to what is shipped; update the version floor.",
  "logs/a8_scprinter.log; scripts/a8_scprinter.py, a8b_assert.py; logs/a4_static_claims.log (tangermeme 0.4.4 has tools/tomtom, 1.5.0 does not); tooling logs/fix_scprinter_tangermeme.out")
f("FOOT-003", "P1", "One-line bioconda install resolves TOBIAS 0.13.3 on Python 3.7", [],
  "conda install -c bioconda tobias rgt pydnase samtools bedtools (with conda-forge) resolves Python 3.7.12, TOBIAS 0.13.3 and samtools 1.18 because rgt and pydnase pin py37, below the stated TOBIAS 0.16+ and samtools 1.19+; with bioconda alone tobias is unsolvable (adjusttext missing). run_tobias.sh was validated only on TOBIAS 0.17.5.",
  "Four tools with incompatible Python pins are installed into one environment.",
  "Replace with separate environments (TOBIAS alone or pip install tobias; rgt; pydnase; scPrinter) and state the conda-forge channel; keep the tested versions listed.",
  "logs/a4_static_claims.log (dry run 2026-09-30); tooling logs/dryrun_install_line.out")
f("FOOT-004", "P2", "rgt-hint fails on the documented install and no HINT-ATAC command is given", [4],
  "The bioconda rgt package ships no data: rgt-hint footprinting exits 1 with FileNotFoundError ~/rgtdata/data.config unless RGTDATA is hand-built. The Skill recommends HINT-ATAC for single-step runs and for two-tool concordance but gives no command, RGT data setup, or genome configuration. With a hand-built data dir, rgt-hint footprinting --atac-seq --paired-end --organism=hg38 produced 358 footprints in 60 peaks.",
  "HINT-ATAC is named without its required data setup or invocation.",
  "Document rgt data installation and one tested HINT-ATAC command (paired-end, organism, regions) or drop it from the concordance rule.",
  "logs/a9_hint_no_rgtdata.log; logs/a5_hint_wellington.log; scripts/a5_hint_wellington.sh")
f("FOOT-005", "P2", "usage-guide JASPAR wget URL returns HTTP 404", [],
  "https://jaspar.genereg.net/download/data/2024/CORE/JASPAR2024_CORE_vertebrates_non-redundant_pfms.txt is 404 (also after redirect to jaspar.elixir.no); the working file is ..._pfms_jaspar.txt (200, JASPAR PFM format that TOBIAS reads). The mv line that follows would also fail.",
  "The download name dropped the _jaspar suffix.",
  "Use the _jaspar.txt URL in the wget and mv lines.",
  "logs/a4_static_claims.log (HTTP status lines); tooling logs/url_check_jaspar.out")
f("FOOT-006", "P2", "Script's top-TF summary is sorted by p-value but labelled by |change|", [1],
  "run_tobias.sh comments the final table as ranked by absolute change but runs sort -k3,3g (p-value). On the real run CTCF_MA0139.2 (-0.222) prints above GATA1_MA0035.5 (-0.385) and GATA1TAL1 (-0.309); by |change| the order is IRF4, GATA1, GATA1TAL1, CTCF. All CTCF/JASPAR motif variants also appear as separate rows.",
  "Comment and command disagree.",
  "Decide the intended ranking (|change| with a p-value filter is what the text implies), fix the command or the comment, and say that per-motif variants are listed separately.",
  "logs/a1b_assertions.log (byp vs byabs); logs/a1_run_tobias_unmodified.log")
f("FOOT-007", "P2", "Unquoted variables break on paths with spaces and leave stray directories", [3],
  "With OUTDIR='out dir' the script's mkdir -p creates 'out' and 'dir', then ATACorrect fails with 'unrecognized arguments: dir/cond1' (rc=2). The same holds for BAM, genome, motif and glob expansions ($OUTDIR/$cond/*_corrected.bw). Nothing else in the script guards against a failed step producing no output file.",
  "Variables are unquoted; globs are expanded without checking for exactly one match.",
  "Quote every expansion, expand each *_corrected.bw glob into an array and require exactly one match, and check that each step's output exists before the next.",
  "logs/a2_no_ctcf_and_spaces.log (ii); logs/a2_first_attempt_concurrent.log (ScoreBigwig cond2 output missing once under 3-way concurrent load; not reproduced on rerun)")
f("FOOT-008", "P2", "CTCF dip gate is selection-circular and uses cond1-bound sites for both conditions", [1],
  "PlotAggregate is run on CTCF_*_cond1_bound.bed, sites chosen because their footprint score is low. Negative control: footprints built from the UNCORRECTED signal (no bias correction) still give bound sites with an equally deep dip in the corrected signal (flank-minus-core 4.44 vs 3.78 for the corrected pipeline; unbound sites 0.38 and 0.15). So a clean dip at bound sites does not show that correction worked, contrary to SKILL.md step 5. The plot shows condition 2 only at condition-1-bound sites.",
  "The QC is evaluated on sites selected from the same score it is supposed to validate.",
  "Validate at all motif sites or ChIP-anchored CTCF sites (bound and unbound, corrected vs uncorrected, plus the bias track) and state what a pass does and does not show; or plot each condition at its own bound sites.",
  "out/a7_ctcf_profiles.png; logs/a7b_qc_profiles.log; scripts/a7_qc_negative_control.sh, a7b_qc_profiles.py")
f("FOOT-009", "P2", "Two-tool concordance rule is undefined and unmet on real data", [4],
  "SKILL.md and method-reference require '>50% overlap' (TOBIAS+HINT-ATAC or TOBIAS+ChIP) for high-confidence calls without defining the unit or direction. On GM12878 chr1:10-13 Mb, 40.6% (58/143) of TOBIAS-bound motif sites overlap a HINT footprint (0/31 unbound), but only 15.1% of HINT footprints overlap a TOBIAS-bound site; Wellington gives 6.3% (11.2% with -A). The rule as written would reject nearly every real result or be satisfied by choice of direction.",
  "Threshold and denominator are unspecified and not calibrated.",
  "Define the overlap statistic (which set is the denominator, site vs footprint level), give an empirical expectation, or replace with per-TF concordance of calls.",
  "logs/a5b_concordance.log; scripts/a5b_concordance.sh")
f("FOOT-010", "P2", "Wellington statements are stale: PE crash claim and missing -A ATAC mode", [4],
  "method-reference says Wellington crashes on paired-end ATAC and needs a post-shift. pyDNase 0.3.0 wellington_footprints.py ran to rc=0 on the paired-end ATAC BAM both by default (54 footprints) and with -A (72 footprints); -A is the tool's ATAC mode and is not mentioned. Skill says ATAC needs a post-shift but gives no shifted-BAM command for Wellington.",
  "Claims were not checked against pyDNase 0.3.0.",
  "Replace with the tested command (wellington_footprints.py -A regions.bed reads.bam outdir), drop the crash claim, and keep alignmentSieve only for custom counting.",
  "logs/a5_hint_wellington.log; logs/a4_static_claims.log (wellington --help lists -A)")
f("FOOT-011", "P3", "HINT-ATAC 'stranded mode' claim is not in rgt-hint 1.0.2", [4],
  "method-reference says pioneer-factor asymmetry can be handled with HINT-ATAC's stranded mode; rgt-hint footprinting --help (1.0.2) has no strand option (0 matches for 'strand').",
  "Unverified claim.", "Remove or cite the option and version.", "logs/a4_static_claims.log (HINT options)")
f("FOOT-012", "P3", "Implausible or unsupported routes in the tool table", [],
  "Table gives scPrinter minimum depth as '>= 1M cells (sc)'; PIQ is recommended for lower depth while also called outdated and hard to install (no instructions, not run); 'TOBIAS + scprinter combination' is listed with no procedure. Static-only; not executed.",
  "Table rows were condensed without procedures or sources.", "Correct or remove rows the Skill cannot support.", "SKILL.md workflow step 3; references/method-reference.md tool taxonomy and decision tree")
f("FOOT-013", "P3", "CTCF example ID MA0139.1 is absent from the JASPAR 2024 non-redundant file", [],
  "usage-guide requests CTCF MA0139.1; the shipped-default JASPAR2024 non-redundant vertebrates file contains MA0139.2, MA1929.2 and MA1930.2 only, and BINDetect creates one directory per ID.",
  "Older ID kept.", "Use MA0139.2 and mention the other CTCF variants.", "logs/a4_static_claims.log (motif IDs)")
f("FOOT-014", "P3", "Flag spelling mixes underscores and hyphens", [],
  "Docs use --cond_names and --share_y while TOBIAS 0.17.5 lists --cond-names and --share-y and the docs use --bound-pvalue; both spellings were accepted in the executed run.",
  "Version drift in flag names.", "Use the --help spellings of the tested version.", "logs/a4_static_claims.log (help text); logs/a1_run_tobias_unmodified.log")
f("FOOT-015", "P3", "Numeric and bias-symptom claims are unsourced (static-only)", [],
  "Examples: GC-rich motifs give a V and AT-rich an inverse V; CTCF ~70% ChIP overlap, nuclear receptors ~30%, ~19-20 bp footprint; 0.1-0.5 typical change. Observed here: IRF4 +0.59, GATA1 -0.39, CTCF flank-core 3.8-5.8 signal units. Not verifiable within this audit; no full-depth run (data are chr1 slices, 1.0 M and 5.5 M reads).",
  "Provider claims carried over.", "Add sources or soften.", "references/method-reference.md")
w("findings.json", F)

# ---------------- report.json ----------------
def inp(i, t, label, status, note, b, s, asserts):
    p = sum(1 for a in asserts if a[1] == "PASS")
    total = b + s
    flag = "\u2705" if status == "COMPLETED" and total >= 75 else ("\u26a0\ufe0f" if status == "COMPLETED" else "\u274c")
    return {"index": i, "type": t, "label": label, "status": status, "status_flag": flag, "note": note, "basic": b,
            "specialized": s, "total": total, "assertions_passed": p, "assertions_total": len(asserts),
            "assertions": [{"text": a[0], "result": a[1], "note": a[2]} for a in asserts]}

inputs = [
 inp(1, "Canonical", "run_tobias.sh unmodified, GM12878 vs K562 chr1:1-30 Mb", "COMPLETED",
     "rc 0 in 6 m 18 s; biology 4/4; CTCF dip 3.8/5.8 units; summary order and QC discrimination fail", 31, 43,
     [("rc 0 and cond bigwigs, bindetect_results.txt and CTCF aggregate PDF all present", "PASS", "13 motif IDs; PDF rendered and legible with dip and shoulders"),
      ("Direction of change: GATA1 < 0 (K562), IRF4 > 0 and EBF1 > 0 (GM12878)", "PASS", "GATA1 -0.385, IRF4 +0.588, EBF1 +0.055"),
      ("CTCF aggregate shows a central dip (flank minus core > 0.5) in both conditions", "PASS", "3.78 and 5.81 signal units, 513 sites"),
      ("Top-TF table is ranked by absolute change as its comment states", "FAIL", "sorted by p-value; CTCF -0.222 printed above GATA1 -0.385"),
      ("Dip gate fails when bias correction is removed (negative control)", "FAIL", "uncorrected-pipeline bound sites dip 4.44 vs 3.78 corrected")]),
 inp(2, "Variant A", "NFR filter, +4/-5 shift and TOBIAS on NFR BAMs", "COMPLETED",
     "NFR counts match independent expectation; shift +4/-5 confirmed; biology preserved on NFR reads", 35, 50,
     [("SKILL.md NFR filter count equals samtools -e expectation", "PASS", "94,478 vs 94,478 (chr1:1-3 Mb); 322,156 and 1,483,886 on the 30 Mb slices"),
      ("No retained read has |TLEN| >= 100 or 0", "PASS", "max |TLEN| 99, 0 violations"),
      ("alignmentSieve --ATACshift moves forward starts +4 and reverse ends -5", "PASS", "119,182/119,182 at +4; 118,152/119,182 at -5"),
      ("run_tobias.sh on NFR BAMs keeps biology and CTCF dip", "PASS", "4/4 asserts; dip 3.65/5.55 units, 645 sites")]),
 inp(3, "Edge", "Motif set without CTCF; output dir containing a space", "COMPLETED",
     "runs, but CTCF validation vanishes silently; space in path breaks with stray dirs", 27, 33,
     [("Run completes with differential results for the supplied motifs", "PASS", "IRF4 +0.588 identical to A1; rc 0"),
      ("Missing CTCF control yields a warning or failure rather than silence", "FAIL", "validation dir empty, no message, rc 0"),
      ("Path with a space works or is rejected cleanly", "FAIL", "rc 2 from TOBIAS argument error; stray out/ and dir/ created"),
      ("Rerun reproduces identical values", "PASS", "one concurrent-load attempt lost cond2 footprints; the rerun matched A1")]),
 inp(4, "Variant B", "HINT-ATAC and Wellington via the documented install", "PARTIAL",
     "no commands in the Skill; rgt-hint fails without data; tools run with improvised commands", 22, 30,
     [("rgt-hint runs after the documented conda install", "FAIL", "FileNotFoundError ~/rgtdata/data.config"),
      ("HINT footprints are enriched at TOBIAS-bound vs unbound sites", "PASS", "40.6% (58/143) vs 0% (0/31)"),
      ("Documented Wellington limitation (crash on paired-end ATAC) matches behavior", "FAIL", "rc 0 on paired-end BAM; -A mode exists"),
      (">50% concordance rule is attainable on real data", "FAIL", "HINT 40.6% / 15.1% by direction; Wellington 6.3-11.2%")]),
 inp(5, "Variant B", "scPrinter multi-scale footprints, GPU, bulk GM12878", "PARTIAL",
     "works only with undocumented pins and no Skill procedure; scores biologically sensible", 24, 36,
     [("import_fragments and get_footprint_score complete with finite output", "PASS", "400x99x200, all finite, 200 bound + 200 unbound"),
      ("CTCF-bound sites score higher than unbound at modes 10/20/30", "PASS", "0.67/0.39, 1.66/0.47, 0.86/0.33; p 1e-15 to 2e-8"),
      ("Mode-20 bound profile peaks at the motif centre", "PASS", "argmax offset -2 bp"),
      ("Documented pip install ./ gives an importable scPrinter", "FAIL", "needs tangermeme 0.4.4 and snapatac2 2.8.0 pins"),
      ("Skill supplies the scPrinter procedure its requests imply", "FAIL", "no command or API guidance in bundle")]),
]
cats = {
 "functional_suitability": (8, 12, "TOBIAS path complete and correct; scPrinter, HINT-ATAC, Wellington, PIQ named without procedures"),
 "reliability": (7, 12, "Silent skip of CTCF QC, no output checks between steps, space-in-path failure"),
 "performance_context": (7, 8, "80-line SKILL.md with routed references; reference file is large but conditional"),
 "agent_usability": (12, 16, "Clear workflow and tool decision table; several stale or unverifiable tool claims"),
 "human_usability": (6, 8, "Natural trigger phrases; positional-argument script and undocumented failure recovery"),
 "security": (10, 12, "No secrets or destructive operations; unquoted expansion and glob handling"),
 "maintainability": (9, 12, "Provenance and MIT license preserved; install line and URL drifted; no pinned environment"),
 "agent_specific": (16, 20, "Description covers goals and four tools; two of four tools lack shipped guidance"),
}
static = {"subtotal": sum(v[0] for v in cats.values()), "max": 100,
          "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}}
avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
sw, dw = round(static["subtotal"] * 0.4, 1), round(avg * 0.6, 1)
score = round(sw + dw)
grade = "Production Ready" if score >= 85 else "Limited Release" if score >= 75 else "Beta Only" if score >= 60 else "Reject"
report = {
 "meta": {"skill_name": "bio-atac-seq-footprinting",
          "description": "Detect transcription factor binding footprints in ATAC-seq using TOBIAS, HINT-ATAC, Wellington, or scprinter. Use when identifying bound TF sites within accessible regions, correcting Tn5 insertion bias before footprinting, choosing between cleavage-based and aggregate-based footprinters, or comparing differential TF activity between conditions.",
          "evaluated_on": "2026-09-30", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis",
          "execution_mode": "D", "complexity": "Moderate", "n_inputs": 5},
 "veto_gates": {
   "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
   "research_veto": {"applicable": True, "gate": "PASS",
     "scientific_integrity": {"result": "PASS", "detail": "No fabricated results; observed values match independent recomputation and real ENCODE biology."},
     "practice_boundaries": {"result": "PASS", "detail": "Public ENCODE data; no clinical or sensitive-data handling; single-tool calls labelled exploratory."},
     "methodological_ground": {"result": "PASS", "detail": "Bias-corrected footprinting is sound; the CTCF-dip gate is circular but does not invalidate the pipeline (FOOT-008)."},
     "code_usability": {"result": "PASS", "detail": "run_tobias.sh ran unmodified to rc 0 on real data on TOBIAS 0.17.5."}}},
 "static_score": static,
 "dynamic_score": {"execution_avg": avg, "max": 100,
   "assertion_pass_rate": {"passed": sum(i["assertions_passed"] for i in inputs), "total": sum(i["assertions_total"] for i in inputs)},
   "inputs": inputs},
 "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": grade,
           "grade_symbol": "\u26a0\ufe0f" if grade == "Beta Only" else "\u2705", "deployable": False, "veto_override": False},
 "key_strengths": [
   "Core TOBIAS pipeline (ATACorrect, ScoreBigwig, BINDetect) is correct and ran unmodified on real ENCODE data with expected biology (GATA1 K562, IRF4/EBF1 GM12878).",
   "NFR filter and +4/-5 Tn5 shift statements were verified numerically against independent counts.",
   "Progressive disclosure is clean: short SKILL.md, routed method reference, provenance and MIT license preserved.",
   "Per-TF failure modes and the exploratory-versus-concordant reporting stance are scientifically careful."],
 "recommendations": [
   {"priority": "P1", "title": "CTCF validation silently skipped without a CTCF motif", "observed_in": [3],
    "problem": "With a motif file lacking CTCF, run_tobias.sh exits 0 with an empty validation directory and no message.",
    "root_cause": "The if [ -f ... ] guard has no else branch.",
    "fix": "Warn or fail when no CTCF bound bed is found and document alternative controls (FOOT-001)."},
   {"priority": "P1", "title": "scPrinter route not runnable as documented", "observed_in": [5],
    "problem": "The clone-install line breaks without tangermeme 0.4.4 and snapatac2 2.8.0 and the bundle has no scPrinter procedure although requests advertise scATAC work.",
    "root_cause": "The tool is named without a tested recipe or version pins.",
    "fix": "Ship a tested pinned recipe or narrow the claims; update the stale 0.1+ floor (FOOT-002, FOOT-012)."},
   {"priority": "P1", "title": "One-line install resolves TOBIAS 0.13.3 on Python 3.7", "observed_in": [],
    "problem": "The documented conda line installs versions below the stated floors; bioconda-only is unsolvable.",
    "root_cause": "rgt and pydnase pin Python 3.7 in the same environment.",
    "fix": "Use separate environments and state channels (FOOT-003)."},
   {"priority": "P2", "title": "JASPAR URL 404; stale HINT-ATAC and Wellington guidance", "observed_in": [4],
    "problem": "The wget URL is 404, rgt-hint needs undocumented data, the Wellington crash claim is contradicted and -A is omitted, the stranded-mode claim is absent from 1.0.2.",
    "root_cause": "Claims and commands were not executed against current tool versions.",
    "fix": "Correct the URL and give tested HINT-ATAC and Wellington commands (FOOT-004, FOOT-005, FOOT-010, FOOT-011)."},
   {"priority": "P2", "title": "run_tobias.sh summary order, quoting and QC gate", "observed_in": [1, 3],
    "problem": "The summary is sorted by p-value though labelled by |change|, unquoted variables break on spaces, and the CTCF dip gate is met even without bias correction.",
    "root_cause": "Script logic was condensed without checking labels, quoting or the discrimination of the QC.",
    "fix": "Fix ranking, quote variables and validate the gate at unselected or ChIP-anchored sites (FOOT-006, FOOT-007, FOOT-008)."},
   {"priority": "P2", "title": "Two-tool concordance rule undefined and unmet on real data", "observed_in": [4],
    "problem": "The >50% overlap rule has no stated denominator; measured values are 40.6% or 15.1% for HINT and 6.3-11.2% for Wellington.",
    "root_cause": "Threshold carried over without calibration.",
    "fix": "Define the statistic and give an empirical expectation (FOOT-009)."}],
}
w("report.json", report)

# ---------------- identity ----------------
def manifest(root):
    files = {}
    for d, _, ns in os.walk(root):
        for n in ns:
            p = pathlib.Path(d, n); files[p.relative_to(root).as_posix()] = p.read_bytes()
    rows, lines = [], []
    for k in sorted(files, key=lambda v: v.encode("utf-8")):
        b = files[k]; sh = hashlib.sha256(b).hexdigest()
        rows.append({"path": k, "bytes": len(b), "sha256": sh}); lines.append(f"{k}\t{len(b)}\t{sh}")
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest(), rows

def git(*a, cwd=None):
    return subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True).stdout.strip()

ms, rows = manifest(CAND)
for r in rows:
    r["git_blob"] = git("hash-object", str(CAND / r["path"]))
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
w("source-identity.json", {
 "origin": {"repository": "GPTomics/bioSkills", "commit": "d91ed3d563019e649dc854c56ccd62551359488a", "path": "atac-seq/footprinting",
            "subtree": git("rev-parse", "d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/footprinting", cwd=r"F:\optimizing-agent-science-skills\external\GPTomics__bioSkills"),
            "checkout": r"F:\optimizing-agent-science-skills\external\GPTomics__bioSkills"},
 "candidate": {"branch": "fix/atac-footprinting", "commit": git("rev-parse", "HEAD", cwd=r"F:\OpenScience\wt\atac-footprinting"),
               "identity": "sha256-manifest-v1", "manifest_sha256": ms, "path": str(CAND),
               "status_before": "5 files untracked (normalization output); no working-tree edits",
               "status_after_execution": "unchanged (manifest re-verified after execution)",
               "manifest_recipe": "relative POSIX path, byte count, lowercase SHA-256; tab-separated; LF joins; ordinal UTF-8 byte ordering; no trailing LF"},
 "files": rows,
 "tooling": {"tools_md_sha256": sha(r"F:\OpenScience\audits\bio-atac-seq-footprinting\TOOLS.md"),
             "environment_fingerprint_sha256": sha(r"F:\OpenScience\audits\bio-atac-seq-footprinting\logs\fingerprint.txt"),
             "rubric_zip_sha256": sha(r"F:\optimizing-agent-science-skills\skill-auditor.zip")},
 "candidate_cache_artifacts_after_execution": []})
print("manifest", ms, "final", report["final"], "avg", avg, "static", static["subtotal"])
