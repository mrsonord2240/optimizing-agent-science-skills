"""Build report.json and source-identity.json for the initial audit of bio-splicing-quantification.
Run: python build_record.py <run_root>   (run_root = ...\\run-initial-1)"""
import json, sys, os, subprocess
root = sys.argv[1]
SKILL = r'F:\OpenScience\wt\norm-bio-splicing-quantification\skills\bio-splicing-quantification'
files = json.loads(subprocess.check_output([sys.executable, os.path.join(root, 'scripts', '00_manifest.py'), SKILL]).decode().splitlines()[0])
IDENT = '1e34dbd9664e334b3feb336a3d624ec99d39ca9b5ad9a056f1f7142448bd489c'

identity = {
    'origin': {
        'repository': 'GPTomics/bioSkills',
        'commit': 'd91ed3d563019e649dc854c56ccd62551359488a',
        'path': 'alternative-splicing/splicing-quantification',
        'subtree': '6e11b64e5f1c319983ec851f3d922655291db35a',
        'checkout': r'F:\optimizing-agent-science-skills\external\GPTomics__bioSkills',
        'status': 'clean',
        'files': [
            {'path': 'SKILL.md', 'git_blob': '686fd3bbca0044c82f86e05ce7cf3231e2fdcb83'},
            {'path': 'examples/quantify_splicing.py', 'git_blob': '43c5d63b74589c582c327559064c47e53696a47a'},
            {'path': 'usage-guide.md', 'git_blob': '37b3fa27d836861548f6e32755e4b72dd757d4a4'},
        ],
        'normalization_note': 'The audited tree moves examples/quantify_splicing.py to scripts/, extracts two references/ files from SKILL.md, and edits SKILL.md and usage-guide.md; origin identifies the source Skill subtree, not a one-to-one file mapping.',
    },
    'candidate': {
        'branch': 'normalize/bio-splicing-quantification',
        'commit': '29f5446',
        'path': SKILL,
        'status_before': 'untracked Skill subtree only',
        'status_after_execution': 'untracked Skill subtree only; candidate files unchanged (preflight re-verified)',
        'content_sha256': IDENT,
        'content_manifest': {
            'file_count': 5,
            'bytes': 37504,
            'recipe': 'relative POSIX path, byte count, and lowercase SHA-256 separated by TAB; records sorted by path and separated by LF; no trailing LF',
        },
    },
    'files': files,
    'tooling': {
        'tools_md': r'F:\OpenScience\audits\bio-splicing-quantification\TOOLS.md',
        'tools_md_sha256': '48cde79a160428e3ae04f5505701b446bae203983b02aca6a9f3f21cdd1e00ed',
        'rubric_zip_sha256': 'recorded from repository skill-auditor.zip (extracted to run-root rubric/)',
        'environment': 'WSL science: as-core (rMATS-turbo 4.4.0, regtools 1.0.0, leafcutter 0.2.9 scripts, STAR 2.7.11b; pandas 2.3.3, statsmodels 0.15.0), as-suppa (SUPPA 2.4, statsmodels 0.14.6, pandas 3.0.6), as-irfinder (IRFinder 1.3.1); combined env sha256 20c07bbbf63a972c04364225b028c9c83e0ee45a0ee9ee775cc56d7a8c26ad3c; staged public data (nf-core rnasplice chrX 2v2, synthetic planted)',
    },
    'candidate_cache_artifacts_after_execution': [],
}

