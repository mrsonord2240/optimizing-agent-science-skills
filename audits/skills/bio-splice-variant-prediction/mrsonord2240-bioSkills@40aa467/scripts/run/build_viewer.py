"""Builds eval_viewer_bio-splice-variant-prediction.md from the JSON report (so the two cannot disagree)."""
import json, os
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(here, '..')
j = json.load(open(os.path.join(root, 'eval_report_bio-splice-variant-prediction_result.json'), encoding='utf-8'))
L = []
a = L.append
f = j['final']; d = j['dynamic_score']
a('# Eval Viewer — bio-splice-variant-prediction (re-audit of the fixed Skill)')
a('Generated: 2026-09-20')
a('Source: `' + j['source'] + '` (read from a copy in `run/skill/`; the worktree `F:\\OpenScience\\wt\\as-spvp` was not written to).')
a('Pre-fix (archived at `F:\\OpenScience\\audits\\_pre-fix-20260920\\bio-splice-variant-prediction\\`): 66, Reject, Research Veto M4 fired, 2 open P0s. **Now: 84, Limited Release, deployable, no veto, no open P0, two open P1s.**')
a('Category: Data Analysis. Mode D. Complexity: Complex. N = 9 (the 7 pre-fix inputs re-run as regression tests + 2 new inputs of my own, 8 and 9; the schema documents 8, the extra one is deliberate). Executed 9/9 (input 6 partial). Every script that ran is in `run/`, logs in `run/out/`, data in `run/data/` (real variants, VCFs assembled by me; REF asserted against the FASTA in every builder).')
a('')
a('## How each Research Veto block was re-judged')
a('| Block | Pre-fix | Now | Evidence |'); a('|---|---|---|---|')
a('| M1 Scientific Integrity | PASS | PASS | Every quoted number reproduced or checked at source (SpliceVault Top-4, 884 MB = Content-Length 883,907,365, CADD record, mask-table cells, tool versions on PyPI); citations sampled against Crossref. |')
a('| M2 Practice Boundaries | PASS (caveats) | PASS | Scope paragraph + usage-guide sentence state research use; PVS1 refused for SpliceAI alone (input 7); no output label contains "pathogenic" (grep + test). Both pre-fix caveats closed. |')
a('| M3 Methodological Ground | PASS | PASS | Inclusive ClinGen boundaries, `.`/missing never BP4, `-D` mechanism and mask trade-off now measured. Residual P2: concordant false positives not warned. |')
a('| **M4 Code Usability** | **FAIL** | **PASS** | Both pre-fix P0 recipes now run on real output (inputs 2, 5); every fenced block of SKILL.md parses and was run (table below); shipped example runs on 3 VCFs. |')
a('')
a('### M4: SKILL.md fenced blocks, one by one')
a('`run/m4_blocks.py` extracts them to `run/blocks/`; syntax log `out/m4_blocks.log`: 12 blocks, 3 python (`ast.parse` OK), 9 bash (`bash -n` rc 0).')
a('')
a('| Block | What | How run | Result |'); a('|---|---|---|---|')
rows = [
 ('B01', 'Install (SpliceAI, Pangolin, MMSplice lines)', '`t2_install_recipe.sh`: fresh venv, `pip --dry-run` of each line, real `--no-deps` install of the tkzeng/Pangolin clone', 'Resolves (spliceai 1.3.1 / TF 2.21; PyVCF3 1.0.0 etc.); clone gives `pangolin` and `create_db.py` on PATH and 64 weight files. Default `pip install torch` plans the CUDA wheel (P2). Dry-run only, no full install.'),
 ('B02', 'SpliceAI CLI', '`run_spliceai.sh` (D 50/500/2000, GRCh37) and `t7a` (GRCh38)', 'Ran, all records tagged, values asserted'),
 ('B03', 'parse / classify / unscored_report', 'Executed literally from an examples-folder copy (`lit_run.sh`) and asserted against a raw INFO split (`t1`)', 'Ran; `[]` for a fully scored VCF; 20 PASS'),
 ('B04', '`create_db.py` + `pangolin` commands', '`t2_pangolin.sh`: real GENCODE v45 chr17+chrX GTF, canonical and `--filter None`, `-m False/True`, `-d 500 -s 0.2`', 'Ran; DBs built (171 s / 262 s under load); 11/11 records tagged in all runs; mask table reproduced'),
 ('B05', '`pangolin_tissue.py`', '`t2_tissue.sh`, 4 variants + wrong REF', 'Ran; tissue maximum equals CLI `-m False` for all 4; guard fires'),
 ('B06', 'SpliceVault `curl` + `splicevault_lookup.py`', '`t6_splicevault_cadd.sh`, `t7d_sv.sh` (remote tabix on the Ensembl file)', "Ran; Skill's TP53 Top-4 reproduced; 5/5 new variants agree with my SpliceAI"),
 ('B07', 'MMSplice', '`t3_mmsplice.py`, GRCh37 and GRCh38', 'Ran; CSV shapes as stated; `parse_mmsplice_csv` equals independent argmax'),
 ('B08', 'SpliceTransformer', '`t6_splicetransformer.sh` in `as-spvp-gpu` (fixer-staged repo + weights)', 'Ran (11 records, 56 s on the RTX 5070 Ti); scores match the Skill; install lines dry-run only'),
 ('B09', 'CI-SpliceAI `cis-vcf`', '`t7c_cispliceai.sh`, GRCh38, `-d 500 --all`', 'Ran (33 s); `CISpliceAI=` tag parses'),
 ('B10', 'CADD API `curl`', '`t6_splicevault_cadd.sh`, `out/t9_cadd.log`', 'Ran; documented TP53 record returned; 7 new records scored'),
 ('B11', 'SpliceAI `-D 500` re-run', '`run_spliceai.sh`, `t7a`', 'Ran'),
 ('B12', '`build_concordance`', 'Executed literally (`lit_run.sh`), then `t5_concordance.py`, `t7_check.py`', 'Ran; 10, 11 and 12 rows for 10, 11 and 12 input variants'),
]
for r in rows: a('| ' + ' | '.join(r) + ' |')
a('')
a('Shipped means present (gate 8): `examples/{splice_parsers,spliceai_clingen_classify,splicevault_lookup,pangolin_tissue,test_splice_parsers}.py` and `examples/test_data/` exist and parse; SKILL.md and usage-guide.md name no file that is missing. `python examples/test_splice_parsers.py` passes 5/5 from the clean copy (that test data comes from the fixer, so I ran independent data as well).')
a('')
a('## Step 1 — Skill Veto: PASS')
a('T1 Stability: all runs completed or failed as documented (the symbolic `<DEL>` crash is documented). T2 Contract: stable INFO/CSV schemas. T3 Determinism: the PLCXD1 record gave `0.00|0.00|0.90|1.00|28|-10|28|-1` in every SpliceAI run; SpliceTransformer on GPU matched the Skill. T4 Security: list-style `subprocess.run`, no eval/exec/secrets.')
a('')
a('## Step 2 — Static (25 criteria): 83/100')
a('| Category | Score | Note |'); a('|---|---|---|')
for k, v in j['static_score']['categories'].items(): a(f"| {k} | {v['score']}/{v['max']} | {v['note']} |")
a('')
a('Pre-fix static was 71 (functional 8, reliability 7, performance 5, agent usability 12, human 7, security 10, maintainability 8, agent-specific 14).')
a('')
a('## Summary Table')
a('| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |'); a('|---|---|---|---|---|---|---|')
for i in d['inputs']:
    a(f"| {i['index']} | {i['type']}: {i['label'][:80]} | {i['basic']} | {i['specialized']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} | {i['status_flag']} {i['status']} |")
