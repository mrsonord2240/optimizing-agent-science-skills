import json, io
SK = 'bio-data-visualization-multipanel-figures'
D = r'F:\OpenScience\audits\%s' % SK
A = lambda t, r, n: {"text": t, "result": r, "note": n}
OK, WARN = "\u2705", "\u26a0\ufe0f"
inputs = [
 dict(index=1, type="Canonical", label="Nature-style 2x2 patchwork figure (SKILL.md block as written), 180x140 mm cairo_pdf + 300 dpi PNG, synthetic data",
  status="COMPLETED", status_flag=OK, note="Layout, legend, embedding and pixel size correct; the documented tag styling (bold, size 10) is silently ignored (13.2 pt regular). Tick text 8.8 pt / titles 11 pt vs the Skill's own 5-7 pt threshold.",
  basic=31, specialized=44, total=75, executed=True,
  execution_note="Executed: run/i1_canonical.R (r.sh, ggplot2 4.0.3, patchwork 1.3.2), i1_tagsize.R and i1_tagsize_g35.R (ggplot2 3.5.2), i1_tag_defaulttheme.R; PDF read with poppler pdffonts/pdftotext -bbox in WSL dv-cli; PNG opened.",
  assertions=[
   A("PDF page is 180x140 mm (510x396 pt) and the 300 dpi PNG is 2125x1653 px (180x140 mm)", "PASS", "pdfinfo 510x396 pt; PNG 2125x1653 vs expected 2126x1654"),
   A("Four panels with tags a-d, each tag at the top-left of its own panel (checked with unique panel titles in the PDF text layer)", "PASS", "a/b/c/d sit left of SCATTER/BOX/HIST/COLOR at the correct row and column"),
   A("guides='collect' yields exactly one legend with the right mapping (ctrl/trt from panel d)", "PASS", "one legend at right, group title once, ctrl/trt once"),
   A("Text is vector and fonts are embedded (cairo_pdf)", "PASS", "ArialMT TrueType, emb=yes, 49 words in the text layer"),
   A("plot_annotation(theme = theme(plot.tag = element_text(face='bold', size=10))) styles the tags as documented", "FAIL", "tag height identical for size 6, 10 and 20 (13.2 pt default), no Bold font in the PDF; same on ggplot2 3.5.2, patchwork 1.2.0 and 1.3.2, with or without theme_classic; only '& theme(plot.tag=...)' works"),
  ]),
 dict(index=2, type="Variant A", label="Layout operators: widths ratio, (p1|p2)/p3, design string, inset_element, cowplot plot_grid/rel_*/labels, gridExtra",
  status="COMPLETED", status_flag=OK, note="Every layout claim measured by panel-colour bounding boxes in the PNG matched; cowplot labels AUTO/auto and patchwork 'A'/'i' land on the right panels. gridExtra is named in the description but has no code in the Skill.",
  basic=33, specialized=48, total=81, executed=True,
  execution_note="Executed: run/i2_layout.R (all checks PASS), run/i2_cowplot_blocks.R; gridExtra arrangeGrob run separately to confirm it works (not shown by the Skill).",
  assertions=[
   A("plot_layout(widths=c(2,1)) gives panel widths 2:1", "PASS", "398 px vs 198 px (2.01)"),
   A("Design string AAB/AAB/CCC gives A two columns and two rows, C the full width", "PASS", "A 398x202 px, B 198x202, C 644x100 (A/C height 2.02)"),
   A("inset_element(p2, 0.6, 0.6, 1, 1) places the inset in the upper-right of the parent panel", "PASS", "inset x 476-685, y 74-148 inside parent 49-692 x 41-420"),
   A("cowplot plot_grid labels 'AUTO'/'auto', nested rel_heights=c(1,1.2), rel_widths and patchwork tag_levels 'A'/'i' put the right letters on the right panels; ggsave cairo_pdf embeds Arial regular+bold", "PASS", "A-D, a-c and i-iii read at each panel's top-left in the text layer; bottom row 1.32x top (cell ratio 1.2)"),
   A("The description promises gridExtra composition; the Skill body shows how to use it", "FAIL", "no gridExtra code anywhere in SKILL.md or the examples (only the install line); arrangeGrob(layout_matrix) works when tried"),
  ]),
 dict(index=3, type="Variant B", label="Python GridSpec, subfigures with colorbar, and 89 mm single-column blocks; PDF fonts and saved size",
  status="COMPLETED", status_flag=WARN, note="Layout and label attachment are right, but bbox_inches='tight' makes the saved figures 182.9 mm and 91.9 mm wide, every PDF carries Type 3 fonts (fonttype 42 is never set), and axes-fraction label offsets differ by panel width.",
  basic=27, specialized=38, total=65, executed=True,
  execution_note="Executed: run/i3_python.py (py.sh, matplotlib 3.11.2): 7 PASS, 2 FAIL; PDFs read with pdffonts.",
  assertions=[
   A("GridSpec(2,3): ax2 spans columns 1-2, ax3 spans all columns", "PASS", "ax2.x1 == ax3.x1 and ax3.x0 == ax1.x0"),
   A("Subfigures width_ratios=[2,1]: 2 stacked left axes, image plus colorbar on the right", "PASS", "subfigure width ratio 2.000; right subfigure has 2 axes"),
   A("Panel labels a/b/c are attached to their own axes (transAxes), lowercase, inside the canvas and not over tick labels", "PASS", "no overlap with tick labels or neighbours; but label c sits about 250 px left of its y axis versus 60 px for a (offset scales with axes width)"),
   A("The 180 mm and 89 mm blocks save at the stated width", "FAIL", "180x120 block saved as 182.9x122.9 mm; 89 mm block as 91.9x62.9 mm (bbox_inches='tight'); Nature single column is 89 mm"),
   A("PDFs use embedded TrueType/Type 42 fonts as the description promises", "FAIL", "matplotlib default pdf.fonttype=3: every PDF from the blocks and both examples lists Type 3 fonts; rcParams['pdf.fonttype']=42 gives CID TrueType (verified) but appears only as a comment and a usage-guide bullet"),
  ]),
 dict(index=4, type="Edge", label="Every 'Per-Method Failure Modes' claim reproduced: tag alignment, shared legend, axes='collect', default device, units, cowplot align, old patchwork",
  status="COMPLETED", status_flag=WARN, note="Some claims reproduce; the tag-alignment fix does not align, the cowplot align='v' failure does not occur, the 'silently ignored' claim is wrong (unused-argument error), and axes='collect' in the Skill's nested 2x2 form collects nothing.",
  basic=27, specialized=40, total=67, executed=True,
  execution_note="Executed: run/i4_failmodes.R + i4_analyze.py, i4_collect.R + i4_collect_an.py, i4_collect_pw120.R, i4_oldpw.R (patchwork 1.2.0 and 1.1.3 installed into an audit-private lib), i4_extra.R. patchwork 1.1.3 cannot render at all with ggplot2 3.5.2 (add_guides error), so only its formals were tested.",
  assertions=[
   A("Default ggsave() pdf device gives non-embedded fonts; cairo_pdf embeds them", "PASS", "Helvetica Type 1 emb=no vs ArialMT TrueType emb=yes"),
   A("Different scales with guides='collect' give duplicate legends; identical scales give one", "PASS", "ctrl label count 2 vs 1; a colour panel next to a fill panel with the same palette also stays at 2 legends (not mentioned)"),
   A("The documented fix for tag misalignment (plot.tag.position=c(0.02,0.98)) makes labels sit at the same offset from each panel", "FAIL", "symptom reproduces (14.8 pt offset difference); after the fix 14.5 pt; inside plot_annotation(theme=) it is ignored entirely"),
   A("cowplot plot_grid(p_wide, p_narrow, align='v') misaligns and needs 'hv'", "FAIL", "align='v' aligns stacked panels exactly (0 px left/right difference); only align='none' or 'h' is off"),
   A("plot_layout(axes='collect', axis_titles='collect') on the Skill's (p1+p2)/(p3+p4) collapses repeated axes when scales are shared", "FAIL", "4 x-titles and 4 y-titles remain (no-op) on patchwork 1.2.0 and 1.3.2; works on flat wrap_plots(ncol=2) (1 and 1) or when set at every nesting level (2 and 2)"),
  ]),
 dict(index=5, type="Stress", label="Both shipped examples end to end (R under ggplot2 4.0.3 and 3.5.2; Python) measured against the Skill's journal/font/legend advice",
  status="COMPLETED", status_flag=WARN, note="Both examples run and label A-D correctly, but neither follows the Skill: 254x203 mm and 215x201 mm outputs, unembedded Helvetica (R) and Type 3 (Python), and the R figure has four un-merged legends clipped at the page edges.",
  basic=26, specialized=36, total=62, executed=True,
  execution_note="Executed from copies in run/scratch_r, scratch_r35, scratch_py: multi_panel_figure.R wrote Figure1.pdf/png in both ggplot2 versions; multipanel_matplotlib.py wrote 4 files. PNGs opened.",
  assertions=[
   A("Both examples run from a clean copy and write non-blank PDF and PNG", "PASS", "R 3000x2400 px PNG 334 KB; Python 2534x2373 and 3007x2149 px; PNGs opened"),
   A("Panel labels A-D sit on the intended panels in both examples", "PASS", "A/B/C/D at the top-left of Differential Expression/PCA/Top DE Genes/DE Summary; Python A-D likewise"),
   A("The R example's guides='collect' produces one shared legend and stays inside the page", "FAIL", "four legends (significant, Group colour, Group fill, category) because legend.position='bottom' is re-applied to all and colour/fill do not merge; the row is clipped at both page edges"),
   A("Output size follows the Skill's journal spec (mm, <= 183 mm wide)", "FAIL", "R example 254x203 mm (10x8 in, units='in'); Python 214x201 mm and 255x182 mm"),
   A("PDF fonts are embedded as the Skill's own advice requires", "FAIL", "R: default pdf() device, Helvetica/Helvetica-Bold/Symbol Type 1 emb=no; Python: DejaVu Type 3 (its header comment mentions pdf.fonttype=42 but never sets it)"),
  ]),
]
for i in inputs:
    i['assertions_passed'] = sum(1 for a in i['assertions'] if a['result'] == 'PASS')
    i['assertions_total'] = len(i['assertions'])
    assert i['basic'] + i['specialized'] == i['total'] and 3 <= len(i['assertions']) <= 5
avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
cats = {
 "functional_suitability": (8, 12, "Completeness 3, correctness 2, appropriateness 3. Layout operators are right, but the headline recipe's tag styling and axes='collect' do not do what is stated, the Python blocks never deliver Type-42 fonts or mm-exact size, and gridExtra and shared Python legends are promised and absent."),
 "reliability": (7, 12, "Several documented behaviours fail silently (tag theme ignored, axes='collect' no-op on nested composition, bbox_inches='tight' resizes the figure); the failure-mode fixes for tag alignment and cowplot align were not reproduced."),
 "performance_context": (6, 8, "About 270 lines plus a 60-line guide; concise, with some duplicated size and label text between SKILL.md and usage-guide.md."),
 "agent_usability": (11, 16, "Goal/Approach blocks and version stamps help; inconsistent numbers (label 8 pt vs 9/10/12 pt in code, 180 mm vs Nature 183 / Cell 174, body text 5-7 pt vs default 8.8-11 pt) and code blocks that use undefined df/x/y."),
 "human_usability": (7, 8, "Natural example prompts and a clear operator cheat sheet; little help when a step silently does nothing."),
 "security": (10, 12, "No credentials, network or eval; examples write into the working directory and overwrite silently."),
 "maintainability": (9, 12, "Version-stamped and modular; the examples do not exemplify the Skill's own rules, and there is no old-patchwork/ggplot2-4 compatibility note (patchwork 1.2.0 errors 'object is not a unit' on ggplot2 4.0.3)."),
 "agent_specific": (15, 20, "Precise trigger, all four Related Skills exist; no references/ layer, few stop conditions, re-runs are safe."),
}
sub = sum(v[0] for v in cats.values()); assert sub == 73
sw = round(sub * 0.4, 1); dw = round(avg * 0.6, 1); score = round(sw + dw)
print('static', sub, 'exec', avg, 'final', sw + dw, score)
rec = [
 ("P1", "plot_annotation(theme=plot.tag) is silently ignored", [1, 4], "The headline patchwork recipe sets bold size-10 tags through plot_annotation(theme=...); the PDF shows 13.2 pt regular tags for size 6, 10 and 20, on patchwork 1.2.0/1.3.2 and ggplot2 3.5.2/4.0.3.", "Tags take the theme of each sub-plot, not the annotation theme.", "Show '& theme(plot.tag = element_text(face=\"bold\", size=8))' (verified to work) and state the journal label size (8 pt) once; make every snippet match."),
 ("P1", "axes='collect' does nothing in the Skill's nested 2x2 form", [1, 4], "(p1+p2)/(p3+p4) + plot_layout(axes='collect', axis_titles='collect') leaves 4 x and 4 y titles even when all scales are identical (patchwork 1.2.0 and 1.3.2); the demo panels do not share scales anyway.", "plot_layout at the top level only reaches the two nested rows.", "Use wrap_plots(list, ncol=2) + plot_layout(axes='collect', axis_titles='collect') (verified: one x and one y title), or set plot_layout at every nesting level, and say collection needs identical scales."),
 ("P1", "Python blocks break the mm size and never set Type-42", [3, 5], "bbox_inches='tight' turns the 180 mm and 89 mm figures into 182.9 and 91.9 mm; pdf.fonttype is never set so every PDF has Type 3 fonts, although the description advertises Type-42 embedding.", "Snippets copied from a generic export recipe; the rcParams line lives only in a comment and a usage-guide bullet.", "Add rcParams['pdf.fonttype']=42 to the block, drop bbox_inches='tight' (or keep labels inside the axes) and assert the saved size in mm."),
 ("P1", "Shipped examples violate the Skill's own rules", [5], "multi_panel_figure.R saves 10x8 in with the default pdf device (unembedded Helvetica) and produces four un-merged, clipped legends; multipanel_matplotlib.py is 12x8 in with Type 3 fonts and hspace/wspace instead of constrained layout.", "Examples predate the journal-spec guidance.", "Rewrite both examples to 183 mm, units='mm', cairo_pdf / fonttype 42, a single merged legend (same aesthetic and palette across panels), and print the measured size."),
 ("P1", "Several failure-mode explanations are wrong or ineffective", [4], "Tag fix plot.tag.position=c(0.02,0.98) does not equalise offsets (14.5 pt vs 14.8 pt); cowplot align='v' does not fail as described; patchwork 1.1.3 raises 'unused argument' instead of silently ignoring axes=; ggsave with default units errors ('Dimensions exceed 50 inches') instead of writing a 180 in file; 'constrained_layout is default-on in 3.6+' is false (default layout engine is None).", "Claims were written from memory and not run.", "Re-test and correct each claim; for tag alignment use a tag position relative to the panel (plot.tag.location='panel') or a constant y-label width."),
 ("P2", "Inconsistent label/text sizes and column widths", [1, 3, 5], "Panel labels are 8 pt in the table, 9/10 pt in R snippets and 10/12/14 in Python; default text is 8.8-11 pt against the stated 5-7 pt; code uses 180 mm, not 183 (Nature) or 174 (Cell); Nature labels are called 'serif' while the code is sans.", "Numbers and code maintained separately.", "One size table (label, body, line) referenced by all snippets, use the per-journal widths from the sizing table, and drop 'serif'."),
 ("P2", "Promised coverage missing", [2, 3], "gridExtra, matplotlib shared legends/sharex/sharey and subplot_mosaic are named or implied but have no code; Python panel-label offsets in axes fraction differ with axes width.", "Description wider than the body.", "Add a short gridExtra/arrangeGrob block and a fig.legend/subplot_mosaic block, or narrow the description; use a fixed-point offset for labels."),
 ("P2", "Version notes incomplete", [4], "patchwork 1.2.0 (CRAN 2024-01-08, not 01-05) errors 'object is not a unit' under ggplot2 4.0.3, and 1.1.3 fails inside add_guides on ggplot2 3.5.2; dropping a legend with legend.position='none' is only safe when the mapping is identical.", "Compatibility matrix not checked.", "State patchwork >= 1.3 for ggplot2 4.x, correct the release date, and warn that dropping N-1 legends misleads when palettes differ."),
]
recs = [dict(priority=p, title=t, observed_in=o, problem=pr, root_cause=rc, fix=f) for p, t, o, pr, rc, f in rec]
for r in recs: assert len(r['title']) <= 60, r['title']
keys = ("index", "type", "label", "status", "status_flag", "note", "basic", "specialized", "total", "assertions_passed", "assertions_total", "assertions", "executed", "execution_note")
out = {
 "meta": {"skill_name": SK,
  "description": "Compose multi-panel publication figures with patchwork, cowplot, gridExtra (R), or matplotlib GridSpec/subfigures (Python) including shared axes/legends/guides collection, panel labels in Nature/Cell convention, and journal-spec sizing.",
  "evaluated_on": "2026-09-20", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "A", "complexity": "Moderate", "n_inputs": 5,
  "source": "mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/multipanel-figures",
  "audit_type": "first audit (unmodified upstream GPTomics/bioSkills)",
  "executed": True,
  "execution_note": "Executed 5/5 inputs. R 4.4.3 via r.sh (ggplot2 4.0.3, patchwork 1.3.2, cowplot 1.2.0, gridExtra 2.3) and r-gg35.sh (ggplot2 3.5.2); patchwork 1.2.0 and 1.1.3 installed into an audit-private library from the CRAN archive; Python via py.sh (matplotlib 3.11.2); PDF fonts, page size and text positions read with poppler (WSL dv-cli); panel geometry measured from panel-colour bounding boxes in PNGs; PNGs opened with Read. Data are synthetic (seeded). Shipped examples ran from copies."},
 "veto_gates": {
  "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
  "research_veto": {"applicable": True, "gate": "PASS",
   "scientific_integrity": {"result": "PASS", "detail": "No fabricated DOI, statistic or result; the only inaccurate statement of fact is a package release date (patchwork 1.2.0 CRAN 2024-01-08 vs stated 2024-01-05), recorded as P2."},
   "practice_boundaries": {"result": "PASS", "detail": "Figure-composition Skill; no diagnostic or prescriptive content."},
   "methodological_ground": {"result": "PASS", "detail": "No principled methodological fallacy in figure composition; several documented behaviours are wrong (recorded as P1) but none invalidates a scientific conclusion."},
   "code_usability": {"result": "PASS", "detail": "Every R block, Python block and both shipped examples parse and ran (R on ggplot2 4.0.3 and 3.5.2, Python on matplotlib 3.11.2); blocks that use undefined df/x/y ran once data were supplied. Output-spec defects are scored, not vetoed."}}},
 "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
 "dynamic_score": {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": sum(i['assertions_passed'] for i in inputs), "total": sum(i['assertions_total'] for i in inputs)},
  "inputs": [{k: i[k] for k in keys} for i in inputs]},
 "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": "Beta Only", "grade_symbol": WARN, "deployable": False, "veto_override": False},
 "key_strengths": [
  "Layout operators are exact: widths ratio, design string, inset_element and cowplot rel_widths/rel_heights all measured within 1-2 px of the stated ratios",
  "cairo_pdf embeds TrueType fonts with vector text, and guides='collect' yields one correct legend when scales are identical",
  "Nature single/double column widths (89/183 mm) and the units='mm' and default-device warnings are accurate and useful",
  "All shipped files exist, all code runs, and every referenced Related Skill is present"],
 "recommendations": recs}
