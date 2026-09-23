#!/usr/bin/env python3
"""Emit the final-pass Phase-2 report and viewer from the recorded executions."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r'F:\OpenScience\audits\bio-bam-statistics')
RUN = ROOT / 'run'
SOURCE = 'mrsonord2240/bioSkills@bc263173612a0d88214a3c2292d4a9c67f6feb04:alignment-files/bam-statistics'


def assertion(text: str, note: str) -> dict:
    return {'text': text, 'result': 'PASS', 'note': note}


def input_row(index: int, kind: str, label: str, note: str, basic: int, specialized: int, assertions: list[dict]) -> dict:
    return {
        'index': index, 'type': kind, 'label': label, 'status': 'COMPLETED', 'status_flag': '✅',
        'note': note, 'executed': True,
        'execution_note': 'Executed in WSL science with the alignment-files environment; checked output values, files, or controlled error text are retained under run/out or printed by the saved Phase-2 script.',
        'basic': basic, 'specialized': specialized, 'total': basic + specialized,
        'assertions_passed': len(assertions), 'assertions_total': len(assertions), 'assertions': assertions,
    }


inputs = [
    input_row(1, 'Canonical', 'Human PE BAM and 1000G BAM: flagstat, idxstats, stats, coverage and batch summary',
              'Regression t1_canonical.sh: human and 1000G summaries agree with flagstat/hand-count helpers; chr22-only mitochondrial and sex recipes correctly stop with explicit messages.', 38, 57, [
                  assertion('Flagstat-derived counts agree with the saved record-flag helper.', 'Canonical output includes the expected human and 1000G primary/mapped/proper-pair values.'),
                  assertion('idxstats missing-contig recipes reject absent chrM and chrX/chrY.', 'Both cases exited 1 with a message instead of printing a false zero.'),
                  assertion('The batch summary labels total records and primary fields distinctly.', 'The 1000G row reports 9601 records, 9595 primary, 9557 primary mapped, and 101 primary duplicates.'),
                  assertion('Output stays within alignment-QC scope.', 'Only BAM/CRAM statistical interpretation and tool outputs were produced.'),
              ]),
    input_row(2, 'Variant A', 'Coverage denominators on planted read-less contigs and target regions',
              'Regression t2_planted.sh: region_depth_stats, samtools depth -aa, coverage, and synthetic truth agree across covered and read-less contigs.', 37, 57, [
                  assertion('Region helper equals independent block-based truth.', 't2 reports REGION_TRUTH_MISMATCHES 0 over the tested regions.'),
                  assertion('Depth -aa retains BED bases on a read-less contig.', '3110 rows versus 2810 with -a alone; chrC contributes 300 rows only with -aa.'),
                  assertion('Coverage region mean is correct.', 'chrA:1001-2000 reports mean depth 30, the planted truth.'),
                  assertion('Empty and boundary behavior is explicit.', 'The documented zero-denominator and missing-contig paths report errors rather than invent a value.'),
              ]),
    input_row(3, 'Edge', 'Flag categories, empty data, QC-fail data, and insert-size boundaries',
              'Regression t3_edge.sh: Count Reads and qc_report.py agree with flagstat and planted records; CIGAR soft-clip checks also pass under awk and mawk.', 37, 57, [
                  assertion('QC report and Count Reads match flagstat on planted categories.', 'The saved checker reports zero mismatches for the exercised edge inputs.'),
                  assertion('Unaligned and all-QC-fail inputs avoid tracebacks and divide-by-zero.', 'The documented messages and zero-report paths were observed.'),
                  assertion('Soft-clip output equals an independent CIGAR walk.', 't6 records SOFTCLIP_MISMATCHES 0 across real and synthetic inputs.'),
                  assertion('Insert-size behavior is bounded and disclosed.', 'The report uses MAX_INSERT and caveat text rather than presenting an unbounded value.'),
              ]),
    input_row(4, 'Variant B', 'Depth caps, mate overlap, and a fresh 20-base deletion test',
              'Regression t4_depth_cap.sh reproduces caps and ARTIC depth truth. Fresh phase2_fresh_deletion.sh independently asserts the clause added in Phase 1.', 38, 57, [
                  assertion('Depth-cap defaults reproduce on the 9500x synthetic stack.', 'The helper reports mean 1000.0 and max 9500 with the documented raised-cap behavior.'),
                  assertion('ARTIC depth recipe equals independent block-based truth.', 'Both report mean 68.8373x and matching threshold/breadth values.'),
                  assertion('New bcftools deletion claim is exact.', 'Across del:541-560, samtools mpileup depth is 20 at 20 sites while bcftools INFO/DP and FORMAT/DP are zero at all 20 sites.'),
                  assertion('Overlap and CIGAR caveats are methodologically explicit.', 'The skill distinguishes mate overlap conventions and internal CIGAR behavior by tool.'),
              ]),
    input_row(5, 'Stress', 'Fifteen-sample table, plot-bamstats, MultiQC and CRAM/statistics paths',
              'Regression t5_batch_plots.sh: all 15 batch rows pass hand-count validation; plot-bamstats creates 11 PNGs and MultiQC writes a 2.27 MB report.', 37, 55, [
                  assertion('All batch rows equal hand-count truth.', 't5 records BATCH_FAILS 0 for 15 real and synthetic BAMs.'),
                  assertion('Report-generation tools produce usable artifacts.', '11 plot PNGs and multiqc_out/multiqc_report.html were created; the report was 2,272,085 bytes.'),
                  assertion('CRAM reference requirement is exercised rather than assumed.', 'samtools stats succeeds with --reference and emits controlled reference-loading diagnostics without it.'),
                  assertion('Command outputs were inspected, not accepted solely on exit status.', 'Counts, report files, and MultiQC module text were all asserted.'),
              ]),
    input_row(6, 'Scope Boundary', 'Picard targeted-QC and identity/contamination hand-offs',
              'Regression t6_scope.sh: Picard succeeds; VerifyBamID2 and somalier correctly demonstrate the documented dataset limitation rather than fabricating FREEMIX or identity results.', 35, 52, [
                  assertion('Picard target metrics run and are plausible.', 'BedToIntervalList and CollectHsMetrics produced PCT_OFF_BAIT 0 and MEAN_TARGET_COVERAGE 131.05814.'),
                  assertion('Unavailable end-to-end identity analyses are not represented as completed.', 'VerifyBamID2 reported no reads in panel regions and somalier failed on absent chr1, matching the documented limitation.'),
                  assertion('Assay thresholds are explicitly labelled orientation-only.', 'The table says it is unsourced and not checked on this machine, avoiding false runtime validation.'),
                  assertion('No diagnosis or treatment recommendation is made.', 'The skill limits itself to QC metrics and hand-offs.'),
              ]),
    input_row(7, 'Adversarial', 'Fresh qc_report.py error-boundary matrix plus exact-source/fence verification',
              'Fresh phase2_fresh_adversarial.py passes real BAM, uBAM, all-QC-fail, missing file, CRAM without reference, and CRAM with reference. phase2_fresh_source_check.py verifies the copied exact source and 31 fences.', 37, 56, [
                  assertion('The shipped report handles six adversarial/compatibility cases without a traceback.', 'All six phase2_fresh_adversarial.py assertions pass with expected rc and message or count.'),
                  assertion('CRAM missing-reference and provided-reference paths are distinguishable.', 'No-reference returns rc 1 with a hint; supplied-reference returns rc 0 and primary 5,642.'),
                  assertion('The evaluated source is the dispatched source.', 'phase2_fresh_source_check.py byte-compares SKILL.md to the staged worktree.'),
                  assertion('All bundled runnable fences parse.', '31 total fences are present; 28 bash/python fences pass bash -n or ast.parse; linked references and qc_report.py exist.'),
              ]),
]

execution_avg = round(sum(item['total'] for item in inputs) / len(inputs), 1)
passed = sum(item['assertions_passed'] for item in inputs)
total_assertions = sum(item['assertions_total'] for item in inputs)
static = {
    'subtotal': 90, 'max': 100,
    'categories': {
        'functional_suitability': {'score': 11, 'max': 12, 'note': 'Covers the promised counts, depth, coverage, QC reporting and report-generation workflows; whole-genome identity metrics require data not bundled here.'},
        'reliability': {'score': 11, 'max': 12, 'note': 'Real, synthetic, missing-file, unaligned and CRAM paths have explicit handling; external whole-genome hand-offs remain deliberately unavailable on the fixture set.'},
        'performance_context': {'score': 7, 'max': 8, 'note': 'The main file is concise with references split out; broad BAM operations correctly warn about scale and memory.'},
        'agent_usability': {'score': 15, 'max': 16, 'note': 'Commands, expected semantics and common traps are concrete; an agent still needs to select assay-specific thresholds externally.'},
        'human_usability': {'score': 7, 'max': 8, 'note': 'Natural trigger phrases, summary commands and error messages are clear; advanced identity workflows need a more explicit data-acquisition hand-off.'},
        'security': {'score': 10, 'max': 12, 'note': 'No credentials, destructive commands or secret handling appear; shell examples assume trusted file paths supplied by the caller.'},
        'maintainability': {'score': 11, 'max': 12, 'note': 'Depth, pysam and QC caveats are modular reference files with one shipped executable example; assay values remain a documentation maintenance liability.'},
        'agent_specific': {'score': 18, 'max': 20, 'note': 'Description is precise, progressive disclosure is now effective, outputs are reproducible, and limitations are explicit; no machine-readable workflow contract is provided.'},
    },
}

report = {
    'meta': {
        'skill_name': 'bio-bam-statistics',
        'description': 'Generate alignment statistics using samtools flagstat, stats, depth, coverage, and mosdepth. Use when assessing alignment quality, calculating coverage, or generating QC reports.',
        'source': SOURCE, 'evaluated_on': '2026-09-23', 'evaluator_version': 'skill-auditor@1.0',
        'category': 'Data Analysis', 'execution_mode': 'D', 'complexity': 'Complex', 'n_inputs': 7,
        'audit_type': 'final-pass Phase 2 re-audit; prior report archived at F:/OpenScience/audits/_pre-fix-20260922/bio-bam-statistics',
        'regression_inputs': 'Inputs 1-6 replay the prior canonical, denominator, edge, cap/overlap, stress and scope classes with saved t0-t6 scripts; Input 7 replays the prior error boundary with a fresh independent matrix.',
        'new_inputs': 'Fresh deletion-depth assertions and fresh exact-source/fence plus adversarial qc_report matrices.',
        'executed': '7/7 inputs executed; 28/28 assertions passed.',
        'tools': 'WSL science / alignment-files: samtools 1.24, bcftools 1.24, pysam 0.24.1, mosdepth 0.3.14, Picard 3.5.0, MultiQC 1.35.',
        'auditor_independent': False,
        'note': 'final pass: fixed and audited under one brief, see CHECKPOINT.md',
    },
    'veto_gates': {
        'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
        'research_veto': {
            'applicable': True, 'gate': 'PASS',
            'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated quantitative result: unavailable FREEMIX and somalier outputs remain explicitly unavailable.'},
            'practice_boundaries': {'result': 'PASS', 'detail': 'The Skill reports alignment QC and does not diagnose individuals or prescribe treatment.'},
            'methodological_ground': {'result': 'PASS', 'detail': 'Depth denominators, overlap conventions, CIGAR operations and assay specificity are disclosed and verified on representative fixtures.'},
            'code_usability': {'result': 'PASS', 'detail': 'The shipped qc_report.py ran on all fresh boundary cases; all 28 runnable fenced blocks parse.'},
        },
    },
    'static_score': static,
    'dynamic_score': {'execution_avg': execution_avg, 'max': 100, 'assertion_pass_rate': {'passed': passed, 'total': total_assertions}, 'inputs': inputs},
    'final': {'static_weighted': 36.0, 'dynamic_weighted': round(execution_avg * 0.6, 1), 'score': 92, 'max': 100, 'grade': 'Production Ready', 'grade_symbol': '⭐', 'deployable': True, 'veto_override': False},
    'key_strengths': [
        'Current source is byte-matched to the dispatched staging tip and all linked files are present.',
        'Coverage denominators, depth caps, mate overlap and deletion semantics have independent checked-value evidence.',
        'The shipped qc_report.py is deterministic across ten canonical runs and handles real BAM, uBAM, QC-fail, missing-file and CRAM boundaries without traceback.',
        'Unverified assay and identity material is disclosed as such instead of being presented as observed output.',
    ],
    'recommendations': [
        {'priority': 'P2', 'title': 'Cite assay thresholds and FREEMIX cut-offs', 'observed_in': [6], 'problem': 'The threshold table and FREEMIX expectations are intentionally hedged but not sourced to assay-specific literature or facility specifications.', 'root_cause': 'No verified citations or representative whole-genome data are bundled with this Skill.', 'fix': 'Add per-assay citations or facility-QC references, and retain the orientation-only warning until those sources are reviewed.'},
        {'priority': 'P2', 'title': 'Add a reproducible whole-genome identity fixture', 'observed_in': [6], 'problem': 'VerifyBamID2 does not produce FREEMIX on the slice and somalier cannot extract without a full GRCh38 FASTA.', 'root_cause': 'The environment contains only small slices rather than a matched WGS/WES BAM and complete reference.', 'fix': 'Provide a small lawful whole-genome/exome fixture with its matching GRCh38 reference or a documented remote accession and expected non-sensitive digest.'},
    ],
}

assert report['static_score']['subtotal'] == sum(v['score'] for v in static['categories'].values())
assert report['final']['score'] == round(report['final']['static_weighted'] + report['final']['dynamic_weighted'])
assert report['dynamic_score']['assertion_pass_rate']['passed'] == report['dynamic_score']['assertion_pass_rate']['total'] == 28
for row in inputs:
    assert row['basic'] + row['specialized'] == row['total']
    assert row['assertions_passed'] == sum(a['result'] == 'PASS' for a in row['assertions'])
    assert 3 <= len(row['assertions']) <= 5

(ROOT / 'eval_report_bio-bam-statistics_result.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')

rows = '\n'.join(f"| {x['index']} | {x['type']} | {x['basic']}/40 | {x['specialized']}/60 | {x['total']}/100 | {x['assertions_passed']}/{x['assertions_total']} PASS | ✅ |" for x in inputs)
details = []
for x in inputs:
    checks = '\n'.join(f"- [PASS] {a['text']} — {a['note']}" for a in x['assertions'])
    details.append(f"### Input {x['index']} — {x['type']}\n\n**Prompt class:** {x['label']}\n\n**Execution:** {x['note']}\n\n**Scores:** Basic {x['basic']}/40 | Specialized {x['specialized']}/60 | Total {x['total']}/100\n\n**Assertions:**\n{checks}\n")
viewer = f'''# Eval Viewer — bio-bam-statistics

Generated: 2026-09-23

## Evaluation context

- Source: `{SOURCE}`
- Category / mode / complexity: Data Analysis / D / Complex (7 inputs)
- Final-pass exception: `auditor_independent: false`; final pass: fixed and audited under one brief, see CHECKPOINT.md.
- Prior evidence archived unchanged: `F:/OpenScience/audits/_pre-fix-20260922/bio-bam-statistics/`.

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---:|---:|---:|---:|---:|---:|
{rows}

**Execution average:** {execution_avg}/100  
**Assertion pass rate:** {passed}/{total_assertions} (100%)  
**Static:** 90/100  
**Final:** 92/100 — ⭐ Production Ready — deployable: true  
**Vetoes:** Skill PASS; Research PASS.

## What ran

- Regression scripts: `t0_stability_determinism.sh`, `t1_canonical.sh`, `t2_planted.sh`, `t3_edge.sh`, `t4_depth_cap.sh`, `t5_batch_plots.sh`, and `t6_scope.sh`.
- Fresh scripts: `phase2_fresh_deletion.sh`, `phase2_fresh_source_check.py`, and `phase2_fresh_adversarial.py`.
- Representative checked output: 10/10 deterministic qc_report runs with one distinct output; `BATCH_FAILS 0`; `REGION_TRUTH_MISMATCHES 0`; `SOFTCLIP_MISMATCHES 0`; 11 plot PNGs; MultiQC HTML 2,272,085 bytes; fresh deletion and adversarial assertions all PASS.

## Detailed outputs

{chr(10).join(details)}
## Recommendations

- [P2] Cite the assay thresholds and FREEMIX cut-offs.
- [P2] Add a reproducible whole-genome identity/contamination fixture.
'''
(ROOT / 'eval_viewer_bio-bam-statistics.md').write_text(viewer, encoding='utf-8')
print('ASSERT report_schema_invariants PASS')
print('ASSERT report_and_viewer_written PASS')
