"""Input 4: Skill's comut block on real TCGA-LAML data; assert cell colours/order/annotation against an independent pandas count."""
import sys, warnings
import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import comut
print('import comut; hasattr(comut,"CoMut") =', hasattr(comut,'CoMut'), '(Skill uses comut.CoMut())')
from comut import comut as _cm
comut.CoMut = _cm.CoMut   # shim ONLY so the rest of the Skill block can be assessed; the verbatim failure is recorded above
from matplotlib import patches
from matplotlib.colors import to_hex, to_rgba

print("comut", getattr(comut, "__version__", "0.0.3?"), "pandas", pd.__version__, "matplotlib", matplotlib.__version__)
DV = r"F:\OpenScience\audit-envs\data-visualization\public-data\mutations"
maf = pd.read_csv(DV + r"\tcga_laml.maf.gz", sep="\t", comment="#", low_memory=False)
ann = pd.read_csv(DV + r"\tcga_laml_annot.tsv", sep="\t")
CLS = {"Missense_Mutation": "Missense", "In_Frame_Ins": "Missense", "In_Frame_Del": "Missense",
       "Nonsense_Mutation": "Truncating", "Frame_Shift_Ins": "Truncating", "Frame_Shift_Del": "Truncating",
       "Splice_Site": "Splice"}
m = maf[maf.Variant_Classification.isin(CLS)].copy()
m["value"] = m.Variant_Classification.map(CLS)
mutation_long_df = m.rename(columns={"Tumor_Sample_Barcode": "sample", "Hugo_Symbol": "category"})[["sample", "category", "value"]].drop_duplicates()
top_genes = list(mutation_long_df.groupby("category")["sample"].nunique().sort_values(ascending=False).index[:10])
mutation_long_df = mutation_long_df[mutation_long_df.category.isin(top_genes)]
clinical_long_df = ann.rename(columns={"Tumor_Sample_Barcode": "sample"}).assign(category="Subtype", value=lambda d: d.FAB_classification)[["sample", "category", "value"]].dropna()
tmb = maf[maf.Variant_Classification.isin(CLS)].groupby("Tumor_Sample_Barcode").size().rename("value").reset_index().rename(columns={"Tumor_Sample_Barcode": "sample"})
tmb_long_df = tmb.assign(category="TMB")[["sample", "category", "value"]]
print("top genes:", top_genes, "| TMB max", tmb_long_df.value.max(), "n samples in mut df", mutation_long_df["sample"].nunique())

# ---- Skill block, verbatim apart from data names ----
try:
    toy_comut = comut.CoMut()
    toy_comut.add_categorical_data(
        data=mutation_long_df,
        name='Mutations',
        category_order=top_genes,
        value_order=['Truncating', 'Missense', 'Splice', 'Amp', 'HomDel'],
        mapping={'Truncating': '#000000', 'Missense': '#56B4E9',
                 'Splice': '#CC79A7', 'Amp': '#D55E00', 'HomDel': '#0072B2'})
    toy_comut.add_categorical_data(
        data=clinical_long_df,
        name='Subtype',
        mapping={'Luminal': '#0072B2', 'Basal': '#D55E00'})   # Skill's placeholder subtype names (do not exist in LAML)
    toy_comut.add_continuous_data(
        data=tmb_long_df,
        name='TMB',
        mapping='viridis',
        value_range=(0, 30))
    toy_comut.plot_comut(figsize=(12, 8))
    toy_comut.figure.savefig('out/i4_skill_verbatim.png', dpi=100, bbox_inches='tight')
    print('verbatim block: ran')

except Exception as e:
    print('verbatim block (with import shim) ERROR:', type(e).__name__, str(e)[:160])

# ---- corrected data names (FAB values) so we can assess the plot content ----
fab = sorted(clinical_long_df.value.unique())
fabcol = dict(zip(fab, ['#0072B2', '#D55E00', '#009E73', '#F0E442', '#CC79A7', '#56B4E9', '#999999', '#E69F00']))
all_samples = sorted(maf.Tumor_Sample_Barcode.unique())
c = comut.CoMut()
c.samples = all_samples   # required: comut rejects later datasets whose samples are not in the first dataset (zero-mutation samples)
mp = {'Truncating': '#000000', 'Missense': '#56B4E9', 'Splice': '#CC79A7', 'Amp': '#D55E00', 'HomDel': '#0072B2'}
c.add_categorical_data(data=mutation_long_df, name='Mutations', category_order=top_genes,
                       value_order=['Truncating', 'Missense', 'Splice', 'Amp', 'HomDel'], mapping=mp)
