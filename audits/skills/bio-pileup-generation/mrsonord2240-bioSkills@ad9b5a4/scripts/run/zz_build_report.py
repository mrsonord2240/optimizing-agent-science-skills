#!/usr/bin/env python3
"""Builds eval_report_bio-pileup-generation_result.json and eval_viewer_bio-pileup-generation.md from the scores decided in the
re-audit (scores are the auditor's judgement; the check counts are read back from run/checks_in*.json written by t01..t07)."""
import json, os, re

RUN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(RUN)
chk = {i: json.load(open(f"{RUN}/checks_in{i}.json", encoding="utf-8")) for i in range(1, 8)}
cnt = {i: (sum(1 for c in chk[i] if c[2]), len(chk[i])) for i in chk}
tot_p, tot_n = sum(a for a, b in cnt.values()), sum(b for a, b in cnt.values())
print("checks passed per input:", cnt, tot_p, tot_n)

SRC = "mrsonord2240/bioSkills@ad9b5a4ec484bcfc7d12e38a03a31d2a60cf6429:alignment-files/pileup-generation"
DESC = "Generate pileup data for variant calling using samtools mpileup and pysam. Use when preparing data for variant calling, analyzing per-position read data, or calculating allele frequencies."


def A(t, ok, n):
    return {"text": t, "result": "PASS" if ok else "FAIL", "note": n}