json.dump(out, io.open(D + r'\eval_report_%s_result.json' % SK, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

detail = {
1: 'SKILL.md block run as written (titles SCATTER/BOX/HIST/COLOR added so panels can be identified in the PDF text layer), `ggsave(..., width=180, height=140, units="mm", device=cairo_pdf)`. Measured: PDF 510x396 pt = 179.9x139.7 mm; PNG 2125x1653 px; one legend; ArialMT TrueType embedded, 49 words of vector text. Text sizes: ticks 8.8 pt, axis titles 11 pt, tags 13.2 pt regular; tag size 6/10/20 give identical output (i1_tagsize*.R), `& theme(plot.tag=element_text(face="bold",size=6))` gives 6.7 pt bold. Same on ggplot2 3.5.2 and patchwork 1.2.0. PNG opened: four panels, tags a-d, one legend at right, not blank.',
2: 'Panels coloured A-D, PNG bounding boxes: widths c(2,1) 398:198 px; (A|B)/C: C spans 644 px, A/B 298; design AAB/AAB/CCC: A 398x202, B 198x202, C 644x100; inset at x 476-685, y 74-148 within the parent; cowplot rel_widths c(1,2) 187:423; nested rel_heights c(1,1.2) 179:136 (1.32 panel ratio because the axis area is fixed). cowplot AUTO/auto and patchwork tag_levels A and i verified in the text layer; gridExtra arrangeGrob(layout_matrix) works but the Skill contains no gridExtra code.',
3: 'GridSpec block and subfigures block run as written (data supplied). Layout correct (ax2 spans cols 1-2, ax3 all; subfigure ratio 2.000; colorbar present). Saved: 180x120 mm block -> 182.9x122.9 mm, 89 mm block -> 91.9x62.9 mm because of `bbox_inches="tight"`; PDFs list DejaVu Type 3 fonts; with pdf.fonttype=42 CID TrueType (verified) but that is never set. Default `figure.constrained_layout.use` is False and the default layout engine is None (the "default-on in 3.6+" statement is wrong). PNGs opened: label c sits far left of the wide bar axes.',
4: 'Results (i4_analyze.log, i4_collect.log): default pdf device Helvetica unembedded (claim true); tag offsets differ 14.8 pt between panels with different y-label widths (symptom true) and 14.5 pt after the documented fix (fix ineffective; ignored inside the plot_annotation theme); different palettes give 2 legends, same palette 1, colour vs fill 2; dropping the second legend leaves a legend that is wrong for panel 2; cowplot align="v" aligns exactly (claim false); `axes="collect"` on the nested 2x2: 4 x and 4 y titles remain (patchwork 1.2.0 and 1.3.2), flat wrap_plots: 1 and 1, collect at every level: 2 and 2; patchwork 1.1.3 `plot_layout(axes=)` raises "unused argument" (not silent); ggsave default units errors "Dimensions exceed 50 inches"; patchwork 1.2.0 on ggplot2 4.0.3 errors "object is not a unit".',
5: 'R example: Figure1.pdf/png written in both ggplot2 versions; 720x576 pt (254x203 mm), Helvetica/Helvetica-Bold/Symbol Type 1 not embedded; PNG opened: tags A-D correct, but the bottom legend row holds four legends and is clipped left ("significant") and right ("Upregulated"). Python example: multipanel_2x2 214.5x200.9 mm, multipanel_complex 254.6x181.9 mm, Type 3 fonts, correct A-D labels; the suptitle leaves a large blank band.'}
L = []
L.append('# Eval Viewer - %s\n\nGenerated: 2026-09-20 | source: mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/multipanel-figures | Category: Data Analysis | Mode A | Moderate, N=5\n' % SK)
L.append('Environment: R 4.4.3 (`r.sh`: ggplot2 4.0.3, patchwork 1.3.2, cowplot 1.2.0, gridExtra 2.3; `r-gg35.sh`: ggplot2 3.5.2), audit-private patchwork 1.2.0 and 1.1.3, Python 3.12 (`py.sh`: matplotlib 3.11.2), poppler in WSL `dv-cli` for PDF fonts, page size and text positions. Data are synthetic and seeded (`data/`). All scripts are in `run/`; figures in `out/`.\n')
L.append('## Skill Veto\nT1-T4 PASS (no eval/exec, no network, deterministic with seeds; frontmatter complete; all shipped files present: SKILL.md, usage-guide.md, 2 examples; all four Related Skills exist in the staging repo).\n')
L.append('## Summary Table\n\n| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |\n|---|---|---|---|---|---|---|')
for i in inputs:
    L.append('| %d | %s | %d | %d | %d | %d/%d PASS | %s |' % (i['index'], i['type'], i['basic'], i['specialized'], i['total'], i['assertions_passed'], i['assertions_total'], i['status_flag']))
ar = out['dynamic_score']['assertion_pass_rate']
L.append('\n**Static: %d / 100 | Execution average: %s / 100 | Final: %.1f -> %d, Beta Only (not deployable) | Assertion pass rate: %d/%d | Research Veto: PASS | open P0: none**\n' % (sub, avg, sw + dw, score, ar['passed'], ar['total']))
L.append('Floors: static 73 (>= 70 ok), execution average %s (< 75), assertions 60%% (< 80%%), so Limited Release is not reached; the grade follows the score (71).\n' % avg)
L.append('## Detailed Outputs\n')
for i in inputs:
    L.append('### Input %d - %s: %s\n\n**Executed:** %s\n\n%s\n\n**Scores:** Basic %d/40 | Specialized %d/60 | Total %d/100\n\n**Assertions:**' % (i['index'], i['type'], i['label'], i['execution_note'], detail[i['index']], i['basic'], i['specialized'], i['total']))
    for a in i['assertions']: L.append('- [%s] %s - %s' % (a['result'], a['text'], a['note']))
    L.append('')
L.append('## Recommendations\n')
for r in recs: L.append('- **[%s] %s** (inputs %s): %s Fix: %s' % (r['priority'], r['title'], r['observed_in'], r['problem'], r['fix']))
io.open(D + r'\eval_viewer_%s.md' % SK, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
