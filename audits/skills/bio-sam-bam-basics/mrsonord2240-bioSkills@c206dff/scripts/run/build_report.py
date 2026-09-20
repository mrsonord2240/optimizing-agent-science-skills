"""Builds eval_report_bio-sam-bam-basics_result.json from the per-input judgements below and validates it against the
schema's pre-emit checklist. Scores are the auditor's judgement from out/*.txt (see viewer); this script only assembles and checks."""
import json, os, sys
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = 'bio-sam-bam-basics'

def A(text, ok, note):
    return {'text': text, 'result': 'PASS' if ok else 'FAIL', 'note': note}

inputs = [
 dict(index=1, type='Canonical', label='Inspect the real human PE BAM: header, reads, FLAG decode, counts, regions, pysam vs samtools',
      status='COMPLETED', note='Core facts verified; shipped view_bam.py crashes without an index; naive multi-region call duplicates 1930 of 5426 records (exit 0)',
      basic=34, specialized=49, executed=True,
      execution_note='Ran on real nf-core human BAM (5644 records) with samtools 1.24, pysam 0.24.1 and Rsamtools 2.22.0 via r.sh; run/in1.py, in1b.py, in1_rsamtools.R; 26 asserted checks (23 pass, 3 fail).',
      assertions=[
        A('FLAG decoding (samtools flags, the 12-row table, 99/147 text, pysam is_* properties) equals an independent SAM-spec decoder', True, 'Every flag seen (83, 99, 147, 163) and all 12 bits agree; 99/147 TLEN signs +157/-135 as spec'),
        A('Coordinate statements hold: SAM POS = reference_start+1, samtools chr:a-b == fetch(a-1,b), faidx 1-based, boundary read lost by verbatim copy', True, 'E=2094: samtools 512 vs fetch(E,E+1) 493; 1952-1952 equals fetch(1951,1952)'),
        A('Shipped examples/view_bam.py runs and prints correct stats on the canonical indexed BAM', True, 'References 1, Mapped 5642, Unmapped 2, first read chr22:1951 (0-based, unlabelled)'),
        A('Instructions/examples degrade safely on a BAM without index, a wrong contig name and a multi-region request', False, 'view_bam.py raises ValueError without .bai; wrong contig 22 vs chr22 returns 0 rows with exit 0; `view bam r1 r2` over overlapping regions returns 7356 rows vs 5426 unique (no warning); Skill has no -M/-L guidance'),
        A('Output stays in scope: read-only commands, no fabricated values', True, 'All commands non-destructive; R scanBam bullet also verified (5644, pos 1952, flag 99)'),
      ]),
 dict(index=2, type='Variant A', label='Convert BAM<->SAM<->CRAM with samtools, pysam and the shipped convert_formats.sh; confirm nothing lost',
      status='COMPLETED', note='Documented conversions lossless; helper ignores the reference for CRAM input, rejects .BAM, and destroys its input when in==out',
      basic=34, specialized=49, executed=True,
      execution_note='Ran on the real BAM/CRAM + genome.fasta; run/in2.py, in2_diff.sh; 45 asserted/observed checks (33 pass, 1 fail, 11 notes).',
      assertions=[
        A('All documented conversion commands (BAM->SAM->BAM->CRAM->BAM, pipe form) exit 0 and round-trip 5644 records with every field identical', True, 'Identical after sorting optional tags; raw text differs only because CRAM re-orders NM/MD tags (in2_diff.sh)'),
        A('pysam conversions (w, wb, wc with reference_filename) preserve all records; modes r/rc/rb behave as the usage-guide table says', True, "p.sam/p.bam/p.cram identical; 'r' auto-detects BAM; 'rc'+reference reads CRAM; header['SQ'] snippet works"),
        A('convert_formats.sh performs SAM/BAM/CRAM(+ref) conversions correctly and errors cleanly on missing reference/usage/unknown extension', True, 'BAM->SAM, SAM->BAM, BAM->CRAM outputs identical to original; clean messages for the three error paths'),
        A('The helper is safe for every conversion it advertises (CRAM input with reference, uppercase extension, input==output)', False, 'Third argument silently ignored for CRAM->BAM/SAM; .BAM -> "Unknown output format"; `h.bam h.bam` left a 0-record BAM (input destroyed)'),
        A('Statements about formats hold: SAM > BAM > CRAM size, header preserved, CRAM decode without reference fails loudly (rc 1)', True, 'sizes 1881176 > 176101 > 66597 bytes; @HD/@SQ/@RG preserved (M5/UR added); rc=1 with no records'),
      ]),
 dict(index=3, type='Edge', label='Synthetic edge-case BAM: unmapped-with-position, secondary/supplementary, hard/soft clips, N, MAPQ 255/0, 66,000-op CIGAR, empty BAM',
      status='COMPLETED', note='Every statement the Skill makes about these cases holds; view_bam.py crashes on an empty unindexed BAM and gives no unmapped marker',
      basic=33, specialized=49, executed=True,
      execution_note='Ran on 15 hand-written SYNTHETIC records (make_synth.py) against a spec-derived CIGAR model; run/in3.py; 57 checks (47 pass, 1 fail, 9 notes).',
      assertions=[
        A('CIGAR semantics stated by the Skill (N not covered, S kept in SEQ, H absent, M overloaded, =/X, P) match pysam and a spec-derived consumption model', True, 'reference_length/query_length/query_alignment_*/get_reference_positions agree on 13 CIGARs; N jump 128->1129; hard clip 30 vs infer_read_length 50; 10M2I30M5D20M = 62 query/65 ref'),
        A('Secondary vs supplementary arithmetic holds: -F 256 / -F 2304 / -F 2048 counts and flag bits', True, '14 / 13 / 14 of 15 records; samtools flags matches spec for every synthetic flag'),
        A('Unmapped-with-position, "*" SEQ/QUAL, MAPQ 255/0, mate fields and TLEN sign, 66,000-op CIGAR and empty BAM are handled as the Skill patterns imply', True, 'placed unmapped read returned by region query; TLEN +90/-90; -q 255 keeps exactly the 255 read; 66000-op CIGAR via CG tag intact; empty BAM iterates 0 reads'),
        A('Shipped view_bam.py copes with the edge inputs (empty unindexed BAM, unplaced/unmapped reads)', False, 'Empty unindexed BAM raises ValueError; unmapped read printed as "None:-1 + None" with no unmapped marker; a SAM input raises AttributeError'),
        A('Skill alone covers what the prompt asks (consumption of reference/query bases per CIGAR op, TLEN sign)', True, 'CIGAR table plus M/I/D/N notes suffice with general knowledge; no explicit consumption table or TLEN-sign statement (P2 gap)'),
      ]),
 dict(index=4, type='Variant B', label='CRAM offline: how samtools finds the reference, REF_CACHE recipe, proving a CRAM is readable, is archive lossy',
      status='COMPLETED', note='Resolution order, cache recipe, no-network default and archive-lossless all verified; the "view -c proves reference reachable" recipe is false and "silently corrupts" is stale',
      basic=30, specialized=41, executed=True,
      execution_note='Ran with samtools 1.24 on real BAM + genome.fasta using poisoned caches, a moved FASTA, ignore_md5 and a bogus proxy; run/in4.py, in4b.py; 44 checks (31 pass, 1 fail, 12 notes).',
      assertions=[
        A('Reference resolution order -T > REF_CACHE > REF_PATH > @SQ UR, seq_cache_populate.pl layout and the offline REF_CACHE/REF_PATH recipe', True, 'Poisoned-cache/poisoned-path/poisoned-UR experiments confirm every ordering claim; REF_PATH/REF_CACHE alone also decode'),
        A('htslib >=1.22 has no built-in ENA lookup; archive preset is accepted, lossless and the smallest profile; quickcheck is header+EOF only', True, 'no network attempt with a bogus proxy, 0 ebi.ac.uk/ena/cram strings in libhts; archive 64152 B (smallest) with identical records; quickcheck rc 0 on a mid-file-corrupted CRAM'),
        A('"samtools view -c file.cram forces full decode; proves reference reachable"', False, 'With the reference unreachable `view -c` prints 5644 and exits 0 (and passes on a corrupted CRAM); a full decode (`view -o /dev/null`) is what fails, rc=1'),
        A('"A different reference silently corrupts bases on read-back" describes samtools 1.24', False, 'Mismatched reference gives a hard "MD5 checksum reference mismatch" error (rc 1); bases are silently wrong only when the user sets --input-fmt-option ignore_md5=1 (129 reads differed)'),
        A('Output stays in scope: no destructive commands, no fabricated values; -C without -T behaviour disclosed', True, 'BAM->CRAM without -T exits 0 with warnings and embeds the reference (Skill says -T required; embed_ref/no_ref never mentioned)'),
      ]),
 dict(index=5, type='Stress', label='Six aligners on a synthetic repeat genome: MAPQ scale per aligner, -q thresholds, tags, @PG chain, fixmate/markdup',
      status='COMPLETED', note='MAPQ table, HI base, tag table and @PG chain verified with real aligner output; four peripheral failure-mode claims are wrong',
      basic=35, specialized=48, executed=True,
      execution_note='Ran bwa, bwa-mem2, minimap2 (M and --eqx), bowtie2, hisat2 and STAR (HI base 1 and 0) on 2500 SYNTHETIC pairs plus the real STAR RNA BAM; run/in5.sh, in5.py; 54 checks (31 pass, 1 fail, 22 notes).',
      assertions=[
        A('MAPQ table rows hold: bwa/bwa-mem2/minimap2 0-60 max 60, HISAT2 {0,1,60}, Bowtie2 max 42, STAR {0,1,3,255} with 255 = unique (NH=1)', True, 'STAR MAPQ = f(NH): 1->255, 2->3, 3-4->1, >=5->0 over 6356 records; no 255 from bwa/minimap2'),
        A('-q guidance behaves as stated: bowtie2 -q 60 keeps 0; STAR -q 30 == -q 255 == unique only', True, 'bowtie2 -q 60 -> 0 reads; STAR 4444 = 4444 = 4444'),
        A('Tag/provenance statements hold: NM/MD from bwa, no MD from minimap2, NH/HI from STAR, HI 1-based (0-based with --outSAMattrIHstart 0), RG, fixmate -m adds ms/MC, @PG PP chain linear, "@PG | head -1" names the aligner', True, 'all six aligners named by first @PG; chain bwa->samtools->samtools.1..4 linear'),
        A('Stated failure modes and compatibility notes are accurate (markdup silently marks nothing; MD needed by mpileup BAQ; bcftools needs M not =/X; Bowtie2 42 is rare)', False, 'markdup without ms/MC exits 1 with "run samtools fixmate"; mpileup output byte-identical without MD/NM; identical on =/X BAM; MAPQ 42 is 97.4% of Bowtie2 records'),
        A('Output stays in scope: no fabricated statistics, no destructive commands', True, 'Every number above was produced by the runs'),
      ]),
]
for i in inputs:
    i['total'] = i['basic'] + i['specialized']
    i['assertions_total'] = len(i['assertions'])
    i['assertions_passed'] = sum(1 for a in i['assertions'] if a['result'] == 'PASS')
    i['status_flag'] = '✅' if i['total'] >= 75 else '⚠️'
    i['label'] = i['label']

