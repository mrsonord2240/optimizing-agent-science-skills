import json, pathlib
H = pathlib.Path(__file__).resolve().parent.parent
M = json.load(open(H / 'out' / 'manifest.json'))
blob = {"LICENSE": "87da87fcf00d56ea67be30ed0f0ec07045f1263a", "SKILL.md": "49e0bdfc3fda49ec3d2f891ca1e454686fa80828",
        "references/method-reference.md": "72e134047ab18ee5567bcf0406990c8343983366",
        "references/usage-guide.md": "1db550b87efd54026aedc7ea2743a573d8bb19cf",
        "scripts/call_atac_peaks.sh": "e3460d14a106c04cd58b89a99ac4466409b40e84"}
src = {
    "origin": {"repository": "GPTomics/bioSkills", "commit": "d91ed3d563019e649dc854c56ccd62551359488a",
               "path": "atac-seq/atac-peak-calling", "subtree": "821b1f00393b73c7b940de82e7f57b2555c3fb5a",
               "checkout": "F:\\optimizing-agent-science-skills\\external\\GPTomics__bioSkills", "status": "clean"},
    "candidate": {"branch": "fix/atac-atac-peak-calling", "commit": "3186916406e9cc6b0e6dc24ffe47880951fc0f93",
                  "identity": "sha256-manifest-v1", "manifest_sha256": M["manifest_sha256"],
                  "path": "F:\\OpenScience\\wt\\atac-atac-peak-calling\\skills\\bio-atac-seq-atac-peak-calling",
                  "status_before": "5 files staged (A), normalization output; no working-tree edits",
                  "status_after_execution": "unchanged (manifest re-verified after execution)",
                  "manifest_recipe": "relative POSIX path, byte count, lowercase SHA-256; tab-separated; LF joins; ordinal UTF-8 byte ordering; no trailing LF"},
    "files": [{"path": f["path"], "git_blob": blob[f["path"]], "sha256": f["sha256"], "bytes": f["bytes"]} for f in M["files"]],
    "tooling": {"tools_md_sha256": "86d6679d9ffe162870f2c94965c50f2ae62d42b1d115749efadbe694b07edc25",
                "environment_fingerprint_sha256": "08bd20dfc98af31b1acf5751fd307372decbc33017586ea9a5e80e8677a902b6",
                "rubric_zip_sha256": "e54e9ff8b0c3677abcfe657ad6ed92ba34dbdb8ad205c7157ad881f25afcf0de"},
    "candidate_cache_artifacts_after_execution": []}
json.dump(src, open(H / 'source-identity.json', 'w', encoding='utf-8'), indent=2)


def F(i, sev, title, obs, problem, root, fix, ev):
    return {"id": f"ATACPC-{i:03d}", "severity": sev, "state": "open", "title": title, "observed_in": obs,
            "problem": problem, "root_cause": root, "fix": fix, "evidence": ev}


