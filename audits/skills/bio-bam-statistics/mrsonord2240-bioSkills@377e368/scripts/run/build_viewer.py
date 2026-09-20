#!/usr/bin/env python3
"""Builds eval_viewer_bio-bam-statistics.md from the report JSON and trimmed excerpts of run/out/*.txt (the real outputs of the scripts in run/)."""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = json.load(open(os.path.join(ROOT, 'eval_report_bio-bam-statistics_result.json'), encoding='utf-8'))
OUT = os.path.join(ROOT, 'run', 'out')

def excerpt(name, start=None, end=None, maxlines=40, width=200):
    lines = open(os.path.join(OUT, name), encoding='utf-8', errors='replace').read().splitlines()
    if start:
        idx = next((i for i, l in enumerate(lines) if start in l), 0)
        lines = lines[idx:]
    if end:
        idx = next((i for i, l in enumerate(lines[1:], 1) if end in l), len(lines))
        lines = lines[:idx]
    lines = [l[:width] for l in lines[:maxlines]]
    return '\n'.join(lines)

PROMPTS = {
 1: "I have a paired-end BAM from an nf-core run and a 1000 Genomes slice. Give me flagstat, per-contig counts, the samtools stats summary, coverage, and the mean depth and % of bases at >=10x and >=20x.",
 2: "My targeted BAM has regions with no reads and a whole contig with none. What are mean depth and >=10x/>=20x over the reference, and per BED region? Do your recipes count the zeros?",
 3: "This BAM has secondary, supplementary, QC-failed and duplicate records and unmapped mates. Give me a QC report and check it matches flagstat.",
 4: "My amplicon data is 9500x deep at the peak. What depth does each tool report and is anything silently capping it?",
 5: "Make one summary table for all the BAMs in this directory, plot the samtools stats and give me a MultiQC report.",
 6: "Is my mate-pair library's insert size sensible? Is there adapter read-through, off-target signal, or contamination I should check beyond flagstat?",
 7: "Run your stats recipes on an empty BAM, a single-end BAM, an unindexed BAM, an Ensembl-style MT contig, an unaligned BAM and a CRAM.",
}
CODE = {
 1: ("t1_canonical.sh, t1_check.py, t1b_depth_real.sh, depth_truth.py, rb.sh",
     "python t1_check.py BAM   # flagstat -O tsv vs truth.counts() from record flags\nbash rb.sh 18 $H         # SKILL.md block 018 verbatim (samtools depth -aa | awk ...)\nsamtools depth -a -s / mpileup [-x|-Q 0] / bcftools mpileup [-x] / mosdepth [--fast-mode] / region_depth_stats (block 030) vs alignment-block truth",
     [('t1_canonical.sh', '################ /mnt/openscience/audit-envs/alignment-files/public-data/human', '--- idxstats', 32), ('t1b_depth_real.sh', None, None, 45)]),
 2: ("make_depth.py, t2_planted.sh, t2_region_vs_truth.py",
     "python make_depth.py                 # planted truth by construction (22000 bp, chrC has no reads)\nbash rb.sh 18 planted_depth.bam      # block 018, -aa; then the same with -a\nsamtools depth -a -b BED / coverage loop (block 026) / mosdepth --by --thresholds\npython t2_region_vs_truth.py         # block 030 vs 13 truth arrays and samtools depth -a",
     [('t2_planted.sh', None, None, 60)]),
 3: ("make_synth.py, make_edge.py, t3_edge.sh, t3_qc_vs_flagstat.py, t3_expected.py, check_counts.py, truth.py",
     "python t3_qc_vs_flagstat.py BAM ...   # Skill block 028 + examples/qc_report.py vs flagstat -O tsv vs hand counts, 18 BAMs\npython t3_expected.py                 # 9 NEW edge BAMs vs counts planted by construction\npython check_counts.py synth.bam      # tools + the Skill's cross-check identity",
     [('t3_edge.sh', '=== check_counts.py', '=== qc_report.py + block 028', 22), ('t3_edge.sh', '=== qc_report.py + block 028', '=== NEW edge BAMs', 26), ('t3_edge.sh', '=== NEW edge BAMs', '=== MAPQ', 22)]),
 4: ("t4_depth_cap.sh, t4_helper.py",
     "samtools depth -aa / -d 100 / coverage [-d 8000] / mosdepth / samtools mpileup [-d 1000000] / bcftools mpileup [-d 1000000] / pysam pileup [max_depth=1_000_000] on a 9500x stack; block 030 and block 018 on the stack and on the real ARTIC BAM",
     [('t4_depth_cap.sh', None, None, 60)]),
 5: ("t5_batch_plots.sh, t5_batch_check.py",
     "bash blocks/006_bash.sh   # summary table loop, 15 BAMs\nplot-bamstats -p plots/ stats.txt ; multiqc . -o multiqc_out ; samtools stats [-r ref.fa] [--GC-depth]",
     [('t5_batch_plots.sh', '=== block 006 verbatim', '=== plot-bamstats', 24), ('t5_batch_plots.sh', '=== rows vs hand counts', '=== plot-bamstats', 20), ('t5_batch_plots.sh', '=== multiqc', '=== stats -r ref', 14)]),
 6: ("t6_scope.sh, t6_softclip.py, t6b_qc_insert_cap.sh, t10_make_vb2_data.py, t10_vb2.sh",
     "python t6_softclip.py BAM ...       # block 033 (awk recipe) under gawk and mawk vs pysam cigartuples truth\nsamtools stats rf.bam; python examples/qc_report.py rf.bam\npicard BedToIntervalList / CollectHsMetrics ; verifybamid2 --SVDPrefix ...dat --Reference --BamFile --Output ; somalier extract",
     [('t6_scope.sh', '=== A.', '=== B.', 14), ('t6_scope.sh', '=== C.', '=== D.', 12), ('t10_vb2.txt', None, None, 12), ('t6b_qc_insert_cap.txt', None, None, 14)]),
 7: ("t7_adversarial.sh, t8_misc_claims.sh, t0_stability_determinism.sh, t9_syntax_sweep.sh, g1_mt.sh",
     "python t3_qc_vs_flagstat.py empty.bam se.bam noindex.bam synth_MT.bam ; block 028/031 on empty ; depth -aa recipe on empty ; mito/sex recipes ; samtools idxstats / pysam get_index_statistics / mosdepth on unindexed ; uBAM, SAM and CRAM into qc_report.py ; bash -n every fenced bash block, py_compile every Python block",
     [('t7_adversarial.sh', None, None, 45), ('t0_stability_determinism.txt', None, None, 6)]),
}