A = lambda t, r, n: {'text': t, 'result': r, 'note': n}
inputs = [
    dict(index=1, type='Canonical', label='rMATS-turbo on real chrX 2v2 BAMs, then parse PSI per the Skill', status='PARTIAL', status_flag='\u274c',
         note='rMATS ran with the Skill flags (rc 0, 958 SE events); the inline pandas snippet raised TypeError and the shipped parser reports wrong mean_PSI on 310 of 958 SE rows',
         basic=24, specialized=34, assertions=[
             A('rMATS runs with the flags the Skill states and writes all five *.MATS.JC.txt files', 'PASS', 'rc 0; SE 958, A5SS 216, A3SS 251, MXE 51, RI 174 rows'),
             A('The SKILL.md inline snippet computes mean PSI from the real JC file', 'FAIL', 'TypeError: IncLevel1/2 are comma strings and startswith(IncLevel) also matches IncLevelDifference (SQ-01)'),
             A('parse_rmats_output returns the mean of the replicate IncLevel values', 'FAIL', 'mean_PSI includes IncLevelDifference: 310/958 SE rows differ from the true mean, up to 0.5 (e.g. true 0.5 reported 0.0) (SQ-03)'),
             A('Skill PSI formula reproduces rMATS IncLevel on real data', 'PASS', '1465 replicate values, max abs diff 0.0005 with IncFormLen 148 / SkipFormLen 74'),
             A('Reliability filter covers both conditions', 'FAIL', 'Both snippet and script filter on SAMPLE_1 only; 47 vs 50 events pass in SAMPLE_2 vs SAMPLE_1 (SQ-03)')]),
    dict(index=2, type='Variant A', label='rMATS on planted hand-checkable SE data, effective-length PSI', status='COMPLETED', status_flag='\u2705',
         note='IJC 80,80,80 / SJC 10,10,12 gives IncLevel1 0.8,0.8,0.769 and a 0.587 difference, matching hand values; JC IncFormLen 98 / SkipFormLen 49',
         basic=33, specialized=50, assertions=[
             A('rMATS IncLevel equals the hand-computed PSI', 'PASS', '0.8/0.8/0.769 vs 0.8/0.8/0.769; IncLevel2 0.2/0.2/0.208'),
             A('Effective-length formula in the Skill gives the planted PSI and differs from naive counts', 'PASS', 'formula 0.8000, naive 0.8889 (about 11% bias)'),
             A('IncLevelDifference sign matches --b1 minus --b2', 'PASS', '+0.587 with b1 the high group'),
             A('IncFormLen description matches the JC file', 'FAIL', 'Skill says IncFormLen includes exon body bases; JC value 98 = 2*(50-1), the body appears only in JCEC (149) (SQ-08)')]),
    dict(index=3, type='Variant B', label='SUPPA2 PSI from TPM via run_suppa2_quantification, planted and real chrX, concordance with rMATS', status='COMPLETED', status_flag='\u26a0\ufe0f',
         note='Planted TPM gives PSI 0.8/0.2/0.5 exactly; real chrX yields all seven psi files; SE r=0.864, A5 r=0.718, A3 r=0.849 vs rMATS; undocumented TPM header and statsmodels limits reproduced',
         basic=31, specialized=46, assertions=[
             A('SUPPA2 PSI equals the planted PSI', 'PASS', 'G1;SE:chrP:200-501:600-901:+ = 0.8, 0.2, 0.5'),
             A('SS yields A5+A3 and FL yields AF+AL files as the script states', 'PASS', 'seven psi files from five -e codes'),
             A('Independent tools agree on direction and magnitude for matched events', 'PASS', 'SE 892 matched events r=0.864; A5SS 161 r=0.718; A3SS 197 r=0.849, positive, so the A5/A3 sign claim holds'),
             A('Skill states the TPM header contract and a SUPPA2 dependency pin that works', 'FAIL', 'pandas-default header gives "No expression values have been buffered" and no output; suppa.py fails ImportError (multipletests) with statsmodels 0.15.0 (SQ-06)'),
             A('filter_reliable_events matches the documented dynamic range', 'FAIL', 'hardcodes mean PSI 0.1-0.9; Skill states 0.05-0.95 (SQ-07)')]),
    dict(index=4, type='Edge', label='Shipped parser on the other four rMATS event types', status='ERROR', status_flag='\u274c',
         note='parse_rmats_output raises KeyError for A5SS, A3SS, MXE and RI; only SE works',
         basic=16, specialized=20, assertions=[
             A('parse_rmats_output handles every event_type its docstring lists', 'FAIL', "KeyError ['exonStart_0base', 'exonEnd'] not in index for A5SS, A3SS, MXE, RI (SQ-02)"),
             A('Failure is reported with an actionable message', 'FAIL', 'raw pandas KeyError after printing event counts'),
             A('SE path returns reliable events', 'PASS', '50 reliable of 958 at >=20 reads on tiny chrX data')]),
    dict(index=5, type='Stress', label='regtools junctions + leafcutter clustering on STAR-style BAMs, with and without XS tags', status='PARTIAL', status_flag='\u274c',
         note='BAMs without XS give strand ? for every junction and leafcutter exits 0 with 0 clusters; XS-tagged BAMs give 115 clusters at -m 5; the Skill never mentions XS or --outSAMstrandField',
         basic=24, specialized=34, assertions=[
             A('regtools extract with the Skill flags succeeds on the aligned BAMs', 'PASS', 'rc 0 for all four BAMs'),
             A('Junction strand is resolved for the Skill route (STAR 2-pass BAM, -s XS)', 'FAIL', 'noXS: 2,838 of 2,838 junctions strand ?; XS: 1,398 + / 1,343 - / 99 ? (SQ-04)'),
             A('leafcutter clustering yields clusters for the stated route', 'FAIL', '0 clusters from untagged BAMs at -m 5 (rc 0, silent); 115 from tagged BAMs'),
             A('Skill warns about XS-tag prerequisite', 'FAIL', 'no mention; STAR default outSAMstrandField None confirmed'),
             A('Skill -m 50 default is workable on realistic data', 'PASS', 'tiny test data give 0 clusters at -m 50; not a Skill defect')]),
    dict(index=6, type='Scope Boundary', label='IRFinder intron retention route from references/', status='PARTIAL', status_flag='\u274c',
         note='The literal reference command fails (rc 1, "-r is required"); the real syntax IRFinder -m FastQ works on single-end FASTQ (7,955 intron rows); IRFinder-S 2.0 is not what installs',
         basic=24, specialized=32, assertions=[
             A('Literal reference command IRFinder FastQ -r REF/ -d out sample.fastq runs', 'FAIL', 'Argument error: -r is required, rc 1; FastQ is a -m value (SQ-05)'),
             A('Corrected command IRFinder -m FastQ -r REF -d out reads.fq.gz produces IR ratios', 'PASS', '7,955 rows in IRFinder-IR-nondir.txt in 15 s on chrX reads'),
             A('Skill gives how to obtain the reference and the claimed IRFinder-S 2.0 tool', 'FAIL', 'no BuildRef step; installable release is IRFinder 1.3.1 (SQ-05)'),
             A('Scope: IR route stays within quantification', 'PASS', 'no differential testing claimed')]),
]
for i in inputs:
    i['assertions_passed'] = sum(a['result'] == 'PASS' for a in i['assertions'])
    i['assertions_total'] = len(i['assertions'])
    i['total'] = i['basic'] + i['specialized']
    assert 3 <= i['assertions_total'] <= 5
