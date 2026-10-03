#!/usr/bin/env python3
"""Delta re-audit record builder (lane D1). Carries the certifying report forward, applies the re-scores and finding changes below,
re-derives every aggregate, validates with validate_report.py and writes report.json, viewer.md and source-identity.json into each run root.
Usage: py d1_build.py   (run from anywhere; paths are absolute)"""
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REC = Path(r"F:\optimizing-agent-science-skills")
AUD = Path(r"F:\OpenScience\audits")
WT = r"F:\OpenScience\wt\normalize-dv-lane1"
RUN = "delta-dv1-20261003"
MAXC = {"functional_suitability": 12, "reliability": 12, "performance_context": 8, "agent_usability": 16,
        "human_usability": 8, "security": 12, "maintainability": 12, "agent_specific": 20}

S = {}

# ---------------------------------------------------------------- volcano
S["bio-data-visualization-volcano-and-ma-plots"] = dict(
    upstream="volcano-and-ma-plots",
    cert_run="candidate@fa3ec8783a79-reaudit-dv1-20261003", cert_id="fa3ec8783a79b7c7a36fcf2d941d4fcc1aca6ab2ec3a8925e72fe6fa3a9af008",
    cert_files=7, cert_bytes=37956, new_id="a86f2698a953bfc46b2db74122acd9d20a49a5e0195bace6e3663282a44d8d83", new_bytes=37959,
    static={"functional_suitability": (11, "Covers shrinkage choice, ggplot2, EnhancedVolcano, MA and sanbomics with verified API facts; the quoted airway numbers now equal the re-measured values (VOL-009 closed); the capped-axis labelling is still unreadable (VOL-010)."),
            "agent_usability": (15, "Operational rule and design choices are explicit and each tested; the numbers in failure-modes and reconciliation now match a re-measurement on real data (39 hidden genes, median 0.7648 printed as 0.76).")},
    inputs={5: dict(basic=35, specialized=54, status="COMPLETED",
                    note="API behaviour reproduces and the quoted numbers equal the re-measured values: cap 50 hides 39 significant genes, median |LFC| 0.7648 (printed 0.76), 17,994 drawn points, PDFs 555,573 and 685,915 B (0.56 and 0.69 MB), MA 444/23 KB on all 29,391 rows.",
                    flip={"Measured numbers quoted in the references equal re-measured values.":
                          "39 hidden genes (r2b), 0.7648 printed as 0.76 (r3), 17,994 drawn points and 555,573 / 685,915 B PDFs (d1_core), 444 / 23 KB on 29,391 rows (r5), all re-run on the candidate bytes."})},
    findings={"VOL-009": ("closed", "all five stale numbers corrected and re-measured on the candidate bytes; no new number wrong")},
    drop=["VOL-009"], add=[],
    strengths_add=[],
    verdict_rows=[
        ("VOL-009 (P2) stale quoted numbers", "corrected (closed)",
         "failure-modes.md and reconciliation: 39 hidden genes = 39 re-measured (`scripts/logs/d1_cap50.log`); SKILL.md median 0.76 = round(0.7648) (`scripts/logs/d1_stats.log`); volcano_phd.R comment 17,994 drawn points, 0.56 / 0.69 MB = 555,573 / 685,915 B decimal MB (`scripts/logs/d1_core.log`); MA 23/444 KB tied to all 29,391 rows = 23 / 444 KB measured on 29,391 rows (`scripts/logs/d1_ma.log`)"),
        ("VOL-010 (P2) y_cap labels pile onto the cap", "open, untouched", "no change in the delta (needs code); certifying evidence stands"),
        ("Other certified findings and passes", "carried forward unchanged", "scripts' executable statements are byte-for-byte equivalent (R parse identical); untouched assertions are the certifying run's")],
    executed=[
        ("`scripts/volcano_phd.R` (comment-only edit)", "executed", "`scripts/d1_core.R`, `scripts/logs/d1_core.log`: ran to the end on the fitted airway dds, exit 0, RESULT PASS; volcano.pdf 555,573 B, ma_plot.pdf 685,915 B; counts, boundary and EnhancedVolcano colours as certified"),
        ("Changed numeric claims (39 genes, median, MA sizes)", "executed", "`scripts/r2b_cap50.R`, `scripts/r3_stats_claims.R`, `scripts/r5_ma_python.py` re-run on the candidate; the r3 script's own '0.77' assertion is the stale pre-fix claim and fails by design, the Skill now says 0.76"),
        ("`scripts/volcano_plot.R`, `scripts/ma_plot.py` bytes", "carried (hash-identical)", "certifying run `reaudit-dv1-20261003`; ma_plot.py also re-run above"),
        ("SKILL.md R blocks, sanbomics and shrinkage statements", "carried", "certifying run; prose around them unchanged except the two edited sentences")],
    rec_rewrite={},
)

