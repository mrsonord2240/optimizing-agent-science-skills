#!/usr/bin/env python
"""Builds eval_report_bio-alignment-sorting_result.json from the scores decided after reading the run logs
(run/log_in0*.txt) and validates the schema pre-emit checklist. Windows or WSL python, stdlib only."""
import json, os, sys

OUT = r"F:\OpenScience\audits\bio-alignment-sorting\eval_report_bio-alignment-sorting_result.json"
if not os.path.isdir(os.path.dirname(OUT)):
    OUT = "/mnt/openscience/audits/bio-alignment-sorting/eval_report_bio-alignment-sorting_result.json"

def A(text, result, note):
    return {"text": text, "result": result, "note": note}

inputs = [
 dict(index=1, type="Canonical", label="Coordinate-sort an unsorted real BAM, verify order, index it (CLI, pysam, flags, CRAM)",
  status="COMPLETED", status_flag="✅",
  executed=True,
  execution_note="in01_coordinate.sh ran end to end in WSL (samtools 1.24, pysam 0.24.1) on record-shuffled copies of real nf-core human PE BAM (5644 rec), real 1000G chr20 BAM (9601 rec, GRCh38 header with alts) and the real UMI BAM that has no @HD; 15/15 checked assertions passed in log_in01.txt.",
  note="All documented sort commands and flags reproduced the ground truth (SO:coordinate, independent (tid,pos) check, record multiset identical, idxstats 5642/2); only gap: no explicit post-sort integrity check beyond the header.",
  basic=35, specialized=53,
  assertions=[
   A("Sorted output header says SO:coordinate and an independent pysam (tid,pos) walk confirms coordinate order on real 5644-record and 9601-record multi-contig BAMs", "PASS", "order_check.py coordinate_sorted=True on sorted.bam and s1000.bam; unmapped reads last"),
   A("Sorting preserves the record multiset and equals the original coordinate-sorted BAM's record set", "PASS", "recmd5 identical (1267f5d9a548) for input, output and the nf-core sorted original"),
   A("Sorted BAM indexes and idxstats matches known counts", "PASS", "samtools index ok; chr22 mapped 5642, unplaced * 2; 1000G and UMI BAM index too"),
   A("SKILL flag/API variants (-@ 8 -m 4G, -T prefix, -l 1, -O bam, -O cram --reference, pysam.sort with -@ -m -T) reproduce the default CLI result", "PASS", "record streams identical; CRAM read back with -T = 5644 records, @HD SO:coordinate; pysam.sort == CLI asserted in pysort.py"),
   A("Sort-order check helper copes with a real BAM that has no @HD line and re-sorts it", "PASS", "get_sort_order -> 'unknown'; ensure_coordinate_sorted sorts; raw unsorted UMI BAM cannot be indexed (E::hts_idx_push) until sorted"),
  ]),
 dict(index=2, type="Variant A", label="Name sort, fixmate/markdup workflow, collate, paired FASTQ extraction (planted-duplicate BAM + Picard cross-check)",
  status="COMPLETED", status_flag="⚠️",
  executed=True,
  execution_note="in02_namesort_dup.sh ran end to end in WSL with samtools 1.24 and Picard 3.5.0 on derived/planted_dups.bam (real reads, 50 planted pairs), the real human PE BAM and a synthetic multi-contig BAM with mixed-width names; log_in02.txt.",
  note="Every workflow gave the right answer (100 dup reads = Picard 50 pairs; real BAM 1656 = Picard 1656), but the Skill's description of `sort -n` as strict lexicographic is wrong for samtools 1.24 (natural order; -N is ASCII) and Picard rejects `-n` output.",
  basic=29, specialized=42,
  assertions=[
   A("The 4-command 'Re-sort by Name for Duplicate Marking' workflow flags exactly the planted duplicates", "PASS", "markdup -s: DUPLICATE PAIR 100; Picard READ_PAIR_DUPLICATES 50 (=100 reads); final SO:coordinate; indexes"),
   A("The collate|fixmate|sort|markdup pipeline (SKILL) and the usage-guide sort -n|fixmate|sort|markdup pipeline give the same result", "PASS", "both 100 dup reads; on the real human BAM samtools 1656 == Picard 1656"),
   A("SKILL statement that `sort -n` is a 'full lexicographic sort by QNAME / strict total order' is correct for the installed samtools", "FAIL", "samtools 1.24 -n is NATURAL (header SS:queryname:natural; read10 before read100 after read9); -N is ASCII and equals Picard's order; the Skill never mentions -N"),
   A("Name-sorted output produced by the Skill's own commands is accepted by a downstream name-order consumer (Picard)", "FAIL", "Picard MarkDuplicates on `samtools sort -n` output: IllegalArgumentException 'Alignments added out of order ... Sort order is queryname'; ValidateSamFile RECORD_OUT_OF_ORDER x3; works on `sort -N` (100 dups)"),
   A("collate -> fastq yields one R1 and one R2 record per pair, in identical name order, and collate keeps mates adjacent", "PASS", "250 R1 == 250 R2, names identical line by line; no QNAME split across blocks; header SO:unsorted GO:query; -o form without prefix works"),
  ]),
 dict(index=3, type="Edge", label="Tag sort (CB/RX), header-less and mislabelled BAM, sort-order verification, failure modes, memory spill",
  status="COMPLETED", status_flag="⚠️",
  executed=True,
  execution_note="in03_edge.sh ran end to end in WSL: synthetic 3-contig BAM (CB tags, unmapped pairs, cross-contig pair), the real UMI BAM (RX), real 1000G BAM, a header-liar BAM, truncated/junk/missing inputs, a killed sort and a 48k-record spill test; log_in03.txt.",
  note="sort -t and the awk check work, but the advice to trust @HD SO: as 'authoritative' is unsafe (ensure_coordinate_sorted returns a shuffled BAM unchanged) and the awk check cannot see contig-order violations; -m floor (1M) and unindexable tag-sorted output are not stated.",
  basic=29, specialized=42,
  assertions=[
   A("`samtools sort -t CB` orders by tag value and uses position as secondary key, on synthetic CB and real RX data", "PASS", "cbcheck.py asserted tag non-decreasing and position secondary; RX values non-decreasing (sort -c) on 15788 real records; header SO:unsorted SS:unsorted:CB:coordinate"),
   A("The Skill's advice ('trust the @HD SO: header') and its ensure_coordinate_sorted helper are safe when the header is wrong", "FAIL", "liar.bam (SO:coordinate, shuffled records): helper returns it unchanged, samtools index fails; only the awk check returns 1"),
   A("The awk sort-verification snippet returns 0 for sorted (incl. multi-contig real BAM) and 1 for unsorted BAMs", "PASS", "0 on good.bam and 1000G, 1 on shuffled and liar; but returns 0 on a chr2-before-chr1 file that order_check flags coordinate_sorted=False"),
   A("Failure modes are surfaced (missing input, non-BAM, truncated BAM, killed sort) with non-zero exit or detectably invalid output", "PASS", "rc=1 with clear messages; truncated input: 'samtools sort: truncated file. Aborting'; killed sort leaves 0-byte file, quickcheck rc=4"),
   A("Sort output is identical across -@ 0/4/8 and when spilling to temp files (-m 1M), and temp files are cleaned up", "PASS", "record streams identical; 14 temp files merged and removed. (Not documented: -m below 1M is rejected: '[bam_sort] -m setting (100K bytes) is less than the minimum required (1M)')"),
  ]),
 dict(index=4, type="Variant B", label="Merge per-lane BAMs: consistency check, -c -p, RG collisions, mismatched sort orders, -b/-f/-R, name-sorted merge, pysam.merge",
  status="COMPLETED", status_flag="✅",
  executed=True,
  execution_note="in04_merge.sh ran end to end in WSL on real human/planted BAMs (6144 merged records) plus synthetic RG-collision BAMs (rgcollide_A/B) and name-sorted variants; log_in04.txt.",
  note="Every stated merge claim held (silent malformed output for mismatched sort orders, -c/-p behaviour, RG-collision warning, addreplacerg remedy, pysam.merge); omissions: no -n/-N for name-sorted merge, -R needs indexed inputs.",
  basic=34, specialized=51,
  assertions=[
   A("The sort-consistency loop prints one line for a consistent set and more than one for a mixed set", "PASS", "1 line (SO:coordinate) vs 2 lines (SO:coordinate + SO:queryname SS:queryname:natural)"),
   A("`samtools merge -c -p -@ 8` yields all records, a single @RG, coordinate order and SO:coordinate", "PASS", "6144 = 5644+500; order_check coordinate_sorted=True; @RG 1; without -c the second file's reads become RG:Z:1-<hash>"),
   A("SKILL claim that merge does not validate sort order and silently produces a malformed output for mismatched inputs is accurate", "PASS", "coordinate + name-sorted inputs: rc 0, no warning, header still SO:coordinate, coordinate_sorted=False, index fails"),
   A("SKILL warning about RG-ID collisions is accurate and its remedy (addreplacerg before merge) works", "PASS", "-c collapsed two different RGs (sampleA/lane1, sampleB/lane7) into one, B reads relabelled to sampleA's L1; after addreplacerg two @RG survive and B reads carry L1B"),
   A("The merge section documents what is needed to merge name-sorted inputs and to use -R", "FAIL", "plain merge of two `sort -n` BAMs is not name-ordered (needs -n/-N, never mentioned); -R on unindexed inputs fails ('Could not retrieve index file'); -R shown without stating the index requirement"),
  ]),
 dict(index=5, type="Stress", label="Shipped examples/sort_pipeline.sh from a clean copy, downstream sort-order table verified with 8 real tools, performance claims measured",
  status="PARTIAL", status_flag="❌",
  executed=True,
  execution_note="in05a-d ran in WSL: the shipped example from a clean copy (PE and SE, real SARS-CoV-2 FASTQ, bwa 0.7.19), a PATH-shim simulated aligner crash, samtools index/markdup/fixmate, bcftools mpileup, GATK HaplotypeCaller and MarkDuplicatesSpark (4.6.2.0), Picard, umi_tools dedup, fgbio 4.1.1 GroupReadsByUmi, HTSeq, plus timing runs. Table rows for featureCounts, Salmon, RSEM, Sniffles, cuteSV, Manta, Delly and fgbio CallMolecularConsensusReads were NOT executed (tools not installed / no input).",
  note="Table rows that could be run all matched tool behaviour, but the example needs an undocumented `bwa index` step, exits 0 with a truncated BAM when the aligner dies mid-stream (no pipefail), and the collate '3-10x faster' and compression-table numbers did not reproduce.",
  basic=29, specialized=42,
  assertions=[
   A("The shipped example runs from a clean copy without undocumented prerequisites and produces a sorted, indexed, complete BAM", "FAIL", "after `bwa index` it works (PE 200 rec, SE 100 rec, SO:coordinate, flagstat 200 mapped == raw bwa count); before, it fails (fail to locate the index files) and neither SKILL.md, usage-guide.md nor the script header mention indexing"),
   A("The example propagates an aligner failure through its exit status", "FAIL", "PATH-shim bwa dying mid-stream (exit 3): script exits 0, prints Done, leaves a 57-of-100-read BAM; the same script with `set -eo pipefail` exits 3"),
   A("Rows of the 'Sort Order Required by Downstream Tool' table that can be run match the tools' real behaviour", "PASS", "index refuses name-sorted; markdup needs fixmate ms + coordinate; bcftools mpileup 'input is not sorted'; GATK HaplotypeCaller rejects unindexed name-sorted; umi_tools dedup needs index (15788->5689); fgbio GroupReadsByUmi identical 2823 MI groups for 4 orders; HTSeq -r name on coordinate-sorted double counts (5709 vs 2884). Wrong detail: HTSeq -p is --samout-format, not paired"),
   A("Quantitative performance claims (collate ~3-10x faster than sort -n; compression level table) reproduce", "FAIL", "192k-record BAM: sort -n 0.76 s vs collate 3.1 s (collate 4x slower); -l 9 wall +853% vs claimed +50-100%; -l 0 size +3819% (redundant data) vs +200-400%; unsourced"),
   A("Every file the SKILL.md / usage-guide.md points at exists", "PASS", "no primary file missing; Related Skills folders sam-bam-basics, alignment-indexing, duplicate-handling, alignment-filtering all exist; examples/sort_pipeline.sh present (unreferenced)"),
  ]),
]