n_pass = sum(i['assertions_passed'] for i in inputs); n_tot = sum(i['assertions_total'] for i in inputs)
avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)

cats = {
    'functional_suitability': (7, 12, 'Broad, accurate taxonomy and tool-selection guidance; the rMATS formula, SUPPA2 and regtools commands reproduce, but the inline snippet, the shipped parser (4 of 5 event types), mean_PSI and the IRFinder command are wrong'),
    'reliability': (6, 12, 'Raw KeyError/TypeError on documented use, silent exit 0 with zero clusters on untagged BAMs, run_suppa2_quantification silently skips missing event files'),
    'performance_context': (6, 8, 'SKILL.md 290 lines with failure modes and IR/microexon detail routed to references; the tool matrix and decision tree overlap'),
    'agent_usability': (11, 16, 'Decision tables, quality thresholds and reconciliation rules are clear; no format contract for rMATS BAM lists or SUPPA2 TPM and no XS prerequisite'),
    'human_usability': (6, 8, 'Good pitfalls and prompts; errors are uninformative and unsupported benchmark figures are stated as fact'),
    'security': (11, 12, 'No credentials; subprocess calls use argument lists; no shell interpolation'),
    'maintainability': (7, 12, 'Small modular script, but SE-only column assumptions, hardcoded 0.1-0.9 filter, no tests, no dependency pins'),
    'agent_specific': (15, 20, 'Precise trigger description; progressive disclosure works; Related Skills names do not resolve on the shelf and MAJIQ/VAST are not labeled not-executed'),
}
static = sum(v[0] for v in cats.values())
sw = round(static * 0.4, 1); dw = round(avg * 0.6, 1); score = round(sw + dw)

