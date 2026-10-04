import json, os
A = r"F:\OpenScience\audits"
res = json.load(open(os.path.join(A, "delta2_results.json")))
RUN = "reaudit-delta2-20261003"
ROOT_T = "F:" + chr(92) + "OpenScience" + chr(92) + "audits" + chr(92) + "{sid}" + chr(92) + RUN + chr(92)
VERD = {
"bio-splicing-quantification": """**Sufficient, accurate, no finding.** "Use when measuring splice-site usage or isoform inclusion ratios (PSI) from short-read RNA-seq."
Shelf siblings checked (read-only): `bio-differential-splicing` (comparing patterns between groups), `bio-long-read-splicing` (long reads), `bio-single-cell-splicing`, `bio-splicing-qc` (data suitability), `bio-outlier-splicing-detection` (single-patient outliers), `bio-splice-variant-prediction` (DNA variants), `bio-isoform-switching` (DTU consequences), `bio-sashimi-plots` (figures). Each has a trigger on a different activity or data type; "measuring PSI ... short-read" does not collide with any of them. Related Skills routing stays in the body.
Observation, not a defect: tool names and "intron retention" no longer appear in the description, so a request phrased only as "quantify intron retention with IRFinder" relies on the agent reading IR as splicing quantification. IR is one of the five canonical classes the Skill covers; the trigger still reads as a fit.
Static score moved: **no**. Category scores are unchanged (static 84, agent_specific 18/20); static weighted 84 x 0.4 = 33.6; execution average 86.4 x 0.6 = 51.84 (recorded 51.8); sum 85.44, recorded 85.4, rounds to 85. The margin over the 85 gate is 0.44, identical to the certified record. A one-point static deduction would give 85.04, still at the gate; none was applied because the trigger is precise.""",
"bio-machine-learning-survival-analysis": """**Sufficient, accurate, no finding.** "Use when building an individualized time-to-event risk predictor or prognostic omics signature, choosing a survival model, or evaluating one beyond the C-index."
The clinical-biostatistics survival Skill is not on the shelf (`F:/optimized-scientific-skills/skills` has only `bio-clinical-biostatistics-adaptive-designs`); the removed pointer was to an ID that does not exist there. The prediction-versus-inference separation is carried by "individualized risk predictor ... beyond the C-index", and the body keeps the hand-off table (SKILL.md rows for KM, log-rank and trial hazard ratios -> clinical-biostatistics/survival-analysis). `bio-machine-learning-model-validation` is generic performance estimation and does not collide with a survival-specific trigger.
Observation, not a defect: "competing risks" and "Kaplan-Meier" are no longer named; a competing-risks CIF question still reads as time-to-event model building, and the body covers it.
Static score moved: **no** (88; agent_specific 18/20; execution average 85.6; final 35.2 + 51.4 = 86.6, 87).""",
"bio-machine-learning-atlas-mapping": """**Accurate but not a sufficient discriminator: one P2 finding (AM-009).** "Use when annotating new single-cell datasets against a pre-trained reference atlas, deciding which mapping method fits, or judging whether transferred labels are trustworthy."
Shelf sibling `bio-single-cell-cell-annotation` says "annotating cell types from a reference atlas or pretrained model, transferring labels onto a query, assessing prediction confidence and rejection". The two triggers now read alike. The removed tool list (scArches surgery, Symphony, scPoli, popV, foundation models, out-of-distribution gating) and the removed pointer to cell-annotation were the separators, and the body has no hand-off to cell-annotation (it names markers-annotation, batch-integration, preprocessing, doublet-detection). An agent choosing between them has no signal to prefer the projection-and-OOD-gating Skill, and a query for a scArches or Symphony mapping may be routed to the classifier Skill. `bio-single-cell-batch-integration` (no reference) is separated adequately.
Static score moved: **yes, 88 to 87**. agent_specific 17 to 16 (trigger precision, rubric 8.1: precise to mostly precise, with over-triggering risk). Static weighted 34.8; execution average 85.7 unchanged (34.8? no: 51.4 dynamic); sum 86.2, final 86 (was 87). Still Production Ready.""",
}
for sid, r in res.items():
    q = r["q"]
    chain = "\n- Reverting the SA-006 edit (`fix-textbatch-20261003`) after the description edit reproduces `c60f873f52f63ad78a5009b351f8451510f86bbae3f7d46886c03e3bcf9eaf39`: the chain back to the earlier certified identity is fully reproduced." if q.get("chain_reproduces") else ""
    v = VERD[sid].replace(" (34.8? no: 51.4 dynamic)", "").replace("execution average 85.7 unchanged (34.8? no: 51.4 dynamic)", "execution average 85.7 unchanged, 51.4 weighted")
    recs = "\n".join(f"- {p}: {t}" for p, t in r["recs"]) or "- none"
    ROOT = ROOT_T.replace('{sid}', sid)
    md = f"""# Eval Viewer - {sid}

Generated: 2026-10-03
Audit type: independent delta re-audit (text-only change to certified bytes: frontmatter description trimmed to its "Use when" clause), lane E2, worker E2 (did not normalize, tool, audit or fix this Skill)
Exact candidate content SHA-256: `{r['ident']}` ({r['nfiles']} files, {r['nbytes']} bytes; `skill_preflight --offline` PASS before and after, candidate bytes untouched)
Certified baseline: `{r['certid']}` (final {r['prior_score']}), scores carried forward; only the dimension touched by the change was re-scored.

## Result

**Static {r['sub']}/100; Execution average {r['avg']}/100; Final {r['sw'] + r['dw']:.1f} ({r['score']}); assertion pass rate {r['ap']['passed']}/{r['ap']['total']}; Layer 1 {r['l1']}/40; Layer 2 {r['l2']}/60.**
Grade: Production Ready. Skill veto PASS; Research veto PASS. Decision: **candidate-ready** for exact identity `{r['ident'][:12]}`.

## Delta qualification

- Only `SKILL.md` differs from the certified bytes; all other files are byte-identical. The SKILL.md line diff is exactly one line, the `description:` frontmatter line.
- Reverting `fix-description-20261003/edits.json` on a scratch copy reproduces `{q['after_desc_revert']}` (the certified identity).{chain}
- Frontmatter parsed with PyYAML `safe_load`: valid, `description` is one `str` ({q['new_description_len']} chars), keys {', '.join(q['yaml_keys'])}, `name` equals the directory.
- No script, command, or body statement changed, so the certified execution evidence stands unchanged (SKILL.md body is byte-identical to the certified body).

## Verdict on the trimmed description

{v}

## Open findings

{recs}

All other certified dispositions are unchanged.

## Not executed

Unchanged from the certified record; nothing was rerun. `tools/smoke_irfinder.sh` was not run.

## Evidence

Run root `{ROOT}` (scripts/qualify_delta2.py, scripts/build_delta2.py, logs/qualify.json).
"""
    open(os.path.join(A, sid, RUN, "viewer.md"), "w", encoding="utf-8").write(md)
    os.makedirs(os.path.join(A, sid, RUN, "scripts"), exist_ok=True)
    for s in ("qualify_delta2.py", "build_delta2.py", "viewer_delta2.py"):
        open(os.path.join(A, sid, RUN, "scripts", s), "wb").write(open(os.path.join(A, s), "rb").read())