exec_avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
passed = sum(i['assertions_passed'] for i in inputs)
total = sum(i['assertions_total'] for i in inputs)

cats = {
 'functional_suitability': (8, 12, 'Completeness 3 / Correctness 2 / Appropriateness 3. Core FLAG/CIGAR/coordinate/conversion content is correct; the CRAM "view -c proves reference reachable" recipe, two stale failure-mode statements and the MD/=X compatibility notes are wrong; multi-region extraction (a usage-guide prompt) has no snippet.'),
 'reliability': (7, 12, 'Fault tolerance 2 / Error reporting 2 / Recoverability 3. view_bam.py dies with a raw ValueError on unindexed/empty BAMs and AttributeError on SAM, and prints Mapped 0/Unmapped 0 on CRAM; convert_formats.sh ignores the reference for CRAM input and can overwrite its own input; wrong contig names exit 0.'),
 'performance_context': (5, 8, 'Token cost 2 / Efficiency 3. SKILL.md is 373 lines and usage-guide.md (210 lines) repeats the header, fields, FLAG, CIGAR, command and pysam material; no references/ layering.'),
 'agent_usability': (12, 16, 'Learnability 3 / Consistency 3 / Feedback 3 / Error prevention 3. Tables are clear and mostly consistent; view_bam prints 0-based starts unlabelled next to 1-based SAM text; footgun sections (coordinates, MAPQ, CRAM reference) are strong but miss multi-region duplicates and the count-only CRAM trap.'),
 'human_usability': (6, 8, 'Discoverability 3 / Forgiveness 3. Description uses natural trigger words; helper rejects uppercase extensions and gives no hint about needing an index.'),
 'security': (10, 12, 'Credential 4 / Input validation 3 / Data safety 3. No secrets, no eval; helper quotes variables and checks arguments but does not guard input==output (data loss observed) or check the input exists before converting.'),
 'maintainability': (8, 12, 'Modularity 3 / Modifiability 3 / Testability 2. Split into SKILL/usage-guide/examples but facts are duplicated across two documents; two examples with no expected output or test data; version-pinned claims (1.22 default change) would need re-verification.'),
 'agent_specific': (16, 20, 'Trigger 3 / Progressive disclosure 3 / Composability 4 / Idempotency 3 / Escape hatches 3. Related Skills all exist (checked); version-drift instruction is present; no explicit when-not-to-use or hand-off for filtering/duplicates beyond the Related Skills list.'),
}
subtotal = sum(v[0] for v in cats.values())
static_w = round(subtotal * 0.4, 1)
dyn_w = round(exec_avg * 0.6, 1)
score = int(round(static_w + dyn_w))
assert score == 77, score

