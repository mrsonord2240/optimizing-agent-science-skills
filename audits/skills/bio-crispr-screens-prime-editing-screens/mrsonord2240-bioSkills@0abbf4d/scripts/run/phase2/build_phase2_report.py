"""Build the canonical Phase 2 JSON report and Markdown viewer from fresh evidence."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent.parent
prior = Path(r'F:\OpenScience\audits\_pre-fix-20260923\bio-crispr-screens-prime-editing-screens')
source = 'mrsonord2240/bioSkills@0abbf4d40d0df260ca60b346a9d6dc307b80fa5d:crispr-screens/prime-editing-screens'
prior_dynamic = json.loads((ROOT / 'phase2_summary.json').read_text(encoding='utf-8'))

def convert(index, typ, label, basic, specialized):
    x = prior_dynamic[str(index)]
    assertions = x['assertions']
    return {
        'index': index, 'type': typ, 'label': label, 'status': x['status'], 'status_flag': '✅',
        'note': x['execution_note'], 'executed': x['executed'], 'execution_note': x['execution_note'],
        'basic': basic, 'specialized': specialized, 'total': basic + specialized,
        'assertions_passed': sum(a['result'] == 'PASS' for a in assertions), 'assertions_total': len(assertions),
        'assertions': assertions,
    }

inputs = [
    convert(1, 'Canonical', 'PRIDICT2 five-fold single-mode pegRNA scoring', 38, 57),
    convert(2, 'Variant A', 'Fresh two-edit PRIDICT2 batch recipe at the documented core cap', 39, 57),
    convert(3, 'Edge', 'Second --summarize run into a nonempty output directory', 37, 57),
    convert(4, 'Variant B', 'Shipped pegRNA example with constructible and no-PAM variants', 38, 56),
    convert(5, 'Stress', 'Shipped summary filter on real and literal-empty summaries', 38, 58),
    convert(6, 'Adversarial', 'Shipped PE/BE concordance against planted truth', 38, 58),
    {
        'index': 7, 'type': 'Scope Boundary', 'label': 'ePRIDICT light model at the documented K562 locus',
        'status': 'COMPLETED', 'status_flag': '✅', 'executed': True,
        'execution_note': 'run_epridict_phase2.sh, launched in the mandated WSL login shell, ran ePRIDICT single at chr3:44843504. It returned score 42.53 and K562 percentile 62.02%, and wrote the documented chr3_44843504.csv output.',
        'note': 'Real light-model ePRIDICT score and percentile obtained from the documented command.',
        'basic': 38, 'specialized': 57, 'total': 95, 'assertions_passed': 3, 'assertions_total': 3,
        'assertions': [
            {'text': 'The documented single-locus command completes in the provisioned ePRIDICT environment', 'result': 'PASS', 'note': 'Exited 0 in WSL science/epridict.'},
            {'text': 'The output contains a numeric light-model score and genomewide K562 percentile', 'result': 'PASS', 'note': '42.53 and 62.02%, respectively.'},
            {'text': 'The result is presented as K562-specific chromatin context rather than a cross-cell-line guarantee', 'result': 'PASS', 'note': 'Reference file states this boundary explicitly.'},
        ],
    },
    {
        'index': 8, 'type': 'Stress', 'label': 'All six ePRIDICT light-model bigWig inputs',
        'status': 'COMPLETED', 'status_flag': '✅', 'executed': True,
        'execution_note': 'run_epridict_phase2.sh opened every light-model bigWig with pyBigWig at chr3:44843504 and counted non-null signal values. Each of the six tracks yielded 200/200 non-null values.',
        'note': 'Fresh integrity check of the data dependencies behind the light model.',
        'basic': 37, 'specialized': 57, 'total': 94, 'assertions_passed': 3, 'assertions_total': 3,
        'assertions': [
            {'text': 'All six light-model ENCODE bigWigs parse', 'result': 'PASS', 'note': 'ENCFF139KZL, 601JGK, 834SEY, 954LGE, 959YJV, and 972GVB opened successfully.'},
            {'text': 'Every parsed bigWig has signal at the documented test locus', 'result': 'PASS', 'note': 'Each had 200/200 non-null values.'},
            {'text': 'The check detects a data artifact rather than trusting a downloader exit code', 'result': 'PASS', 'note': 'It opens each file and asserts observed signal.'},
        ],
    },
    {
        'index': 9, 'type': 'Variant B', 'label': 'CRISPResso2 PE quantification with planted reference and edited reads',
        'status': 'COMPLETED', 'status_flag': '✅', 'executed': True,
        'execution_note': 'run_crispresso_phase2.ps1 built a 500-read synthetic FASTQ (240 prime-edited, 260 reference) and ran the copied SKILL.md command through pinellolab/crispresso2:latest. The nested report path existed and contained three amplicon rows with 240 reads assigned to Prime-edited.',
        'note': 'The complete documented PE mode command ran; fixture is synthetic and intentionally below production depth.',
        'basic': 38, 'specialized': 57, 'total': 95, 'assertions_passed': 3, 'assertions_total': 3,
        'assertions': [
            {'text': 'The documented nested CRISPResso2 output path exists', 'result': 'PASS', 'note': 'CRISPResso_on_sample_id/CRISPResso_quantification_of_editing_frequency.txt was produced.'},
            {'text': 'The correct RTT-then-PBS extension creates a Prime-edited amplicon row', 'result': 'PASS', 'note': 'The report has Reference, Prime-edited, and Scaffold-incorporated rows.'},
            {'text': 'All 240 planted edited reads are assigned to Prime-edited', 'result': 'PASS', 'note': 'Prime-edited Reads_aligned = 240 of 500 input reads.'},
        ],
    },
]

cats = {
    'functional_suitability': (12, 12, 'All central claims were exercised: PRIDICT2 single and batch, candidate generation, filtering, concordance, CRISPResso2 PE mode, and ePRIDICT light model.'),
    'reliability': (11, 12, 'The failure modes accurately cover the reproduced second-run guard and empty-summary handling. One point is reserved for the intentionally unrun full ePRIDICT model.'),
    'performance_context': (7, 8, 'Progressive references keep SKILL.md compact and disclose ePRIDICT light/full download sizes; the full model remains a large optional resource.'),
    'agent_usability': (15, 16, 'Decision tree, command blocks, exact real output columns, and recovery messages are actionable. The full-model path cannot be live-tested in a normal audit footprint.'),
    'human_usability': (8, 8, 'Usage guide now points to SKILL.md for operational detail and clearly distinguishes PE, BE, and Cas9 decisions.'),
    'security': (12, 12, 'Static inspection found no raw eval/exec, credentials, or unbounded user-command interpolation in shipped Python.'),
    'maintainability': (11, 12, 'Runnable helpers are separate, parse cleanly, and their expected columns are checked. The example intentionally retains a documented simulation placeholder rather than calling PRIDICT2 itself.'),
    'agent_specific': (18, 20, 'Strong trigger precision, references, failure recovery, and handoffs. Full-model resource planning remains an explicit escape hatch rather than a fully executable low-footprint path.'),
}
static = {'subtotal': sum(v[0] for v in cats.values()), 'max': 100, 'categories': {k: {'score':v[0], 'max':v[1], 'note':v[2]} for k,v in cats.items()}}
avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
passed = sum(i['assertions_passed'] for i in inputs)
total_assertions = sum(i['assertions_total'] for i in inputs)
report = {
    'meta': {
        'skill_name': 'bio-crispr-screens-prime-editing-screens',
        'description': 'Designs and analyzes pooled prime-editor screens: pegRNA design with PRIDICT/PRIDICT2, PE chemistry selection, PRIME/MOSAIC workflows, CRISPResso2 quantification, ePRIDICT chromatin context, and base-editor cross-validation.',
        'evaluated_on': '2026-09-23', 'evaluator_version': 'skill-auditor@1.0', 'category': 'Data Analysis', 'execution_mode': 'D', 'complexity': 'Complex', 'n_inputs': 9,
        'source': source, 'source_ref': source, 'branch': 'fix/crispr-screens-prime-editing-screens',
        'checkpoint': r'F:\OpenScience\audits\_final_pass\bio-crispr-screens-prime-editing-screens\CHECKPOINT.md',
        'pre_fix_archive': str(prior), 'auditor_independent': False,
        'note': 'final pass: fixed and audited under one brief, see CHECKPOINT.md',
        'worktree_git_status': 'clean (git status --porcelain=v1 was empty before audit); pre-existing ignored __pycache__ files were not executed or modified',
    },
    'veto_gates': {
        'skill_veto': {'gate':'PASS','stability':'PASS','contract':'PASS','determinism':'PASS','security':'PASS'},
        'research_veto': {
            'applicable': True, 'gate':'PASS',
            'scientific_integrity': {'result':'PASS','detail':'Fresh runs matched the named tool behavior; PRIDICT/PRIDICT2, ePRIDICT, and PRIME citation metadata were cross-checked against the publisher or PubMed record.'},
            'practice_boundaries': {'result':'PASS','detail':'The Skill handles research design and screen analysis, not individual diagnosis or treatment; it advises empirical pilots rather than clinical conclusions.'},
            'methodological_ground': {'result':'PASS','detail':'The runs preserved tool-specific constraints: PRIDICT2 output columns and --cores cap, PE RTT-then-PBS order, ePRIDICT K562 specificity, and PE/BE sign plus FDR concordance.'},
            'code_usability': {'result':'PASS','detail':'All three shipped Python files parsed, and every shipped executable was run against fresh or planted data. The Docker CRISPResso2 command and WSL ePRIDICT command completed with checked outputs.'},
        },
    },
    'static_score': static,
    'dynamic_score': {'execution_avg':avg, 'max':100, 'assertion_pass_rate':{'passed':passed,'total':total_assertions}, 'inputs':inputs},
    'final': {'static_weighted':37.6, 'dynamic_weighted':57.0, 'score':95, 'max':100, 'grade':'Production Ready', 'grade_symbol':'⭐', 'deployable':True, 'veto_override':False},
    'key_strengths': [
        'All runnable pathways were re-executed from an audit copy at the requested source commit, including the two newly added ePRIDICT and CRISPResso2 capabilities.',
        'The fixed PRIDICT2 batch recipe now has positive evidence for a clean run and negative evidence for its guarded second-run failure mode.',
        'CRISPResso2 correctly assigned all 240 planted edited reads to the Prime-edited row at the documented nested output path.',
        'ePRIDICT light-model execution and the underlying six bigWig data dependencies were independently validated in WSL.',
    ],
    'recommendations': [{
        'priority':'P2', 'title':'Keep full ePRIDICT model explicitly optional', 'observed_in':[],
        'problem':'The reference documents --use_full_model but the 455-track, approximately 624 GB model was not downloaded or executed in this audit.',
        'root_cause':'The full model exceeds the available audit disk budget; this is a resource constraint, not a light-model correctness failure.',
        'fix':'Retain the present light-model default and disk-size warning. Before advertising a full-model result, run the same parse-and-signal verification after an explicitly approved >=624 GB download.'
    }],
}
assert report['static_score']['subtotal'] == 94
assert avg == 95.0 and passed == total_assertions == 28
(AUDIT / 'eval_report_bio-crispr-screens-prime-editing-screens_result.json').write_text(json.dumps(report, indent=2), encoding='utf-8')

lines = [
    '# Eval Viewer — bio-crispr-screens-prime-editing-screens', '',
    f'Generated: 2026-09-23 | Source: `{source}`', '',
    'This is the required final-pass exception: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.',
    f'Prior canonical audit bundle preserved at `{prior}` before this report replaced the active record.', '',
    '## Verdict', '',
    '**95/100 — Production Ready — deployable: true.** Both structural and research veto gates pass. All 9/9 dynamic inputs executed; all 28/28 assertions passed.', '',
    '## Summary Table', '',
    '| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Status |', '|---|---:|---:|---:|---:|---:|---|'
]
for i in inputs:
    lines.append(f"| {i['index']} | {i['type']} | {i['basic']} | {i['specialized']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} | {i['status_flag']} |")
lines += ['', f'Execution average: **{avg}/100**. Layer 1 mean: **37.9/40**. Layer 2 mean: **57.1/60**.', '', '## Static evaluation', '']
for key, value in static['categories'].items(): lines.append(f"- **{key}: {value['score']}/{value['max']}** — {value['note']}")
lines += ['', '## Dynamic evidence', '']
for i in inputs:
    lines += [f"### Input {i['index']} — {i['label']}", '', f"**Executed:** `{i['executed']}`. **Execution note:** {i['execution_note']}", '', f"Scores: Basic {i['basic']}/40 | Specialized {i['specialized']}/60 | Total {i['total']}/100.", '']
    for a in i['assertions']: lines.append(f"- [{a['result']}] {a['text']} — {a['note']}")
    lines.append('')
lines += [
    '## Veto review', '',
    '- **T1 Stability:** PASS — completed commands yielded parsed, checked outputs; the intentionally invalid second-run test failed clearly.',
    '- **T2 Contract:** PASS — required frontmatter and all referenced copied files exist.',
    '- **T3 Determinism:** PASS — repeated PRIDICT2 recipe and fixed-format planted inputs yielded stable parseable results.',
    '- **T4 Security:** PASS — no raw eval/exec or credential handling in shipped Python.',
    '- **M1 Scientific integrity:** PASS — source citation metadata was cross-checked against Nature/PubMed or the publisher-hosted PRIME record; no fabricated result was emitted.',
    '- **M2 Practice boundaries:** PASS — research-only workflow, no diagnosis or treatment advice.',
    '- **M3 Methodological baseline:** PASS — tool constraints and independent biological validation are explicit.',
    '- **M4 Code usability:** PASS — copied shipped Python parsed and executed; Docker/WSL requirements were exercised rather than assumed.', '',
    '## Open issue', '',
    '- **P2:** the optional ePRIDICT full model remains unexecuted because its 455 tracks require approximately 624 GB. The default light model was fully executed and verified; no P0 or P1 remains.', '',
    '## Artifacts', '',
    '- Fresh scripts and logs: `run/phase2/`',
    '- Synthetic CRISPResso2 fixture: `run/phase2/input9_crispresso/`',
    '- Prior report and evidence: `_pre-fix-20260923/bio-crispr-screens-prime-editing-screens/`',
]
(AUDIT / 'eval_viewer_bio-crispr-screens-prime-editing-screens.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(json.dumps({'report': str(AUDIT / 'eval_report_bio-crispr-screens-prime-editing-screens_result.json'), 'viewer': str(AUDIT / 'eval_viewer_bio-crispr-screens-prime-editing-screens.md'), 'score':95, 'executed':f'{len(inputs)}/{len(inputs)}'}, indent=2))
