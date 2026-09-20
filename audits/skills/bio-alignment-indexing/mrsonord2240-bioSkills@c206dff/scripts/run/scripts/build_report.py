#!/usr/bin/env python3
"""Builds eval_report_bio-alignment-indexing_result.json from the scored audit data below and re-checks the schema's
pre-emit checklist. Run on Windows or WSL:  python build_report.py <audit_dir>"""
import json, sys, os

D = sys.argv[1] if len(sys.argv) > 1 else "."
SKILL = "bio-alignment-indexing"

static = {
    "functional_suitability": (8, 12, "Completeness 3, Correctness 2, Appropriateness 3. Covers BAI/CSI/CRAI, region fetch, idxstats, faidx, staleness, contig naming and errors, and the core commands all reproduce ground truth. But: the large-genome section is factually wrong in four places (BAI 'silently truncates', default CSI 'matches BAI 2^29', '-m 18 = 2^33', multi-Gbp contigs in BAM), '-L bed' is filed under index access though it full-scans, pysam idxstats on CRAM is silently 0, and the staleness snippet misbehaves for CSI-only BAMs."),
    "reliability": (8, 12, "Fault tolerance 3 (missing index, unsorted, wrong contig, stale index, >537 Mbp all addressed), error reporting 2 ('file is not sorted' and 'chromosome not found' do not appear in samtools 1.24 / pysam 0.24.1 output; the shipped example dies with raw ValueError tracebacks), recoverability 3 (re-index is byte-identical; remedies given; stale-CSI trap)."),
    "performance_context": (6, 8, "SKILL.md 312 lines plus a 190-line usage-guide.md that repeats most of it (index types, commands, pysam, idxstats); no references/. Workflow itself is minimal."),
    "agent_usability": (12, 16, "Learnability 3, consistency 3 (SKILL.md FastaFile.fetch('chr1',1000,2000) vs usage-guide (999,2000) vs faidx chr1:1000-2000; two different error strings for the same unsorted case), feedback 3 (idxstats output shown, cross-check given), error prevention 3 (contig naming, sort order, staleness, primary-only are called out; CRAM reference, -M and stale CSI are not)."),
    "human_usability": (5, 8, "Discoverability 3 (natural trigger; description omits idxstats/faidx which the body covers). Forgiveness 2: fetch_regions.py rejects region forms samtools accepts (thousands separators, bare contig, start-only, contig names containing ':') with raw tracebacks."),
    "security": (11, 12, "No credentials, no eval/exec, static shell snippets. The example's region parsing is int()-based and rejects rather than injects; it silently writes an index next to the input BAM (announced on stdout)."),
    "maintainability": (8, 12, "Modularity 3, modifiability 3, testability 2: one example script, no expected outputs or self-test; SKILL.md/usage-guide.md duplication means every fix must be made twice."),
    "agent_specific": (17, 20, "Trigger precision 3, progressive disclosure 3 (single file, no references), composability 4 (Related Skills section; all referenced sibling skill folders exist), idempotency 4 (re-running samtools index gives byte-identical .bai/.csi), escape hatches 3 (version-check note, troubleshooting; no explicit out-of-scope list)."),
}
subtotal = sum(v[0] for v in static.values())

def A(text, ok, note): return {"text": text, "result": "PASS" if ok else "FAIL", "note": note}