inputs = [
    dict(index=1, type="Canonical", label="Text pileup of the real human chr22 BAM (region/BED/-q/-Q), columns and symbols, depth cross-checked (REGRESSION of pre-fix input 1)",
         basic=35, specialized=54, note=f"executed; {cnt[1][0]}/{cnt[1][1]} checks pass (t01). One Skill claim is false: stepper='all' + fastafile DOES apply BAQ",
         prompt="Generate a text pileup for chr22:1952-4617 of my BAM (nf-core human test slice) with MAPQ>=20 and baseQ>=20, tell me what each column and symbol means, and check the depth against another tool.",
         assertions=[
             A("Output Format table and the quoted example row 'chr22 1952 T 0 * *' are true: 6 columns, depth == symbols == qualities, depth-0 rows exist", True, "1157 rows; 3 depth-0 rows incl. the exact quoted row"),
             A("pysam len(pileups) == samtools mpileup depth at every position: pysam defaults == -B, stepper='samtools'+fastafile == default; n differs at 1087 of 1157", True, "0 of 1157 differ in both comparisons; 1087 reproduced"),
             A("-q/-Q/-Q 13 default/--ff default UNMAP,SECONDARY,QCFAIL,DUP behave as documented against independent pysam-record counts and samtools depth", True, "-q 20/60 and -Q 13/20/30 equal at every position; named --ff list == default"),
             A("Region, BED, multi-BAM (9 columns), '[E::mpileup] fail to parse region' message, 1000G example rows and bcftools DP (minus '*') are as documented", True, "1000G rows identical to the Skill's example"),
             A("Skill statement 'stepper=all + fastafile does not apply BAQ' is true", False, "false in pysam 0.24.1: depth equals mpileup default (BAQ) at all 1157 positions and differs from -B at 40"),
         ]),
    dict(index=2, type="Variant A", label="pysam allele counts / frequency / find_variants / pileup_text on planted synthetic BAM and real BAM, shipped example (REGRESSION of pre-fix input 2)",
         basic=35, specialized=53, note=f"executed; {cnt[2][0]}/{cnt[2][1]} checks pass (t02); every pre-fix pysam defect here is gone",
         prompt="Count the alleles and alt fraction at synA:100 (planted SNP) and at real chr22 positions with pysam, make a per-position pileup text, and list positions with >10% alternative alleles.",
         assertions=[
             A("allele_counts / allele_frequency / find_variants recover the planted SNP (T30/C10, 25%), report ref-skips as nothing (was DEL 3) and equal a mpileup -B parse at 110 real positions", True, "find_variants on real chr22 == independent parse (4 sites)"),
             A("Module snippets print what they claim: 'Basic Pileup' only the 10 requested columns, refskip vs deletion, quality-filtered depth 4 at synA:725", True, "all equal mpileup -B -q20 -Q20"),
             A("pileup_text == samtools mpileup row-for-row (623 rows, default and -B and -q20 -Q20 -x -A) and hand counts +2AC x3 / +2ac x2, -3CGT x2 / -3cgt x2, '>><'", True, "was 5 columns, 31 wrong depths, no markers pre-fix"),
             A("examples/allele_counts.py: synA:100 -> T 30 / C 10; real chr22:3000 depth 781 == mpileup", True, "runs from the copy"),
             A("usage-guide dedup lost nothing an agent needs", False, "the read-name + strand print variant (query_name / is_reverse) was dropped; examples/allele_counts.py is not referenced from SKILL.md or the guide"),
         ]),
    dict(index=3, type="Edge", label="Exact symbol decoding, every silent default, max depth and the shipped example on hostile input (REGRESSION of pre-fix input 3)",
         basic=36, specialized=54, note=f"executed; {cnt[3][0]}/{cnt[3][1]} checks pass (t03)",
         prompt="Explain exactly how insertions, deletions, spliced reads, read starts/ends and soft clips appear in the pileup base column and which reads mpileup drops by default (flags, MAPQ, baseQ, overlaps, orphans, max depth); my amplicon library is 9000x deep. Then run the example script on unusual region strings.",
         assertions=[
             A("Symbol table (^], $, +2AC/+2ac, -3CGT/-3cgt, *, #, >/<, soft clips absent) matches planted truth; default BAQ hides the deletion (depth 8 -> 4)", True, "hand-derived counts"),
             A("Defaults table verified by behaviour: -Q 13 (4 vs 10), --ff default (10 vs 16), overlap 5 vs 10 with -x and both long forms, orphans 0 vs 4 with -A, bcftools --ns/-Q 1/-d 250, -a vs -aa", True, "and help text for -Q/-d/-q/--ff"),
             A("Max depth: samtools 8000 cap, -d 0 unlimited, bcftools 250 vs -d 0/100000/1000000 = 9000, pysam default 8000 and max_depth=0 NOT unlimited; all 8 cheat-sheet rows run without capping", True, "9000x BAM"),
             A("Common Errors/BAQ statements: no -f -> N (rc 0), bcftools refuses, -B with -E rejected, samtools mpileup -g removed", True, "real messages"),
             A("Shipped example on 9 hostile inputs (range, no colon, pos 0, unknown contig, unindexed, garbage/nonexistent file, letters, empty) exits 1 with a last line 'Error: ...' and no traceback; commas and pos beyond contig end handled", True, "was raw ValueError tracebacks"),
         ]),
    dict(index=4, type="Variant B", label="bcftools mpileup | call: germline, BCF intermediate, multi-sample -d 100000, parallel-by-contig, the 'WRONG' pipe (REGRESSION of pre-fix input 4)",
         basic=35, specialized=54, note=f"executed; {cnt[4][0]}/{cnt[4][1]} checks pass (t04); bash blocks extracted verbatim from SKILL.md",
         prompt="Call variants from my BAM with the modern bcftools mpileup | bcftools call pipeline (single sample, BCF intermediate, joint calling of 2 samples, parallel per chromosome) and tell me if `samtools mpileup | bcftools call` is really wrong and why.",
         assertions=[
             A("Germline, BCF-intermediate and multi-sample blocks reproduce planted truth: SNP 100 AD 30,10 DP 40, AA>AACA, TCGT>T, per-sample AD 17,3 | 8,12", True, "verbatim blocks"),
             A("Multi-sample -d 100000 example is safe and the note is true: no memory warning at 2 samples/-d 100000, warning at -d 1000000 x 2 samples and at 11 files x 100000; none for one sample", True, "bcftools 1.24 prints 'Potential memory hog'"),
             A("The 'WRONG' pipe explanation is now correct: text pileup is not VCF/BCF, real error text 'Failed to read from standard input: unknown file type', exit 255", True, "no 'double cap' rationale left"),
             A("Parallel-by-Contig block: header contig order chr1..chr11 (not glob order), index built, missing reference / bad contig -> non-zero and no all.vcf.gz", True, "was chr1,chr10,chr11,chr2,... with exit 0"),
             A("Real chr22 slice: every strong (>=30% alt, >=10 reads) site of an independent mpileup parse is called; --max-BQ 30 is the ont preset value", True, "sites 3266, 3413"),
         ]),
    dict(index=5, type="Stress", label="Library cheat sheet on real ARTIC, spliced RNA-seq and 1000G BAMs; reference mismatch and index errors (REGRESSION of pre-fix input 5)",
         basic=35, specialized=53, note=f"executed; {cnt[5][0]}/{cnt[5][1]} checks pass (t05); real data only",
         prompt="Apply the library-typed flag cheat-sheet to my ARTIC SARS-CoV-2 nanopore amplicon BAM (consensus needs zero-coverage rows), an RNA-seq BAM and a 1000G germline BAM, and tell me what happens when the reference does not match the BAM.",
         assertions=[
             A("All 8 cheat-sheet rows (read from the SKILL.md table) run; no row uses -d 250; bcftools ONT variant accepted", True, "exome row now -d 0"),
             A("ARTIC: 29903 rows, depth (minus '*') == pysam count at every position, -a == -aa for one contig, 77 zero-depth rows vanish without -a", True, "0 differ"),
             A("RNA-seq: allele_counts at the 40 positions with most ref-skips == mpileup parse; chr22:25548 gives {'G': 5} (was DEL 54)", True, "no false DEL"),
             A("1000G: all-filters-off depth == pysam count; default --ff drops the 101 pre-flagged duplicates (sum 948889 vs 959299)", True, ""),
             A("Reference mismatch and index errors match the fixed Common Errors table: '[E::faidx_adjust_position] ... not found' with exit 0 and N rows, contig pre-check works, no -f, '[E::idx_find_and_load] Could not retrieve index file', empty region", True, "real message texts"),
         ]),
    dict(index=6, type="Variant B", label="NEW: re-auditor's planted-truth BAM (11 event types, soft-masked/N reference, colon contig) + 1,862-read randomized differential test of pileup_text",
         basic=33, specialized=49, note=f"executed; {cnt[6][0]}/{cnt[6][1]} checks pass (t06). Two real defects found: pileup_text drops the 2nd marker of adjacent I/D, find_variants reports N artifacts",
         prompt="Here is a BAM with a reverse-strand deletion, two insertions in one read, MAPQ 19/20/21 and 255 reads, base qualities 12/13/14/93, overlapping mates that disagree, N in the reference and in reads, a soft-masked reference, duplicate/supplementary/orphan flags, clips, a deletion before a ref-skip and a contig named HLA-A*01:01:01:01: give me the pileup rows, allele counts and variants.",
         assertions=[
             A("Planted events match hand truth: -2CC/-2cc, +3ACG/+1T/+2GG, -q 20 boundary (9 of 14), -Q 13 boundary (12 of 15), '^~' cap, overlap 6 vs 12, N ref/read, lower-case reference col3, flags 10/14/12/16, clips, refskip; colon contig works in samtools and pysam", True, "all E1-E11 checks pass"),
             A("pileup_text == samtools mpileup row-for-row on 1,862 random reads (mixed-case reference with N, S/H/I/D/N CIGARs, MAPQ 0-255, Q2-93, overlapping mates, odd flags): 13 option combinations x 4,486 rows", True, "0 differing rows; also equal on the planted BAM apart from one row"),
             A("pileup_text prints the same row as mpileup where an insertion is directly followed by a deletion (10M2I2D10M)", False, "mpileup '+2ca-2at', pileup_text '+2ca'; ~5% of rows differ in exotic-CIGAR fuzz, all indel-marker-only"),
             A("find_variants reports only real SNVs on the planted data", False, "also reports nA:790 G>N (1/7) and the reference-N site nA:800 N>A (9/9)"),
             A("allele_counts, find_variants and examples/allele_counts.py give exact truth on the colon-named contig and the soft-masked block (G6/A4, G5/A3, 3/8 alt, 3 of 6 at the overlap site)", True, "min_base_quality boundary equals -Q"),
         ]),
    dict(index=7, type="Stress", label="NEW: pysam-vs-samtools parameter table re-tested on 4 real + 2 synthetic BAMs, 432,147 real pileup_text rows, stepper/BAQ/flag/BQ-tag probes, usage-guide token diff",
         basic=31, specialized=46, note=f"executed; {cnt[7][0]}/{cnt[7][1]} checks pass (t07). Two documented claims are false (stepper='all'+fastafile; bcftools --nu == samtools --rf)",
         prompt="I want to replace samtools mpileup with pysam. For every option in the Skill's table, show that pysam gives identical depth and rows on my real DNA, RNA-seq, 1000G and ARTIC BAMs, and check the claims about steppers, flag filters and BAQ.",
         assertions=[
             A("12 Skill-table rows: pysam len(pileups) == samtools mpileup depth at every position on human DNA, RNA-seq, 1000G, ARTIC, syn.bam and new.bam (max_depth passed explicitly)", True, "72/72 row x BAM comparisons equal"),
             A("pileup_text == samtools mpileup row-for-row on 432,147 real rows (default, -B, -q20 -Q20 -x -A, --ff 0 -Q 0)", True, "0 differing rows"),
             A("nofilter vs --ff 0 (16 vs 12), flag_filter=0 == --ff 0, flag_require == --rf (16/17/3/2049), existing BQ tag reused by default (35) and ignored by -E/-B (40) / redo_baq", True, "all as documented"),
             A("'stepper=all + fastafile does not apply BAQ' (pysam table and text)", False, "BAQ IS applied: depth 4 at synA:250 (== mpileup default), 8 only with compute_baq=False"),
             A("Table row '--rf FLAGS (bcftools --nu)': both keep the same reads", False, "mask 65: samtools --rf keeps 6 reads (any bit), bcftools --nu keeps 2 (all bits required)"),
         ]),
]
for it in inputs:
    it["total"] = it["basic"] + it["specialized"]
    it["assertions_total"] = len(it["assertions"])
    it["assertions_passed"] = sum(1 for a in it["assertions"] if a["result"] == "PASS")
    assert 3 <= len(it["assertions"]) <= 5
    it["status"] = "COMPLETED"
    it["status_flag"] = "✅" if it["total"] >= 75 else "⚠️"