findings = [
    F(1, "P1", "call_atac_peaks.sh pseudoreplicates share half their reads", [1],
      "The two rep1 pseudoreplicates are independent 50% subsamples (samtools -s 1.5 and 2.5): 131,281 of about 262k read names in each half are shared (50%), so they are not the disjoint split ENCODE uses. Nself at IDR 0.10 was 2,473 with these halves vs 1,234 (0.10) or 1,143 (0.05) for truly disjoint halves of the same BAM; the script reports ratio 2.066 (fail) while disjoint pseudoreplicates give ratios of 1.09-1.16 (pass).",
      "samtools view -s draws each subsample independently; the script comment calls this approximate but the QC decision depends on it.",
      "Split each BAM into complementary halves (samtools view -s SEED.5 -o a.bam -U b.bam) so every read pair lands in exactly one half; fix the same wording in method-reference.md.",
      "initial-audit-20260930/out/a1.log; out/a2_disjoint_pseudoreps.log"),
    F(2, "P1", "Nt/Nself rule is not the ENCODE rescue and self-consistency ratios", [1],
      "SKILL.md, usage-guide.md and the script use a single ratio max(Nt,Nself)/min(Nt,Nself) from rep1 pseudoreps only and say both ratios without defining a second. ENCODE (encode_task_reproducibility.py) uses rescue ratio = Np/Nt (pooled pseudoreps) and self-consistency = N1/N2 (per-replicate pseudoreps): pass if both <=2, borderline if one >2, fail only if both >2. The script builds rep2 pseudorep BAMs and a pooled peak set but never uses them, and compares Nt at IDR 0.05 with Nself at 0.10 (the ENCODE pipeline uses one threshold, 0.05, for all comparisons).",
      "The rule was condensed to one ratio and the pipeline stops after rep1 pseudoreps.",
      "Implement per-replicate and pooled disjoint pseudoreplicates, compute N1, N2, Np, Nt at one stated IDR threshold, report rescue and self ratios with pass/borderline/fail, and align SKILL.md, usage-guide.md and method-reference.md wording.",
      "out/a1.log (pooled and psr2 never referenced); out/a2_disjoint_pseudoreps.log: Nt=1197 N1=1143 N2=1249 Np=1036; ENCODE-DCC/atac-seq-pipeline src/encode_task_reproducibility.py"),
    F(3, "P1", "Documented install line fails; conda idr crashes on numpy>=1.24", [1],
      "usage-guide.md 'conda install -c bioconda macs3 macs2 genrich samtools bedtools idr' does not solve on bioconda alone; adding conda-forge first solves to idr 2.0.4.2 with numpy 1.26, which crashes (np.int) on the first IDR call, so step 4 of the primary workflow cannot run in that environment. SKILL.md asserts tested with IDR 2.0.4+ and HMMRATAC 1.2+, though standalone Java HMMRATAC was never exercised and the stated install does not produce a working IDR.",
      "Install line was not resolved or executed; idr 2.0.4.2 has no numpy pin.",
      "Give a solving install (channel order conda-forge, bioconda) with idr in its own environment or pinned numpy<1.24 (macs3 needs newer numpy), state tested versions accurately, and drop or qualify the HMMRATAC 1.2+ claim (macs3 hmmratac is the tested route).",
      "evidence/dryrun_documented_install.log; TOOLS.md version-drift table"),
    F(4, "P2", "macs2 callpeak import fails on modern glibc; script hardcodes macs2", [1, 2],
      "bioconda macs2 2.2.9.1 fails at import (undefined symbol __log_finite) on this glibc; --version and --help still succeed so a smoke check misleads. Reproduced without the shim. macs3 callpeak gave the same 391 peaks and width 150 as macs2 on the planted BAM with identical flags.",
      "The primary script depends on a MACS2 build that no longer imports on current Linux.",
      "Let the script take a MACS binary variable and default to macs3 callpeak (same flags), note the macs2 import failure, and require a real callpeak run as the version check.",
      "out/a4_misc_snippets.log; evidence/shim_check.log; evidence/check_callers.log"),
    F(5, "P2", "Script default -g hs contradicts the genome-size rule; wrong size in comment", [1],
      "SKILL.md and usage-guide.md say to use the deepTools effective size, not the hs shorthand, but the script defaults to hs and method-reference.md examples use -g hs. The script comment offers 2.701e9 for hg38 100 bp reads while the Skill's own table gives 2.701e9 for 50 bp and 2.806e9 for 100 bp.",
      "Defaults and comments not reconciled with the reference tables.",
      "Make GENOME required or default to a stated size with a read-length note; correct the comment to 2.806e9 (100 bp) or label 2.701e9 as 50 bp; use a variable in method-reference examples.",
      "scripts/call_atac_peaks.sh line 9; references/method-reference.md lines 27-34"),
    F(6, "P2", "SKILL.md says the script validates input BAMs; it does not", [1],
      "SKILL.md states the script validates input BAMs. The script has no check for file existence, index, paired-end, chrM absence or matching blacklist/genome; with set -e it only fails at the first tool error.",
      "Documentation describes intent, not implementation.",
      "Add minimal checks (files readable, indexed, no chrM reads via idxstats, tools on PATH) or remove the claim.",
      "SKILL.md Routed material; scripts/call_atac_peaks.sh"),
    F(7, "P2", "Blacklist and outputs cover only the IDR true-rep set; no final set or bigWig", [1],
      "Workflow steps 6-7 promise blacklist filtering and narrowPeak plus bigWig outputs. The script blacklists only true_reps.idr (1,197 to 1,188 peaks, written as BED with IDR columns), leaves per-rep, pooled and pseudorep peaks unfiltered, produces no conservative or optimal narrowPeak set, and never converts the -B --SPMR bedGraphs (unused, large) to bigWig.",
      "Script stops after the QC ratio.",
      "Emit blacklisted narrowPeak for the reproducible set (pooled peaks overlapping true-rep IDR as in ENCODE) or state plainly that the script is QC-only; add the documented bigWig step or drop -B --SPMR.",
      "out/a1.log; TOOLS.md smoke table"),
    F(8, "P2", "Genrich has no runnable command; coordinate-sorted BAM fails; -q 0.01 advice wrong", [3],
      "Only prose describes Genrich. Genrich 0.6.2 aborts on the coordinate-sorted BAMs the Skill assumes (not sorted by queryname, samtools sort -n); the name-sort step is not documented. The reconciliation table says to rerun Genrich with -q 0.01 for parity with fewer MACS peaks, but on the GM12878 chr1 slice Genrich gave 14,328 peaks at q 0.05, 22,936 at 0.01 and 23,535 at 0.001 (MACS3 4,803); the log-scale vs linear q explanation is unsupported.",
      "Genrich section is descriptive only and its reconciliation claim was not tested.",
      "Add a tested name-sort plus Genrich -j -e chrM -E command, and replace or remove the -q parity advice.",
      "out/a3_genrich_checks.log; evidence/smoke_callers.log"),
    F(9, "P2", "macs3 hmmratac has no runnable command; output description mismatches", [4],
      "No invocation is given. On the GM12878 slice macs3 hmmratac -i BAM -f BAMPE produced *_accessible_regions.narrowPeak (2,064 regions, recovers 2,072/2,088 ENCODE IDR peaks), a model json and a cutoff table; method-reference.md describes an Output BED. The 30M-read minimum and 24 h runtime claims are uncited and untested here.",
      "Section is descriptive.",
      "Add the tested command and output names; cite or soften the depth and runtime figures.",
      "evidence/check_callers.log; evidence/smoke_callers.log"),
    F(10, "P2", "Script called the exact ENCODE pattern but omits --call-summits and tagAlign", [1],
      "method-reference.md says the pattern is exact. The ENCODE ATAC pipeline runs macs2 on Tn5-shifted tagAlign (-f BED) with --call-summits; the script uses -f BAM without --call-summits, so peak segmentation and IDR inputs differ from published ENCODE sets.",
      "Simplified adaptation presented as exact.",
      "Say ENCODE-style and list the differences, or add --call-summits and the tagAlign conversion.",
      "ENCODE-DCC/atac-seq-pipeline src/encode_task_macs2_atac.py; references/method-reference.md line 132"),
    F(11, "P2", "Single-sample guidance inconsistent; rotation method uncited", [],
      "Single-sample advice is -q 0.01 in method-reference.md but -q 0.05 in its decision tree and usage-guide.md. The rotation/circular-shift permutation proxy has no command, citation or test and is presented as a reproducibility proxy (static-only).",
      "Sections written independently.",
      "Pick one tested setting; cite or remove the permutation method.",
      "references/method-reference.md lines 98-104, 191; references/usage-guide.md line 44"),
    F(12, "P3", "ROSE snippet cannot run as written (static-only)", [],
      "The ROSE command needs a GFF of stitched regions and R/samtools; no narrowPeak-to-GFF step is given. ROSE was not installed, so this is static review only.",
      "Snippet copied without a conversion step.",
      "Add the conversion or mark the snippet illustrative.",
      "references/method-reference.md lines 121-128"),
    F(13, "P3", "Script leaves shell variables unquoted", [1],
      "$OUTDIR, BAM and blacklist paths are unquoted, so paths with spaces break; low likelihood in normal use.",
      "Minimal script style.",
      "Quote expansions.",
      "scripts/call_atac_peaks.sh"),
]
json.dump(findings, open(H / 'findings.json', 'w', encoding='utf-8'), indent=2)


