"""Builds eval_viewer_bio-duplicate-handling.md from the report JSON and the run logs (trimmed)."""
import json, re, os
B = r"F:\OpenScience\audits\bio-duplicate-handling"
R = json.load(open(f"{B}/eval_report_bio-duplicate-handling_result.json", encoding="utf-8"))
def log(name, maxlines=45):
    t = open(f"{B}/run/{name}", encoding="utf-8", errors="replace").read()
    t = re.sub(r"\x1b\[[0-9;]*m", "", t)
    lines = [l for l in t.splitlines() if l.strip() and "cannot decipher read name" not in l and "unable to calculate estimated" not in l]
    if len(lines) > maxlines: lines = lines[:maxlines] + [f"... ({len(lines)-maxlines} more lines trimmed; full log in run/{name})"]
    return "\n".join(lines)
scripts = {1: ["in01_canonical.sh"], 2: ["in02_pipeline_optical.sh", "00_make_synth.py"], 3: ["in03_edge_wrong_order.sh", "in03b_fixmate_r.sh", "03_strip_tags.py"],
           4: ["in04_pysam.py"], 5: ["in05_shipped_example.sh", "in05b_aligner_alternatives.sh"], 6: ["in06_assay_scope.sh", "00b_make_synth2.py"], 7: ["in07_umi.sh", "in07b_fgbio.sh"]}
logs = {1: ["in01.log"], 2: ["in02.log"], 3: ["in03.log", "in03b.log"], 4: ["in04.log"], 5: ["in05.log", "in05b.log"], 6: ["in06.log"], 7: ["in07.log", "in07b.log"]}
m = R["meta"]; f = R["final"]; d = R["dynamic_score"]; s = R["static_score"]
o = []
o.append(f"# Eval Viewer - {m['skill_name']}\nGenerated: {m['evaluated_on']}  |  Source: `{m['source']}`  |  Category: {m['category']}  |  Mode: {m['execution_mode']}  |  Complexity: {m['complexity']} (N={m['n_inputs']})\n")
o.append(f"**Final: {f['score']} / 100 - {f['grade_symbol']} {f['grade']} - deployable: {str(f['deployable']).lower()} - veto: none**  (static {s['subtotal']} x 0.4 = {f['static_weighted']}; execution avg {d['execution_avg']} x 0.6 = {f['dynamic_weighted']})\n")
o.append("Executed 7/7 inputs. " + m["executed"] + "\n")
o.append("Complexity rationale: several task types (mark, remove, optical, multi-library, UMI, assay decision, pysam) and branching by assay/platform, so Complex -> 7 inputs, although the Skill has only one usage-guide and one example.\n")
o.append("## Step 1 - Skill Veto\nStability PASS (shipped example and every SKILL.md pipeline run; failures are loud or documented below), Contract PASS (name + description frontmatter), Determinism PASS (identical outputs on re-runs), Security PASS (no eval/exec, no credentials).\n")
o.append("## Step 2 - Static (25 criteria)\n\n| Category | Score | Note |\n|---|---|---|")
for k, v in s["categories"].items(): o.append(f"| {k} | {v['score']}/{v['max']} | {v['note']} |")
o.append(f"\n**Static subtotal: {s['subtotal']} / 100**\n")
o.append("Gate 8 (shipped means present): SKILL.md/usage-guide point only at `examples/markdup_pipeline.sh` (present) and Related Skills that all exist (alignment-sorting, alignment-filtering, alignment-amplicon-clipping, bam-statistics, variant-calling/variant-calling, read-qc/quality-reports). No missing primary file.\n")
o.append("## Summary Table\n\n| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |\n|---|---|---|---|---|---|---|---|")
for i in d["inputs"]: o.append(f"| {i['index']} | {i['type']} | {i['basic']} | {i['specialized']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} PASS | {str(i['executed']).lower()} | {i['status_flag']} |")
l1 = sum(i["basic"] for i in d["inputs"]) / 7; l2 = sum(i["specialized"] for i in d["inputs"]) / 7
o.append(f"\n**Execution Average: {d['execution_avg']} / 100**  |  Layer 1 avg {l1:.1f}/40, Layer 2 avg {l2:.1f}/60  |  **Assertion Pass Rate: {d['assertion_pass_rate']['passed']}/{d['assertion_pass_rate']['total']}**\n")
o.append("Floors for Limited Release (static >= 70, exec >= 75, L1 >= 28, L2 >= 42, assertions >= 80%): all met (73, 79.1, 32.4, 46.7, 81.3%). Not met for Production Ready (static < 80, exec < 85, L2 < 48, assertions < 90%).\n")
o.append("## Detailed Outputs\n")
for i in d["inputs"]:
    o.append(f"### Input {i['index']} - {i['type']}: {i['label']}\n**Prompt:** {i['prompt']}\n")
    o.append(f"**Executed:** {str(i['executed']).lower()} - {i['execution_note']}\n")
    o.append("**Scripts:** " + ", ".join(f"`run/{x}`" for x in scripts[i["index"]]) + "\n")
    for ln in logs[i["index"]]:
        o.append(f"**Output (`run/{ln}`, trimmed):**\n```\n{log(ln)}\n```\n")
    o.append(f"**Result:** {i['note']}\n\n**Scores:** Basic {i['basic']}/40 | Specialized {i['specialized']}/60 | Total {i['total']}/100\n\n**Assertions:**")
    for a in i["assertions"]: o.append(f"- [{a['result']}] {a['text']} - {a['note']}")
    o.append("")
rv = R["veto_gates"]["research_veto"]
o.append("## Research Veto (Data Analysis)\n\n| Dim | Result | Detail |\n|---|---|---|")
for k in ("scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"): o.append(f"| {k} | {rv[k]['result']} | {rv[k]['detail']} |")
o.append("\n## Key Strengths")
for x in R["key_strengths"]: o.append(f"- {x}")
o.append("\n## Recommendations")
for r in R["recommendations"]:
    o.append(f"**[{r['priority']}] {r['title']}** (observed in inputs {r['observed_in']})\n- Problem: {r['problem']}\n- Root cause: {r['root_cause']}\n- Fix: {r['fix']}\n")
o.append("## Verified-as-correct claims (by output)\n- default `-d 0` disables optical detection; `dt:Z:SQ/LB` emitted with -d; `-t` adds `do` tag\n- `--use-read-groups` keys on RG ID (Picard on LB): same-library 2-RG BAM 0 vs 60 flagged\n- `fixmate -r -m` drops secondary/unmapped; `-f`, `-s`, `--json` stats\n- `--barcode-tag RX`, `--read-coords`, `--barcode-name` exist in samtools 1.24 help\n- pysam.fixmate/markdup/sort/index all work; errors raise SamtoolsError\n- `--method=directional` is the umi_tools default; `unique` keeps more molecules\n")
o.append("## Not verified\nbiobambam2, pbmarkdup, '~30% faster' pipeline claim, 'added in samtools 1.16' for --barcode-tag, Cell Ranger CB/UB dedup, ChIP/ATAC/aDNA rows (assay advice inspected, not executed).\n")
o.append("## Cleanup\nrun/work/ (39 MB intermediates) deleted after the run; logs kept in run/*.log. No files written inside F:/OpenScience/external (no __pycache__ in the clone).\n")
open(f"{B}/eval_viewer_bio-duplicate-handling.md", "w", encoding="utf-8", newline="\n").write("\n".join(o))
print("viewer written", sum(len(x) for x in o))
