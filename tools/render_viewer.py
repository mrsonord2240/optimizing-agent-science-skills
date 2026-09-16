#!/usr/bin/env python3
"""Render an eval viewer from a skill-auditor report.

Auditors normally hand-write eval_viewer_<skill-id>.md alongside the report, and that narrative is
the better document: it argues from the runs rather than restating scores. Some audits finished
without one, and publish_audits.py needs a viewer. This renders one from the report alone.

Every line it writes is a field of the report. It adds no finding, evidence or judgement that the
auditor did not record, and it says so at the top of what it writes so the two kinds of viewer are
never mistaken for each other.

Usage:
  render_viewer.py --skill bio-pathway-go-enrichment [--audits F:/OpenScience/audits] [--force]
"""
import argparse
import json
import os

AUDITS = os.environ.get("OASS_AUDITS", "F:/OpenScience/audits")

PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


def clean(text):
    return " ".join(str("" if text is None else text).split())


def table(rows, headers):
    lines = ["| " + " | ".join(headers) + " |",
             "|" + "|".join("---" for _ in headers) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(c).replace("|", "\\|") for c in row) + " |")
    return lines


def render(report, skill_id):
    meta = report.get("meta", {})
    final = report.get("final", {})
    static = report.get("static_score", {})
    dynamic = report.get("dynamic_score", {})
    inputs = dynamic.get("inputs", []) or []
    rate = dynamic.get("assertion_pass_rate", {}) or {}

    out = [
        f"# Eval Viewer — {skill_id}",
        "",
        f"Generated: {meta.get('evaluated_on')} · rendered from `report.json` by `tools/render_viewer.py`.",
        "",
        "> This viewer is **generated from the audit report**, not written by the auditor. It restates"
        " the report's own recorded scores, notes and assertions and adds nothing to them. Where a"
        " hand-written viewer would argue from the runs, this one points at the scripts in"
        " [scripts/](scripts/) instead.",
        "",
        f"Source: `{meta.get('source')}`",
    ]
    if meta.get("audit_type"):
        out.append(f"Audit type: {clean(meta['audit_type'])}")
    out += [
        f"Category: {meta.get('category')} · Execution mode: {meta.get('execution_mode')}"
        f" · Complexity: {meta.get('complexity')} · N = {meta.get('n_inputs')}"
        f" · Executed: {meta.get('executed_inputs')}",
        "",
    ]
    if meta.get("description"):
        out += ["## What the Skill claims to do", "", clean(meta["description"]), ""]

    if inputs:
        out += ["## Summary Table", ""]
        out += table(
            [[i.get("index"), clean(i.get("type")), i.get("basic"), i.get("specialized"),
              f"**{i.get('total')}**",
              f"{i.get('assertions_passed')}/{i.get('assertions_total')}",
              "yes" if i.get("executed") else "no",
              i.get("status_flag") or clean(i.get("status"))] for i in inputs],
            ["Input", "Type", "Basic /40", "Specialized /60", "Total /100",
             "Assertions", "Executed", "Status"])
        out += [
            "",
            f"**Execution Average: {dynamic.get('execution_avg')} / {dynamic.get('max')}**"
            f" · **Assertion Pass Rate: {rate.get('passed')}/{rate.get('total')}**",
            "",
        ]

    out += [
        f"**Static: {static.get('subtotal')}/{static.get('max')}**"
        f" · Static weighted {final.get('static_weighted')} + dynamic weighted"
        f" {final.get('dynamic_weighted')} = **{final.get('score')}/{final.get('max')}**"
        f" → {final.get('grade_symbol', '')} {final.get('grade')},"
        f" {'deployable' if final.get('deployable') else 'not deployable'}."
        + (" **Veto override applied.**" if final.get("veto_override") else ""),
        "",
        "---",
        "",
    ]

    out += ["## Veto gates", ""]
    for name, gate in (report.get("veto_gates") or {}).items():
        if not isinstance(gate, dict):
            continue
        title = name.replace("_", " ").capitalize()
        if gate.get("applicable") is False:
            out += [f"### {title} — not applicable", ""]
            continue
        out += [f"### {title} — **{gate.get('gate')}**", ""]
        rows = []
        for key, value in gate.items():
            if key in ("gate", "applicable"):
                continue
            if isinstance(value, dict):
                rows.append([key.replace("_", " "), value.get("result"), clean(value.get("detail"))])
            else:
                rows.append([key.replace("_", " "), value, ""])
        if rows:
            out += table(rows, ["Check", "Result", "Detail"]) + [""]

    categories = (static.get("categories") or {})
    if categories:
        out += ["## Static score", ""]
        out += table(
            [[k.replace("_", " "), f"{v.get('score')}/{v.get('max')}", clean(v.get("note"))]
             for k, v in categories.items()],
            ["Category", "Score", "Note"]) + [""]

    for item in inputs:
        out += [
            f"## Input {item.get('index')} — {clean(item.get('type'))}: {clean(item.get('label'))}",
            "",
            f"- Status: {item.get('status_flag') or ''} {clean(item.get('status'))}"
            f" · Basic {item.get('basic')}/40 · Specialized {item.get('specialized')}/60"
            f" · **Total {item.get('total')}/100**",
        ]
        if item.get("execution_note"):
            out.append(f"- Execution: {clean(item['execution_note'])}")
        if item.get("note"):
            out.append(f"- Finding: {clean(item['note'])}")
        out.append("")
        assertions = item.get("assertions") or []
        if assertions:
            out += table(
                [[clean(a.get("text")), a.get("result"), clean(a.get("note"))] for a in assertions],
                ["Assertion", "Result", "Evidence"]) + [""]

    strengths = report.get("key_strengths") or []
    if strengths:
        out += ["## Key strengths", ""] + [f"- {clean(s)}" for s in strengths] + [""]

    recommendations = sorted(report.get("recommendations") or [],
                             key=lambda r: PRIORITY_ORDER.get(r.get("priority"), 9))
    if recommendations:
        out += ["## Recommendations", ""]
        for rec in recommendations:
            observed = rec.get("observed_in")
            observed = ", ".join(str(o) for o in observed) if isinstance(observed, list) else clean(observed)
            out += [
                f"### {rec.get('priority')} — {clean(rec.get('title'))}",
                "",
                f"- Observed in inputs: {observed or '—'}",
                f"- Problem: {clean(rec.get('problem'))}",
                f"- Root cause: {clean(rec.get('root_cause'))}",
                f"- Fix: {clean(rec.get('fix'))}",
                "",
            ]

    return "\n".join(out).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True)
    parser.add_argument("--audits", default=AUDITS)
    parser.add_argument("--force", action="store_true",
                        help="overwrite an existing viewer (by default a hand-written one is kept)")
    args = parser.parse_args()

    folder = os.path.join(args.audits, args.skill)
    report_path = os.path.join(folder, f"eval_report_{args.skill}_result.json")
    viewer_path = os.path.join(folder, f"eval_viewer_{args.skill}.md")
    if os.path.isfile(viewer_path) and not args.force:
        raise SystemExit(f"{viewer_path} already exists; pass --force to overwrite it")
    with open(report_path, encoding="utf-8") as f:
        report = json.load(f)
    with open(viewer_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(render(report, args.skill))
    print(f"wrote {viewer_path}")


if __name__ == "__main__":
    main()
