"""Builds eval_report_bio-data-visualization-color-palettes_result.json from the audit results (numbers come from run/*.out)."""
import json, pathlib
A = pathlib.Path(r"F:\OpenScience\audits\bio-data-visualization-color-palettes")
SKILL = "bio-data-visualization-color-palettes"
SRC = "mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/color-palettes"

def a(text, ok, note): return {"text": text, "result": "PASS" if ok else "FAIL", "note": note}

inputs = [
 dict(index=1, type="Canonical", label="CVD-safe categorical palette for 7 cell types on a UMAP, grey reserved for unassigned (Okabe-Ito)",
  status="COMPLETED", status_flag="\u26a0\ufe0f",
  note="The 8 Okabe-Ito hexes are right and the 7-colour set is deutan-safe (min dE 14.8). But the Skill's unnamed scale_color_manual(values=okabe_ito) gives black, not grey, to the 8th (Unassigned) level, and when one level is dropped all 7 remaining cell types change colour with no warning. Okabe-Ito + #999999 grey then collides under simulated deuteranopia (Erythroid vs grey dE 6.5, NK vs grey 9.8). The Skill's mandatory check cvd_emulator(palette, type='deutan') errors: cvd_emulator takes an image file.",
  basic=30, specialized=41, total=71,
  assertions=[
   a("The Skill's 8 Okabe-Ito hexes equal palette.colors(8,'Okabe-Ito') as a set", True, "setequal TRUE; order differs (palette.colors starts with black), so unnamed vectors are not interchangeable"),
   a("The 7-colour Okabe-Ito set stays distinguishable under simulated deuteranopia (min pairwise dE >= 10)", True, "CAM02-UCS min dE 14.8 deutan, 14.0 protan; Dark2 3.7 and Set1 4.7 for contrast"),
   a("The Skill's shown scale_color_manual(values = okabe_ito) keeps each cell type's colour when a level is removed", False, "7 of 7 remaining types changed colour after dropping T cells (ggplot_build); a named vector was stable"),
   a("The Skill's CVD pre-flight cvd_emulator(palette, type='deutan') runs as written", False, "unused argument (type = 'deutan'); formals are file, overwrite, shiny.trace"),
   a("Okabe-Ito 7 plus grey #999999 for Unassigned remains separable under deutan simulation (min dE >= 10)", False, "Erythroid (#CC79A7 -> #9498A5) vs grey dE 6.5; NK cell vs grey 9.8"),
  ]),
 dict(index=2, type="Variant A", label="Diverging log-fold-change heatmap, Crameri vik, symmetric bounds, zero must map to pure white",
  status="COMPLETED", status_flag="\u26a0\ufe0f",
  note="scale_fill_scico(palette='vik', midpoint=0) and the q99 symmetric-limits example both put an exact zero at the palette centre, and the range-based default reproduces the Skill's failure mode (zero drawn blue, #3B85AC). But the usage-guide prompt 'zero must map to pure white' cannot be met with vik: its centre is #EBE5E0 (L* 91.3), darker and warmer than the #EEEEEE the Skill bans as a light-grey midpoint. Recommended RdBu centre is #F7F7F7, roma centre is pale green #C0EAC3.",
  basic=32, specialized=48, total=80,
  assertions=[
   a("scale_fill_scico(palette='vik', midpoint=0) fills an exact-zero cell with the vik centre colour", True, "fill #EBE5E0 = scico(255,'vik')[128]"),
   a("The example's symmetric limits (+-q99, oob=squish) keep zero at the centre and clip few cells", True, "vmax 4.81; 5 of 480 cells squished; zero fill #EBE5E0"),
   a("The prompt requirement 'zero must map to pure white' is met when the Skill's headline diverging palette (vik) is used", False, "zero fill #EBE5E0, CIELab dE76 9.4 from white"),
   a("The Skill's own rule 'light grey midpoint (#EEEEEE) is a failure mode' is consistent with the palettes it recommends (vik, RdBu)", False, "vik centre L* 91.3 vs #EEEEEE L* 94.1; RdBu centre #F7F7F7"),
   a("The Skill's custom ramp #0072B2 / white / #D55E00 gives exactly #FFFFFF at zero with similar-luminance ends", True, "fill #FFFFFF; end L* 46.0 and 54.2"),
  ]),
 dict(index=3, type="Edge", label="Audit candidate palettes for grayscale monotonicity and CVD safety using the Skill's own check blocks",
  status="COMPLETED", status_flag="\u26a0\ufe0f",
  note="Verified twice (R colorspace and Python colorspacious): viridis, cividis, magma, batlow, lipari have strictly monotonic L*; rainbow and jet do not. Turbo, which the Skill offers as the rainbow replacement and calls perceptually uniform, also fails (L* 12 -> 90 -> 24; step CV 0.36 vs viridis 0.012). The grayscale block draws grey(seq(0,1,10)) as the 'equivalent' of viridis(10), which is off by up to 14.9 L*; desaturate() (used in the shipped example) is exact (0.2). The Python CVD block imports cspace_converter and simulates nothing.",
  basic=28, specialized=39, total=67,
  assertions=[
   a("viridis, cividis and batlow have monotonic CIELab L* along the ramp", True, "R 10-step and Python 256-step agree; cividis moves 0.7 dE under deutan vs viridis 15.4"),
   a("rainbow/jet fail the Skill's luminance-monotonicity test", True, "monotonic step fraction 0.51 and 0.57; desaturate(rainbow(10)) L* 53 72 94 88 88 91 48 34 52 56"),
   a("turbo, the Skill's suggested rainbow replacement 'perceptually uniform', passes the Skill's own luminance test", False, "L* non-monotonic in both runtimes; step CV 0.359"),
   a("The CVD emulator call in the 'Mandatory Check' block runs as written", False, "error for deutan, protan and tritan; deutan()/protan()/tritan() work"),
   a("grey(seq(0,1,length=10)) is the grayscale equivalent of viridis(10)", False, "max |L* diff| 14.9 vs 0.2 for desaturate(viridis(10))"),
  ]),
 dict(index=4, type="Variant B", label="Migrate a matplotlib spatial-expression figure from jet, plus signed and cyclic (phase) data, in Python",
  status="COMPLETED", status_flag="\u26a0\ufe0f",
  note="cmcrameri exposes all seven Skill names; symmetric vmin=-vmax puts zero at 0.500 of the range while vmin/vmax=min/max puts it at 0.155 (dark blue), the failure mode as described. Cyclic maps close the seam (romaO 0.6, vikO 0.6, twilight 0.2 dE) and viridis does not (92). Wrong: the 'colorblind' matplotlib style does not exist (OSError; the real name seaborn-v0_8-colorblind holds only 6 of the 8 Okabe-Ito colours), turbo is offered as the jet replacement, and the RdBu_r block hard-codes +-2 so 8.4% of an unscaled signed field saturates silently. A pixel-level rank-correlation test did not separate jet (0.996) from viridis (1.000) on this smooth field, so that metric is not used as evidence.",
  basic=31, specialized=46, total=77,
  assertions=[
   a("All seven Crameri names in the Skill exist in cmcrameri.cm and the Python blocks run", True, "batlow lipari vik roma bam romaO vikO all present; blocks ran under matplotlib 3.11.2"),
   a("Symmetric bounds map zero to the diverging centre; data min/max bounds do not", True, "0.500 vs 0.155 (colour #044F88)"),
   a("Cyclic maps romaO, vikO and twilight have no visible seam, unlike a linear map", True, "seam dE 0.6 / 0.6 / 0.2 vs viridis 92.1; figure opened"),
   a("Migrating jet to turbo yields a luminance-monotonic, perceptually uniform map", False, "turbo L* non-monotonic (frac 0.506), step CV 0.359"),
   a("plt.style.use('colorblind') as described works", False, "OSError: not a valid style; seaborn-v0_8-colorblind exists with 6 colours"),
  ]),
 dict(index=5, type="Stress", label="Run both shipped examples and pick colours for 15 groups plus journal palettes",
  status="COMPLETED", status_flag="\u26a0\ufe0f",
  note="palette_examples.R runs (34.7 KB PDF) but contradicts the Skill: it demonstrates Set1 and NPG-style hexes (not CVD-safe, Set1 deutan min dE 4.7), a custom diverging with #4DBBD5 (L* 70.8) vs #E64B35 (L* 54.1), white points vanish on the white theme_minimal background, and it ends with Python palette names (coolwarm, tab10). palettes_phd.R fails as shipped (df is undefined, resolves to stats::df); with df and de_df supplied all 24 expressions ran and 15 pages were non-blank. 'Journal palettes are CVD-imperfect' is confirmed (aaas 5.9, lancet 7.4, npg 7.8 dE under deutan vs 14.8 for Okabe-Ito). The 9-20 group advice (tab20, Paired, Polychrome) is not CVD-safe (deutan min dE 2.0-4.5, 6-16 pairs below 10).",
  basic=28, specialized=39, total=67,
  assertions=[
   a("examples/palette_examples.R runs and writes a non-empty PDF", True, "34,737 B; PNG rendering opened: 4 panels drawn"),
   a("examples/palettes_phd.R runs as shipped", False, "ggplot2: data cannot be a function (df undefined); 24/24 expressions ran once df/de_df were supplied"),
   a("The Skill's claim that ggsci journal palettes are CVD-imperfect holds", True, "deutan min dE: aaas 5.9, lancet 7.4, npg 7.8, nejm 10.5 vs Okabe-Ito 14.8"),
   a("The shipped palette_examples.R follows the Skill's own advice (CVD-safe categorical, visible white midpoint)", False, "Set1 and NPG-style colours; near-zero points are white on a white panel"),
   a("The 9-20 group recommendation (tab20, Paired, Polychrome) stays distinguishable under deutan simulation", False, "min dE 2.0 to 4.5; tab20 n=20 has 16 pairs below 10"),
  ]),
]
for i in inputs:
    i["assertions_passed"] = sum(x["result"] == "PASS" for x in i["assertions"])
    i["assertions_total"] = len(i["assertions"])
    assert i["basic"] + i["specialized"] == i["total"]
    i["executed"] = True