def out_file(spec):
    n = spec[0]
    return n if n.endswith('.txt') else n.replace('.sh', '.txt')

L = []
a = L.append
d = R['dynamic_score']
a('# Eval Viewer - bio-bam-statistics (re-audit of the fixed Skill)')
a(f"Generated: {R['meta']['evaluated_on']}  |  Source: `{R['meta']['source']}`  |  Pre-fix score {R['meta']['pre_fix_score']} (Beta Only)")
a('')
a(f"Category: {R['meta']['category']}  |  Mode: {R['meta']['execution_mode']}  |  Complexity: {R['meta']['complexity']} (N={R['meta']['n_inputs']})  |  Executed: {R['meta']['executed']}")
a('')
a('Run from a copy of the Skill (`run/skill/`); the worktree was not written to. Scripts are in `run/`, raw outputs in `run/out/`. Synthetic data is generated by `make_synth.py`, `make_depth.py`, `make_edge.py`, `t10_make_vb2_data.py` (truth by construction); real data is from `audit-envs\\alignment-files\\public-data`.')
a('')
a('## Summary Table')
a('')
a('| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |')
a('|---|---|---|---|---|---|---|')
for i in d['inputs']:
    a(f"| {i['index']} | {i['type']} | {i['basic']} | {i['specialized']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} PASS | {i['status_flag']} |")