# ---------------------------------------------------------------- ggplot2
S["bio-data-visualization-ggplot2-fundamentals"] = dict(
    upstream="ggplot2-fundamentals",
    cert_run="candidate@be703ae7f695-reaudit-dv2-20261003", cert_id="be703ae7f69598daa981d477afa71a873d0616a2f2830936b575c014a1f3f120",
    cert_files=5, cert_bytes=22972, new_id="228c088cf299564fd21d2b9d79a3963e5c0b4a500158bcb4732a1b277e6160e6", new_bytes=23322,
    static={"functional_suitability": (12, "Covers grammar, theme, programmatic aes, export and helper workflows; the volcano default (10 symbols / 3 IDs) works and the stated zero-overlap envelope now names width and height, the dataset and 'label boxes only', each re-measured (GG-011 closed)."),
            "agent_usability": (15, "Idioms, guardrails and the label-collision rule are clear and say 'open the figure'; the envelope now states the composite height, the single measured dataset and that threshold lines and points can still cross labels."),
            "human_usability": (8, "Readable; failure-modes.md states the ggrepel drop is silent; the usage-guide install line now names every package the shipped script loads (GG-012 closed).")},
    inputs={},
    findings={"GG-011": ("closed", "envelope wording reproduces row by row"), "GG-012": ("closed", "install line complete; stray axes='collect' remark gone")},
    drop=["GG-011", "GG-012"], add=[], strengths_add=[],
    verdict_rows=[
        ("GG-011 (P2) envelope omits composite height and dataset; 'no collisions' means boxes only", "corrected (closed)",
         "SKILL.md now: airway DESeq2 results only, symbols standalone to 89 mm wide, Ensembl to 120 mm wide, composites at 183 x 120 and 183 x 150 mm, 183 x 90 composite 1 pair (STEAP2~MAOA), re-ranked Ensembl set 3 pairs at 183 x 120 mm, label boxes only, open the figure. Re-run on ggplot2 4.0.3: `scripts/logs/d1_probe_gg4.log` and `scripts/logs/d1_measure_gg4.log` reproduce every number (183 x 90 symbols 1 pair; m3_ens_maxlfc 3 pairs at 183 x 100 and 183 x 120; 183 x 120 and 183 x 150 default composites 0 pairs; 120 x 110 composites collide)"),
        ("GG-012 (P2) install line omits packages the script loads", "corrected (closed)",
         "`scripts/d1_install_line.R` / `scripts/logs/d1_install_line.log`: the line names ggplot2, scales, ggrepel, ggtext, viridis, scico, ggrastr, patchwork, dplyr; `scripts/publication_figures.R` loads ggplot2, ggrepel, patchwork, dplyr (no `::` use): none missing, all nine load in the staged R; no `axes`/`collect` remark remains anywhere in the Skill"),
        ("GG-010 (P2) NA label stops create_volcano", "open, untouched", "needs code; certifying evidence stands"),
        ("Other certified findings and passes", "carried forward unchanged", "no script byte changed (hash-identical to the certified files); the edited files are SKILL.md and usage-guide.md only")],
    executed=[
        ("Label-overlap envelope (changed claim), drawn ggrepel boxes", "executed", "`scripts/lane1_gg_overlap_measure.R`, `scripts/rb_envelope_probe.R`; `scripts/logs/d1_measure_gg4.log`, `scripts/logs/d1_probe_gg4.log` (ggplot2 4.0.3, candidate bytes)"),
        ("Install line vs script loads (changed command)", "executed", "`scripts/d1_install_line.R`, `scripts/logs/d1_install_line.log`: PASS"),
        ("ggplot2 3.5.2 envelope rows", "carried", "certifying run `reaudit-dv2-20261003` (`scripts/logs/measure_gg35.log`): script bytes and packages unchanged; the changed prose only restates the 4.0.3-identical numbers"),
        ("All script behaviour, SKILL.md blocks, PDF fonts, PCA contract, failure modes", "carried (hash-identical scripts)", "certifying run `reaudit-dv2-20261003`")],
    rec_rewrite={},
)