a('')
a(f"**Execution Average: {d['execution_avg']} / 100. Assertion Pass Rate: {d['assertion_pass_rate']['passed']}/{d['assertion_pass_rate']['total']} (88.9%).** Static 83 x 0.4 = {f['static_weighted']}; dynamic {d['execution_avg']} x 0.6 = {f['dynamic_weighted']}; **final {f['score']}**. Layer 1 average {f['layer1_avg']}/40, Layer 2 average {f['layer2_avg']}/60. Limited Release floors all met (static >= 70, exec >= 75, L1 >= 28, L2 >= 42, assertions >= 80%); Production Ready is not reached (84 < 85, assertions < 90%). Pre-fix: static 71, exec 62.0, final 66, assertions 19/35.")
a('')
a('## Detailed Outputs')
for i in d['inputs']:
    a(f"### Input {i['index']} — {i['type']}: {i['label']}")
    a('**Ran:** ' + i['execution_note']); a('')
    a('**Result:** ' + i['note']); a('')
    for x in i['assertions']: a(f"- {x['result']}: {x['text']} — {x['note']}")
    a(f"**Scores:** {i['basic']} / {i['specialized']} / {i['total']}. Assertions {i['assertions_passed']}/{i['assertions_total']}."); a('')
a('### Key printed evidence')
a('```')
a('SpliceAI D50 GRCh37 (delta_max): PLCXD1 G>A 1.00 | GTdel 1.00 | DMD c.9563+1G>A 0.99 | c.31+1G>A 0.95 | OTC c.386+5G>A 0.94 | GLA c.370-1G>A 1.00 | GLA c.639+919G>A 0.30 | 3 benign 0.00')
a('Pangolin GRCh38 (GENCODE v45): mask False / canonical-DB mask True / all-transcript-DB mask True')
a('  GLA c.639+919G>A gain +0.23@-3 / +0.23 / 0.00     OTC c.386+5G>A loss -0.72@-5 / 0.00 / 0.00     TP53 c.673-2A>G loss -0.90@-2 in all four')
a('  auditor-picked DMD non-canonical-only sites (loss): -0.39 / 0.00 / -0.39 and -0.60 / 0.00 / -0.60 (other three sites -0.04 to -0.13)')
a('New panel (SpliceAI D50 | Pangolin | MMSplice | CI-SpliceAI):')
a('  CFTR c.1585-1G>A  0.97 | -0.86 | -1.83 | 1.00     BRCA1 c.594-2A>C  0.83 | -0.81 | -2.86 | 0.95     BRCA1 c.5074+1G>A  0.74 | -0.70 | -2.70 | 0.95')
a('  CFTR 3849+10kb C>T (pseudoexon)  0.16 (D500 0.16, D2000 0.16) | +0.33 | no row | 0.01  -> discordant / inconclusive')
a('  CFTR c.2909-10T>G (ClinVar likely benign)  0.57 | -0.41 | -1.85 | 0.31  -> concordant false positive')
a('shipped example, TP53 VCF: c.673-2A>G 1.0 PP3_supporting_prec0.8 | P72R 0.05 BP4 (wide 0.05) | usage-guide A>G record: WARNING SpliceAI: no score, not_scored')
a('shipped example, edge VCF + one <DEL>: subprocess.CalledProcessError, no output')
a('```')
a('')
a('## Research Veto (Category 3): PASS')
for k, v in j['veto_gates']['research_veto'].items():
    if isinstance(v, dict): a(f"- {k}: **{v['result']}** — {v['detail']}")