inputs = [
 dict(index=1, type="Canonical", label="Index a real 1000G BAM (BAI+CSI), region fetches, idxstats cross-check", status="COMPLETED", status_flag="✅",
  note="30/31 + 4/5 script checks pass. 53 regions x 6 methods (samtools BAI/CSI, pysam fetch/count BAI/CSI, full-scan truth) agree; bedtools agrees; idxstats sums equal a full scan. Only miss: is_indexed() ignores input.bai.",
  basic=36, specialized=55, executed=True,
  execution_note="Executed in WSL science (samtools 1.24, pysam 0.24.1, bedtools 2.31.1) on REAL data: 1000G HG00349 chr20 slice (9601 records) and nf-core human chr22 slice. Scripts: scripts/t1_canonical.py, t1b_snippets.py. Not executed: usage-guide prompt 'X/Y ratio for sex determination' (no code shipped; slice has only chr20).",
  assertions=[
   A("BAI and CSI indices are created and every region count equals the index-free full-scan ground truth", True, "53 regions, 6 methods, 0 mismatches; BAI/CSI bytes identical between samtools and pysam.index"),
   A("Shipped fetch_regions.py output equals samtools view for the same region (names, 1-based positions, strand)", True, "127 reads, identical lists; auto-indexes an unindexed BAM"),
   A("idxstats totals and the SKILL's unmapped cross-check hold against a full scan", True, "9563+38=9601 records; idxstats unmapped 38 == view -c -f 4 -F 2304"),
   A("The is_indexed() helper recognises every index location the SKILL itself lists (.bam.bai, .bai, .csi)", False, "returns False for alt.bam + alt.bai, which samtools loads fine"),
   A("Stays in scope: read-only on inputs (worked on copies), no destructive commands", True, "index files written beside copies only"),
  ]),
 dict(index=2, type="Variant A", label="Index a CRAM, fetch regions, idxstats, FASTA index", status="PARTIAL", status_flag="❌",
  note="samtools path works once -T is added (5642 == BAM; 6 sub-regions equal). SKILL pysam pattern fails 'OSError: truncated file'; pysam get_index_statistics on CRAM returns 0 mapped silently (samtools idxstats: 5642); shipped helpers do not handle CRAM.",
  basic=28, specialized=38, executed=True,
  execution_note="Executed on REAL nf-core human chr22 CRAM + FASTA. The CRAM's UR: header points to a path absent here, which is realistic for shared CRAMs; the SKILL never mentions the reference requirement for retrieval. Scripts: scripts/t2_cram_faidx.py, t2b_cram_probe.py.",
  assertions=[
   A("CRAM is indexed (.crai) and region counts equal the BAM counts of the same reads", True, "5642 == 5642; 6 sub-regions identical (with -T genome.fasta)"),
   A("The SKILL's pysam pattern (AlignmentFile(cram,'rb') + fetch/count) retrieves reads without further guidance", False, "OSError: truncated file (missing reference); the SKILL does not say CRAM retrieval needs a reference"),
   A("bam.get_index_statistics() on a CRAM matches samtools idxstats", False, "pysam returns ('chr22', 0, 0); samtools idxstats gives 5642; the usage-guide pct snippet then prints nothing meaningful, silently"),
   A("samtools faidx / pysam.FastaFile extraction equals an independent plain-Python FASTA parse", True, "chr22:1000-2000 = 1001 bp identical; usage-guide FastaFile.fetch(999,2000) identical; missing .fai auto-built"),
   A("Shipped helpers (is_indexed, fetch_regions.py) work on a .cram", False, "is_indexed False for a real .crai; example re-indexes on every call and then crashes"),
  ]),
 dict(index=3, type="Edge", label="Unsorted BAM, missing index, colon contig names, odd region strings", status="COMPLETED", status_flag="⚠️",
  note="Unsorted input fails cleanly and sort->index works (15788 records preserved), but two of the Common Errors strings do not exist in the tools' output, and fetch_regions.py crashes on colon contigs (HLA-A*01:01:01:01, the real UMI BAM's contig), thousands separators and bare contigs.",
  basic=30, specialized=42, executed=True,
  execution_note="Executed on REAL unsorted UMI BAM and human chr22 BAM plus SYNTHETIC hla_contig.bam and a header-only BAM. Script: scripts/t3_edge.py (21/26 checks pass; the 5 FAILs are documented mismatches).",
  assertions=[
   A("Unsorted BAM: index fails, no index written, and the SKILL's sort->index remedy works with no records lost", True, "'Unsorted positions on sequence #1', 'failed to create index'; sorted BAM idxstats 15787+1 = 15788"),
   A("Error strings in the Common Errors table / usage-guide match the installed tools' messages", False, "'file is not sorted' and 'file is not coordinate sorted' never appear; 'chromosome not found' is really 'specifies an invalid region or unknown reference. Continue anyway.' (rc 0) / pysam 'invalid contig'. 'random alignment retrieval...' and 'could not retrieve index file' do appear"),
   A("Missing-index and wrong-contig-name failures behave as the SKILL warns (loud or zero reads) and pysam raises", True, "pysam ValueError 'fetch called on bamfile without index' / 'invalid contig `22`'; samtools returns 0 with a warning"),
   A("Shipped fetch_regions.py accepts region strings that samtools accepts (colon contig names, thousands separators, bare contig)", False, "ValueError: too many values to unpack / invalid literal for int() '1,952' / not enough values to unpack"),
   A("Stays in scope, no destructive actions, header-only BAM handled", True, "empty BAM: index + idxstats 'chr22 40001 0 0'"),
  ]),
 dict(index=4, type="Variant B", label="Wheat-scale genome: contigs over 537 Mbp, CSI vs BAI, -m", status="COMPLETED", status_flag="⚠️",
  note="Advice to use CSI works and every query equals hand-computed truth, but the explanation is wrong: BAI fails loudly (not silently), default 'samtools index -c' already covers 2^32 (depth auto-raised to 6), '-m 18' yields depth 4 = 2^30 not 2^33, and contigs beyond 2^31-1 cannot be stored in BAM at all.",
  basic=31, specialized=43, executed=True,
  execution_note="Executed on SYNTHETIC BAMs (chr1A 594 Mbp, chr3B 830 Mbp, 2.0 Gbp contig, 3 Gbp SAM) with reads at known positions; CSI header parsed directly. Script: scripts/t4_large_genome.py (14/16 checks pass; both FAILs are the doc claims above).",
  assertions=[
   A("A CSI index is produced for >537 Mbp contigs and every region query equals the hand-computed truth (samtools and pysam)", True, "6 chr3B queries + chr1A read at 590 Mbp, default -c and -m 18, both 100% correct"),
   A("The claim 'BAI silently truncates reads on contigs >537 Mbp' is accurate", False, "samtools index refuses: 'cannot be stored in a bai index. Try using a csi index', no .bai written; pysam raises SamtoolsError"),
   A("The large-genome guidance ('default CSI = 2^29 so use larger -m'; '-m 18 = 2^33'; multi-Gbp genomes need CSI with larger -m) is accurate", False, "default -c stored min_shift=14 depth=6 (2^32) and works on 830 Mbp; -m 18 stored depth=4 (2^30); BAM cannot hold positions >2^31-1 ('Positional data is too large for BAM format')"),
   A("pysam.index('-c', file) builds a usable CSI as documented", True, "count at 830,000,000 == 1"),
   A("idxstats works on CSI-indexed BAMs", True, "chr1A 4 mapped, chr3B 5 mapped"),
  ]),
 dict(index=5, type="Stress", label="Stale/dual indices, -L vs -M, idxstats semantics, batch loop, threads", status="COMPLETED", status_flag="⚠️",
  note="Precedence note verified in both directions (htslib .csi first, GATK/htsjdk .bai first) and idxstats semantics verified. But the SKILL's own staleness snippet leaves a stale .csi winning over a fresh .bai; '-L bed' does not use the index (needs -M / --region-file); 'primary only' recipe counts placed unmapped reads; '-@' gave no measurable gain.",
  basic=30, specialized=42, executed=True,
  execution_note="Executed on REAL 1000G BAM and ARTIC nanopore BAM plus SYNTHETIC semantics.bam (hand-known flags) and a 1.2 M-read big.bam (damaged-tail test). Script: scripts/t5_stress.py (27/28 checks pass; the FAIL is the primary-only recipe).",
  assertions=[
   A("The SKILL's staleness snippet detects and repairs a stale .bai (count returns to truth)", True, "stale .bai warns 'index file is older than the data file' then errors 'Invalid BGZF header'; snippet re-index -> 1095 == truth"),
   A("The index-precedence note is correct (htslib: .csi first; htsjdk: .bai first)", True, "correct .csi + wrong .bai: samtools/pysam 1095 (truth), GATK 0 records; correct .bai + wrong .csi: samtools/pysam error, GATK 1095"),
   A("The staleness snippet and batch loop are safe for CSI-indexed BAMs", False, "'-nt' against the missing .bai is always true: builds a redundant .bai while the stale .csi still wins (samtools error, count not truth); batch loop also adds a redundant .bai"),
   A("'samtools view -L regions.bed', listed under 'Using Indices for Region Access', uses the index", False, "damaged-tail BAM: -L fails like a full scan (CRC error); -M -L and --region-file succeed == truth 1791; intact 1.2 M reads: -L 1.57 s vs -M -L 0.02 s"),
   A("idxstats/primary-only claims hold: mapped column includes secondary+supplementary; unmapped cross-check; primary-only recipe", True, "semantics.bam: chrA 7 mapped 1 unmapped, * 2; cross-check 3==3. Note: 'view -c -F 2304 file chrA' = 5 (includes the placed orphan), -F 2308 = 4"),
  ]),
]

