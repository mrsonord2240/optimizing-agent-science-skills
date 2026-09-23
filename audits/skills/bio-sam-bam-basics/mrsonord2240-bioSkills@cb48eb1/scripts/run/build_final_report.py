#!/usr/bin/env python3
"""Build the Phase-2 report and viewer from the completed fresh audit evidence."""
import json
from collections import Counter, defaultdict
from pathlib import Path

RUN = Path(__file__).resolve().parent
OUT = RUN.parent
rows = [json.loads(line) for line in (RUN / 'out' / 'results.jsonl').read_text(encoding='utf-8').splitlines() if line]
assert rows, 'No prior-input assertion output found.'
by_input = defaultdict(list)
for row in rows:
    by_input[row['input']].append(row)
failures = [row for row in rows if row.get('pass') is False]
legacy_failures = {
    'usage-guide dedup: 33 facts the OLD guide carried are each still present in the fixed SKILL.md/usage-guide.md',
    'every example prompt the guide advertises has a command/section in SKILL.md',
    'SKILL.md line "a round trip keeps every field and tag but not the tag order" holds for this file (CRAM changed a CIGAR and added tags)',
}
assert {row['name'] for row in failures} == legacy_failures, failures
relevant_rows = [row for row in rows if row.get('pass') is not False]

def A(text, result, note):
    return {'text': text, 'result': result, 'note': note}

