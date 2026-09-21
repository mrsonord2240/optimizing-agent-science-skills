import json, os
A = r'F:\OpenScience\audits\bio-data-visualization-matplotlib-fundamentals'
SID = 'bio-data-visualization-matplotlib-fundamentals'


def a(t, r, n):
    return {'text': t, 'result': 'PASS' if r else 'FAIL', 'note': n}


inputs = [
    dict(index=1, type='Canonical', label='Nature single-column (89 mm) PCA scatter, rasterized points, TrueType PDF, on 3000-point synthetic RNA-seq-like data',
         status='COMPLETED', status_flag='✅', executed=True,
         note='SKILL.md blocks 0 and 1 exec verbatim: ran clean; PDF Type-42 (ArialMT), 0 Type-3, text extractable, 6/7 pt fonts, scatter rasterized. Page is 89.42 mm (bbox tight), the shipped example gives 91.96 mm; hard-coded PC labels 45% vs real 34.6%.',
         basic=35, specialized=51, assertions=[
             a('Skill blocks 0+1 run verbatim without error or warning', True, 'ran on matplotlib 3.11.2 / pandas 3.0.6'),
             a('PDF embeds TrueType (Type 42) fonts and no Type 3; text is extractable', True, 'ArialMT TrueType x1, Type3 x0; pdftotext returns the axis labels'),
             a('Scatter is rasterized while axes/text stay vector', True, '2 image XObjects; text present as text'),
             a('Saved page width equals the requested 89 mm', False, '89.42 mm with the Skill rcParams (savefig.bbox tight); 91.96 mm in the shipped example (default pad_inches)'),
             a('Axis labels reflect the computed PCA variance', False, "Skill hard-codes 'PC1 (45%)'; real PCA gave 34.6% / 26.2%; the agent has to override it (done in pca_true.pdf)")]),
    dict(index=2, type='Variant A', label='2x3 multipanel with scatter+colorbar, line+CI, bar, boxplot, histogram, heatmap (Common Chart Types block, 6 segments)',
         status='PARTIAL', status_flag='⚠️', executed=True,
         note='4/6 chart segments ran; boxplot(labels=) raises TypeError on installed matplotlib 3.11.2 (removed; tick_labels replaces it since 3.9); heatmap segment NameError vmax undefined. After the two fixes the 2x3 figure is correct (bar heights, histogram total=2000, boxplot medians equal numpy medians, both colorbar labels).',
         basic=30, specialized=41, assertions=[
             a('Every Common Chart Types segment runs as written', False, '2 of 6 fail: boxplot labels= TypeError, heatmap vmax NameError'),
             a('Bar heights equal the input values', True, '3.1 / 4.7 / 2.2 read back from the patches'),
             a('Histogram bin counts sum to N', True, '2000 == 2000'),
             a('Boxplot medians and tick labels correct once tick_labels is used', True, 'medians 0.074/0.915/2.033 equal np.median; ticks A/B/C')]),
    dict(index=3, type='Edge', label='Volcano scatter into a pre-made Axes via seaborn with Up/Down/NS Okabe-Ito colours, seaborn.objects variant, FacetGrid gotcha',
         status='PARTIAL', status_flag='⚠️', executed=True,
         note="Block 3 runs and draws all 5000 rows, but the list palette ['#999999','#0072B2','#D55E00'] is assigned in first-appearance order: legend shows Up=grey, NS=blue, Down=orange (opened PNG confirms). The seaborn.objects snippet builds a Plot and never renders it.",
         basic=28, specialized=38, assertions=[
             a('Block 3 runs verbatim and draws every input row', True, '5000 of 5000 points, no warnings'),
             a('Colours land on the intended categories (NS grey, Up blue, Down orange)', False, 'list palette follows appearance order: Up=#999999, NS=#0072B2; only a dict palette is safe (verified)'),
             a('seaborn.objects snippet produces a figure as written', False, 'no .plot()/.save()/.show(): returns an unrendered Plot; pl.save() needed'),
             a('FacetGrid vs Axes gotcha is accurate', True, 'displot -> FacetGrid, no set_xlabel (AttributeError), set_axis_labels works; scatterplot -> Axes'),
             a('Volcano PNG at 4x3 in / 300 dpi opens non-blank with labelled axes', True, '1200x900 px, axes labelled, points visible')]),
    dict(index=4, type='Variant B', label='Axis formatting (log, sci-notation, date, ticks), CVD-safe colour, symmetric diverging, save as PDF/PNG/TIFF/SVG',
         status='PARTIAL', status_flag='⚠️', executed=True,
         note="Log, sci-notation, date and grid snippets work; the tick snippet raises NameError (np not imported) and, with np, ValueError (5 tick locations vs 3 labels); the colour block needs an undefined 'data'. Okabe-Ito hexes match the published set; symmetric clim equals the 99th percentile. PNG/TIFF are 300 dpi, TIFF is LZW, PDF fonts fine; SVG has 0 <text> elements (svg.fonttype=path), so it is not editable text.",
         basic=30, specialized=41, assertions=[
             a('Tick-frequency snippet runs', False, 'NameError np; with np: ValueError FixedLocator(5) vs 3 labels'),
             a('Okabe-Ito list is the published 8-colour set and symmetric clim = +/- 99th percentile', True, 'hexes match; clim (-7.710, 7.710) == quantile'),
             a('PNG and TIFF saved at 300 dpi with LZW for TIFF', True, 'PNG 1056x831 dpi 300; TIFF compression tiff_lzw'),
             a('SVG export is editable vector text as claimed', False, '0 <text> elements, 28 <path>; default svg.fonttype=path converts glyphs to outlines'),
             a('Colour and save blocks run once their undefined inputs are supplied', True, 'ran; only data/fig/np must be provided by the caller')]),
    dict(index=5, type='Stress', label='100,000-cell UMAP (12 clusters), 89 mm, colorbar, plus every Common Failure Modes claim',
         status='COMPLETED', status_flag='⚠️', executed=True,
         note="Skill patterns produce a correct, non-blank 100k-point figure (colorbar exactly 0.6 of axes height, no overlap; PDF 0.36 MB rasterized vs 2.0 MB vector, 2 s vs 12 s). Wrong claims: constrained_layout is NOT the default in 3.6+ (rcParams False); fig.set_rasterization_zorder does not exist (AttributeError; it is an Axes method); tight_layout with a colorbar did not clip; an 8-colour palette on 12 clusters cycles silently. The shipped example was also run (5 PDFs written, fonts and text verified).",
         basic=31, specialized=43, assertions=[
             a('rasterized=True keeps a 100k scatter PDF small', True, "2,000,274 B vector vs 363,890 B rasterized (12 s vs 2 s); the Skill's '50 MB' is not reproduced"),
             a('Colorbar shrink=0.6, aspect=20 avoids over-filling the axes and does not overlap', True, 'height ratio 0.60; cbar left 0.874 > axes right 0.838'),
             a("'constrained_layout ... is the default in matplotlib 3.6+' is true", False, "rcParamsDefault['figure.constrained_layout.use'] = False on 3.11.2"),
             a("'fig.set_rasterization_zorder(0)' works", False, "AttributeError: 'Figure' object has no attribute 'set_rasterization_zorder' (ax.set_rasterization_zorder works)"),
             a('Default PDF fonts are Type 3, Type-42 fix removes them', True, 'rcdefaults PDF: Type3 x1, TrueType x0; with the fix Type3 x0')]),
]
for i in inputs:
    i['assertions_total'] = len(i['assertions'])
    i['assertions_passed'] = sum(x['result'] == 'PASS' for x in i['assertions'])
    i['total'] = i['basic'] + i['specialized']
    i['execution_note'] = i['note']
avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
cats = {
    'functional_suitability': (8, 12, "Covers setup, figure/axes, chart types, seaborn, axes, colour, saving. Several verified factual errors: constrained_layout default claim, Figure.set_rasterization_zorder, boxplot labels= (removed in 3.11), list-palette order, editable-SVG claim, 89 mm not met with the Skill's own rcParams"),
    'reliability': (7, 12, 'Version-mismatch handling is one generic sentence; fragments fail with NameError/TypeError/ValueError and nothing tells the agent which variables a fragment expects'),
    'performance_context': (7, 8, '299-line SKILL.md plus a short usage guide; some duplication between SKILL.md, usage-guide and the example; no references/ needed'),
    'agent_usability': (11, 16, 'Clear three-defaults framing and a failure-modes section, but 180 mm vs 183 mm double column, prose claims that are wrong (see functional), and snippets that are not self-contained'),
    'human_usability': (6, 8, 'Natural trigger language (publication figures, Nature, RNA-seq scatter); tolerant of variants but assumes the caller supplies data names'),
    'security': (12, 12, 'No credentials, network or destructive calls; writes only figure files to cwd'),
    'maintainability': (9, 12, 'Single-purpose files, runnable example (ran 7/7 sections on matplotlib 3.11.2 / pandas 3.0.6); the example asserts nothing and hides its stand-in data assumptions'),
    'agent_specific': (16, 20, 'Precise description; no When-Not-To-Use / escape hatch; Related Skills point at existing folders (verified at the commit)'),
}
sub = sum(v[0] for v in cats.values())
static_w = round(sub * 0.4, 1)
dyn_w = round(avg * 0.6, 1)
score = round(static_w + dyn_w)
tp = sum(i['assertions_passed'] for i in inputs)
tt = sum(i['assertions_total'] for i in inputs)
print('static', sub, 'avg', avg, 'final', static_w, dyn_w, static_w + dyn_w, score, 'assertions', tp, tt, round(tp / tt * 100, 1),
      'L1', sum(i['basic'] for i in inputs) / 5, 'L2', sum(i['specialized'] for i in inputs) / 5)