for i in inputs:
    i["total"] = i["basic"] + i["specialized"]
    i["assertions_passed"] = sum(a["result"] == "PASS" for a in i["assertions"])
    i["assertions_total"] = len(i["assertions"])

exec_avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
ap = sum(i["assertions_passed"] for i in inputs); at = sum(i["assertions_total"] for i in inputs)
sw = round(subtotal * 0.4, 1); dw = round(exec_avg * 0.6, 1)
score = int(round(sw + dw))
l1 = sum(i["basic"] for i in inputs) / len(inputs); l2 = sum(i["specialized"] for i in inputs) / len(inputs)

# grade with floors (scoring_rubric.md s5): each unmet floor for the tier reached downgrades one tier
tiers = ["Reject", "Beta Only", "Limited Release", "Production Ready"]
sym = {"Production Ready": "⭐", "Limited Release": "✅", "Beta Only": "⚠️", "Reject": "❌"}
g = "Production Ready" if score >= 85 else "Limited Release" if score >= 75 else "Beta Only" if score >= 60 else "Reject"
floors = {"Production Ready": (80, 85, 32, 48, 0.90), "Limited Release": (70, 75, 28, 42, 0.80)}
unmet = []
if g in floors:
    fs, fe, f1, f2, fa = floors[g]
    for name, val, need in [("static", subtotal, fs), ("execution", exec_avg, fe), ("layer1", l1, f1), ("layer2", l2, f2), ("assertions", ap / at, fa)]:
        if val < need: unmet.append((name, val, need))