recs = [
 dict(priority='P1', title='CRAM check: `samtools view -c` does not prove the reference is reachable', observed_in=[4],
      problem='SKILL.md says `samtools view -c file.cram` forces a full decode and proves the reference is reachable. With the reference FASTA moved away and no cache, `view -c` printed 5644 and exited 0, and it also passed a mid-file-corrupted CRAM; only a real decode fails (rc 1).',
      root_cause='Count-only mode in samtools 1.24 does not decode bases, so it never resolves the reference; the statement was written from assumption, not from a run.',
      fix='Replace with `samtools view -o /dev/null file.cram && echo reference-ok` (or pipe to `md5sum`) and say `-c` and `quickcheck` only prove header/EOF and index counts.'),
 dict(priority='P1', title='Shipped view_bam.py fails or lies outside indexed BAM input', observed_in=[1, 3, 4],
      problem='On an unindexed BAM (also an empty one) it raises ValueError from bam.mapped; on SAM it raises AttributeError; on an indexed CRAM it prints "Mapped: 0 / Unmapped: 0" for a file with 5642+2 records; it prints reference_start 0-based unlabelled and unmapped reads as "None:-1 + None".',
      root_cause='bam.mapped/bam.unmapped need BAM index counts and are unavailable for SAM and CRAM; the script opens with mode "rb" and has no error handling or format detection.',
      fix='Open with mode "r" (autodetect), wrap the mapped/unmapped print in try/except (ValueError, AttributeError) and fall back to counting, label the coordinate as 0-based, and print "unmapped" for is_unmapped records.'),
 dict(priority='P1', title='Multi-region extraction is a silent-wrong trap with no guidance', observed_in=[1],
      problem='usage-guide.md prompts "Get reads from multiple regions" but no snippet exists; `samtools view bam chr22:2000-3000 chr22:2500-3500` returned 7356 records of which 1930 were duplicates (5426 unique) with exit 0, and summing pysam fetch() calls double-counts the same way.',
      root_cause='Neither document mentions -M (multi-region iterator), -L BED, or de-duplicating overlapping fetches.',
      fix='Add a "Multiple regions" example using `samtools view -M bam r1 r2` or `-L regions.bed` (0-based BED), and a pysam note to merge intervals before fetching.'),
 dict(priority='P1', title='Several failure-mode and compatibility statements are wrong for 1.24', observed_in=[4, 5],
      problem='(a) markdup without MC/ms "silently" marks nothing: it exits 1 with "run samtools fixmate"; (b) MD:Z "required by bcftools mpileup BAQ": mpileup output is byte-identical with MD/NM stripped; (c) "bcftools / Picard often need M": bcftools mpileup output is identical on a minimap2 --eqx BAM; (d) Bowtie2 MAPQ 42 "(rare)": 97.4% of records; (e) different reference "silently corrupts": hard MD5-mismatch error unless ignore_md5=1.',
      root_cause='Claims were copied from older tool behaviour or folklore and never run against the tools.',
      fix='Correct each sentence to the observed behaviour above; keep the "verify with `samtools view | awk` and @PG" workflow.'),
 dict(priority='P1', title='convert_formats.sh cannot do what the Skill advertises for CRAM input and can destroy its input', observed_in=[2],
      problem='The reference argument is only used for .cram output, so CRAM->BAM/SAM never gets -T (it worked only because the CRAM header UR pointed at a reachable FASTA); `.BAM` is rejected as an unknown format; `convert_formats.sh h.bam h.bam` left a 0-record BAM.',
      root_cause='The case statement passes -T only in the cram branch, lower-cases nothing, and never compares input and output paths.',
      fix='Build a `${REFERENCE:+-T "$REFERENCE"}` argument used in every branch, lower-case the extension, and exit with an error when INPUT and OUTPUT resolve to the same file.'),
 dict(priority='P2', title='Duplicated documents and missing explicit CIGAR/TLEN rules', observed_in=[3],
      problem='usage-guide.md repeats SKILL.md (header, fields, FLAG, CIGAR, commands, pysam, tips) with a smaller, less complete FLAG/CIGAR table; neither states which CIGAR ops consume query/reference, the TLEN sign rule, or that MAPQ 255 means "not available" outside STAR.',
      root_cause='usage-guide.md was written as a standalone human doc and never de-duplicated against SKILL.md.',
      fix='Keep one copy of the format tables in SKILL.md, reduce usage-guide.md to prompts and troubleshooting, and add a 9-row CIGAR consumption table and a TLEN/MAPQ-255 note.'),
 dict(priority='P2', title='Small accuracy and documentation gaps', observed_in=[1, 2, 4, 5],
      problem='`samtools view -H` appends its own @PG line (use --no-PG); a wrong contig name returns 0 rows with exit 0; the SKILL.md SAM example is space-delimited and not parseable; `-C` without -T exits 0 with warnings and embeds the reference (embed_ref/no_ref never mentioned); CRAM re-orders optional tags; SA:Z is described as a "comma-list" but is semicolon-separated 6-field records; minimap2 also emits an unrelated ms:i tag.',
      root_cause='Behaviours of samtools 1.24 that drifted from the 1.19-era examples were not re-checked.',
      fix='Add one line each: --no-PG, contig-name check via `samtools idxstats`, embed_ref for portable CRAM, SA:Z format, and that `ms` from minimap2 is not the fixmate mate score.'),
]