a('')
a(f"**Execution Average: {d['execution_avg']} / 100**  |  **Assertion Pass Rate: {d['assertion_pass_rate']['passed']}/{d['assertion_pass_rate']['total']}**")
a('')
f = R['final']
a(f"**Static {R['static_score']['subtotal']}/100 x 0.4 = {f['static_weighted']}; Execution {d['execution_avg']} x 0.6 = {f['dynamic_weighted']}; FINAL {f['score']} - {f['grade_symbol']} {f['grade']}; deployable: {f['deployable']}; veto: none (Skill Veto PASS, Research Veto PASS).**")
a('')
a('Floors (scoring_rubric section 5): static >= 80 ok; execution >= 85 ok; Layer 1 avg 35.1 >= 32 ok; Layer 2 avg 51.1 >= 48 ok; assertion pass rate 82% < 90% not met, so Production Ready is not available even if the score were 85. Score 84 = Limited Release.')
a('')
a('Regression versus pre-fix (71): the seven pre-fix P1 findings were re-tested and all seven are fixed (mean/breadth denominator, pysam counting, depth caps, coverage -b, soft-clip grep, RF insert-size caveat, SE/empty/MT recipes). New defects found are P1 x1 (uBAM/CRAM in the pysam tools) and P2 x5. Nothing the fix changed is wrong; two fixer statements are slightly overstated (`depth -a -b`, table row for bcftools -x).')
a('')
a('## Static evaluation')
a('')
a('| Category | Score | Note |')
a('|---|---|---|')
for k, v in R['static_score']['categories'].items():
    a(f"| {k} | {v['score']}/{v['max']} | {v['note']} |")
a(f"| **Subtotal** | **{R['static_score']['subtotal']}/100** | |")
a('')
a('Shipped-means-present: `SKILL.md`, `usage-guide.md`, `examples/qc_report.py` present; all six Related Skills exist in the clone; `python -m py_compile` OK; no `eval`/`exec`/`subprocess`/network/credentials in the shipped files (grep in `out/t8_misc_claims.txt`); all 28 fenced bash blocks pass `bash -n` and the 4 Python blocks compile (`out/t9_syntax_sweep.txt`). Determinism: `qc_report.py` 10/10 rc=0 with 1 distinct output; depth recipe, flagstat and region_depth_stats 1 distinct output each (`out/t0_stability_determinism.txt`).')
a('')
a('## Detailed Outputs')
for i in d['inputs']:
    n = i['index']
    a('')
    a(f"### Input {n} - {i['type']}: {i['label']}")
    a(f"**Prompt:** {PROMPTS[n]}")
    a('')
    a(f"**Executed:** {i['executed']} - {i['execution_note']}")
    a('')
    files, cmds, exc = CODE[n]
    a(f"**Code that ran** (`run/`: {files}):")
    a('```bash')
    a(cmds)
    a('```')
    a(f"**What it printed (trimmed):**")
    for spec in exc:
        name = out_file(spec)
        a('```')
        a(excerpt(name, spec[1], spec[2], spec[3]))
        a('```')
    a(f"**Summary:** {i['note']}")
    a('')
    a(f"**Scores:** Basic {i['basic']}/40 | Specialized {i['specialized']}/60 | Total {i['total']}/100")
    a('')
    a('**Assertions:**')
    for x in i['assertions']:
        a(f"- [{x['result']}] {x['text']} - {x['note']}")
a('')
a('## Research Veto')
for k, v in R['veto_gates']['research_veto'].items():
    if isinstance(v, dict):
        a(f"- {k}: **{v['result']}** - {v['detail']}")
a('')
a('## Judgement on the honesty of the unverified-number labelling')
a('- Assay-threshold table: preceded by "Values below are literature ranges, not thresholds verified on this machine." That is honest and visible. It is not sufficient for citing: no row has a source, so an agent cannot check a value. P2.')
a('- FREEMIX cut-offs: "commonly cited" (twice) and the Quick Summary row says "commonly used expectation". Honest hedge, no source.')
a('- VerifyBamID2/somalier: "Flags checked against --help ...; not run end to end here because no whole-genome BAM was available." I confirmed it and went one step further: VerifyBamID2 with the documented `--SVDPrefix ...dat --Reference --BamFile --Output` accepted the command, loaded the 10k panel and shared 204 markers with a synthetic chr20 BAM, then stopped with "Insufficient Available markers" (`out/t10_vb2.txt`); somalier extract fails on the missing chr1 as the Skill warns. The commands are plausible; the outputs (FREEMIX, .somalier) remain unproduced.')
a('')
a('## Recommendations')
for x in R['recommendations']:
    a(f"- **[{x['priority']}] {x['title']}** (inputs {x['observed_in']}): {x['problem']} Fix: {x['fix']}")
a('')
a('## Key strengths')
for s in R['key_strengths']:
    a(f"- {s}")
open(os.path.join(ROOT, 'eval_viewer_bio-bam-statistics.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('viewer lines', len(L))
