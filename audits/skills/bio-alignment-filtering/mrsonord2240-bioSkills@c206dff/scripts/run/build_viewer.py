#!/usr/bin/env python3
import json, sys
root = sys.argv[1]
j = json.load(open(f'{root}/eval_report_bio-alignment-filtering_result.json', encoding='utf-8'))
logs = {1: ('in1_standard.py', 'in1_standard.txt', 40), 2: ('make_synthetic_flags.py, in2_flags.py', 'in2_flags.txt', 45),
        3: ('in3_regions.py', 'in3_regions.txt', 60), 4: ('in4_subsample.sh, in4_subsample_pysam.py, in4c_pair_consistency.py', 'in4_subsample.txt', 60),
        5: ('make_repeat_genome.py, in5_align.sh, in5_mapq_analysis.py', 'in5_mapq.txt', 60), 6: ('in6_expr.py', 'in6_expr.txt', 40),
        7: ('in7_adversarial.sh', 'in7_adversarial.txt', 40)}
prompts = {
 1: 'Filter this BAM to keep only high-quality reads: mapped, primary, not duplicates, MAPQ 30 or higher. Give me the samtools command and a pysam version and tell me how many reads survive.',
 2: 'I need the right samtools filter flags for germline calling, somatic calling, ChIP-seq, ATAC-seq, SV calling and coverage analysis, and I want to be sure the flag numbers are correct.',
 3: 'Extract the reads overlapping these target regions (a BED with overlapping rows, and chr22:1952-2100 style regions) with samtools and with pysam, using the shipped example script if it helps; also write CRAM.',
 4: 'Give me a reproducible 10% subsample that keeps read pairs together, and also downsample to about 3,000 reads (or 1,000,000 if the BAM is big enough), with samtools and with pysam.',
 5: 'Which -q threshold should I use to drop ambiguous alignments and to keep high-confidence ones for BWA, Bowtie2, HISAT2, STAR and minimap2 output?',
 6: 'Keep reads with NM <= 3, less than 20% soft clipping, insert size 100-500 bp and MAPQ >= 30; also restrict to one read group (library A).',
 7: 'Clean my BAM: remove duplicates, keep only unique high-confidence properly paired primary reads. I will run Manta on it afterwards.',
}
L = []
L.append('# Eval Viewer — bio-alignment-filtering')
L.append(f"Generated: {j['meta']['evaluated_on']}  |  Source: `{j['source']}`  |  Category: Data Analysis  |  Mode: D  |  Complexity: Complex (N=7)\n")
L.append('Environment: WSL `science` env `alignment-files` (samtools 1.24, pysam 0.24.1, bwa, bowtie2, hisat2, minimap2, STAR). Every script is in `run/`; logs in `run/out/`. The Skill folder was copied to `run/skill/` and run from there (no write inside `external\\`, no `__pycache__`).\n')
L.append('## Step 1 — Skill Veto: PASS (T1 stability, T2 contract, T3 determinism, T4 security)')
L.append('Frontmatter has name/description/tool_type/primary_tool/license; no eval/exec/shell=True; samtools -s and the pysam recipe are deterministic; all files SKILL.md points at exist (the six Related Skills are sibling folders); `examples/filter_bam.py` exists but neither SKILL.md nor usage-guide.md links to it.\n')
L.append('## Step 2 — Static score (25 criteria): 74 / 100')
L.append('| Category | Score | Note |\n|---|---|---|')
for k, v in j['static_score']['categories'].items():
    L.append(f"| {k} | {v['score']}/{v['max']} | {v['note']} |")
L.append('\n## Steps 3-4 — Classification and inputs')
L.append('Category 3 Data Analysis; Mode D (CLI recipes plus one example script). Complexity Complex (many task types, branching by assay/aligner) -> 7 inputs.\n')
L.append('## Summary Table\n')
L.append('| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |\n|---|---|---|---|---|---|---|---|')
for i in j['dynamic_score']['inputs']:
    L.append(f"| {i['index']} | {i['type']} | {i['basic']} | {i['specialized']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} PASS | {i['executed']} | {i['status_flag']} |")
d = j['dynamic_score']
L.append(f"\n**Execution Average: {d['execution_avg']} / 100**  |  **Assertion Pass Rate: {d['assertion_pass_rate']['passed']}/{d['assertion_pass_rate']['total']}**  |  Layer 1 avg 30.3/40  |  Layer 2 avg 45.1/60\n")
L.append('## Detailed Outputs\n')
for i in d['inputs']:
    script, logf, n = logs[i['index']]
    L.append(f"### Input {i['index']} — {i['type']}: {i['label']}")
    L.append(f"**Prompt:** {prompts[i['index']]}\n")
    L.append(f"**Executed:** {i['executed']} — {i['execution_note']}\n")
    L.append(f"**Code:** `run/{script}`\n")
    lines = open(f'{root}/run/out/{logf}', encoding='utf-8').read().splitlines()
    L.append(f'**Output (trimmed to {min(n, len(lines))} of {len(lines)} lines, `run/out/{logf}`):**\n```')
    L.extend(lines[:n]); L.append('```\n')
    L.append(f"**Summary:** {i['note']}\n")
    L.append(f"**Scores:** Basic {i['basic']}/40 | Specialized {i['specialized']}/60 | Total {i['total']}/100\n")
    L.append('**Assertions:**')
    for a in i['assertions']:
        L.append(f"- [{a['result']}] {a['text']} — {a['note']}")
    L.append('')
L.append('## Shipped-means-present and snippet smoke test')
L.append('All 6 Related Skills exist as sibling folders; `examples/filter_bam.py` exists. `run/snippets_smoke.py` ran all 42 fenced blocks verbatim from a copy: 36 clean, 6 warned/failed for fixture reasons only (chr1 regions on a chr22 BAM, `conda` absent), see `run/out/snippets_smoke.txt`. Clean exit was never taken as proof; correctness is asserted in inputs 1-7.\n')
L.append('## Research Veto: PASS (M1-M4)')
for k, v in j['veto_gates']['research_veto'].items():
    if isinstance(v, dict): L.append(f"- {k}: {v['result']} — {v['detail']}")
L.append('\n## Step 8 — Final')
f = j['final']
L.append(f"Static 74 x 0.4 = {f['static_weighted']}; Execution {d['execution_avg']} x 0.6 = {f['dynamic_weighted']}; **Final {f['score']} / 100**.")
L.append('Floors (Limited Release): static >= 70 ok (74); execution >= 75 ok (75.4); L1 >= 28 ok (30.3); L2 >= 42 ok (45.1); **assertion pass rate >= 80% NOT met (22/35 = 62.9%)** -> downgraded one tier: **Beta Only, deployable false**, no veto, no P0.\n')
L.append('### Key strengths')
for s in j['key_strengths']: L.append(f'- {s}')
L.append('\n### Recommendations')
for r in j['recommendations']:
    L.append(f"\n**[{r['priority']}] {r['title']}**  (inputs {r['observed_in']})\n- Problem: {r['problem']}\n- Root cause: {r['root_cause']}\n- Fix: {r['fix']}")
open(f'{root}/eval_viewer_bio-alignment-filtering.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('written')