report = {
 'meta': {'skill_name': NAME,
          'description': 'View, convert, and understand SAM/BAM/CRAM alignment files using samtools and pysam. Use when inspecting alignments, converting between formats, or understanding alignment file structure.',
          'evaluated_on': '2026-09-20', 'evaluator_version': 'skill-auditor@1.0',
          'category': 'Data Analysis', 'execution_mode': 'D', 'complexity': 'Moderate', 'n_inputs': 5,
          'source': 'mrsonord2240/bioSkills@c206dff76d081a5126f8497fbabe10995c9b6026:alignment-files/sam-bam-basics',
          'tools': 'samtools 1.24, htslib 1.24, pysam 0.24.1, bcftools 1.24, bwa 0.7.19, bwa-mem2 2.2.1, minimap2 2.31, bowtie2 2.5.5, hisat2 2.2.3, STAR 2.7.11b (WSL science env alignment-files); Rsamtools 2.22.0 (Windows R via r.sh)',
          'floors_check': 'Static 72 >= 70; execution avg 80.4 >= 75; Layer1 avg 33.2 >= 28; Layer2 avg 47.2 >= 42; assertion pass rate 76% < 80% (Limited Release floor NOT met) -> one-tier downgrade to Beta Only; score stays 77',
          'complexity_note': 'Moderate: 4 files (SKILL.md, usage-guide.md, 2 examples), 3-5 task types; 5 inputs by the rule. Grade downgraded one tier from Limited Release by the assertion-pass-rate floor (19/25 = 76% < 80%).'},
 'veto_gates': {
   'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
   'research_veto': {'applicable': True, 'gate': 'PASS',
      'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated identifiers, statistics or results; every numeric claim the Skill makes about tool output that was tested either held or is listed as a P1/P2 finding.'},
      'practice_boundaries': {'result': 'PASS', 'detail': 'File-format tooling only; no diagnostic, prescriptive or clinical content.'},
      'methodological_ground': {'result': 'PASS', 'detail': 'No principled methodological fallacy in the outputs; the false CRAM reachability recipe and stale failure-mode claims are recorded as P1 correctness defects, not as a methodological fallacy.'},
      'code_usability': {'result': 'PASS', 'detail': 'Both shipped examples and every SKILL.md/usage-guide snippet executed from a copy on samtools 1.24 / pysam 0.24.1 with asserted output; view_bam.py and convert_formats.sh fail only outside their documented input (indexed BAM; CRAM output) and are P1 findings.'}}},
 'static_score': {'subtotal': subtotal, 'max': 100,
   'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in cats.items()}},
 'dynamic_score': {'execution_avg': exec_avg, 'max': 100, 'assertion_pass_rate': {'passed': passed, 'total': total},
   'inputs': [{'index': i['index'], 'type': i['type'], 'label': i['label'], 'status': i['status'], 'status_flag': i['status_flag'],
               'note': i['note'], 'basic': i['basic'], 'specialized': i['specialized'], 'total': i['total'],
               'assertions_passed': i['assertions_passed'], 'assertions_total': i['assertions_total'],
               'executed': i['executed'], 'execution_note': i['execution_note'], 'assertions': i['assertions']} for i in inputs]},
 'final': {'static_weighted': static_w, 'dynamic_weighted': dyn_w, 'score': score, 'max': 100,
           'grade': 'Beta Only', 'grade_symbol': '⚠️', 'deployable': False, 'veto_override': False},
 'key_strengths': [
   'Core format facts are correct and verified against an independent spec decoder: the 12-bit FLAG table, samtools flags output, 1-based vs 0-based coordinate table (including the boundary-read footgun), CIGAR semantics (N not covered, S vs H) and secondary vs supplementary filter arithmetic.',
   'CRAM reference resolution is exactly right (-T > REF_CACHE > REF_PATH > UR, offline cache recipe, htslib 1.22 default removal, archive preset lossless): confirmed with poisoned caches, a moved FASTA and a bogus proxy.',
   'The MAPQ-by-aligner table and the -q advice hold against real bwa, bwa-mem2, minimap2, bowtie2, hisat2 and STAR output (STAR MAPQ = f(NH); Bowtie2 max 42); tag table, HI base and @PG PP chain also verified.',
   'All documented conversions round-trip 5644 real records losslessly through SAM, BAM and CRAM by samtools and pysam; every cross-referenced Related Skill exists.'],
 'recommendations': recs,
}