if unmet:
    g = tiers[tiers.index(g) - 1]
print("subtotal", subtotal, "exec_avg", exec_avg, "L1", l1, "L2", l2, "assert", ap, at, round(ap / at, 2), "raw score", score, "unmet floors", unmet, "grade", g)

recs = [
 dict(priority="P1", title="Staleness snippet and batch loop break for CSI-indexed BAMs", observed_in=[5],
  problem="'[ x.bam -nt x.bam.bai ]' is true whenever no .bai exists, so a CSI-only BAM gets a redundant .bai; if the BAM changed, the stale .csi still takes precedence (htslib prefers .csi, which the SKILL itself states) and region queries error or return wrong reads after the 'fix'. The usage-guide batch loop also only tests for .bai.",
  root_cause="Both snippets assume the index is always x.bam.bai.",
  fix="Test whichever index exists (.bai, .csi, .bai alternative) and its mtime; when re-indexing, delete every other index file for that BAM first (or index with -o/-c explicitly), and make the batch loop skip any BAM that has a fresh .bai or .csi."),
 dict(priority="P1", title="CRAM: no reference guidance; pysam idxstats silently 0; helpers ignore .crai", observed_in=[2],
  problem="Region retrieval from CRAM needs the reference (-T / reference_filename / REF_PATH); without it pysam raises 'OSError: truncated file' and samtools view prints no records. pysam get_index_statistics() on a CRAM returns 0 mapped while samtools idxstats returns the true counts. is_indexed() and fetch_regions.py only know .bai/.csi, so a CRAM is re-indexed on every call and then crashes.",
  root_cause="The CRAM section is three lines (samtools index x.cram) and the Python patterns were written for BAM only.",
  fix="Add a CRAM subsection: samtools view -T ref.fa, pysam AlignmentFile(f,'rb',reference_filename=ref), REF_PATH, and use `samtools idxstats` (not pysam) for CRAM counts. Make is_indexed/ensure_indexed check .crai and choose the mode automatically."),
 dict(priority="P1", title="Large-genome section is factually wrong in four places", observed_in=[4],
  problem="samtools index on a >537 Mbp contig fails loudly and writes no .bai (the table says 'silently truncates'); default `samtools index -c` already auto-raises the depth (min_shift 14, depth 6 = 2^32) so `-m 18` is not needed and actually gives depth 4 = 2^30, not the claimed 2^33; and contigs beyond 2^31-1 bp cannot be stored in BAM at all ('Positional data is too large for BAM format'), so the pine/axolotl 'multi-Gbp | CSI with larger -m' row is not achievable.",
  root_cause="CSI parameters were described from the format's theoretical limits rather than from htslib's behaviour.",
  fix="State: BAI hard-errors above 2^29; `samtools index -c` (default -m) works up to ~2^31; -m only sets the smallest bin size; contigs above 2^31-1 need the reference split before alignment. Delete the '2^(18+15)' comment and the silent-truncation row."),
 dict(priority="P1", title="'-L regions.bed' shown as index-based region access", observed_in=[5],
  problem="Under 'Using Indices for Region Access' and in the usage-guide, `samtools view -L regions.bed in.bam` is presented as index use. It is a full-file filter: on a damaged-tail BAM it fails like a full scan and on a 1.2 M-read BAM it took 1.57 s versus 0.02 s for `-M -L` / `--region-file`.",
  root_cause="samtools' -L (filter) versus -M (index + multi-region iterator) distinction is not documented in the Skill.",
  fix="Use `samtools view -M -L regions.bed in.bam` (or --region-file) for index-based BED access and add one line that plain -L scans the whole file."),
 dict(priority="P2", title="Common Errors strings do not match the installed tools", observed_in=[3],
  problem="'file is not sorted' (SKILL) and 'file is not coordinate sorted' (usage-guide) do not appear; samtools 1.24 prints 'Unsorted positions on sequence #1 ... failed to create index'. 'chromosome not found' is really 'specifies an invalid region or unknown reference. Continue anyway.' with exit 0, or pysam 'invalid contig'.",
  root_cause="Messages were written from memory, and the two files disagree.",
  fix="Quote the exact current messages, keep one table, and say that samtools returns 0 reads with rc 0 on an unknown contig."),
 dict(priority="P2", title="fetch_regions.py rejects region forms samtools accepts", observed_in=[3],
  problem="Raw ValueError tracebacks for 'chr22:1,952-4,700', 'chr22', 'chr22:1952-' and contig names containing ':' (HLA-A*01:01:01:01, the real UMI BAM's contig). Also no CRAM support and no staleness check.",
  root_cause="Region parsed with split(':') and int().",
  fix="Pass the region string to bam.fetch(region=...) (pysam parses it like samtools), or rsplit(':',1) with comma stripping and a clear error; check index freshness and CRAM."),
 dict(priority="P2", title="is_indexed() misses input.bai, .crai and gives sibling false positives", observed_in=[1, 2],
  problem="The helper returns False for alt.bam + alt.bai (a location the SKILL lists) and for a real .crai; for x.cram it looks for x.bam.bai, so a sibling x.bam.bai gives a false True.",
  root_cause="with_suffix('.bam.bai') is BAM-specific.",
  fix="Use pysam.AlignmentFile(path).has_index() or test the exact candidate list per format."),
 dict(priority="P2", title="usage-guide mito fraction awk hard-codes chrM", observed_in=[1],
  problem="`/^chrM/` reports 'MT: 0.00%' on an Ensembl-style BAM whose contig is 'MT' (true 33.33% in the test), the exact naming trap the SKILL warns about elsewhere; division by zero on an empty BAM. The 'X/Y ratio for sex determination' prompt has no code.",
  root_cause="Naming convention not handled in the snippet.",
  fix="Match /^(chr)?(M|MT)$/ and guard total==0; either add the X/Y snippet (normalised by contig length) or drop the prompt."),
 dict(priority="P2", title="'primary only' recipe, FASTA off-by-one, threads claim, duplication", observed_in=[2, 5],
  problem="`samtools view -c -F 2304 in.bam chr` also counts placed unmapped reads (5 vs 4 primary mapped in the test; use -F 2308). SKILL.md FastaFile.fetch('chr1',1000,2000) is 1000 bp while faidx chr1:1000-2000 and the usage-guide (999,2000) are 1001 bp. `-@ 8` gave no measurable speedup on a 43 MB BAM (1.61 s -> 1.58 s). SKILL.md and usage-guide.md duplicate most content.",
  root_cause="Unverified claims and copy-paste between the two files.",
  fix="Use -F 2308 for primary mapped, align the FASTA coordinates, soften or measure the threads claim, and cut the duplicated sections from usage-guide.md."),
]