# ---------------------------------------------------------------- matplotlib
NEW_MPL = {
    "priority": "P2",
    "title": "MPL-011 the named public legend route omits margins and clips the x label",
    "observed_in": [3],
    "problem": "SKILL.md and the script comment name the public route as Plot.on(fig), move fig.legends[0], fig.subplots_adjust(right=0.76). Run exactly so on an 89 x 70 mm figure the legend sits inside the page and clear of the axes (x 0.815-0.988, axes end 0.760), but the axes tight box reaches y = -0.007 and the x-axis label is cut at the page edge (ink on the last pixel row, scripts/figures/right076_only.png). The measured route in the certifying run also set left = 0.13, bottom = 0.17 and top = 0.97 and is clean (44 px bottom margin).",
    "root_cause": "The disclosure wording kept only the right-margin argument of the measured subplots_adjust call.",
    "fix": "Text-only: write the route as fig.subplots_adjust(left=0.13, bottom=0.17, right=0.76, top=0.97) in SKILL.md and in the script comment, or name only the legend move and say the margins must be set so the x label stays inside the page.",
}
S["bio-data-visualization-matplotlib-fundamentals"] = dict(
    upstream="matplotlib-fundamentals",
    cert_run="candidate@f1efaf7eef6c-reaudit-dv2-20261003", cert_id="f1efaf7eef6c18085eabaa140a3696db8e35e5d14624396d1f7c22643d398e7a",
    cert_files=5, cert_bytes=24264, new_id="79a08cbdf5339dbf6f824d9532cc4720ef00102a9985831c5c56c051c8150611", new_bytes=24925,
    static={"agent_usability": (15, "Clear defaults and guardrails with trigger/mechanism/symptom/fix; section 7 now names the private-attribute dependency, the fixed 22 % reserve and the 29-character-title overflow (13 mm), but its public alternative is incomplete (MPL-011).")},
    inputs={3: dict(basic=34, specialized=50, status="PARTIAL",
                    note="Page stays exactly 89x70 mm and the legend stays inside it in every variant; it clears the axes for the shipped labels, longer labels alone and 8 and 12 classes; a 29-character title overflows into the axes by 13.0 mm with the shipped labels (51 characters: x0 0.299). The Skill now discloses the private Plot.plot()._figure use, the seaborn 0.13.2-only check, the fixed 22 % reserve and that overflow, and names a public route; that route as worded (right=0.76 only) clips the x label (MPL-011).",
                    flip={"The limits of the recipe (fixed 22 % reserve, private Plot.plot()._figure, verified on seaborn 0.13.2 only) are disclosed in SKILL.md or the script":
                          "SKILL.md and the script comment now state the private Plot.plot()._figure use, seaborn 0.13.2 only, the fixed 22 % reserve and that a 29-character title covers 13 mm; re-measured: 'Differential expression class' with the shipped labels x0 0.604 vs axes end 0.750 = 13.0 mm (`scripts/logs/d1_legend_probe.log`)."},
                    append=[{"text": "The public route as worded (Plot.on(fig), move fig.legends[0], fig.subplots_adjust(right=0.76)) gives a clean 89 x 70 mm figure", "result": "FAIL",
                             "note": "legend x 0.815-0.988 inside the page and clear of the axes (0.760), but the axes tight box reaches y -0.007 and the x label is clipped at the page edge; the measured route also set left 0.13, bottom 0.17, top 0.97 (`scripts/logs/d1_legend_probe.log`, `scripts/logs/d1_ink_probe.log`, right076_only.png opened)."}])},
    findings={"MPL-010": ("closed", "disclosure present and measured true; the public route it names is incomplete, raised as MPL-011")},
    drop=["MPL-010"], add=[NEW_MPL], strengths_add=[],
    verdict_rows=[
        ("MPL-010 (P2) legend recipe discloses neither private attribute nor 22 % reserve", "corrected (closed); residual P2 MPL-011",
         "SKILL.md and `scripts/matplotlib_phd.py` comment now state: p._figure private, seaborn 0.13.2 only, fixed 22 %, 29-character title covered 13 mm. Re-measured: 29-character title with the shipped labels x0 0.604 vs axes end 0.750 = 13.0 mm; with longer labels the same; shipped title clear (`scripts/logs/d1_legend_probe.log`); script re-run: exit 0, five PDFs 89x70, 180x110, 89x90, 89x70, 89x70 mm, legend 0.815-0.988, rerun reproduces every PDF (`scripts/logs/d1_m1_phd.log`, `scripts/logs/d1_standalone.log`)"),
        ("MPL-011 (P2, new) public route as worded clips the x label", "open (raised by this delta)",
         "`scripts/logs/d1_legend_probe.log`, `scripts/logs/d1_ink_probe.log`: with only right=0.76 the label is cut at the page edge; with left 0.13 / bottom 0.17 / right 0.76 / top 0.97 it is clean (44 px margin at 300 dpi). The edit followed the certifying record's own suggestion verbatim."),
        ("Other certified findings and passes", "carried forward unchanged", "script AST identical to the certified bytes (comments only); other blocks and references untouched")],
    executed=[
        ("`scripts/matplotlib_phd.py` (comment-only edit)", "executed", "standalone `py.sh matplotlib_phd.py`: exit 0 (`scripts/logs/d1_standalone.log`); `scripts/m1_phd.py` on the candidate: 5 PDFs at exact mm sizes, legend inside the page and clear of the axes, determinism across two runs; the lone known FAIL is the seaborn-internal Pandas4Warning, identical to the certifying log"),
        ("Section 7 limits and public route (changed claims)", "executed", "`scripts/d1_legend_probe.py`, `scripts/d1_ink_probe.py`; `scripts/logs/d1_legend_probe.log`, `scripts/logs/d1_ink_probe.log`; figures opened"),
        ("SKILL.md blocks, chart-recipes, failure-modes, usage-guide, other claims", "carried (hash-identical)", "certifying run `reaudit-dv2-20261003`")],
    rec_rewrite={},
)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def build(sid, c):
    run = AUD / sid / RUN
    cert = json.loads((REC / "audits/skills" / sid / c["cert_run"] / "report.json").read_text(encoding="utf-8"))
    r = copy.deepcopy(cert)
    r["meta"]["evaluated_on"] = "2026-10-03"
    for k, (score, note) in c["static"].items():
        r["static_score"]["categories"][k] = {"score": score, "max": MAXC[k], "note": note}
    for n, spec in c["inputs"].items():
        i = r["dynamic_score"]["inputs"][n - 1]
        i["basic"], i["specialized"], i["status"], i["note"] = spec["basic"], spec["specialized"], spec["status"], spec["note"]
        for a in i["assertions"]:
            for key, note in spec.get("flip", {}).items():
                if a["text"].startswith(key[:60]) or key.startswith(a["text"][:60]):
                    a["result"], a["note"] = "PASS", note
                    break
        i["assertions"] += spec.get("append", [])
        if n == 5 and "Measured numbers quoted in the references equal re-measured values." not in [a["text"] for a in i["assertions"]]:
            pass
    # recompute derived values
    cats = r["static_score"]["categories"]
    r["static_score"]["subtotal"] = sum(v["score"] for v in cats.values())
    ins = r["dynamic_score"]["inputs"]
    P = T = 0
    for i in ins:
        i["total"] = i["basic"] + i["specialized"]
        i["assertions_passed"] = sum(a["result"] == "PASS" for a in i["assertions"])
        i["assertions_total"] = len(i["assertions"])
        i["status_flag"] = "\u274c" if i["status"] in ("PARTIAL", "ERROR") else ("\u2705" if i["total"] >= 75 else "\u26a0\ufe0f")
        P += i["assertions_passed"]
        T += i["assertions_total"]
    avg = round(sum(i["total"] for i in ins) / len(ins), 1)
    r["dynamic_score"]["execution_avg"] = avg
    r["dynamic_score"]["assertion_pass_rate"] = {"passed": P, "total": T}
    sw, dw = round(r["static_score"]["subtotal"] * 0.4, 1), round(avg * 0.6, 1)
    score = round(sw + dw)
    f = r["final"]
    f.update(static_weighted=sw, dynamic_weighted=dw, score=score)
    assert score >= 85 and f["grade"] == "Production Ready" and f["deployable"] and not f["veto_override"]
    recs = [x for x in r["recommendations"] if x["title"].split(" ", 1)[0] not in c["drop"]] + c["add"]
    r["recommendations"] = sorted(recs, key=lambda x: x["priority"])
    (run / "report.json").write_text(json.dumps(r, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    v = subprocess.run([sys.executable, str(run / "scripts/validate_report.py"), str(run / "report.json")], capture_output=True, text=True)
    print(sid, v.stdout.replace("\n", " "), v.stderr)
    assert v.returncode == 0
    # source identity
    ident = run / "source-identity.json"
    cand = rf"{WT}\skills\{sid}"
    m = subprocess.run([sys.executable, str(run / "scripts/make_identity.py"), sid, c["upstream"], cand, WT, str(ident)], capture_output=True, text=True)
    print(m.stdout.strip(), m.stderr.strip())
    assert c["new_id"] in m.stdout
    # viewer
    me, d, s, vg = r["meta"], r["dynamic_score"], r["static_score"], r["veto_gates"]
    L = [f"# Eval Viewer \u2014 {me['skill_name']}", "", f"Generated: {me['evaluated_on']}  ",
         "Audit type: delta re-audit (text-only changes to certified bytes)  ", f"Exact candidate content SHA-256: `{c['new_id']}` (files={c['cert_files']}, bytes={c['new_bytes']})  ",
         f"Certified baseline (carried forward): `{c['cert_id']}` (files={c['cert_files']}, bytes={c['cert_bytes']}), record `{c['cert_run']}`", "",
         "## Delta qualification", "",
         f"- `skill_preflight --offline` on the candidate: PASS, identity {c['new_id']}, files={c['cert_files']}, bytes={c['new_bytes']}.",
         "- Reverting the edit pairs listed in the fix log on a scratch copy (`scripts/d1_revert.py`, `scratch/`) reproduces the certified identity exactly" + (" (and the certifying run's own work copy `reaudit-dv2-20261003/work_gg4/skill` has the certified file hashes)." if sid.endswith("ggplot2-fundamentals") else "."),
         "- Changed files differ only in prose, comments or string literals (per-file diffs in `scripts/diff_*.txt`)." ,
         ("- `scripts/volcano_phd.R`: `deparse(parse(keep.source = FALSE))` identical to the certified bytes (50 lines, `scripts/r_ast_compare.R`); script re-run once, exit 0." if sid.endswith("volcano-and-ma-plots") else
          "- `scripts/matplotlib_phd.py`: `ast.dump` identical to the certified bytes; script re-run once, exit 0 (`scripts/logs/d1_standalone.log`)." if sid.endswith("matplotlib-fundamentals") else
          "- No script file changed; `scripts/publication_figures.R` is byte-identical to the certified file."),
         "- Environment fingerprint sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 over `snapshots/lane1_versions.txt`, re-hashed identical at start and end.", "",
         "## Summary", "", "| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |", "|---|---|---:|---:|---:|---:|---|"]
    for i in d["inputs"]:
        L.append(f"| {i['index']} | {i['type']} | {i['basic']} | {i['specialized']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} | {i['status_flag']} {i['status']} |")
    ap = d["assertion_pass_rate"]
    open_ids = ", ".join(x["title"].split(" ", 1)[0] for x in r["recommendations"])
    L += ["", f"**Execution average:** {d['execution_avg']} / 100  ", f"**Assertion pass rate:** {ap['passed']} / {ap['total']} ({100 * ap['passed'] / ap['total']:.1f} %)  ",
          f"**Static score:** {s['subtotal']} / 100  ", f"**Final score:** {f['score']} / 100 \u2014 {f['grade_symbol']} {f['grade']}  ", f"**Research veto:** {vg['research_veto']['gate']}", "",
          f"Readiness decision: **candidate-ready** for this exact identity ({f['score']} final, static {s['subtotal']}, execution average {d['execution_avg']}, assertions {ap['passed']}/{ap['total']}, no veto, no open P0 or P1; open P2: {open_ids}). Scores are the certifying report's, re-scored only where the change touches (see below).", "",
         "## Finding verdicts", "", "| Finding | Verdict | Evidence |", "|---|---|---|"]
    for a, b, e in c["verdict_rows"]:
        L.append(f"| {a} | {b} | {e} |")
    L += ["", "## Executed versus carried", "", "| Surface | Classification | Evidence |", "|---|---|---|"]
    for a, b, e in c["executed"]:
        L.append(f"| {a} | {b} | {e} |")
    L += ["", "## Veto review", "", f"- Skill veto: {vg['skill_veto']['gate']} (stability, contract, determinism, security all {vg['skill_veto']['stability']}); carried, no executable byte changed.", f"- Research veto: {vg['research_veto']['gate']}"]
    for k in ("scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"):
        L.append(f"  - {k}: {vg['research_veto'][k]['result']} \u2014 {vg['research_veto'][k]['detail']}")
    L += ["", "## Static categories", ""] + [f"- {k}: {x['score']}/{x['max']} \u2014 {x['note']}" for k, x in cats.items()]
    L += ["", "## Detailed outputs", ""]
    for i in d["inputs"]:
        L += [f"### Input {i['index']} \u2014 {i['type']}: {i['label']}", "", f"**Status:** {i['status']} \u2014 {i['note']}  ", f"**Scores:** Basic {i['basic']}/40 | Specialized {i['specialized']}/60 | Total {i['total']}/100", "", "**Assertions:**", ""]
        L += [f"- {a['result']} \u2014 {a['text']} ({a['note']})" for a in i["assertions"]]
        L.append("")
    L += ["## Key strengths", ""] + [f"- {x}" for x in r["key_strengths"]]
    L += ["", "## Recommendations", ""] + [f"- **[{x['priority']}] {x['title']}** (inputs {x['observed_in']}): {x['problem']} Fix: {x['fix']}" for x in r["recommendations"]]
    (run / "viewer.md").write_text("\n".join(L) + "\n", encoding="utf-8")


for sid, c in S.items():
    build(sid, c)