# ---------------- pre-emit checklist ----------------
d = report
assert len(d['dynamic_score']['inputs']) == d['meta']['n_inputs']
for i in d['dynamic_score']['inputs']:
    assert 3 <= len(i['assertions']) <= 5
    assert i['assertions_passed'] == sum(a['result'] == 'PASS' for a in i['assertions'])
    assert i['basic'] + i['specialized'] == i['total'] and 0 <= i['basic'] <= 40 and 0 <= i['specialized'] <= 60
assert d['static_score']['subtotal'] == sum(c['score'] for c in d['static_score']['categories'].values())
assert all(0 <= c['score'] <= c['max'] for c in d['static_score']['categories'].values()) and len(d['static_score']['categories']) == 8
assert 2 <= len(d['key_strengths']) <= 5
assert [r['priority'] for r in recs] == sorted(r['priority'] for r in recs)
assert d['dynamic_score']['execution_avg'] == round(sum(i['total'] for i in d['dynamic_score']['inputs']) / 5, 1)
print('static', subtotal, 'exec', exec_avg, 'weighted', static_w, dyn_w, 'score', score, 'assertions', passed, total, 'L1', round(sum(i['basic'] for i in inputs)/5,1), 'L2', round(sum(i['specialized'] for i in inputs)/5,1))
with open(os.path.join(OUT, f'eval_report_{NAME}_result.json'), 'w', encoding='utf-8') as fh:
    json.dump(d, fh, indent=2, ensure_ascii=False)
print('written')