def A(t, r, n):
    return {"text": t, "result": r, "note": n}


inputs = [
    {"index": 1, "type": "Canonical", "label": "ENCODE-4 script on GM12878 rep1/rep2 chr1:1-30Mb", "status": "COMPLETED", "status_flag": "\u26a0\ufe0f",
     "note": "Runs to completion; pseudoreplicates overlap and Nself/ratio differ from ENCODE definition (ratio 2.066 vs 1.09-1.16 disjoint)",
     "basic": 28, "specialized": 36, "total": 64,
     "assertions": [
         A("Script exits 0 and writes per-rep, pooled, pseudorep, IDR, plot and blacklist outputs", "PASS", "All files present and parsed: 4803/4366/4310 peaks, IDR 1197 and 2473 rows, both PNGs"),
         A("Reported Nt equals the count of IDR rows at the threshold", "PASS", "Nt=1197 equals true_reps.idr row count"),
         A("The two pseudoreplicates are disjoint halves of the BAM", "FAIL", "131,281 of about 262k read names shared between halves"),
         A("Reported ratios agree with ENCODE rescue and self-consistency ratios on the same data", "FAIL", "Script 2.066 (fail); disjoint pseudoreplicates give rescue 1.155, self 1.093"),
         A("All called peak sets (pooled, rep2 pseudoreps) feed the final QC decision", "FAIL", "Pooled peaks and rep2 pseudorep BAMs are never used")]},
    {"index": 2, "type": "Variant A", "label": "MACS3/MACS2 callpeak, shift-extend vs BAMPE, planted and real", "status": "COMPLETED", "status_flag": "\u2705",
     "note": "Method-reference claims confirmed; macs2 import needs a shim", "basic": 36, "specialized": 52, "total": 88,
     "assertions": [
         A("MACS3 -f BAMPE recovers the 20 planted regions", "PASS", "24 peaks, 20/20 truth, median width 373"),
         A("MACS3/MACS2 -f BAM --shift -75 --extsize 150 recover planted regions at width 150", "PASS", "391 peaks each, 20/20, width 150"),
         A("-f BAMPE ignores --shift/--extsize as documented", "PASS", "Identical 24 peaks and widths with and without the flags"),
         A("MACS3 ENCODE-pattern peaks on GM12878 rep1 recover ENCODE IDR peaks", "PASS", "4,803 peaks; 2,087 of 2,088 ENCODE peaks overlapped"),
         A("Documented macs2 callpeak runs in a fresh install", "FAIL", "ImportError undefined symbol __log_finite without shim")]},
    {"index": 3, "type": "Variant B", "label": "Genrich joint mode with chrM exclusion and blacklist", "status": "COMPLETED", "status_flag": "\u26a0\ufe0f",
     "note": "Works on name-sorted input; requirement and q-cutoff advice not in Skill", "basic": 30, "specialized": 42, "total": 72,
     "assertions": [
         A("Genrich recovers 20 planted regions", "PASS", "20/20 (2,327 peaks, noisy on tiny fixture)"),
         A("Genrich joint on GM12878 reps recovers ENCODE IDR peaks", "PASS", "14,498 peaks, 2,085 of 2,088 recovered"),
         A("Genrich accepts the coordinate-sorted BAMs the Skill assumes", "FAIL", "Error: not sorted by queryname (samtools sort -n)"),
         A("Skill advice -q 0.01 brings Genrich closer to MACS peak counts", "FAIL", "14,328 peaks at 0.05 rose to 22,936 at 0.01")]},
    {"index": 4, "type": "Variant B", "label": "macs3 hmmratac on GM12878 rep1", "status": "COMPLETED", "status_flag": "\u2705",
     "note": "Produces sensible accessible regions; no invocation or output names in Skill", "basic": 32, "specialized": 46, "total": 78,
     "assertions": [
         A("hmmratac completes and writes parseable regions and model", "PASS", "2,064 regions narrowPeak, model json, cutoff table"),
         A("hmmratac regions recover ENCODE IDR peaks", "PASS", "2,072 of 2,088 overlapped"),
         A("Documented output description matches actual outputs", "FAIL", "Skill says BED; tool writes *_accessible_regions.narrowPeak")]},
    {"index": 5, "type": "Edge", "label": "NFR-only recipe, blacklist filter, bigWig, grep -v chrM", "status": "COMPLETED", "status_flag": "\u2705",
     "note": "Recipes run and give sensible output; bigWig checked structurally only", "basic": 33, "specialized": 47, "total": 80,
     "assertions": [
         A("NFR-only recipe calls peaks that recover ENCODE peaks", "PASS", "10,951 peaks; 2,078 of 2,088 recovered"),
         A("Blacklist intersect -v removes blacklisted peaks only", "PASS", "4,803 to 4,753 with the 636-region v2 list"),
         A("bedGraph to bigWig recipe produces a valid bigWig", "PASS", "3.2 MB file, magic 0x888FFC26 (signal values not read back)"),
         A("grep -v chrM snippet removes chrM reads and their chr1 mates cleanly", "PASS", "Synthetic pair with mate on chrM: both records and chrM @SQ removed")]},
]
for i in inputs:
    i["assertions_passed"] = sum(a["result"] == "PASS" for a in i["assertions"])
    i["assertions_total"] = len(i["assertions"])
    assert i["basic"] + i["specialized"] == i["total"]
    assert 3 <= i["assertions_total"] <= 5
avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
cats = {"functional_suitability": (9, 12, "Broad, mostly accurate caller coverage; QC ratio logic and install instructions wrong"),
        "reliability": (7, 12, "Script has no input validation and depends on a macs2 build that fails to import; no IDR environment guard"),
        "performance_context": (7, 8, "SKILL.md is short with routed references; method-reference.md is long but sectioned"),
        "agent_usability": (12, 16, "Clear workflow and routing; Genrich, hmmratac and NFR lack tested invocations in the Skill"),
        "human_usability": (6, 8, "Quick-start prompts and decision tables help; single-sample and reconciliation advice inconsistent"),
        "security": (10, 12, "No credentials or destructive operations; unquoted variables and blacklist download without checksum"),
        "maintainability": (9, 12, "License and provenance preserved, references organized; unpinned versions and stale claims"),
        "agent_specific": (15, 20, "Trigger-rich description; ENCODE-exact and script-validation claims overstated")}
sub = sum(v[0] for v in cats.values())
sw = round(sub * 0.4, 1)
dw = round(avg * 0.6, 1)
score = round(sw + dw)
tp = sum(i["assertions_passed"] for i in inputs)
tt = sum(i["assertions_total"] for i in inputs)
report = {
    "meta": {"skill_name": "bio-atac-seq-atac-peak-calling",
             "description": "Call accessible chromatin regions from ATAC-seq BAM files using MACS3, MACS2, Genrich, or HMMRATAC. Use when identifying open chromatin from aligned ATAC-seq, choosing between point-source vs HMM peak callers, applying ENCODE-style pseudoreplicate IDR, removing blacklist regions, or fixing 501bp consensus peaks for downstream differential analysis.",
             "evaluated_on": "2026-09-30", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis",
             "execution_mode": "D", "complexity": "Moderate", "n_inputs": 5},
    "veto_gates": {"skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
                   "research_veto": {"applicable": True, "gate": "PASS",
                                     "scientific_integrity": {"result": "PASS", "detail": "No fabricated values; checked figures (effective genome sizes, MACS behaviours) are traceable; uncited depth and runtime claims are noted in ATACPC-009"},
                                     "practice_boundaries": {"result": "PASS", "detail": "Research-only genomics skill with no clinical conclusions"},
                                     "methodological_ground": {"result": "PASS", "detail": "The self-consistency implementation departs from ENCODE (ATACPC-001, ATACPC-002) and flags a passing library, but the script discloses approximate pseudoreplicates and the method is not fabricated or causally invalid; scored down in Layer 2 and filed P1"},
                                     "code_usability": {"result": "PASS", "detail": "call_atac_peaks.sh ran to completion on real ENCODE BAMs; install and macs2 import problems are environment issues filed as ATACPC-003 and ATACPC-004"}}},
    "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
    "dynamic_score": {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": tp, "total": tt}, "inputs": inputs},
    "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": "Beta Only", "grade_symbol": "\u26a0\ufe0f",
              "deployable": False, "veto_override": False},
    "key_strengths": [
        "Caller coverage (MACS3/MACS2 shift-extend and BAMPE, Genrich joint, hmmratac, NFR-only) recovered planted truth and 2,072-2,087 of 2,088 ENCODE IDR peaks on real GM12878 data",
        "The claim that -f BAMPE ignores --shift/--extsize is correct and shown by identical outputs",
        "Effective genome size tables match deepTools values; license and provenance are preserved",
        "Routed structure keeps SKILL.md short and sends detail to references and a runnable script"],
    "recommendations": [
        {"priority": "P1", "title": "Use disjoint pseudoreplicates in the ENCODE script", "observed_in": [1],
         "problem": "The two pseudoreplicates share 50% of their reads and Nself is inflated (2,473 vs 1,234 with disjoint halves), giving a false ratio of 2.066.",
         "root_cause": "samtools view -s with two seeds draws independent subsamples.",
         "fix": "Split each BAM with -s SEED.5 -o a.bam -U b.bam and correct the method-reference wording. (ATACPC-001)"},
        {"priority": "P1", "title": "Implement ENCODE rescue and self-consistency ratios", "observed_in": [1],
         "problem": "One Nt/Nself ratio from rep1 only is reported; pooled and rep2 pseudoreplicates are built or ignored, and thresholds differ (0.05 vs 0.10).",
         "root_cause": "The ENCODE rule was condensed and the pipeline stops early.",
         "fix": "Compute N1, N2, Np, Nt at one IDR threshold and report rescue and self ratios with pass/borderline/fail; align all three files. (ATACPC-002)"},
        {"priority": "P1", "title": "Fix the install line and the idr numpy incompatibility", "observed_in": [1],
         "problem": "The documented conda line does not solve on bioconda alone and yields an idr that crashes on numpy>=1.24.",
         "root_cause": "Install line and tested-version claim were never executed.",
         "fix": "Document a solving install with idr isolated or numpy<1.24 and correct the tested-versions statement. (ATACPC-003)"},
        {"priority": "P2", "title": "Prefer macs3 callpeak; macs2 import fails on new glibc", "observed_in": [1, 2],
         "problem": "macs2 2.2.9.1 fails at import with __log_finite and the script hardcodes macs2.",
         "root_cause": "Build depends on removed glibc symbols.",
         "fix": "Make the binary a variable defaulting to macs3 callpeak. (ATACPC-004)"},
        {"priority": "P2", "title": "Reconcile genome-size default and comment with the tables", "observed_in": [1],
         "problem": "Script defaults to -g hs and labels 2.701e9 as 100 bp while the Skill table says 2.806e9.",
         "root_cause": "Unreconciled defaults.",
         "fix": "Require the size or default to a stated value and correct the comment. (ATACPC-005)"},
        {"priority": "P2", "title": "Align script claims with behaviour", "observed_in": [1],
         "problem": "The script does not validate BAMs, filters only the IDR true-rep set, yields no final peak set or bigWig, and is called exact ENCODE without --call-summits or tagAlign.",
         "root_cause": "Documentation describes intended rather than implemented behaviour.",
         "fix": "Add minimal checks and the missing outputs or narrow the claims. (ATACPC-006, ATACPC-007, ATACPC-010)"},
        {"priority": "P2", "title": "Add tested Genrich and hmmratac commands", "observed_in": [3, 4],
         "problem": "Genrich needs name-sorted BAMs and the q-cutoff parity advice is wrong; hmmratac has no command and writes narrowPeak, not BED.",
         "root_cause": "Sections are descriptive and were untested.",
         "fix": "Add executed commands and correct the reconciliation and output descriptions. (ATACPC-008, ATACPC-009)"},
        {"priority": "P2", "title": "Resolve single-sample guidance and uncited methods", "observed_in": [],
         "problem": "Single-sample -q differs between files, the rotation-permutation proxy has no source or test, and the ROSE snippet lacks a GFF step.",
         "root_cause": "Sections written independently.",
         "fix": "Choose one setting, cite or remove the proxy, fix or mark the ROSE snippet. (ATACPC-011, ATACPC-012, ATACPC-013)"}]}
json.dump(report, open(H / 'report.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print(sub, avg, sw, dw, score, tp, tt)