static = {
    "functional_suitability": (9, 12, "Completeness 3: text pileup, region/BED, multi-BAM, filters, defaults table, BAQ, bcftools calling/joint/parallel, pysam helpers all present and verified; indel allele counting deliberately out of scope (stated). Correctness 3: every checked command, default and message reproduced, but three statements are wrong (stepper='all'+fastafile BAQ, --nu == --rf, pileup_text on adjacent I/D). Appropriateness 3: a 40-line Python pileup_text re-implements a tool that is one shell command."),
    "reliability": (10, 12, "Fault tolerance 3 and error reporting 3: Common Errors quote real messages and the exit-0-with-N trap plus a contig pre-check; the shipped example rejects 9 hostile inputs with one 'Error:' line (a missing file also prints an htslib line first); the parallel block stops on failure. Recoverability 4: read-only, idempotent, safe to re-run."),
    "performance_context": (6, 8, "Token cost 3: SKILL.md grew to 446 lines (was 375) but the guide fell from 258 to 46 lines and the duplicated recipes are gone; no references/ split. Execution efficiency 3: linear workflows, one long helper (pileup_text)."),
    "agent_usability": (14, 16, "Learnability 3, consistency 4 (0/1-based rule and 'depth = len(pileups)' stated and used everywhere), feedback design 3 (formats, message texts and example rows given; no expected-output self-check for the pipelines), error prevention 4 (max depth, BAQ, -Q 13, default flags, ref mismatch exit 0, max_depth=0, concat order, memory hog all called out and verified)."),
    "human_usability": (6, 8, "Discoverability 3: description unchanged and terse (no mention of text pileup/depth/BAQ). Forgiveness 3: example accepts commas and colon contigs and rejects ranges/typos with a one-line message."),
    "security": (11, 12, "No credentials, no eval/exec, no shell built from user strings in the example; helpers take paths only. Input validation 3: shell blocks assume trusted file names."),
    "maintainability": (9, 12, "Modularity 3 (one SKILL.md holds everything, guide is thin), modifiability 3, testability 3 (real example rows and message texts to check against; still one example and no test script)."),
    "agent_specific": (16, 20, "Trigger precision 3, progressive disclosure 3 (446 lines, under 500, no references/), composability 3 (Related Skills all exist), idempotency 4, escape hatches 3 (tool table sends somatic/WGS production/long-read work elsewhere)."),
}
subtotal = sum(v[0] for v in static.values())
exe = round(sum(i["total"] for i in inputs) / len(inputs), 1)
sw, dw = round(subtotal * 0.4, 1), round(exe * 0.6, 1)
score = round(sw + dw)
L1 = sum(i["basic"] for i in inputs) / len(inputs); L2 = sum(i["specialized"] for i in inputs) / len(inputs)
ap = sum(i["assertions_passed"] for i in inputs); at = sum(i["assertions_total"] for i in inputs)
print("static", subtotal, "exec", exe, "sw", sw, "dw", dw, "score", score, "L1", round(L1, 1), "L2", round(L2, 1), "assert", ap, at)
grade, sym = ("Production Ready", "⭐") if score >= 85 else ("Limited Release", "✅") if score >= 75 else ("Beta Only", "⚠️") if score >= 60 else ("Reject", "❌")

