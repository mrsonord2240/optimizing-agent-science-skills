#!/usr/bin/env python3
"""Assemble eval_report_bio-sashimi-plots_result.json from the scores/assertions decided after the runs (values typed here,
each backed by a run in run/out and listed in eval_viewer_bio-sashimi-plots.md). Validates the schema's pre-emit checklist."""
import json, pathlib

OUT = pathlib.Path(r'F:\OpenScience\audits\bio-sashimi-plots')
A = lambda t, r, n: {'text': t, 'result': r, 'note': n}

inputs = [
    dict(index=1, type='Canonical', label='ggsashimi Control v Treatment overlay on planted 3v3 BAMs + edge semantics + ggplot2 pin (regression of pre-fix inputs 1 and 3)',
         executed=True, execution_note='SKILL.md block 02 run verbatim in as-viz-gg34 (ggplot2 3.4.4); same command in as-viz-gg35 (3.5.2) and as-viz (4.0.3); 12 edge runs in scripts/i1c_edge.sh. PNGs viewed.',
         status='COMPLETED', note='PDF 18,346 B; 6/6 labels = pysam group means (41/11/39, 10/39/10); 3.4.4 aligned, 3.5.2 and 4.0.3 gene model shifted and ticks clipped; -M default 1, -M 10 shows 11 (10.33 without filter), -C alone red/green, no -C grey, -s gives _+/_-',
         basic=36, specialized=56, assertions=[
             A('SKILL.md ggsashimi block runs verbatim on the planted BAMs and writes a non-empty PDF', 'PASS', 'rc 0, 18,346 B PDF, plus SVG and PNG variants'),
             A('Arc labels equal independent pysam group means (mean_j, half to even)', 'PASS', 'LABELS_OK 6/6 against jtruth.py (own CIGAR scan)'),
             A('Group colours and gene-model alignment are right under the pinned ggplot2 3.4.4 and the pin claim reproduces', 'PASS', 'viewed: blue/orange, exon edges line up with arcs; 3.5.2 and 4.0.3 shift the gene model and clip tick labels; arc labels unchanged'),
             A('Corrected defaults and claims reproduce (-M default 1 and inclusive, per-sample -M before -A, -C/-P colours, -s file names, median_j)', 'PASS', '-M 10: Treatment 201-501 shows 11; grey without -C, red/green with -C only; st files _+/_-; median_j 40/10/40 and 10/40/10'),
             A('Silent-failure claims reproduce (missing BAM dropped rc 0, empty region rc 0, bad palette rc 0 and no file, --shrink StopIteration)', 'PASS', 'all four seen; bad contig, -A without -O and all-missing BAMs exit 1 with the quoted messages')]),
    dict(index=2, type='Variant A', label='Batch sashimi for significant rMATS SE hits, Ensembl contig X vs rMATS chrX (SKILL.md block + examples/plot_sashimi.py)',
         executed=True, execution_note='Blocks 02+03 run in sequence (block 03 needs the earlier block state) on planted rMATS (start -400) and real chrX rMATS (5 events); the example module driven from the run/skill copy incl. 5 failure paths.',
         status='COMPLETED', note='planted 1/1 and real 5/5 figures; region start clamped to 1; all 6 events LABELS_OK (6/6, 8/8, 5/5, 6/6, 4/4, 7/7); example batch 5/5, plot_specific_event works, bad contig/empty region/missing BAM/bad palette all raise',
         basic=35, specialized=54, assertions=[
             A('SKILL.md batch block writes a non-empty figure for every significant event on real Ensembl-contig data', 'PASS', 'planted 1 PDF, real chrX 5 PDFs (DMD, GEMIN8, PDZD11, RP11-357C3.3, TAZ); rMATS says chrX, BAM says X'),
             A('Contig mapping and the start clamp work', 'PASS', 'region strings X:62651743-... and chrP:1-1500 (start -400 clamped)'),
             A('Every figure label equals the independent pysam count', 'PASS', 'jtruth.py on the SVG variant of each event: 36 of 36 labels found'),
             A('examples/plot_sashimi.py runs its batch, specific-event and plot functions and raises on bad input', 'PASS', 'batch 5/5 PDFs; bad contig, empty region, bad region string, missing BAM, bad palette all raise; --shrink guard prints a warning and writes the figure'),
             A('Every recipe has a post-run figure-exists check', 'PASS', 'ggsashimi block, batch block and rmats2sashimiplot block assert; the example raises RuntimeError listing failed events')]),
    dict(index=3, type='Variant B', label='rmats2sashimiplot on rMATS SE output with group colours; forced failures (regression of pre-fix input 4)',
         executed=True, execution_note='SKILL.md block 04 verbatim on planted and real chrX; four forced-failure variants (i3_variants.py); tool exit codes checked without the assert (i3b_tool_rc.sh). PDFs viewed.',
         status='COMPLETED', note='planted PDF text 41/11/39, IncLevel 0.79 and 10/39/10, 0.20; real 5/5 PDFs, PDZD11 labels 6 / 1,2,3 = pysam means (zeros count in the mean); assert fires on all four failures ("wrote 0 of 1"); tool rc 0 (colour mismatch, missing group file) and 2 (-t SE)',
         basic=36, specialized=55, assertions=[
             A('The block writes one PDF per event (planted 1/1, real 5/5)', 'PASS', 'block rc 0; PDFs 27,925 B (planted) and 5 real files'),
             A('Arc labels and IncLevel in the figures match independent counts and rMATS', 'PASS', 'planted 41/11/39 and 10/39/10, 0.79/0.20; real PDZD11 6, 1, 2, 3 and TAZ 2,1 / 2,0,1 = pysam means with zeros included, half to even'),
             A('The figure-exists assert fires when the tool fails silently', 'PASS', 'A: colours without group info, B: missing group file, C: -t SE, D: one colour: block rc 1 and "rmats2sashimiplot wrote 0 of 1 figures"'),
             A('Documented error text and exit codes reproduce', 'PASS', '"Error: Must provide sample label and color..." rc 0, FileNotFoundError rc 0, "-t SE" rc 2; without --group-info and 6 colours a per-replicate figure is written'),
             A('rMATS chrX events plot against BAMs whose contig is X without manual mapping', 'PASS', 'real 5/5 with BAMs on contig X')]),
    dict(index=4, type='Stress', label='Real ENCODE 12-BAM locus, three groups, strandedness (regression of pre-fix input 5)',
         executed=True, execution_note='ggsashimi in as-viz-gg34 with the Skill flags and a 3-colour palette (public-data\\sashimi); per-strand runs. PNG viewed.',
         status='COMPLETED', note='10/10 aggregate labels and 12/12 per-sample labels equal pysam when every alignment record is counted (ggsashimi also counts secondary alignments); -s SENSE/ANTISENSE split correct (+ 98 203 110 / 125 228 165 / 11 124 43 / 71 127 82 = independent counts); 3 colours in order of first appearance',
         basic=35, specialized=54, assertions=[
             A('Three-group overlay draws three palette colours with fixed y-scale and an aligned gene model', 'PASS', 'green/orange/purple from a 3-colour -P file, all y-axes 0-750, arcs on exon edges'),
             A('Aggregate and per-sample labels equal independent pysam counts', 'PASS', '10/10 and 12/12; needs secondary alignments counted (43 to 178 per BAM): 2/10 without them'),
             A('-s SENSE/ANTISENSE routes junctions to _+ and _- files as documented and the counts match an independent strand count', 'PASS', 'SENSE_+ equals ANTISENSE_- and the numbers equal jtruth.py --strand SENSE'),
             A('Arc-count interpretation in the Skill agrees with what the tool counts', 'PASS', 'per alignment record with an N operation; the Skill says reads and does not mention secondary records (P2)')]),
    dict(index=5, type='Scope Boundary', label='pyGenomeTracks multi-track figure with regtools junction arcs (regression of pre-fix input 6)',
         executed=True, execution_note='SKILL.md blocks 08-11 run verbatim (planted 3v3, real chrX 2v2 XS-tagged BAMs) in as-viz-gg34 with regtools 1.0.0; PNG and PDF; BAM-track error rows (i10_error_rows.sh).',
         status='COMPLETED', note='planted BEDPE scores 153/150/147 = pysam sums over 6 replicates; real PDZD11 19/3/2 = pysam; figures viewed: intron gaps (-split), arcs on exon edges; junction arcs are cropped at the bottom of the height = 2 track; max_value = 200 makes real chrX coverage nearly invisible',
         basic=33, specialized=50, assertions=[
             A('The four blocks run verbatim and write bedGraphs, BEDPE and a figure', 'PASS', 'planted PDF 13,922 B; real PDF 13,967 B; 3 and 4,712 BEDPE lines'),
             A('BEDPE scores equal independent per-junction read sums', 'PASS', 'planted 153/150/147 (=40+44+38+10+12+9 ...); real 19/3/2 vs jtruth 7+6+3+3, 2+1, 2+0'),
             A('Coverage shows intron gaps and arcs land on the exon edges', 'PASS', 'viewed: planted arcs end at x of exon boundaries; introns empty because of -split'),
             A('Junction arcs are fully visible in the documented layout', 'FAIL', 'the arcs in both figures are cut off at the lower edge of the junction track (height = 2)'),
             A('BAM-track error rows match the observed pyGenomeTracks messages', 'PASS', '"the file_type bam does not exists" and "can not identify file type. Please specify the file_type"')]),
    dict(index=6, type='Adversarial', label='leafviz, Jutils, install lines and the hedged VOILA section (regression of pre-fix input 7)',
         executed=True, execution_note='leafviz workflow end to end on planted leafcutter 0.2.9 output (Shiny app started, curl HTTP 200); Jutils convert/heatmap/sashimi/venn on planted and real chrX; dry-run solve of the conda lines; git ls-remote; public MAJIQ docs read. VOILA itself not run (licence-gated).',
         status='COMPLETED', note='leafviz app HTTP 200 "LeafViz"; Jutils sashimi labels 40,44,38 / 10,10,12 / 40,36,42 = pysam, heatmap on 16 real events, venn 5/18-19/9 genes; conda solve OK (R 4.2.3, ggplot2 3.4.4); VOILA not run; MAJIQ V3 docs show `voila view sg.zarr file.psicov file.sgc`, the Skill block lacks the .sgc',
         basic=33, specialized=50, assertions=[
             A('leafviz workflow runs end to end and the app answers', 'PASS', 'gtf2leafcutter.pl, prepare_results.R, run_leafviz.R from leafviz/: "Listening on http://127.0.0.1:3595", HTTP 200 title LeafViz'),
             A('library(leafviz) does not exist and the wrong-directory error reproduces', 'PASS', 'requireNamespace("leafviz") FALSE; "App dir must contain either app.R or server.R"; wrong prefix gives "does not exist"'),
             A('Jutils convert-results, heatmap, sashimi and venn-diagram run as documented and sashimi labels match pysam', 'PASS', 'real and planted output produced; comma list reproduces FileNotFoundError'),
             A('Install lines resolve: bioconda/conda-forge solve, clone URLs exist, ggsashimi and Jutils not on conda', 'PASS', 'dry-run rc 0 with r-base 4.2.3 + ggplot2 3.4.4 + rmats2sashimiplot 4.0.0; two git ls-remote hits; "No entries matching"'),
             A('The VOILA command block is complete for a current MAJIQ V3 build', 'FAIL', 'public MAJIQ V3 docs: voila view needs sg.zarr, the .psicov and the .sgc coverage file; the Skill block names one splicegraph and one voila file (hedged as not run)')]),
    dict(index=7, type='Variant B', label='NEW: mutually exclusive exons on real chrX (plus and minus strand genes), ggsashimi and rmats2sashimiplot --event-type MXE',
         executed=True, execution_note='i7_mxe.py: top-4 MXE events of real rMATS 2v2 output; ggsashimi with the batch-recipe region (SVG + PNG), rmats2sashimiplot MXE with the Skill flags; PNG viewed.',
         status='COMPLETED', note='upstreamES..downstreamEE covers both alternative exons in 17/17 rows; ggsashimi labels 19/19, 11/11, 19/19, 16/16 = pysam; rmats2sashimiplot 4/4 PDFs (TAZ, JPX, TAZ, IRAK1 minus strand)',
         basic=36, specialized=55, assertions=[
             A('The MXE span claim holds', 'PASS', '17 of 17 rows contain both alternative exons'),
             A('ggsashimi labels for the four MXE events equal pysam group means', 'PASS', 'LABELS_OK 19/19, 11/11, 19/19, 16/16'),
             A('rmats2sashimiplot --event-type MXE writes every requested figure', 'PASS', '4 PDFs of 4, assert OK'),
             A('Minus-strand and plus-strand genes are drawn with correct arcs and gene model', 'PASS', 'IRAK1 (-) and TAZ/JPX (+) viewed; arcs on exon edges')]),
    dict(index=8, type='Edge', label='NEW: low-junction-count real region (DMD, 0-3 reads per sample) with -M, --shrink and the example guard',
         executed=True, execution_note='i8_sparse.py: -M 1 and -M 5 with and without --shrink on DMD chrX:31136844-31152811, then examples/plot_sashimi.py plot_specific_event. PNG viewed.',
         status='COMPLETED', note='-M 1 labels 4/4 = pysam (1.5 -> 2, 1.0, 2.0); -M 5 --shrink raises StopIteration as documented; -M 5 without shrink and the example draw no arcs and only warn about --shrink',
         basic=34, specialized=52, assertions=[
             A('At -M 1 the sparse-region labels equal pysam means with half-to-even rounding', 'PASS', 'GBR 1.5 -> 2 (x2), YRI 1.0 -> 1, 2.0 -> 2; LABELS_OK 4/4'),
             A('The documented --shrink crash reproduces', 'PASS', 'rc 1, "generator raised StopIteration" at -M 5'),
             A('The example guard turns the crash into a warning and still writes the figure', 'PASS', '"no junction has >= 5 reads ... dropping --shrink"; d_specific.pdf 184,137 B'),
             A('A figure with no drawn junctions is flagged to the user', 'FAIL', '-M 5 without --shrink and plot_specific_event (hard-coded min_junc 5) return rc 0 / a file with no arcs and only the shrink warning')]),
]