a('')
a('## Step 8 — Final')
a(f"Static 83 x 0.4 = {f['static_weighted']}; Execution {d['execution_avg']} x 0.6 = {f['dynamic_weighted']}; **final {f['score']}, {f['grade']}, deployable, veto_override false.** No open P0. Open P1: 2, P2: 4.")
a('')
a('### Key strengths')
for s in j['key_strengths']: a('- ' + s)
a('')
a('### Recommendations')
for r in j['recommendations']: a(f"[{r['priority']}] {r['title']} (inputs {r['observed_in']}) — {r['problem']} Fix: {r['fix']}")
a('')
a('## What I could not verify')
a("- BPHunter, LaBranchoR, BPP, SVM-BPfinder were not run (BPHunter's standalone page redirects to a GitHub 404, checked); the Skill says \"none was run here\".")
a("- Installs of SpliceTransformer (Google Drive weights, pyensembl index) and CI-SpliceAI were verified by `pip --dry-run` only; the tools were run in the fixer's staged envs (`as-spvp`, `as-spvp-gpu`, `as-cispliceai`) and repo. SpliceTransformer's staged FASTA has no chr7, so the new panel was not scored by it.")
a("- The MMSplice `setuptools<81` / `cyvcf2` note is from TOOLS.md traps 21/23; `as-mmsplice` already has a working cyvcf2 0.34.0, so the failing state was not reproduced. The dry-run plans cyvcf2 0.30.15, which matches the Skill's warning.")
a('- Input 7 is scored from the Skill text applied to real numbers (no agent transcript), as in the pre-fix audit.')
a('- `TOOLS.md` does not yet list `as-spvp`, `as-cispliceai`, `as-spvp-gpu` in detail (the orchestrator records them). I changed no package versions; the only install was a throwaway venv in WSL `/tmp`. Large scratch (chr7 FASTA, GENCODE subsets) is in `F:\\OpenScience\\as-spvp-reaudit-scratch\\`; the gffutils DBs and GTF copies were deleted from `run/out/`.')
a('')
a('## Files')
a('- Report: `F:\\OpenScience\\audits\\bio-splice-variant-prediction\\eval_report_bio-splice-variant-prediction_result.json` (built and schema-asserted by `run\\build_report.py`; this viewer by `run\\build_viewer.py`)')
a('- Scripts: `run\\*.py`, `run\\*.sh` (`w.sh`/`wenv.sh` drive WSL); logs `run\\out\\*.log`; Skill copy audited `run\\skill\\` (commit 40aa467b3e6ca58f2aeb4cbf30a8cc2b81cf7197).')
with open(os.path.join(root, 'eval_viewer_bio-splice-variant-prediction.md'), 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('\n'.join(L) + '\n')
print(len(L), 'lines')