print('clinical rows with samples not in the MAF cohort (comut raises on these):', int((~clinical_long_df['sample'].isin(all_samples)).sum()))
c.add_categorical_data(data=clinical_long_df[clinical_long_df['sample'].isin(all_samples)], name='Subtype', mapping=fabcol)
c.add_continuous_data(data=tmb_long_df, name='TMB', mapping='viridis', value_range=(0, 30))
c.plot_comut(figsize=(12, 8))
c.figure.savefig('out/i4_comut.png', dpi=100, bbox_inches='tight')
print("samples in comut:", len(c.samples), "(cohort 193; mutation df has", mutation_long_df["sample"].nunique(), ")")

# sample order: first appearance in the first data frame added (i.e. NOT sorted by burden / memo sort)
first_seen = list(mutation_long_df["sample"].drop_duplicates())
print("comut sample order == order of first appearance in mutation df:", c.samples == first_seen)
print("first 8 comut samples:", c.samples[:8])

# ---- content assertions from patches ----
ax = c.axes['Mutations']
ticks = [t.get_text() for t in ax.get_yticklabels()]
print("y tick order (bottom->top):", ticks)
exp = {}
for (g, s), grp in mutation_long_df.groupby(['category', 'sample']):
    exp[(g, s)] = sorted(set(grp.value))
tri = {}; rect = {}
def cell(xy):  # patch origin -> (col,row)
    return int(round(xy[0])), int(round(xy[1]))
for p in ax.patches:
    if isinstance(p, patches.Rectangle):
        j, i = cell(p.get_xy()); rect[(i, j)] = to_hex(p.get_facecolor())
    else:
        pts = p.get_xy(); j = int(np.floor(pts[:, 0].min() + 1e-6)); i = int(np.floor(pts[:, 1].min() + 1e-6)); tri.setdefault((i, j), []).append(to_hex(p.get_facecolor()))
inv = {v.lower(): k for k, v in mp.items()}
mism = 0; checked = 0; nmulti2 = 0; nmulti3 = 0; multi_cells = []
for i, g in enumerate(ticks):
    for j, s in enumerate(c.samples):
        e = exp.get((g, s), [])
        checked += 1
        if len(e) == 0: got = [] if rect.get((i, j)) in ('#ffffff', None) else ['?']
        elif len(e) == 1: got = [inv.get(rect.get((i, j)), '?')]
        elif len(e) == 2:
            nmulti2 += 1; got = sorted(inv.get(x, '?') for x in tri.get((i, j), []))
        else:
            nmulti3 += 1; got = ['Multiple']; multi_cells.append((g, s, e))
        if len(e) <= 2 and got != e: mism += 1
        if len(e) > 2: print("3+ classes cell", g, s, e, "drawn rect colour", rect.get((i, j)))
print("cells checked:", checked, "| mismatches vs independent groupby (single & 2-class cells):", mism,
      "| 2-class triangle cells:", nmulti2, "| 3-class 'Multiple' cells:", nmulti3)

# TMB colour: with value_range=(0,30) but max TMB 42 -> values >30 normalise > 1
print("TMB values above the Skill's hard-coded 30:", int((tmb_long_df.value > 30).sum()), "of", len(tmb_long_df))
# comut's own normalise is (x-min)/max: for a nonzero min it is not min-max scaling
cc = comut.CoMut(); cc.add_continuous_data(data=pd.DataFrame({'sample': ['a','b','c'], 'category': 'T', 'value': [10, 20, 30]}), name='T', mapping='viridis', value_range=(10, 30))
pdat = cc._plots['T']['patches_options']
print("comut normalised keys for values 10,20,30 with range (10,30):", sorted(k for k in pdat if isinstance(k, float)), "(expect 0, .5, 1)")

# Subtype annotation mapping to samples
ax2 = c.axes['Subtype']; sub = {}
for p in ax2.patches:
    if isinstance(p, patches.Rectangle): sub[cell(p.get_xy())[0]] = to_hex(p.get_facecolor())
fabmap = dict(zip(ann.Tumor_Sample_Barcode, ann.FAB_classification))
invf = {v.lower(): k for k, v in fabcol.items()}
bad = sum(1 for j, s in enumerate(c.samples) if invf.get(sub.get(j)) != fabmap.get(s))
print("subtype annotation mismatches by sample:", bad, "of", len(c.samples))
# zero-mutation samples: LAML samples whose only variants are not in the top 10 -> kept?
print("LAML samples with no top-10 alteration present as columns:", len(set(c.samples)) , "vs cohort", maf.Tumor_Sample_Barcode.nunique())
