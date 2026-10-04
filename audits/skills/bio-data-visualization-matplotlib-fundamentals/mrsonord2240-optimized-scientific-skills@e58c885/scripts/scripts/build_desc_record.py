"""Build the description-trim delta record (report.json, viewer.md) from the certifying record.
Usage: build_desc_record.py <skill-id>"""
import json, re, sys
from pathlib import Path

sid = sys.argv[1]
REC = Path(r"F:\optimizing-agent-science-skills\audits\skills")
RUN = Path(rf"F:\OpenScience\audits\{sid}\delta-desc-20261003")
W = Path(r"F:\OpenScience\wt\normalize-dv-lane1\skills") / sid
cfg = {
    "bio-data-visualization-volcano-and-ma-plots": dict(
        cert="a86f2698a953bfc46b2db74122acd9d20a49a5e0195bace6e3663282a44d8d83", ver="candidate@a86f2698a953-delta-dv1-20261003",
        cb=37959, new="0bc1e67d46d6b7cfdffd1d42ef1f35779a7f0fe712d8460e3ee602684bd4aeeb", nf=7, nb=37711, openp2="VOL-010",
        verdict="Sufficient and accurate. It names the domain (volcano or MA plot), the input (per-feature effect-size and p-value table) and the data types, and no sibling covers differential-expression plots. The dropped clauses (LFC shrinkage, EnhancedVolcano/ggplot2/matplotlib, axis truncation) describe what the Skill does once loaded, not when to load it, and a query naming shrinkage or EnhancedVolcano still contains 'volcano' or 'MA plot'."),
    "bio-data-visualization-ggplot2-fundamentals": dict(
        cert="228c088cf299564fd21d2b9d79a3963e5c0b4a500158bcb4732a1b277e6160e6", ver="candidate@228c088cf299-delta-dv1-20261003",
        cb=23322, new="9d1247b0d8cd48c336a6e7ca866603cc3499b667e759af8f866583d076f0507b", nf=5, nb=23077, openp2="GG-010",
        verdict="Sufficient and accurate. It names the tool (ggplot2), the language (R) and the intent (static publication figures for papers, presentations or reports), which separates it from the matplotlib Skill (Python) and from the shelf's specialised plot Skills (volcano, forest, oncoprint, network, sequence logo, annotation, dimensionality reduction, palettes), none of which is a generic ggplot2 fundamentals Skill. Dropped detail (cairo_pdf, tidy evaluation, theme_classic) is body content."),
    "bio-data-visualization-matplotlib-fundamentals": dict(
        cert="79a08cbdf5339dbf6f824d9532cc4720ef00102a9985831c5c56c051c8150611", ver="candidate@79a08cbdf533-delta-dv1-20261003",
        cb=24925, new="f5acfdfb52509e5422c25f3dec2481ef4f182e5c0730398f2bd5bcd2d7fb2a90", nf=5, nb=24583, openp2="MPL-011",
        verdict="Sufficient and accurate, with one soft spot. It names the tool (matplotlib), language (Python) and intent (publication figures) and separates cleanly from the ggplot2 Skill. Soft spot, not recorded as a finding: the example 'single-cell embeddings' overlaps dimensionality-reduction-plots, whose description (PCA, t-SNE, UMAP) is more specific and should win for embedding requests; the clause is inherited from the certified description, but it is now the only text, and seaborn (covered by an SKILL.md section) is no longer named, so a seaborn-only request may not surface this Skill. Neither is likely to cause a wrong pick; both are cheap to adjust if Sam wants."),
}[sid]
PRIOR = sorted((RUN.parent).glob("delta-dv1-20261003"))[0]
rep = json.loads((PRIOR / "report.json").read_text(encoding="utf-8"))
txt = (W / "SKILL.md").read_text(encoding="utf-8")
import yaml
desc = yaml.safe_load(txt.split("---", 2)[1])["description"]
assert desc.startswith("Use when")
rep["meta"]["description"] = desc
if sid.endswith("matplotlib-fundamentals"):
    c = rep["static_score"]["categories"]["agent_specific"]
    c["note"] = c["note"] + " The trimmed description keeps the Python/matplotlib trigger; its 'single-cell embeddings' example overlaps dimensionality-reduction-plots (inherited, not a defect)."
(RUN / "report.json").write_text(json.dumps(rep, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

v = (PRIOR / "viewer.md").read_text(encoding="utf-8")
sec = lambda name: v.index(name)
summary = v[sec("## Summary"):sec("## Finding verdicts")]
tail = v[sec("## Veto review"):]
summary = re.sub(r"Readiness decision:.*", lambda m: f"Readiness decision: **candidate-ready** for this exact identity (final {rep['final']['score']}, static {rep['static_score']['subtotal']}, execution average {rep['dynamic_score']['execution_avg']}, assertions {rep['dynamic_score']['assertion_pass_rate']['passed']}/{rep['dynamic_score']['assertion_pass_rate']['total']}, no veto, no open P0 or P1; open P2: {cfg['openp2']}). Scores are the certifying record's, carried forward; the static score did not move.", summary)
head = f"""# Eval Viewer — {sid}

Generated: 2026-10-03  
Audit type: delta re-audit (frontmatter `description` trimmed to its "Use when ..." clause)  
Exact candidate content SHA-256: `{cfg['new']}` (files={cfg['nf']}, bytes={cfg['nb']})  
Certified baseline (carried forward): `{cfg['cert']}` (files={cfg['nf']}, bytes={cfg['cb']}), record `{cfg['ver']}`

## Delta qualification

- `skill_preflight --offline` on the candidate: PASS, identity {cfg['new']}, files={cfg['nf']}, bytes={cfg['nb']} (re-checked at the end of the run).
- Reverting `edits.json` (fix-description-20261003) on a scratch copy (`scripts/desc_qualify.py`, `scripts/logs/qualify.log`) reproduces the certified identity {cfg['cert']} exactly.
- File sets are identical; exactly one file differs (`SKILL.md`), and exactly one line (line 3, `description:`) differs (`scripts/diff_SKILL.md.txt`). No script, reference or usage-guide byte changed.
- The new frontmatter parses with a YAML loader as a single string beginning "Use when" (log above); `name` equals the directory name.
- Delta mode qualifies: prose/frontmatter only, under the contract's limits.

## New description

> {desc}

Verdict: {cfg['verdict']}

"""
mid = f"""## Finding verdicts

| Finding | Verdict | Evidence |
|---|---|---|
| {cfg['openp2']} (P2) | open, untouched | no code or body change in this delta; certifying evidence stands |
| Description trim | no new finding | accurate to the Skill body, parses as one YAML string, sufficient trigger (see verdict above) |
| Other certified findings and passes | carried forward unchanged | every non-frontmatter byte is identical to the certified bytes, so the certifying record's execution evidence (record `{cfg['ver']}` and its scripts) applies unchanged |

## Executed versus carried

| Surface | Classification | Evidence |
|---|---|---|
| Changed line (frontmatter `description`) | executed | YAML parse and revert/diff qualification, `scripts/logs/qualify.log` |
| All scripts and workflows | carried (hash-identical to the certified bytes) | record `{cfg['ver']}`; no behaviour changed, no rerun required by the delta contract |

"""
(RUN / "viewer.md").write_text(head + summary + mid + tail, encoding="utf-8")
print("ok", sid, rep["final"]["score"], rep["static_score"]["subtotal"], rep["dynamic_score"]["execution_avg"])