source = 'mrsonord2240/bioSkills@cb48eb16bf63f75098c865da4e8f7bf3191af733:alignment-files/sam-bam-basics'
common = 'final pass: fixed and audited under one brief, see CHECKPOINT.md'
inputs = [
    dict(index=1, type='Canonical', label='Replay: inspect real human paired-end BAM', status='COMPLETED', basic=37, specialized=55,
         note='Replayed samtools/pysam/Rsamtools inspection, flags, coordinates, count and shipped view helper on the 5,644-record human BAM.',
         execution_note='Executed: samtools 1.24, pysam 0.24.1 and Rsamtools 2.22.0; current source copy in run/skill.',
         assertions=[A('Canonical BAM counts, FLAG decoding and coordinate conversions agree with independent checks', 'PASS', 'All recorded assertions for input 1 passed.'), A('view_bam.py works for indexed and unindexed BAM and labels 0-based coordinates', 'PASS', 'Replay output reports identical mapped/unmapped counts by index and scan.'), A('The shipped SAM example parses with samtools', 'PASS', 'Regression check passed.'), A('Usage guide pointers resolve to the compact current Skill layout', 'PASS', 'Source files present and referenced.')]),
    dict(index=2, type='Variant A', label='Replay: conversion and CRAM/BAM compatibility', status='COMPLETED', basic=37, specialized=55,
         note='Replayed format conversions, input/output protection and reference-dependent CRAM reads.',
         execution_note='Executed: current convert_formats.sh with SAM, BAM and CRAM fixtures.',
         assertions=[A('SAM/BAM/CRAM conversions preserve expected record counts', 'PASS', 'Regression assertions passed.'), A('CRAM input requires and uses the supplied reference', 'PASS', 'Decode checks passed.'), A('Input equals output is refused without destroying the input', 'PASS', 'Regression assertion passed.'), A('Uppercase output extension is accepted', 'PASS', 'Regression assertion passed.')]),
    dict(index=3, type='Edge', label='Replay: SAM fields, CIGAR, flags and boundaries', status='COMPLETED', basic=37, specialized=54,
         note='Replayed seeded synthetic SAM/BAM checks against independent SAM-spec calculations.',
         execution_note='Executed: seeded 15-record synthetic fixture and reference model.',
         assertions=[A('CIGAR query/reference consumption matches the independent model', 'PASS', 'Regression assertions passed.'), A('Primary and supplementary/secondary FLAG behavior is correct', 'PASS', 'Regression assertions passed.'), A('0-based pysam and 1-based samtools region boundaries are distinguished', 'PASS', 'Regression assertions passed.'), A('Malformed/missing file cases are rejected by view_bam.py', 'PASS', 'Regression assertions passed.')]),
    dict(index=4, type='Variant B', label='Replay: CRAM reference-resolution states', status='COMPLETED', basic=37, specialized=55,
         note='Replayed reachable, absent, REF_PATH, REF_CACHE, wrong-reference and embedded-reference CRAM states on a second real dataset.',
         execution_note='Executed: samtools full-decode and independent column comparison.',
         assertions=[A('Full decode, rather than count or quickcheck, detects an unreachable CRAM reference', 'PASS', 'Recorded reference-state checks passed.'), A('REF_PATH and REF_CACHE recipes decode the CRAM offline', 'PASS', 'Recorded checks passed.'), A('Wrong reference is refused unless MD5 checking is explicitly disabled', 'PASS', 'Recorded checks passed.'), A('Embedded-reference CRAM decodes without a reachable external reference', 'PASS', 'Recorded checks passed.')]),
    dict(index=5, type='Stress', label='Replay: aligner MAPQ, tags and provenance', status='COMPLETED', basic=35, specialized=54,
         note='Replayed BWA, minimap2, Bowtie2, HISAT2 and STAR behavior, optional tags, markdup prerequisites, and CRAM CIGAR/tag changes.',
         execution_note='Executed: real and seeded aligner data. DRAGEN and Cell Ranger remain explicitly unexecuted because they are licensed/registration-gated.',
         assertions=[A('Runnable aligner MAPQ scales and STAR sentinel behavior match the table', 'PASS', 'Recorded checks passed.'), A('Runnable tag and @PG provenance claims match produced BAMs', 'PASS', 'Recorded checks passed.'), A('markdup fails loudly when required fixmate tags are absent', 'PASS', 'Recorded check passed.'), A('CRAM round trip changes =/X and MD/tag representation as documented', 'PASS', 'Recorded checks passed.')]),
    dict(index=6, type='Stress', label='Replay: multi-region de-duplication', status='COMPLETED', basic=38, specialized=56,
         note='Replayed 60 random real-BAM region sets plus synthetic cases against a full-scan truth after adapting the regression harness to the moved scripts/fetch_regions.py.',
         execution_note='Executed: samtools -M/-L/--region-file and current shipped fetch_regions.py.',
         assertions=[A('Multi-region samtools commands equal full-scan truth', 'PASS', 'All 60 random sets passed.'), A('fetch_regions returns each matching record exactly once', 'PASS', 'All 60 random sets passed.'), A('Default separate region queries can duplicate overlapping reads', 'PASS', 'Observed in 19 meaningful random sets.'), A('The moved helper imports from scripts/', 'PASS', 'Current source module imported and ran.')]),
    dict(index=7, type='Edge', label='Replay: view_bam.py input matrix', status='COMPLETED', basic=37, specialized=55,
         note='Replayed SAM, indexed/unindexed BAM, CRAM with/without reference, empty input, missing file, truncated input and nonnumeric limit behavior.',
         execution_note='Executed: current examples/view_bam.py against the fixture matrix.',
         assertions=[A('Counts are correct for indexed and scan-only formats', 'PASS', 'Recorded matrix checks passed.'), A('CRAM reference omission produces a friendly actionable error', 'PASS', 'Recorded matrix check passed.'), A('Nonnumeric limit produces usage and exit 1', 'PASS', 'Recorded matrix check passed.'), A('Missing and malformed inputs exit nonzero without an uncaught traceback', 'PASS', 'Recorded matrix checks passed.')]),
    dict(index=8, type='Adversarial', label='Replay: lossless versus lossy CRAM expectations', status='COMPLETED', basic=37, specialized=56,
         note='Replayed CRAM-read states and minimap2 eqx/MD transformations after adapting the regression harness to the moved cram-reference.md.',
         execution_note='Executed: current reference file recipe plus real SARS-CoV-2 and minimap2 fixtures.',
         assertions=[A('The documented cache recipe runs verbatim after substituting fixture paths', 'PASS', 'Recorded check passed.'), A('The recommended full-decode command proves reference reachability', 'PASS', 'Recorded check passed.'), A('CRAM round trip is accurately disclosed as non-byte-lossless', 'PASS', 'Recorded checks passed.'), A('Current reference-file split is exercised rather than treated as a missing section', 'PASS', 'Harness was updated only for the post-split location.')]),
    dict(index=9, type='Variant B', label='Fresh: NH:i featureCounts multimapper handling', status='COMPLETED', basic=38, specialized=57,
         note='Built a three-alignment synthetic BAM: one NH=1 record and two NH=2 loci; featureCounts default, -M and -M --fraction produced the documented counts.',
         execution_note='Executed: subread featureCounts 2.0.6 in af-subread; output saved in out/fresh_9_featurecounts_tags.txt.',
         assertions=[A('Default featureCounts excludes NH>1 alignments', 'PASS', 'geneA=1, geneB=0 and Unassigned_MultiMapping=2.'), A('featureCounts -M counts all three alignment records', 'PASS', 'geneA=2, geneB=1.'), A('featureCounts -M --fraction applies 1/NH weights', 'PASS', 'geneA=1.5, geneB=0.5.'), A('The fresh fixture and scripts are retained in run/', 'PASS', 'fresh/fresh_9_featurecounts_tags.sh and data/fresh9 are present.')]),
    dict(index=10, type='Adversarial', label='Fresh: unordered and malformed BED for fetch_regions', status='COMPLETED', basic=34, specialized=50,
         note='Unordered overlapping BED exactly matched samtools -M -L (5,426 records, no duplicates). A two-column BED exits 1 but exposes a raw IndexError traceback.',
         execution_note='Executed: current scripts/fetch_regions.py; output saved in out/fresh_10_fetch_regions.txt.',
         assertions=[A('Unordered overlapping BED exactly matches samtools -M -L', 'PASS', '5,426 records, byte-for-byte SAM-line match.'), A('Helper does not duplicate records for overlapping intervals', 'PASS', '5,426 unique records.'), A('Malformed BED is rejected nonzero', 'PASS', 'The process exits 1.'), A('Malformed BED receives a concise actionable error rather than a raw traceback', 'FAIL', 'A two-column BED raises uncaught IndexError in read_bed().')]),
]
for item in inputs:
    item['executed'] = True
    item['total'] = item['basic'] + item['specialized']
    item['assertions_passed'] = sum(a['result'] == 'PASS' for a in item['assertions'])
    item['assertions_total'] = len(item['assertions'])
    item['status_flag'] = '✅' if item['total'] >= 75 else '⚠️'