P = 'priority'
rep = {
    'source': 'mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/matplotlib-fundamentals',
    'meta': dict(skill_name=SID,
                 description='Build publication-quality figures with matplotlib using the object-oriented Figure/Axes API, constrained_layout, rcParams customization, TrueType (Type-42) font embedding for journal submission, and CVD-safe palettes; covers seaborn integration, common chart types, axis formatting and saving.',
                 evaluated_on='2026-09-20', evaluator_version='skill-auditor@1.0', category='Data Analysis', execution_mode='A', complexity='Moderate', n_inputs=5,
                 execution_note='Every SKILL.md python block was extracted and exec-ed verbatim (run/blocks.py) and the shipped example ran from a scratch copy; matplotlib 3.11.2, seaborn 0.13.2, numpy 2.5.3, pandas 3.0.6, Python 3.12.13 (env data-visualization, py.sh). Data is synthetic and labelled so in every script.'),
    'veto_gates': {
        'skill_veto': dict(gate='PASS', stability='PASS', contract='PASS', determinism='PASS', security='PASS'),
        'research_veto': dict(
            applicable=True, gate='PASS',
            scientific_integrity=dict(result='PASS', detail="No fabricated results. The example labels axes 'PC1 (45.2%)' over random stand-in data and says the data are illustrative; flagged as P1, not fabrication"),
            practice_boundaries=dict(result='PASS', detail='Plotting Skill; no clinical or individual-level advice'),
            methodological_ground=dict(result='PASS', detail='No statistical claims; symmetric diverging limits and rasterization guidance verified. The list-palette order pitfall is a defect but the legend is drawn from the same mapping, so no conclusion is inverted'),
            code_usability=dict(result='PASS', detail='Shipped example ran (5 PDFs written, fonts and text verified). Fragments fail on 3 lines on the installed matplotlib or need undefined names (boxplot labels=, Figure.set_rasterization_zorder, tick label count); flagged P1/P2; syntax parses, imports exist')),
    },
    'static_score': dict(subtotal=sub, max=100, categories={k: dict(score=v[0], max=v[1], note=v[2]) for k, v in cats.items()}),
    'dynamic_score': dict(execution_avg=avg, max=100, assertion_pass_rate=dict(passed=tp, total=tt), inputs=inputs),
    'final': dict(static_weighted=static_w, dynamic_weighted=dyn_w, score=score, max=100, grade='Beta Only', grade_symbol='⚠️', deployable=False, veto_override=False,
                  note='75 is numerically Limited Release; downgraded one tier by scoring_rubric section 5 floors: execution average 73.6 < 75 and assertion pass rate 15/24 = 62.5% < 80%. Other floors met (static 76, L1 avg 30.8/40, L2 avg 42.8/60). No veto fired. Beta Only is not deployable under this repo rule (deployable = Production Ready or Limited Release, no P0).'),
    'key_strengths': [
        'The core recipe works: rcParams block + subplots(constrained_layout=True) + rasterized scatter gave a Type-42 PDF (ArialMT TrueType, 0 Type 3), extractable text, 6/7 pt font sizes and a rasterized point layer, verified on the PDF bytes',
        'Type-3 default, FacetGrid-vs-Axes, figsize-in-inches, mm-to-inch and colorbar shrink/aspect pitfalls are all real and were reproduced',
        'Okabe-Ito hexes match the published palette; the symmetric diverging-limits pattern gives exactly +/- the 99th percentile',
        'Shipped example runs unchanged on matplotlib 3.11 / pandas 3 and writes all five figures'],
    'recommendations': [
        {P: 'P1', 'title': 'boxplot(labels=) removed in matplotlib 3.11', 'observed_in': [2], 'problem': "The Common Chart Types boxplot line raises TypeError on 3.11.2 ('labels' removed; deprecated in 3.9). The Skill advertises 3.8+.", 'root_cause': 'API drift not tracked; the version line stops at 3.8+.', 'fix': 'Use tick_labels= (3.9+) and say labels= is for 3.8 only; raise the version floor or show both.'},
        {P: 'P1', 'title': 'fig.set_rasterization_zorder does not exist', 'observed_in': [5], 'problem': 'Failure Modes tells the agent to call fig.set_rasterization_zorder(0); it raises AttributeError. It is Axes.set_rasterization_zorder.', 'root_cause': 'Wrong object in prose.', 'fix': 'Write ax.set_rasterization_zorder(0) and show that artists with zorder below the threshold are rasterized.'},
        {P: 'P1', 'title': 'False claim: constrained_layout is the default in 3.6+', 'observed_in': [5], 'problem': "rcParamsDefault['figure.constrained_layout.use'] is False on 3.11.2; without constrained_layout=True no layout engine is applied. An agent trusting the claim would omit it.", 'root_cause': 'Confusion with availability of the option.', 'fix': "State that constrained_layout must be requested (constrained_layout=True or layout='constrained') and remove the default claim."},
        {P: 'P1', 'title': 'List palette maps colours by appearance order, silently', 'observed_in': [3], 'problem': "palette=['#999999','#0072B2','#D55E00'] with hue values Up/NS/Down painted Up grey and NS blue (figure opened). A volcano plot with upregulated genes grey is wrong while looking finished.", 'root_cause': 'Skill and example use a list where a category-keyed dict is needed.', 'fix': "Use palette={'NS':..., 'Up':..., 'Down':...} and hue_order in block 3, the seaborn.objects snippet and the example; add a check that legend colours match."},
        {P: 'P1', 'title': 'Hard-coded, invented PC variance labels', 'observed_in': [1], 'problem': "'PC1 (45%)' / 'PC1 (45.2%)' are typed into the examples over data whose real variance was 34.6% (canonical input) or random. An agent may copy them.", 'root_cause': 'Literal placeholders in code.', 'fix': 'Compute from pca.explained_variance_ratio_ in the recipe, or mark the labels as placeholders to replace.'},
        {P: 'P1', 'title': "'89 mm' is not what is saved; seaborn.objects recipe ignores the setup", 'observed_in': [1, 5], 'problem': "With savefig.bbox=tight the saved page is 89.42 mm (Skill rcParams) or 91.96 mm (example, default pad), over Nature's 89 mm column. The example's so.Plot figure is 162.56 x 121.92 mm with 11-12 pt text and no rasterization.", 'root_cause': 'bbox tight resizes the figure; so.Plot uses its own theme and size.', 'fix': 'For exact size use constrained_layout without bbox tight (or set savefig.pad_inches=0 and state the tolerance); for so.Plot add .layout(size=(w,h)) and .theme(mpl.rcParams) then re-check the size.'},
        {P: 'P2', 'title': 'Fragments are not self-contained', 'observed_in': [2, 4], 'problem': 'The tick snippet needs np and mismatches 5 ticks with 3 labels (ValueError); the colour block needs data; the heatmap needs vmax defined; the seaborn.objects snippet never renders.', 'root_cause': 'Snippets lifted from context.', 'fix': 'Import numpy where used, make tick and label counts agree, define vmax/data or say so, end the objects snippet with .save() or .plot().'},
        {P: 'P2', 'title': "SVG is 'editable' only after svg.fonttype='none'", 'observed_in': [4], 'problem': 'Default svg.fonttype=path: 0 <text> elements in the saved SVG, text is outlines.', 'root_cause': 'Missing rcParam.', 'fix': "Add 'svg.fonttype': 'none' to the rcParams block or reword the claim."},
        {P: 'P2', 'title': 'Inconsistent and unsourced journal numbers', 'observed_in': [1, 5], 'problem': 'Double column 180 mm (SKILL.md, example) vs 183 mm (usage-guide); Nature 5-7 pt, PDF-rejection and the "50 MB" for 100k vector points are unsourced (measured 2.0 MB / 12 s vs 0.36 MB / 2 s).', 'root_cause': 'Recall-based numbers.', 'fix': 'Cite each publisher rule or hedge; use measured numbers.'},
        {P: 'P2', 'title': 'No guidance for >8 categories or overplotting order', 'observed_in': [5], 'problem': 'Okabe-Ito has 8 colours; seaborn cycles the list for 12 clusters (8 distinct colours, warning only). Marker-gene colouring is drawn in random order.', 'root_cause': 'Palette section assumes few categories.', 'fix': 'Point to color-palettes for >8 levels; add sort-by-value for continuous colouring.'},
        {P: 'P2', 'title': 'Deprecation and warning debt', 'observed_in': [2, 5], 'problem': 'fig.set_constrained_layout emits PendingDeprecationWarning; seaborn 0.13.2 emits Pandas4Warning on pandas 3; the tight_layout + colorbar clipping claim did not reproduce on 3.11.2.', 'root_cause': 'Unversioned advice.', 'fix': "Use fig.set_layout_engine('constrained'); note the versions; soften or drop the tight_layout claim."},
        {P: 'P2', 'title': 'No when-not-to-use / hand-off section', 'observed_in': [], 'problem': 'The Skill does not say to leave R/ggplot users, interactive figures or genome tracks to other Skills.', 'root_cause': 'Escape hatches only in Related Skills.', 'fix': 'Add three lines of scope limits.'},
    ],
}
ps = {'P0': 0, 'P1': 1, 'P2': 2}
assert [ps[r[P]] for r in rep['recommendations']] == sorted(ps[r[P]] for r in rep['recommendations'])
json.dump(rep, open(os.path.join(A, f'eval_report_{SID}_result.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print('written')