ex = {
 1: "Executed: run/i1_categorical.R (ggplot_build assertions on a 1,270-cell SYNTHETIC UMAP), run/i1b_grey_conflict.py; two PNGs opened.",
 2: "Executed: run/i2_diverging.R on a 480-cell SYNTHETIC skewed LFC matrix; ggplot_build fills asserted; PNG opened; rerun output identical.",
 3: "Executed: run/i3_cvd_gray.R (R colorspace), run/i1_metrics.py (Python colorspacious, 19 colormaps), run/i3_python_snippet.py; show_col and demoplot PNGs opened.",
 4: "Executed: run/i4_python_migration.py on a SYNTHETIC 120x160 field; three PNGs opened.",
 5: "Executed: shipped palette_examples.R verbatim and palettes_phd.R verbatim (fails) and via run/i5c_phd_harness.R with SYNTHETIC df/de_df; run/i5f_many_groups.py; palette_examples PNG and one harness page opened, 15 pages pixel-checked.",
}
for i in inputs: i["execution_note"] = ex[i["index"]]

cats = {
 "functional_suitability": (8, 12, "Completeness 3, correctness 2, appropriateness 3. Covers sequential, diverging, cyclic, categorical, brand palettes and CVD/grayscale checks, but no path for a grey 'unassigned' class, no stable group-to-colour pattern, and the 9-20 group advice is not CVD-safe. Correctness: turbo called uniform, cvd_emulator misused, grey ramp called the grayscale equivalent, 'colorblind' style does not exist, bam described as brown (it is magenta to green), viridis default since 2.0 not 3.0."),
 "reliability": (7, 12, "Fault tolerance 2, error reporting 2, recoverability 3. The Version Compatibility note tells the agent to introspect on ImportError, but the Skill's central pre-flight (cvd_emulator) errors and the Python CVD block does nothing; the Common Errors table lists design errors, not runtime ones. Read-only and re-runnable."),
 "performance_context": (5, 8, "Token cost 2, efficiency 3. About 300 lines in one SKILL.md with a usage-guide.md that restates the same tips (Okabe-Ito hexes, symmetric bounds, white midpoint, grayscale test, rainbow, journal palettes) almost verbatim."),
 "agent_usability": (10, 16, "Learnability 3, consistency 2, feedback design 2, error prevention 3. Failure-mode blocks (trigger, mechanism, symptom, fix) are good. Consistency suffers: pure-white midpoint rule vs recommended vik/RdBu/roma centres, grayscale test described as the CVD check, examples use Set1/NPG against the advice. No output contract for what a palette recommendation or CVD audit should report."),
 "human_usability": (7, 8, "Discoverability 4, forgiveness 3. Natural example prompts (heatmap, LFC, cell types, jet migration, CVD audit) match how researchers ask."),
 "security": (11, 12, "Credentials 4, input validation 3, data safety 4. No network, eval or shell; examples write palette_examples.pdf to the cwd."),
 "maintainability": (7, 12, "Modularity 3, modifiability 2, testability 2. Single SKILL.md plus duplicated guide; palettes_phd.R references undefined df/de_df so it cannot be run or tested as shipped; no palette-check script although the checks are a dozen lines."),
 "agent_specific": (16, 20, "Trigger precision 4, progressive disclosure 2, composability 3, idempotency 4, escape hatches 3. Precise description; four Related Skills all exist in staging; no references/ layering; '>20 groups: reconsider design' is a real stop condition."),
}
static = {"subtotal": sum(v[0] for v in cats.values()), "max": 100,
          "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}}
assert static["subtotal"] == 71
avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
passed = sum(i["assertions_passed"] for i in inputs); total = sum(i["assertions_total"] for i in inputs)
sw = round(71 * 0.4, 1); dw = round(avg * 0.6, 1); score = round(71 * 0.4 + avg * 0.6, 1)
print(avg, passed, total, sw, dw, score)

recs = [
 dict(priority="P1", title="Turbo offered as a perceptually uniform rainbow fix, but fails the Skill's own luminance test",
  observed_in=[3, 4],
  problem="SKILL.md (viridis list, Rainbow failure mode) and usage-guide (Tips, jet migration prompt) say turbo is 'jet-like but perceptually uniform' and offer it as the fix for rainbow banding. CIELab L* along turbo runs 12 to 90 to 24 (non-monotonic in R colorspace and Python colorspacious) and step CV is 0.359 against 0.012 for viridis.",
  root_cause="Turbo is a smoothed rainbow: better than jet but not uniform and not luminance-monotonic, so it fails criterion 3 that the Skill calls the most actionable.",
  fix="Say turbo is a last resort for audiences who need a jet-like look, that it fails the grayscale test, and make viridis/batlow the default jet replacement in every place turbo appears."),
 dict(priority="P1", title="The mandatory CVD pre-flight does not run: cvd_emulator takes an image file",
  observed_in=[1, 3],
  problem="cvd_emulator(palette, type='deutan'|'protan'|'tritan') raises 'unused argument (type = ...)' (formals: file, overwrite, shiny.trace). The paired Python block imports cspace_converter and simulates nothing. The shipped example already uses the working deutan()/protan()/tritan().",
  root_cause="Function signature guessed from the name; the Python block stops at the import.",
  fix="Replace with demoplot(deutan(palette), 'heatmap') / deutan(palette) in R, and cspace_convert(rgb, {'name':'sRGB1+CVD','cvd_type':'deuteranomaly','severity':100}, 'sRGB1') in Python; add one line reporting the minimum pairwise distance under each simulation."),
 dict(priority="P1", title="Pure-white midpoint rule contradicts the diverging palettes the Skill recommends",
  observed_in=[2, 4],
  problem="The Skill and usage-guide require white at the diverging midpoint and call #EEEEEE a failure mode, and the guide prompt asks vik with 'zero must map to pure white'. The recommended centres are vik #ECE5E0 (L* 91.3), roma #C0EAC3 (pale green), bam #F6F1F0, RdBu #F7F7F7 (also RdBu_r in matplotlib), all darker or tinted relative to white. The rule only holds for hand-built ramps (#0072B2/white/#D55E00 gives #FFFFFF).",
  root_cause="A rule for custom ramps was stated as a universal one, and the palette table never lists the true centre colours.",
  fix="Add the measured centre colour to the Crameri and ColorBrewer tables, restrict the pure-white rule to custom ramps, and say that vik/roma/RdBu centres are near-neutral by design and zero is still anchored by midpoint=0 or symmetric limits."),
 dict(priority="P1", title="Unnamed Okabe-Ito vector silently recolours groups and has no grey for 'unassigned'",
  observed_in=[1],
  problem="scale_color_manual(values = okabe_ito) with an unnamed 8-vector maps by level order: dropping one level changed the colour of all 7 remaining cell types, and the 8th level gets black. The usage-guide prompt 'reserve grey for ambient/unassigned' has no code path, and Okabe-Ito 7 plus #999999 falls to dE 6.5 (Erythroid) and 9.8 (NK) under deutan simulation.",
  root_cause="Only the custom-palette example uses a named vector; the Okabe-Ito block does not, and the grey rule is never shown.",
  fix="Show setNames(okabe_ito[1:7], levels) with a separate grey for the reserve class, state that named vectors keep colours stable across panels and subsets, and warn that #CC79A7 and #009E73 approach mid-grey under deutan (choose #BBBBBB/light grey or a marker shape)."),
 dict(priority="P1", title="Grayscale test replaces the image with a generic grey ramp and is billed as the CVD check",
  observed_in=[3],
  problem="show_col(grey(seq(0,1,length=10))) is presented as the 'equivalent grayscale gradient' of viridis(10); it differs by up to 14.9 L* (0-100 ramp vs viridis 15-91). desaturate() differs by 0.2. The usage-guide tip calls the grayscale test 'the most actionable CVD check', but grayscale monotonicity is not colour-vision simulation.",
  root_cause="Two different tests conflated; the exact one (desaturate) is only in the example.",
  fix="Use desaturate(pal) in SKILL.md, add an L* monotonicity one-liner (coords(as(hex2RGB(pal),'LAB'))[, 'L']), and separate the grayscale check from the CVD check."),
 dict(priority="P1", title="Shipped examples contradict the Skill and one does not run",
  observed_in=[5],
  problem="palette_examples.R demonstrates Set1 and an NPG-style vector as the 'qualitative' example, a custom diverging with unmatched luminance ends (L* 70.8 vs 54.1) whose near-zero points are white on white, and ends with Python names (coolwarm, tab10). palettes_phd.R defines no df or de_df, so ggplot fails with 'data cannot be a function'.",
  root_cause="Two examples written independently of the SKILL.md guidance; the second is a template.",
  fix="Rewrite palette_examples.R with Okabe-Ito (named), scico batlow/vik and a visible midpoint (grey panel or outlined points); add a small simulated df/de_df to palettes_phd.R so it runs, and drop non-R names from the closing cat()."),
 dict(priority="P2", title="9-20 group palettes are recommended without a CVD caveat",
  observed_in=[5],
  problem="tab20 (n=20), Paired (12), Set3 (12) and Polychrome 36 (first 15/20) drop to deutan min dE 2.0-4.5 with 6-16 pairs below 10, against 14.8 for Okabe-Ito.",
  root_cause="The palette-by-count table optimises normal-vision separation only.",
  fix="Add that beyond 8 groups no listed palette is CVD-safe and pair colour with marker shape, direct labels or facets."),
 dict(priority="P2", title="Smaller factual errors in the palette descriptions",
  observed_in=[3, 4],
  problem="'colorblind' matplotlib style does not exist (seaborn-v0_8-colorblind, 6 colours); viridis became the matplotlib default in 2.0 (classic.mplstyle still sets jet), not 3.0; bam runs magenta to white to green, not brown; roma is red/pale-green/blue, not 'slightly warmer than vik'; RdBu is called perceptually uniform in the usage-guide (step CV 0.22 vs vik 0.18); colorRampPalette(...)(100) of the custom ramp has no exact #FFFFFF entry (odd N does); the matplotlib RdBu_r block hard-codes +-2 and saturated 8.4% of an unscaled field.",
  root_cause="Palette facts written from memory and not checked against the installed packages.",
  fix="Correct each statement; for RdBu_r use vmax = np.nanpercentile(np.abs(data), 99) as in the R example."),
 dict(priority="P2", title="usage-guide.md restates SKILL.md and lists tools no code uses",
  observed_in=[1, 2, 3],
  problem="The guide repeats the Okabe-Ito hexes, symmetric-bounds, white-midpoint, grayscale, rainbow, brand-palette and custom-palette tips already in SKILL.md; khroma and colorcet are in the version line and install list but no code block or example uses them.",
  root_cause="Two documents maintained for the same content.",
  fix="Keep prompts and prerequisites in the guide, reference SKILL.md for the tips, and either add a khroma/colorcet snippet or drop them from the install list."),
]

report = {
 "meta": {
  "skill_name": SKILL,
  "description": "Select colormaps and qualitative palettes for scientific figures using perceptual-uniformity, color-vision-deficiency safety, and luminance-monotonicity criteria. Covers Crameri scientific colormaps, viridis/cividis/magma, Okabe-Ito categorical, ColorBrewer, and the rainbow/jet critique.",
  "evaluated_on": "2026-09-20", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "A",
  "complexity": "Moderate", "n_inputs": 5, "source": SRC,
  "audit_type": "first audit (unmodified upstream GPTomics/bioSkills content)", "executed": True,
  "execution_note": "Executed 5/5 inputs on the data-visualization env: R 4.4.3 via r.sh (ggplot2 4.0.3, viridis 0.6.5, RColorBrewer 1.1.3, scico 1.5.0, khroma 1.17.0, ggsci 5.2.0, colorspace 2.1.2, scales 1.4.0, patchwork, circlize) and Python 3.12 via py.sh (matplotlib 3.11.2, cmcrameri 1.10, colorcet 3.2.1, colorspacious 1.1.2, seaborn 0.13.2). Every SKILL.md R and Python block and both shipped examples were run. Claims were asserted by computation: CIELab L* monotonicity in R colorspace and Python colorspacious (two independent methods), CAM02-UCS pairwise distances under deuteranopia/protanopia/tritanopia simulation, ggplot_build fill values for group-to-colour and zero-to-midpoint mapping. All figures are from SYNTHETIC data (seed 20260920; files under data/) and every PNG used as evidence was opened or pixel-checked. Note: pixel-level rank correlation did not discriminate jet on a smooth field and is not used as evidence."},
 "veto_gates": {
  "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
  "research_veto": {"applicable": True, "gate": "PASS",
   "scientific_integrity": {"result": "PASS", "detail": "No fabricated numbers; the eight cited papers (Crameri 2020 Nat Commun 11:5444, Nunez 2018 PLOS ONE e0199239, Wong 2010/2011, Harrower 2003, Borland 2007, Light 2004, Gehlenborg 2012) are real. Several tool statements are wrong (turbo uniform, cvd_emulator, colorblind style, default since 3.0), recorded as P1/P2."},
   "practice_boundaries": {"result": "PASS", "detail": "Palette choice for figures; nothing diagnostic or prescriptive."},
   "methodological_ground": {"result": "PASS", "detail": "The core criteria (uniform, CVD-safe, luminance-monotonic) and the named recommendations were verified. The turbo advice and the pure-white rule are self-contradictory but do not invert a conclusion; recorded as P1."},
   "code_usability": {"result": "PASS", "detail": "All SKILL.md R and Python blocks ran except cvd_emulator(palette, type=), which errors, and palettes_phd.R, which fails as shipped because df is undefined and ran 24/24 with data supplied; the Skill's version note tells the agent to adapt to the installed API and the shipped example already carries the working deutan() calls. Recorded as P1."}}},
 "static_score": static,
 "dynamic_score": {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": passed, "total": total}, "inputs": inputs},
 "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": "Beta Only", "grade_symbol": "\u26a0\ufe0f",
  "deployable": False, "veto_override": False,
  "grade_note": "71.8 is Beta Only (60-74). Floors: static 71 >= 70, execution 72.4 < 75, L1 avg 29.8 >= 28, L2 avg 42.6 >= 42, assertions 12/25 = 48% < 80%, so Limited Release is out of reach on three floors. No veto fired and no P0 is open (no safety-assertion failure, score >= 60); deployable is false because of the grade."},
 "key_strengths": [
  "The core recommendations hold under computation: viridis, magma, inferno, plasma, cividis, batlow and lipari have strictly monotonic CIELab L* (R colorspace and Python colorspacious agree), and cividis moves 0.7 dE under simulated deuteranopia against 15.4 for viridis.",
  "Okabe-Ito is verified as the right categorical default: the Skill's hexes match palette.colors and khroma, the 7-colour set keeps min dE 14.8 under deutan against 3.7 (Dark2) and 4.7 (Set1), and the claim that ggsci journal palettes are CVD-imperfect is confirmed (aaas 5.9).",
  "Every named function and palette exists with a working signature in the installed versions (7 scico names, 6 viridis options incl. turbo, cmcrameri names, six ggsci scales, scale_fill_scico midpoint=), and the failure-mode blocks reproduce: range-based vik puts zero on blue, data min/max bounds move zero to 0.155 of the range, linear maps show a 92 dE cyclic seam.",
  "The Common Failure Modes section (trigger, mechanism, symptom, fix) is the strongest part, and the shipped palettes_phd.R uses the correct deutan()/protan()/desaturate() calls.",
 ],
 "recommendations": recs,
}
(A / f"eval_report_{SKILL}_result.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print("written; recs", [r["priority"] for r in recs])