for i in inputs:
    i["total"] = i["basic"] + i["specialized"]
    i["assertions_total"] = len(i["assertions"])
    i["assertions_passed"] = sum(1 for a in i["assertions"] if a["result"] == "PASS")

cats = {
 "functional_suitability": (9, 12, "Sort/collate/merge/tag/check/pysam/pipelines all covered and core commands are correct (verified); deductions: `sort -n` mislabelled lexicographic (Picard crash), -N and --template-coordinate absent, merge -n/-R gaps, HTSeq -p, unsourced performance numbers"),
 "reliability": (7, 12, "Common Errors table has 3 rows and the example checks argc, but no pipefail, no bwa-index step, no quickcheck/truncation guidance; recovery is 're-run from the original', which is sound because sort never modifies its input"),
 "performance_context": (5, 8, "SKILL.md 323 lines plus usage-guide 180 lines repeat nearly every command (context bloat); workflows themselves are linear, and using -u between piped stages is good advice"),
 "agent_usability": (11, 16, "Clear commands and a useful downstream-requirements table (learnability 3); terminology drifts (-T 'temporary directory' vs PREFIX, 'lexicographic' vs natural) (consistency 3); no explicit verification/confirmation output beyond @HD (feedback 2); many pitfalls flagged (RG collisions, merge sort-order, in-Python sorted()) but not -m floor, natural vs ASCII, unindexable outputs (error prevention 3)"),
 "human_usability": (6, 8, "Description matches how users ask ('sort my BAM', 'prepare for indexing/variant calling'), but merge/collate are not in the description (discoverability 3); documented alternatives (collate vs -n, pysam vs CLI) but no handling of headerless/mislabelled BAM (forgiveness 3)"),
 "security": (11, 12, "No credentials, nothing destructive, no eval/exec, temp files documented; the example quotes its variables but does not check that input files exist (input validation 3)"),
 "maintainability": (8, 12, "SKILL.md / usage-guide / one example is a clean split, but usage-guide duplicates SKILL.md commands so every change is made twice (modularity 3, modifiability 2); verification commands exist but no test inputs (testability 3)"),
 "agent_specific": (16, 20, "Trigger precise (3); SKILL.md under 500 lines but no references/ (3); Related Skills and the sort-order table are good integration points (4); re-sorting is idempotent, record stream unchanged, verified (4); no out-of-scope/hand-off guidance and 'trust the header' as an escape hatch is wrong for mislabelled files (2)"),
}
sub = sum(v[0] for v in cats.values())
static_categories = {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}
totals = [i["total"] for i in inputs]
exec_avg = round(sum(totals) / len(totals), 1)
sw = round(sub * 0.4, 1); dw = round(exec_avg * 0.6, 1)
score = int(round(sw + dw))
ap = sum(i["assertions_passed"] for i in inputs); at = sum(i["assertions_total"] for i in inputs)
l1 = sum(i["basic"] for i in inputs) / 5; l2 = sum(i["specialized"] for i in inputs) / 5
print("static", sub, "exec_avg", exec_avg, "weighted", sw, dw, "raw", sw + dw, "score", score, "assert", ap, at, round(100 * ap / at), "L1", l1, "L2", l2)