for i in inputs:
    i['assertions_passed'] = sum(a['result'] == 'PASS' for a in i['assertions'])
    i['assertions_total'] = len(i['assertions'])
    i['total'] = i['basic'] + i['specialized']
    i['status_flag'] = '✅' if i['total'] >= 75 else '⚠️'
    assert 3 <= i['assertions_total'] <= 5
    assert 0 <= i['basic'] <= 40 and 0 <= i['specialized'] <= 60

static = {
    'functional_suitability': (11, 12, 'Six tools, decision tree and every recipe ran with matching independent counts; VOILA is licence-gated, hedged and not run, and misses the .sgc file MAJIQ V3 needs'),
    'reliability': (11, 12, 'Silent Failures section, figure-exists asserts in every recipe, contig mapping, BAM checks; example raises after the loop with the failed-event list; error table rebuilt from observed messages (all reproduced)'),
    'performance_context': (6, 8, 'One 433-line SKILL.md loads six tools at once and there is no references/ split; usage-guide is now a short prompt list'),
    'agent_usability': (15, 16, 'Goal/Approach headings, flag list with observed behaviour, "look at the figure" instruction; the batch block needs the previous block state and the install block does not say to put ggsashimi.py on PATH though the recipes call it bare'),
    'human_usability': (7, 8, 'Natural triggers and worked prompts; strict input checks give clear messages; sparse-data no-arc figures are not flagged'),
    'security': (11, 12, 'List-form subprocess, sanitised output names, contig and BAM validation; no credentials; user paths still flow into shell blocks unquoted'),
    'maintainability': (9, 12, 'Everything verified against ggsashimi 1.1.5, rmats2sashimiplot 4.0.0, pyGenomeTracks 3.9, Jutils, leafcutter 0.2.9, but no shipped test data and version pins only in prose'),
    'agent_specific': (18, 20, 'Precise trigger, licence-gated escape hatches, ggplot2 pin with a visual check, related skills; single-file layout limits progressive disclosure'),
}
sub = sum(v[0] for v in static.values())
avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
sw, dw = round(sub * 0.4, 1), round(avg * 0.6, 1)
score = round(sw + dw)
n_pass = sum(i['assertions_passed'] for i in inputs)
n_tot = sum(i['assertions_total'] for i in inputs)
l1 = sum(i['basic'] for i in inputs) / len(inputs)
l2 = sum(i['specialized'] for i in inputs) / len(inputs)
print(f'static {sub} exec {avg} final {score} assertions {n_pass}/{n_tot} = {100 * n_pass / n_tot:.1f}% L1 {l1:.1f} L2 {l2:.1f}')
assert sub >= 80 and avg >= 85 and l1 >= 32 and l2 >= 48 and n_pass / n_tot >= 0.9, 'a Production Ready floor is not met'
grade = 'Production Ready' if score >= 85 else 'Limited Release'