report = {
 "source": "mrsonord2240/bioSkills@c206dff76d081a5126f8497fbabe10995c9b6026:alignment-files/alignment-indexing",
 "meta": {
  "skill_name": SKILL,
  "description": "Create and use BAI/CSI indices for BAM/CRAM files using samtools and pysam. Use when enabling random access to alignment files or fetching specific genomic regions.",
  "evaluated_on": "2026-09-20",
  "evaluator_version": "skill-auditor@1.0",
  "category": "Data Analysis",
  "execution_mode": "D",
  "complexity": "Moderate",
  "n_inputs": 5,
  "executed": "5/5",
  "environment": "WSL science env alignment-files: samtools 1.24, htslib 1.24, pysam 0.24.1, bedtools 2.31.1, GATK 4.6.2.0 (htsjdk 4.2.0); real data from audit-envs/alignment-files/public-data plus labelled synthetic data in run/data",
  "floors_note": "Score 75 maps to Limited Release, but the assertion-pass-rate floor (>=80%) is not met (15/25 = 60%), so the grade is downgraded one tier to Beta Only per scoring_rubric section 5."
 },
 "veto_gates": {
  "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
  "research_veto": {
   "applicable": True, "gate": "PASS",
   "scientific_integrity": {"result": "PASS", "detail": "No DOI/PMID, statistics or clinical claims are produced; every count in the Skill's examples was reproduced against independent ground truth."},
   "practice_boundaries": {"result": "PASS", "detail": "Indexing utility with no diagnostic content. The usage-guide prompt 'X/Y ratio for sex determination' is a data-QC use with no code or caveat shipped; nothing prescribes or diagnoses for an individual."},
   "methodological_ground": {"result": "PASS", "detail": "No methodological fallacy. Factual errors (large-genome CSI explanation, -L index claim) are recorded as P1 accuracy findings; the commands they accompany still return correct results."},
   "code_usability": {"result": "PASS", "detail": "All generated snippets and the shipped example run from a copy and returned ground-truth values on the documented forms (30/31, 4/5, 15/18, 21/26, 14/16, 27/28 script checks; every FAIL is a documented defect, not a syntax/import failure). fetch_regions.py crashes only on undocumented region forms."}
  }
 },
 "static_score": {"subtotal": subtotal, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in static.items()}},
 "dynamic_score": {
  "execution_avg": exec_avg, "max": 100,
  "assertion_pass_rate": {"passed": ap, "total": at},
  "inputs": inputs,
 },
 "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": g, "grade_symbol": sym[g],
           "deployable": g in ("Production Ready", "Limited Release"), "veto_override": False},
 "key_strengths": [
  "Core commands are correct and reproduce independent ground truth: 53 regions x 6 methods agree (samtools BAI/CSI, pysam fetch/count, full scan), bedtools agrees, idxstats sums equal a full scan, and re-indexing is byte-identical.",
  "The index-precedence note is right and non-obvious: htslib prefers .csi and htsjdk (GATK) prefers .bai, verified with deliberately wrong indices in both directions.",
  "idxstats caveats (mapped column includes secondary/supplementary, placed unmapped orphans sit in column 4, the unmapped cross-check) all hold on hand-built flags.",
  "Real production pitfalls are called out: contig-naming mismatch, sort-before-index, stale index, BAI 537 Mbp limit with the correct CSI remedy; all referenced sibling skills and the example exist.",
 ],
 "recommendations": recs,
}

# ---- pre-emit checklist -----------------------------------------------------------------------------------
assert report["static_score"]["subtotal"] == sum(c["score"] for c in report["static_score"]["categories"].values())
assert len(report["static_score"]["categories"]) == 8 and all(0 <= c["score"] <= c["max"] for c in report["static_score"]["categories"].values())
assert len(inputs) == report["meta"]["n_inputs"] == 5
for i in inputs:
    assert 3 <= len(i["assertions"]) <= 5 and i["assertions_passed"] == sum(a["result"] == "PASS" for a in i["assertions"])
    assert i["basic"] + i["specialized"] == i["total"] and 0 <= i["basic"] <= 40 and 0 <= i["specialized"] <= 60
    assert i["status_flag"] in ("✅", "⚠️", "❌")
assert 2 <= len(report["key_strengths"]) <= 5
assert [r["priority"] for r in recs] == sorted(r["priority"] for r in recs)
assert report["final"]["score"] == round(sw + dw)
json.dump(report, open(os.path.join(D, f"eval_report_{SKILL}_result.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("written; final", score, g, "deployable", report["final"]["deployable"])