recs = [
    dict(priority="P1", title="False claim: pysam stepper='all' + fastafile applies no BAQ", observed_in=[1, 7],
         problem="SKILL.md says the default stepper='all' does not apply BAQ even with a fastafile. In pysam 0.24.1 it does: depth equals samtools mpileup default (BAQ on) at all 1157 real positions, differs from -B at 40, and is 4 vs 8 at the planted deletion; only compute_baq=False restores -B.",
         root_cause="The fixer verified stepper='samtools'+fastafile and the no-fastafile default, but never the combination it asserted a negative about.",
         fix="Replace the sentence with: passing fastafile enables BAQ with either stepper ('all' or 'samtools'); use compute_baq=False (or omit fastafile) to match `-B`. Keep the table row `-f ref.fa` -> fastafile=..., and drop the stepper='samtools' requirement or say it is optional."),
    dict(priority="P2", title="Options table equates bcftools --nu with samtools --rf", observed_in=[7],
         problem="Row '--rf FLAGS (bcftools --nu): keep only reads with any of these flags set' is wrong for bcftools: --nu skips reads with ANY bit unset, i.e. needs ALL bits. Mask 65 keeps 6 reads in samtools --rf and 2 in bcftools --nu.",
         root_cause="Names were paired by position in the two help texts, not by behaviour.",
         fix="Give bcftools its own wording ('--nu: skip reads missing any listed bit = require all bits') or restrict the row to single-bit masks."),
    dict(priority="P2", title="pileup_text drops a second indel marker next to another indel", observed_in=[6],
         problem="For a read whose CIGAR has an insertion directly before a deletion (10M2I2D10M) or a deletion before an insertion, samtools prints '+2ca-2at' and pileup_text prints '+2ca'. Equal on 4,486 clean-CIGAR fuzz rows x 13 option sets and 432,147 real rows; ~5% of exotic-CIGAR fuzz rows differ, all indel-marker only.",
         root_cause="pysam exposes one indel value per pileup read; the helper cannot see the adjacent second event.",
         fix="Add to the docstring: 'CIGARs with adjacent I/D ops lose the second marker; use samtools mpileup for exact text.'"),
    dict(priority="P2", title="find_variants reports N artifacts", observed_in=[6],
         problem="On the planted N sites it returns nA:800 ref N > A (9/9) and nA:790 G>N (1/7) as variants (min_base_quality default 20 keeps the Q40 N read).",
         root_cause="No skip for reference N or read-base N.",
         fix="Skip columns where ref_base == 'N' and alleles equal to 'N' (one condition each)."),
    dict(priority="P2", title="Dedup dropped read-name/strand access; example not referenced", observed_in=[2, 7],
         problem="The old 'Access Individual Reads' variant printed alignment.query_name and strand; SKILL.md keeps only base+quality, so 'which reads carry the alt allele' has no snippet. examples/allele_counts.py is mentioned nowhere in SKILL.md or the guide.",
         root_cause="Dedup removed the only snippet showing read-level attributes and never linked the shipped example.",
         fix="Add one line to the Access Reads snippet printing pileup_read.alignment.query_name and is_reverse, and one sentence pointing to examples/allele_counts.py."),
    dict(priority="P2", title="Soft-masked FASTA prints lower-case reference bases", observed_in=[6],
         problem="With a soft-masked reference (UCSC-style hg38.fa) samtools mpileup column 3 is lower-case ('g'); the Output Format table says only 'Reference base'. pileup_text reproduces it, allele helpers upper-case.",
         root_cause="Real-data case not in the Skill's examples.",
         fix="Add '(lower-case where the FASTA is soft-masked)' to column 3."),
]