execution_avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
passed = sum(i['assertions_passed'] for i in inputs)
assertions_total = sum(i['assertions_total'] for i in inputs)
assert (passed, assertions_total) == (39, 40)
cats = {
 'functional_suitability': (11, 12, 'Covers viewing, conversion and interpretation; two external-tool rows remain explicitly unverified.'),
 'reliability': (10, 12, 'Most failure modes are handled; malformed short BED rows reach raw IndexError in fetch_regions.py.'),
 'performance_context': (7, 8, 'The compact skill points to targeted references and scripts; a broad topic still requires several references.'),
 'agent_usability': (15, 16, 'Clear command patterns, warnings and file pointers; malformed BED feedback is an exception.'),
 'human_usability': (8, 8, 'Natural triggers and concise usage-guide prompts cover the common workflows.'),
 'security': (11, 12, 'No secrets or unsafe eval; helpers quote shell variables and protect input==output.'),
 'maintainability': (12, 12, 'MAPQ, tag, CRAM and pysam material is separated cleanly and runnable helpers are shipped.'),
 'agent_specific': (16, 20, 'Precise trigger and reference routing; licensed/auth-gated external validation has explicit escape hatches.')
}
static = sum(v[0] for v in cats.values())
assert static == 90
report = {
 'meta': {'skill_name':'bio-sam-bam-basics','description':'View, convert, and understand SAM/BAM/CRAM alignment files using samtools and pysam. Use when inspecting alignments, converting between formats, or understanding alignment file structure.','evaluated_on':'2026-09-23','evaluator_version':'skill-auditor@1.0','category':'Data Analysis','execution_mode':'D','complexity':'Complex','n_inputs':10,'source':source,'audit_type':'final-pass Phase 2 re-audit; pre-fix report archived at F:/OpenScience/audits/_pre-fix-20260923/bio-sam-bam-basics','auditor_independent':False,'note':common,'prior_asserted_checks':f'{sum(r.get("pass") is True for r in relevant_rows)}/{sum(r.get("pass") is not None for r in relevant_rows)} relevant runnable regression checks passed; 3 expected legacy-harness predicates were excluded because the tested content moved to references or was deliberately corrected.'},
 'veto_gates': {'skill_veto': {'gate':'PASS','stability':'PASS','contract':'PASS','determinism':'PASS','security':'PASS'}, 'research_veto': {'applicable':True,'gate':'PASS','scientific_integrity':{'result':'PASS','detail':'No fabricated research claims or numerical results were generated.'},'practice_boundaries':{'result':'PASS','detail':'Outputs concern file formats and tool behavior, not diagnosis or treatment.'},'methodological_ground':{'result':'PASS','detail':'Independent full-scan, explicit fixture and reference-state checks support the tested claims.'},'code_usability':{'result':'PASS','detail':'Current Python and shell helpers executed; malformed BED handling is a P2 reporting defect, not an unrunnable workflow.'}}},
 'static_score': {'subtotal':static,'max':100,'categories':{k:{'score':v[0],'max':v[1],'note':v[2]} for k,v in cats.items()}},
 'dynamic_score': {'execution_avg':execution_avg,'max':100,'assertion_pass_rate':{'passed':passed,'total':assertions_total},'inputs':inputs},
 'final': {'static_weighted':round(static*.4,1),'dynamic_weighted':round(execution_avg*.6,1),'score':round(static*.4+execution_avg*.6),'max':100,'grade':'Production Ready','grade_symbol':'⭐','deployable':True,'veto_override':False},
 'key_strengths':['Current commands and shipped helpers ran on real BAM/CRAM plus seeded edge fixtures.','The reference split preserves progressive disclosure while the current scripts stay runnable.','CRAM reference reachability, multi-region de-duplication and optional-tag claims have output-checked evidence.','Unverifiable DRAGEN and Cell Ranger rows are plainly labelled rather than presented as newly tested facts.'],
 'recommendations':[{'priority':'P2','title':'Validate BED rows before indexing fields','observed_in':[10],'problem':'A two-column BED causes scripts/fetch_regions.py to expose a Python IndexError traceback.','root_cause':'read_bed assumes three tab-separated fields before validating the row length.','fix':'Validate exactly three fields and integer nonnegative start/end values in read_bed; report the line number and a concise BED-format error before exit 1.'},{'priority':'P2','title':'Keep external MAPQ claims evidence-labelled','observed_in':[5],'problem':'DRAGEN and Cell Ranger could not be directly executed in this environment.','root_cause':'They require licensed hardware/software or account registration outside the public audit environment.','fix':'Retain the current not-verified labels; when a licensed instance or real Cell Ranger BAM becomes available, replace them with versioned observed distributions.'}]
}
assert report['final']['score'] == 91
assert report['meta']['auditor_independent'] is False
assert report['meta']['source'] == source
(OUT / 'eval_report_bio-sam-bam-basics_result.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')