# floors for Limited Release (>=75): static>=70, exec>=75, L1>=28, L2>=42, assertions>=80%
floors = {"static>=70": sub >= 70, "exec>=75": exec_avg >= 75, "L1>=28": l1 >= 28, "L2>=42": l2 >= 42, "assert>=80%": ap / at >= 0.8}
print("floors", floors)
grade, sym = "Limited Release", "✅"
if not all(floors.values()):
    grade, sym = "Beta Only", "⚠️"   # one tier down
assert 75 <= score <= 84 and grade == "Beta Only"

report = {
 "source": "mrsonord2240/bioSkills@c206dff76d081a5126f8497fbabe10995c9b6026:alignment-files/alignment-sorting",
 "meta": {
  "skill_name": "bio-alignment-sorting",
  "description": "Sort alignment files by coordinate or read name using samtools and pysam. Use when preparing BAM files for indexing, variant calling, or paired-end analysis.",
  "evaluated_on": "2026-09-20",
  "evaluator_version": "skill-auditor@1.0",
  "category": "Data Analysis",
  "execution_mode": "B",
  "complexity": "Moderate",
  "n_inputs": 5,
  "executed": "5/5 inputs executed (input 5 partially: the downstream-table rows for Salmon, RSEM, Sniffles/cuteSV/Manta/Delly, featureCounts, Mutect2 and fgbio CallMolecularConsensusReads were not run)",
  "execution_note": "WSL science env alignment-files: samtools 1.24, pysam 0.24.1, bwa 0.7.19, bcftools 1.24, Picard 3.5.0, GATK 4.6.2.0, umi_tools 1.1.6, fgbio 4.1.1, HTSeq 2.1.2. Real data from public-data (nf-core human/sarscov2, 1000G HG00349 chr20 slice, planted-duplicate BAM built from real reads) plus labelled synthetic BAMs in run/data.",
  "skill_commit_note": "Skill content byte-identical between c206dff and staging HEAD 9193f86 (git diff empty); last touched by 558aea5."
 },
 "veto_gates": {
  "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
  "research_veto": {
   "applicable": True, "gate": "PASS",
   "scientific_integrity": {"result": "PASS", "detail": "No fabricated identifiers, results or statistics in any output; the Compression Level Decision and 'collate ~3-10x faster' figures are unsourced heuristics that did not reproduce (recorded as a P2, not fabrication of study data)."},
   "practice_boundaries": {"result": "PASS", "detail": "File-format utility; no diagnostic, prescriptive or individual-level clinical output in any of the 5 inputs."},
   "methodological_ground": {"result": "PASS", "detail": "The name-order description is a factual error that makes Picard reject the file loudly (recorded as P1), not a silently wrong analysis; the duplicate-marking workflows produced the ground-truth counts."},
   "code_usability": {"result": "PASS", "detail": "Every command, pipeline, pysam snippet and the shipped example executed and parsed (bash -n ok); the example needs an undocumented bwa index and fails loudly without it (P1)."}
  }
 },
 "static_score": {"subtotal": sub, "max": 100, "categories": static_categories},
 "dynamic_score": {
  "execution_avg": exec_avg, "max": 100,
  "assertion_pass_rate": {"passed": ap, "total": at},
  "inputs": inputs
 },
 "final": {
  "static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100,
  "grade": grade, "grade_symbol": sym,
  "deployable": False, "veto_override": False
 },
 "key_strengths": [
  "Every documented sort, merge, collate, pysam and pipe command reproduced ground truth on real data: coordinate/name orders, 100 planted duplicates (= Picard), real-BAM dup count equal to Picard (1656), merged 6144 records",
  "Sort-order consequences are explained with accurate warnings: merge does not validate sort order (confirmed silent malformed output), RG-ID collisions under -c (confirmed), do not sort() in Python, -u between piped stages",
  "The 'Sort Order Required by Downstream Tool' table held for every row that could be run (samtools index/fixmate/markdup, bcftools, GATK HaplotypeCaller, umi_tools, fgbio, HTSeq)",
  "Sorting is deterministic and idempotent: identical record streams across -@ 0/4/8, across spill-to-disk, and on re-sort; pysam.sort equals the CLI"
 ],
 "recommendations": [
  {"priority": "P1", "title": "`sort -n` described as lexicographic; it is natural order", "observed_in": [2, 5],
   "problem": "The collate-vs-sort table calls `sort -n` a 'full lexicographic sort / strict total order by QNAME' and advises it for tools needing true lexicographic order. In samtools 1.24 -n is natural order (SS:queryname:natural) and -N is ASCII; Picard MarkDuplicates crashes on `sort -n` output ('Alignments added out of order') and ValidateSamFile reports RECORD_OUT_OF_ORDER, while `sort -N` works.",
   "root_cause": "The table predates or ignores the -n/-N split and the Skill never mentions -N or the SS header tag.",
   "fix": "State that -n = natural, -N = ASCII/Picard-compatible; recommend -N (or Picard SortSam) whenever a Picard/GATK/htsjdk consumer reads the file; add SS: to the header-check section. Fix the RSEM/Salmon advice (they need mates adjacent, not lexicographic order) and give the same -n/-N note for merge."},
  {"priority": "P1", "title": "Shipped example needs an undocumented bwa index and masks aligner failure", "observed_in": [5],
   "problem": "From a clean copy the example fails ('fail to locate the index files') because nothing says to run `bwa index`; and with `set -e` but no pipefail a mid-stream aligner failure (simulated exit 3) still gives exit 0, 'Done' and a truncated BAM (57 of 100 reads). The same pattern appears in the SKILL's Python subprocess/shell=True snippet.",
   "root_cause": "The script assumes a prepared reference and reads only the last pipeline stage's exit status.",
   "fix": "Add `set -eo pipefail`, an index-exists check with a `bwa index` hint, an input-file existence check, and a final read-count sanity check (flagstat total vs FASTQ reads); use `set -o pipefail; ...` in the Python shell string."},
  {"priority": "P1", "title": "'Trust the @HD SO: header' is unsafe; verification is header-only", "observed_in": [3],
   "problem": "The Skill calls the header 'simpler and authoritative' and ensure_coordinate_sorted() returns a mislabelled (SO:coordinate but shuffled) BAM unchanged, which then fails to index; the awk check catches this but cannot see contig-order violations, and nothing recommends `samtools quickcheck` or an index attempt.",
   "root_cause": "Sort state is inferred from metadata rather than checked against the records.",
   "fix": "Make the awk/pysam record check the primary verification (or call `samtools index` as the test), keep the header as a fast hint only, add `samtools quickcheck` after long sorts, and drop 'authoritative'."},
  {"priority": "P2", "title": "Merge section omissions", "observed_in": [4],
   "problem": "No -n/-N (or -t) for merging name- or tag-sorted inputs, so a plain merge silently yields non-name-ordered output; `-R` requires indexed inputs (fails otherwise); the 'Safe Merge' label sits on -c, which collapses distinct RGs that share an ID.",
   "root_cause": "Merge examples cover only the coordinate-sorted case.",
   "fix": "Add `merge -n/-N` and the -R index requirement, and rename the block 'Merge (dedup identical @RG/@PG)' with the RG-collision warning first."},
  {"priority": "P2", "title": "Unreproduced performance claims and small flag inaccuracies", "observed_in": [2, 3, 5],
   "problem": "'collate ~3-10x faster than sort -n' (measured: collate 4x slower on 192k reads), the compression table (-l 9 wall +853%, sizes far from claims) are unsourced; `-T` is labelled 'Temporary Directory' but is a PREFIX; `-m` below 1M is rejected and not stated; total memory is (threads+1) x -m, not threads x -m; the HTSeq row says '-p for paired' but -p is --samout-format.",
   "root_cause": "Numbers and flag semantics copied from general knowledge without checking against 1.19+.",
   "fix": "Remove or source the numeric claims (or mark them data-dependent), label -T as a prefix, add the -m 1M floor and the (threads+1) memory note, and correct the HTSeq/featureCounts parenthetical."},
  {"priority": "P2", "title": "Missing modern sort options that the Skill itself recommends", "observed_in": [3, 5],
   "problem": "fgbio GroupReadsByUmi is said to prefer template-coordinate order but no command is given (`samtools sort --template-coordinate` works); `--write-index` (sort + index in one pass) and the fact that -n/-N/-t outputs cannot be indexed are not mentioned.",
   "root_cause": "Section written around the classic coordinate/name/tag trio.",
   "fix": "Add a short template-coordinate and --write-index entry and a one-line 'cannot be indexed' note under name and tag sorts."},
  {"priority": "P2", "title": "SKILL.md and usage-guide.md duplicate each other", "observed_in": [],
   "problem": "Nearly every command, the fixmate/markdup workflow, collate FASTQ extraction and the pysam snippets appear in both files (503 lines together for a three-topic Skill), doubling maintenance and context cost.",
   "root_cause": "usage-guide.md restates SKILL.md instead of holding only prompts and troubleshooting.",
   "fix": "Keep commands only in SKILL.md; reduce usage-guide.md to example prompts, what-the-agent-does and troubleshooting."}
 ]
}

# ---- pre-emit checklist ----
assert len(report["dynamic_score"]["inputs"]) == 5
for i in inputs:
    assert 3 <= len(i["assertions"]) <= 5
    assert i["assertions_passed"] == sum(a["result"] == "PASS" for a in i["assertions"])
    assert i["basic"] + i["specialized"] == i["total"]
    assert 0 <= i["basic"] <= 40 and 0 <= i["specialized"] <= 60
assert sub == sum(c["score"] for c in static_categories.values())
for k, c in static_categories.items():
    assert 0 <= c["score"] <= c["max"] and c["note"]
assert len(static_categories) == 8
assert 2 <= len(report["key_strengths"]) <= 5
pr = [r["priority"] for r in report["recommendations"]]
assert pr == sorted(pr)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print("wrote", OUT)