report = {
    "meta": {"skill_name": "bio-pileup-generation", "description": DESC, "evaluated_on": "2026-09-20", "evaluator_version": "skill-auditor@1.0",
             "category": "Data Analysis", "execution_mode": "D", "complexity": "Moderate", "n_inputs": 7,
             "source": SRC, "audit_type": "re-audit of a fixed Skill (pre-fix 71, Beta Only); auditor differs from first auditor and fixer",
             "executed": f"7/7 inputs executed; {tot_p}/{tot_n} scripted checks pass",
             "execution_note": "WSL science, env alignment-files: samtools 1.24, bcftools 1.24, pysam 0.24.1 (TOOLS.md). Skill copied from worktree F:\\OpenScience\\wt\\af-pileup (commit ad9b5a4) to run/skill; Python and bash blocks extracted verbatim from the copied SKILL.md; the worktree and external clone were never written (no __pycache__). Inputs 1-5 re-run the archived pre-fix inputs as regression tests (pre-fix generator re-used unchanged for data/syn, deep, multi, s1, s2); inputs 6-7 are new: own synthetic BAM (data/new.*, hand-derived truth), two random-read BAMs (fz_clean, fz_exotic), real human/RNA/1000G/ARTIC BAMs. Complexity Moderate (5 regression inputs) plus 2 new inputs = 7."},
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {"applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "No fabricated DOIs, results or numbers. Every number in the Skill's examples that was checked (1087/1157, 1000G example rows, depth 8->4, memory-hog thresholds) reproduced; the one unsourced '~30% slower' claim was removed."},
            "practice_boundaries": {"result": "PASS", "detail": "No diagnosis or prescription; somatic, WGS production and long-read work are routed to dedicated callers."},
            "methodological_ground": {"result": "PASS", "detail": "No principled fallacy. Three statements are wrong in detail (stepper='all'+fastafile BAQ, bcftools --nu vs samtools --rf, pileup_text on adjacent indels) and are listed as P1/P2; none inverts a conclusion of the recommended workflows."},
            "code_usability": {"result": "PASS", "detail": "All Python helpers, the shipped example and every bash block ran on real and synthetic data (7/7 inputs executed); helpers equal samtools mpileup row-for-row on 432,147 real rows and 4,486 random rows x 13 option sets."}}},
    "static_score": {"subtotal": subtotal, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in static.items()}},
    "dynamic_score": {"execution_avg": exe, "max": 100, "assertion_pass_rate": {"passed": ap, "total": at},
                      "inputs": [{k: it[k] for k in ("index", "type", "label", "status", "status_flag", "note", "basic", "specialized", "total", "assertions_passed", "assertions_total", "assertions")} for it in inputs]},
    "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": grade, "grade_symbol": sym, "deployable": True, "veto_override": False},
    "key_strengths": [
        "Every pre-fix defect is gone and verified by output: pileup_text now equals samtools mpileup row-for-row (0 differing rows on 432,147 real rows and 4,486 random rows x 13 option sets), ref-skips no longer counted as deletions, the parallel block keeps header contig order and stops on failure.",
        "The pysam-to-mpileup parameter table holds position by position for 12 options on 4 real and 2 synthetic BAMs, including max_depth=0 not being unlimited, flag_filter/nofilter and the BQ-tag rules.",
        "Defaults that silently change results are documented and true: -Q 13/1, excluded flags, depth-0 rows, BAQ hiding a deletion, exit status 0 on a reference mismatch, memory warning at -d 1000000 with 2 samples.",
        "usage-guide.md is now 46 lines and SKILL.md keeps one copy of each recipe; the shipped example turns nine hostile inputs into one-line errors.",
    ],
    "recommendations": recs,
}
assert sum(v["score"] for v in report["static_score"]["categories"].values()) == subtotal
for it in report["dynamic_score"]["inputs"]:
    assert it["basic"] + it["specialized"] == it["total"] and it["assertions_passed"] == sum(1 for a in it["assertions"] if a["result"] == "PASS")