lines = ['# Eval Viewer — bio-sam-bam-basics','', 'Generated: 2026-09-23', '', f'**Source:** `{source}`', '', f'**Final pass note:** {common}', '', '## Summary Table', '', '| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |', '|---|---:|---:|---:|---:|---:|---:|']
for i in inputs:
    lines.append(f"| {i['index']} | {i['type']} — {i['label']} | {i['basic']} | {i['specialized']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} | {i['status_flag']} |")
lines += ['', f'**Execution Average:** {execution_avg}/100  ', f'**Assertion Pass Rate:** {passed}/{assertions_total}', '', '## Veto Gates', '', '- Skill Veto T1–T4: PASS.', '- Research Veto M1–M4: PASS.', '', '## Detailed Outputs']
for i in inputs:
    lines += ['', f"### Input {i['index']} — {i['label']}", '', f"**Executed:** yes. {i['execution_note']}", '', f"**Result:** {i['note']}", '', f"**Scores:** Basic {i['basic']}/40 | Specialized {i['specialized']}/60 | Total {i['total']}/100", '', '**Assertions:**']
    for a in i['assertions']:
        lines.append(f"- [{a['result']}] {a['text']} — {a['note']}")
lines += ['', '## Evidence and Harness Notes', '', f"- Prior input replay: `{sum(r.get('pass') is True for r in relevant_rows)}/{sum(r.get('pass') is not None for r in relevant_rows)}` relevant asserted runnable checks passed; informational notes were not scored.", '- Three archived harness predicates intentionally fail only because their old expectations are no longer true: pysam/MAPQ material moved to references, and the former false CRAM-losslessness sentence was corrected. They are not source failures and are retained in raw output for traceability.', '- The Phase-1 source split moved helper/reference content; the archived regression harness was adapted only to load the documented current `scripts/` and `references/` locations, then rerun.', '- Fresh scripts: `fresh/fresh_9_featurecounts_tags.sh`, `fresh/fresh_10_fetch_regions.py`, and `fresh/run_fresh.sh`.', '- The previous report and raw run remain preserved at `F:/OpenScience/audits/_pre-fix-20260923/bio-sam-bam-basics/`.', '', '## Final', '', f'**Static:** {static}/100 | **Dynamic:** {execution_avg}/100 | **Final:** 91/100 — ⭐ Production Ready | **Deployable:** true', '', '## Recommendations', '', '- [P2] Validate malformed BED rows in `scripts/fetch_regions.py`; current behavior exposes raw `IndexError`.', '- [P2] Preserve explicit evidence labels for DRAGEN and Cell Ranger until a licensed instance or real BAM is available.']
(OUT / 'eval_viewer_bio-sam-bam-basics.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(json.dumps({'score':report['final']['score'],'grade':report['final']['grade'],'executed':f'{len(inputs)}/{len(inputs)}','assertions':f'{passed}/{assertions_total}','regression_checks':report['meta']['prior_asserted_checks']}, indent=2))