recs = [
    ('P1', 'SKILL.md inline rMATS snippet raises TypeError', [1], 'se_jc[inc_cols].mean(axis=1) fails on every real rMATS JC file: IncLevel1/2 are comma-separated strings and startswith(IncLevel) also selects IncLevelDifference.', 'The snippet was written for numeric columns.', 'Split IncLevel1 and IncLevel2 on commas, convert to float with NA handling, average per event, and exclude IncLevelDifference; execute against a real JC file. (SQ-01)'),
    ('P1', 'parse_rmats_output fails for A5SS/A3SS/MXE/RI', [4], 'The function selects exonStart_0base and exonEnd, which exist only in SE files; A5SS, A3SS, MXE and RI raise KeyError although its docstring lists them.', 'Column names are hardcoded for SE.', 'Select coordinate columns per event type (longExon*/shortE*/flanking*, 1stExon*/2ndExon*, riExon*) or return only common columns; test all five types. (SQ-02)'),
    ('P1', 'Shipped mean_PSI is silently wrong; filter ignores group 2', [1], 'The script averages IncLevelDifference with replicate PSI values (310 of 958 SE rows differ, up to 0.5; e.g. true 0.5 reported 0.0), and both snippet and script apply read-count reliability to SAMPLE_1 only.', 'Prefix match on IncLevel and SAMPLE_1-only filtering.', 'Restrict to IncLevel1 and IncLevel2, report group-wise means, and apply the junction-read filter to both groups; add a regression on the planted data. (SQ-03)'),
    ('P1', 'regtools/leafcutter route silently empty without XS tags', [5], 'Without XS tags every junction gets strand ? and leafcutter exits 0 with zero clusters (115 clusters from XS-tagged BAMs); the Skill never states the XS prerequisite or STAR --outSAMstrandField intronMotif.', 'STAR default outSAMstrandField is None; the Skill assumes tagged BAMs.', 'State the XS requirement beside the regtools command (STAR --outSAMstrandField intronMotif or add XS), and tell the reader that zero clusters means a prerequisite or -m problem. (SQ-04)'),
    ('P1', 'IRFinder command and tool version do not run as written', [6], 'IRFinder FastQ -r REF/ -d out sample.fastq exits 1 (-r is required); the real form is IRFinder -m FastQ. The reference build is undocumented, and IRFinder-S 2.0+ is not what installs (IRFinder 1.3.1; BuildRef is FTP-only, use BuildRefFromSTARRef).', 'Command written from memory; version floor not checked.', 'Replace with the working IRFinder -m FastQ form, document reference building, and state which IRFinder release was exercised; label IRFinder-S 2.0 unverified if not obtainable. (SQ-05)'),
    ('P2', 'SUPPA2 TPM header and statsmodels pin not stated', [3], 'A pandas-default TPM header yields no output (psiCalculator: no expression values buffered), and SUPPA 2.4 fails on import with statsmodels 0.15.0; 0.14.6 works.', 'Input contract and dependency ceiling are undocumented.', 'Document the header-without-index-name TPM format and pin statsmodels<0.15 in the prerequisites. (SQ-06)'),
    ('P2', 'filter_reliable_events range disagrees with the Skill', [3], 'The script hardcodes mean PSI 0.1-0.9 while the quality table says 0.05-0.95 and claims rMATS/SUPPA2 default filters drop near-constitutive events; rMATS output contains PSI 0 and 1 rows.', 'Threshold duplicated and unparameterized.', 'Expose the bounds as parameters defaulting to the documented range and correct the default-filter claim. (SQ-07)'),
    ('P2', 'IncFormLen description wrong for JC files', [2], 'The Skill says IncFormLen adds exon body bases; JC IncFormLen is 2*(L-1) (98 at L=50) and the body appears only in JCEC (149).', 'JC and JCEC lengths conflated.', 'State the JC and JCEC lengths separately. (SQ-08)'),
    ('P2', 'MAJIQ V3 and VAST-TOOLS not labeled not-executed; benchmark figures unsourced', [], 'MAJIQ V3 commands and Zarr claims (restricted licence) and VAST-TOOLS (heavy VASTDB) are presented without an unexecuted/unverified label; figures such as FDR 15-30% and 14% novel-junction loss lack inline evidence.', 'Surfaces that cannot be run are written like tested ones.', 'Add a one-line not-executed label for MAJIQ and VAST-TOOLS and mark unsourced figures as literature claims. (SQ-09)'),
    ('P2', 'Related Skills names do not resolve on the shelf', [], 'differential-splicing and others lack the bio- prefix, and read-alignment/star-alignment and rna-quantification/alignment-free-quant (both required upstream) have no shelf Skill.', 'Provider-style paths were kept in normalization.', 'Use shelf IDs where they exist and describe or drop the two missing upstream steps. (SQ-10)'),
    ('P2', 'Input formats and tool provenance not stated', [], 'rMATS --b1/--b2 list-file format is not described, leafcutter_cluster_regtools.py has no stated source (usage-guide installs only the R package), and there is no Skill-root LICENSE.', 'Prerequisites written for a reader who already knows the tools.', 'Describe the comma-separated BAM list, name where the clustering script comes from, and add a LICENSE. (SQ-11)'),
]
report = {
    'meta': {
        'skill_name': 'bio-splicing-quantification',
        'description': 'Quantifies alternative splicing as PSI from RNA-seq with rMATS-turbo, SUPPA2, MAJIQ V3, leafcutter, VAST-TOOLS, Shiba and IRFinder-S, with event taxonomy, tool selection, quality thresholds and reconciliation rules.',
        'evaluated_on': '2026-10-03',
        'evaluator_version': 'skill-auditor@1.0',
        'category': 'Data Analysis',
        'execution_mode': 'D',
        'complexity': 'Complex',
        'n_inputs': len(inputs),
        'performed_by': 'Claude (Anthropic) initial-audit worker, lane 2',
        'auditor_independent': True,
    },
    'veto_gates': {
        'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
        'research_veto': {
            'applicable': True, 'gate': 'FAIL',
            'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated values; planted PSI, formula and cross-tool concordance reproduce'},
            'practice_boundaries': {'result': 'PASS', 'detail': 'Research-method Skill with no clinical conclusions; disease signatures are cited literature'},
            'methodological_ground': {'result': 'PASS', 'detail': 'Effective-length PSI, tool-family reconciliation and sign conventions held; SUPPA2 and rMATS agree in direction'},
            'code_usability': {'result': 'FAIL', 'detail': 'Documented code does not run on real output: the inline snippet raises TypeError on every real rMATS JC file and parse_rmats_output raises KeyError for 4 of 5 listed event types (SQ-01, SQ-02); the SE path silently returns wrong mean_PSI (SQ-03)'},
        },
    },
    'static_score': {'subtotal': static, 'max': 100, 'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in cats.items()}},
    'dynamic_score': {'execution_avg': avg, 'max': 100, 'assertion_pass_rate': {'passed': n_pass, 'total': n_tot}, 'inputs': inputs},
    'final': {'static_weighted': sw, 'dynamic_weighted': dw, 'score': score, 'max': 100, 'grade': 'Reject', 'grade_symbol': '\u274c', 'deployable': False, 'veto_override': True},
    'key_strengths': [
        'Tool-family taxonomy, selection matrix and reconciliation rules are scientifically sound and useful',
        'rMATS effective-length PSI formula, SUPPA2 PSI and A5/A3 sign claims reproduce on planted and real data (rMATS vs SUPPA2 r 0.72-0.86)',
        'Progressive disclosure keeps detail in references/ and the SUPPA2 wrapper and filter run correctly',
        'No credentials, and subprocess calls use argument lists',
    ],
    'recommendations': [dict(priority=p, title=t, observed_in=o, problem=pr, root_cause=rc, fix=f) for p, t, o, pr, rc, f in recs],
}
json.dump(report, open(os.path.join(root, 'report.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
json.dump(identity, open(os.path.join(root, 'source-identity.json'), 'w', encoding='utf-8'), indent=2)
print('static', static, 'avg', avg, 'assertions', n_pass, n_tot, 'weighted', sw, dw, 'numeric score', score)