desc = ('Creates sashimi-style plots showing RNA-seq read coverage and splice junction counts using ggsashimi (general-purpose, condition-grouped overlays), '
        'rmats2sashimiplot (rMATS-output-aware), MAJIQ-VOILA (LSV posteriors, interactive viewer; licence-gated), leafviz (leafcutter clusters Shiny), '
        'Jutils (tool-agnostic heatmaps and sashimi for rMATS/leafcutter/MntJULiP/MAJIQ output), or pyGenomeTracks (multi-track publication figures). '
        'Tool choice depends on the upstream differential-splicing tool\'s output format and the publication vs interactive use case.')
report = {
    'meta': {
        'skill_name': 'bio-sashimi-plots', 'description': desc, 'evaluated_on': '2026-09-20', 'evaluator_version': 'skill-auditor@1.0',
        'category': 'Data Analysis', 'execution_mode': 'D', 'complexity': 'Complex', 'n_inputs': 8,
        'source': 'mrsonord2240/bioSkills@b11c5abf964aa7a7f49acc37dc8e051ea875c4d7:alternative-splicing/sashimi-plots',
        'audit_kind': 're-audit of a fixed Skill (third agent); pre-fix score 67 Reject (Research Veto M4, P0), archived in _pre-fix-20260920',
        'inputs_note': 'Inputs 1-6 re-run the pre-fix inputs (input 1 also absorbs pre-fix input 3, edge semantics) as regression tests; inputs 7 and 8 are new.',
        'executed_k_of_n': '8/8 (VOILA inside input 6 not run: MAJIQ/VOILA is licence-gated; only its public docs were read)',
        'env': 'F:/OpenScience/audit-envs/alternative-splicing: WSL as-viz-gg34 (R 4.2.3, ggplot2 3.4.4), as-viz-gg35 (3.5.2), as-viz (4.0.3); ggsashimi 1.1.5 (a6d3c81), rmats2sashimiplot 4.0.0, pyGenomeTracks 3.9, Jutils 400c10f, leafcutter 0.2.9 (as-rleaf), rMATS-turbo 4.4.0, regtools 1.0.0, pysam 0.24',
    },
    'veto_gates': {
        'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
        'research_veto': {
            'applicable': True, 'gate': 'PASS',
            'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated identifiers or values; every quantitative claim I tested (defaults, rounding, colours, file names, error text, ggplot2 pin, MXE span) reproduced or is hedged as not run (VOILA)'},
            'practice_boundaries': {'result': 'PASS', 'detail': 'Visualisation only; no diagnostic or prescriptive content'},
            'methodological_ground': {'result': 'PASS', 'detail': 'Group aggregation, per-sample -M before -A, strand routing and rounding are stated as the tools do them and were verified against independent counts'},
            'code_usability': {'result': 'PASS', 'detail': 'Every documented command ran and produced a real non-empty figure whose junction labels match an independent pysam count: ggsashimi, batch block and example module (Ensembl contigs), rmats2sashimiplot SE and MXE with the assert forced to fire, leafviz app (HTTP 200), Jutils convert/heatmap/sashimi/venn, pyGenomeTracks + regtools BEDPE, install lines by dry-run solve. Not run: MAJIQ/VOILA (licence-gated); hedged in the text'},
        },
    },
    'static_score': {'subtotal': sub, 'max': 100, 'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in static.items()}},
    'dynamic_score': {'execution_avg': avg, 'max': 100, 'assertion_pass_rate': {'passed': n_pass, 'total': n_tot}, 'inputs': inputs},
    'final': {'static_weighted': sw, 'dynamic_weighted': dw, 'score': score, 'max': 100, 'grade': grade, 'grade_symbol': '⭐' if grade == 'Production Ready' else '✅',
              'deployable': True, 'veto_override': False},
    'key_strengths': [
        'Every recipe was run and its figure labels match an independent pysam count (planted 3v3, real chrX 2v2 with Ensembl contigs, 12-BAM ENCODE locus, MXE events)',
        'Post-run figure-exists asserts catch the exit-0 failures of ggsashimi and rmats2sashimiplot; forced failures made the asserts fire',
        'Corrected ggsashimi defaults (-M 1, mean_j, colours, -s files) and the ggplot2 < 3.5 pin were reproduced, with the layout regression visible in the images',
        'Install lines solve (conda dry-run) and the not-on-conda tools are cloned from URLs that exist; leafviz, Jutils and pyGenomeTracks workflows run end to end',
        'The licence-gated VOILA section says plainly that it was not run',
    ],
    'recommendations': [
        {'priority': 'P2', 'title': 'pyGenomeTracks junction arcs are cropped', 'observed_in': [5],
         'problem': 'In the documented tracks.ini the arcs in the junctions track are cut off at its lower edge (height = 2).',
         'root_cause': 'Arc height scales with junction span, the track is too short.', 'fix': 'Raise the junction track height (or shrink the arcs) and re-render; look at the figure as the ggplot2 note already advises.'},
        {'priority': 'P2', 'title': 'VOILA block incomplete for MAJIQ V3', 'observed_in': [6],
         'problem': 'Public MAJIQ V3 docs give `voila view sg.zarr <file>.psicov <group>.sgc`; the Skill block names one splicegraph and one voila file.',
         'root_cause': 'The section was written without a licence, generically (usage-guide once mentioned splicegraph.zarr for V3; that hint was dropped).', 'fix': 'Add the V3 form with the .sgc coverage file next to the V2 splicegraph.sql form, keep the not-run statement.'},
        {'priority': 'P2', 'title': 'No warning when no junction is drawn', 'observed_in': [8],
         'problem': 'ggsashimi -M above every junction writes a coverage-only figure with rc 0; the example drops --shrink and warns only about that; plot_specific_event hard-codes min_junc 5.',
         'root_cause': 'The example checks the shrink crash but not the arc-free result.', 'fix': 'Have plot_sashimi warn (or raise) when best < min_junc, and let plot_specific_event take min_junc.'},
        {'priority': 'P2', 'title': 'ggsashimi.py is called bare but only cloned', 'observed_in': [1, 2],
         'problem': 'The install block clones the repo, the recipes call `ggsashimi.py` from subprocess; that resolves only if the clone is on PATH (script is executable with a python shebang).',
         'root_cause': 'PATH step missing.', 'fix': 'Add `export PATH=$PWD/ggsashimi:$PATH` (and a note that the python it finds needs pysam).'},
        {'priority': 'P2', 'title': 'Batch block needs earlier state; secondary reads counted', 'observed_in': [2, 4],
         'problem': 'The batch block uses `groups`, sashimi_groups.tsv, palette.txt from the previous block; and ggsashimi labels reproduce only when secondary alignments are counted (2/10 without).',
         'root_cause': 'Blocks written as a sequence; counting rule not stated.', 'fix': 'Say the batch block continues the previous one, and add "counts every alignment record, secondary included" to the arc-count row.'},
    ],
}
assert len(report['key_strengths']) <= 5
assert [r['priority'] for r in report['recommendations']] == sorted(r['priority'] for r in report['recommendations'])
(OUT / 'eval_report_bio-sashimi-plots_result.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
print('written', grade, score)