json.dump(report, open(f"{OUT}/eval_report_bio-pileup-generation_result.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)

# ------------- viewer -------------
def excerpt(i, pat=None, maxn=60, w=300):
    lines = open(f"{RUN}/log_t0{i}.txt", encoding="utf-8", errors="replace").read().splitlines()
    keep = [l[:w] for l in lines if l.startswith(("[PASS]", "[FAIL]", "SUMMARY", "total rows")) or (pat and re.search(pat, l))]
    if len(keep) > maxn:
        fails = [l for l in keep if l.startswith("[FAIL]")]
        keep = keep[: maxn - len(fails) - 1] + ["... (trimmed; full log in run/log_t0%d.txt)" % i] + fails
    return "\n".join(keep)

md = []
md.append(f"# Eval Viewer — bio-pileup-generation (RE-AUDIT)\n\nGenerated: 2026-09-20 | Re-auditor: fresh Sonnet (different from first auditor and fixer) | Source: `{SRC}`\n")
md.append("Env: WSL `science`, env `alignment-files` (samtools 1.24, bcftools 1.24, pysam 0.24.1). The Skill folder was copied from worktree `wt\\af-pileup` (commit ad9b5a4) to `run/skill/` (md5 identical to the worktree files) and run from the copy; the worktree was not written.\n")
md.append(f"## Result\n\n**Pre-fix 71 (Beta Only, not deployable) -> now {score}/100, {sym} {grade}, deployable: true, veto: none, executed 7/7 inputs, scripted checks {tot_p}/{tot_n}, assertions {ap}/{at}.** Static {subtotal}/100 (x0.4 = {sw}); execution average {exe}/100 (x0.6 = {dw}); Layer 1 avg {L1:.1f}/40, Layer 2 avg {L2:.1f}/60. No open P0. One open P1, five P2. Floors for Limited Release met (static >= 70, exec >= 75, L1 >= 28, L2 >= 42, assertions {ap}/{at} = {100 * ap / at:.0f}% >= 80%); the Production Ready floor for assertions (90%) is not met and the score is 84.\n")
md.append("Skill Veto: T1 PASS, T2 PASS, T3 PASS (all outputs deterministic on repeat), T4 PASS. Research Veto (Data Analysis): M1-M4 PASS.\n")
md.append("**Classification:** Data Analysis (3), mode D, Moderate. N = 7: inputs 1-5 are the archived pre-fix inputs re-run as regression tests; inputs 6-7 are new and use planted truth and data the fixer never saw.\n")
md.append("## What broke or was left (only my runs count as evidence)\n")
for r in recs:
    md.append(f"- **[{r['priority']}] {r['title']}** (inputs {r['observed_in']}): {r['problem']}")
md.append("\nI found no regression of anything that worked before the fix: the five re-run pre-fix inputs (t01-t05) pass 145 of 146 scripted checks; the one failure is the P1 above.\n")
md.append("## Static scores (25 criteria)\n\n| Category | Score | Note |\n|---|---|---|")
for k, v in static.items():
    md.append(f"| {k} | {v[0]}/{v[1]} | {v[2]} |")
md.append(f"\n**Static subtotal: {subtotal}/100** (pre-fix 69)\n")
md.append("## Summary table\n\n| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Checks | Executed | Status |\n|---|---|---|---|---|---|---|---|---|")
for it in inputs:
    i = it["index"]
    md.append(f"| {i} | {it['type']} | {it['basic']} | {it['specialized']} | {it['total']} | {it['assertions_passed']}/{it['assertions_total']} | {cnt[i][0]}/{cnt[i][1]} | yes | {it['status_flag']} |")
md.append(f"\n**Execution Average: {exe} / 100** | **Assertion Pass Rate: {ap}/{at}**\n")
scripts = {1: "t01_regress_real_mpileup.py", 2: "t02_regress_pysam_helpers.py", 3: "t03_regress_edge_defaults.py", 4: "t04_regress_bcftools.py", 5: "t05_regress_library_real.py", 6: "01_make_new_data.py, 02_make_fuzz.py, t06_new_planted_and_fuzz.py, x_probe_exotic_other.py", 7: "t07_new_real_matrix.py"}
md.append("## Detailed inputs\n")
for it in inputs:
    i = it["index"]
    md.append(f"### Input {i} — {it['type']}: {it['label']}\n\n**Prompt:** {it['prompt']}\n\n**Executed:** true. {it['note']}.\n\n**Code that ran:** `run/{scripts[i]}` (Skill code loaded verbatim from `run/skill/`).\n")
    pat = {6: r"^\s+\[info\]|find_variants E5|E10 row|with min_base", 7: r"^\s+stepper|^depth at|^mpileup:|BQ-tag|^tokens|^old prompts|^positions where|^nA:1120", 1: r"^symbols|^flag dist", 3: r"help text", 5: r"^40 positions|^top ref|^cheat"}.get(i)
    md.append("**Output (trimmed; PASS/FAIL lines are the scripted checks the scores depend on):**\n\n```text\n" + excerpt(i, pat, maxn=70 if i in (3, 6) else 45) + "\n```\n")
    md.append(f"**Scores:** Basic {it['basic']}/40 | Specialized {it['specialized']}/60 | Total {it['total']}/100\n\n**Assertions:**")
    for a in it["assertions"]:
        md.append(f"- [{a['result']}] {a['text']} — {a['note']}")
    md.append("")
md.append("## Notes on method\n\n- Independent second methods: `samtools depth -a -J`, pysam record walks (`get_aligned_pairs`), a separate decoder of the mpileup base column, `bcftools mpileup` DP, hand-derived counts from the generator designs (`01_make_new_data.py`, `00_make_data.py`), and tool help text.\n- `x_probe_exotic_other.py` shows the only 4 exotic-fuzz rows that were not caught by the automatic 'indel-marker-only' classification: all are indel markers adjacent to a ref-skip.\n- Env traps honoured: no bare Rscript, WSL only via `.sh`/`bash -lc`, public-data never written (BAMs copied to `run/work`, deleted afterwards), no symlinks, no `__pycache__`.\n- Data generated for this audit lives in `run/data/` (all synthetic: `00_make_data.py` regression data re-used unchanged from the pre-fix audit; `01_make_new_data.py` and `02_make_fuzz.py` are new).\n")
open(f"{OUT}/eval_viewer_bio-pileup-generation.md", "w", encoding="utf-8").write("\n".join(md))
print("written")
