"""Independent Fisher check of maftools::somaticInteractions (scipy) from the raw MAF files; plus Clopper-Pearson and Haldane-Anscombe checks."""
import pandas as pd, numpy as np
from scipy.stats import fisher_exact, binomtest
DV = r"F:\OpenScience\audit-envs\data-visualization\public-data\mutations"
SIL = {"Silent", "Intron", "RNA", "IGR", "3'UTR", "5'UTR", "3'Flank", "5'Flank"}
def load(path):
    m = pd.read_csv(path, sep="\t", comment="#", low_memory=False)
    return m[~m.Variant_Classification.isin(SIL)]
def check(tag, maf, si_csv, samples=None, universe_override=None):
    si = pd.read_csv(si_csv)
    if samples is not None: maf = maf[maf.Tumor_Sample_Barcode.isin(samples)]
    universe = sorted(maf.Tumor_Sample_Barcode.unique())     # maftools denominator: samples present in the MAF
    if universe_override is not None: universe = universe_override
    N = len(universe)
    sets = {g: set(d.Tumor_Sample_Barcode) for g, d in maf.groupby("Hugo_Symbol")}
    bad_p = bad_cnt = 0; maxdiff = 0; sign_bad = 0; n = 0
    for _, r in si.iterrows():
        a, b = sets.get(r.gene1, set()), sets.get(r.gene2, set())
        n11 = len(a & b); n10 = len(a - b); n01 = len(b - a); n00 = N - n11 - n10 - n01
        # maftools columns: 11 both, 10 only gene1?, 01 only gene2? -> compare as unordered
        cnt_ok = (n11 == r["11"]) and (n00 == r["00"]) and ({n10, n01} == {r["10"], r["01"]} or (n10 == r["10"] and n01 == r["01"]))
        if not cnt_ok: bad_cnt += 1
        orr, p = fisher_exact([[n11, n10], [n01, n00]])          # two-sided, as R fisher.test default
        d = abs(p - r.pValue) / max(p, 1e-300); maxdiff = max(maxdiff, d if p > 1e-290 else 0)
        if not np.isclose(p, r.pValue, rtol=1e-6, atol=1e-12): bad_p += 1
        expected_event = "Co_Occurence" if orr > 1 else "Mutually_Exclusive"
        if r.pValue < 0.05 and r.Event != expected_event: sign_bad += 1
        n += 1
    print(f"[{tag}] N={N} pairs={n} | 2x2 count mismatches={bad_cnt} | p-value mismatches (scipy two-sided Fisher, rtol 1e-6)={bad_p} | max rel diff={maxdiff:.2e} | Event-direction disagreements among p<0.05={sign_bad}")
    return si
laml = load(DV + r"\tcga_laml.maf.gz")
allsamp = sorted(pd.read_csv(DV + chr(92) + "tcga_laml.maf.gz", sep=chr(9), comment="#", low_memory=False).Tumor_Sample_Barcode.unique())
print("LAML: samples in raw file", len(allsamp), "| samples with a non-silent variant", laml.Tumor_Sample_Barcode.nunique())
check("LAML top20 (N = all samples in file, as maftools)", laml, "out/i6_laml_si.csv", universe_override=allsamp)
syn = load("data/synth_cohort.maf")
si = check("synthetic N=600 (10 genes)", syn, "out/i6_synth_si.csv")
s20 = [l.strip() for l in open("out/i6_s20.txt")]
si20 = check("synthetic subset N=20", syn, "out/i6_synth20_si.csv", samples=s20)
# planted structure recovered?
def row(df, x, y):
    r = df[((df.gene1 == x) & (df.gene2 == y)) | ((df.gene1 == y) & (df.gene2 == x))].iloc[0]; return r
for x, y, want in [("TP53", "MYC", "co-occur"), ("BRAF", "NRAS", "mutex"), ("KRAS", "EGFR", "mutex")]:
    r = row(si, x, y); print(f"planted {x}-{y} ({want}) N=600 -> p={r.pValue:.2e} OR={r.oddsRatio:.3f} event={r.Event} table11/10/01/00={r['11']}/{r['10']}/{r['01']}/{r['00']}")
    r = row(si20, x, y); print(f"   same pair, N=20 subset -> p={r.pValue:.3f} OR={r.oddsRatio:.3f} event={r.Event} table={r['11']}/{r['10']}/{r['01']}/{r['00']} pAdj={r.pAdj:.3f}")
# Skill small-cohort recipe: Clopper-Pearson per gene (compare with R binom.test output) and Haldane-Anscombe OR
cp = pd.read_csv("out/i6_cp_R.csv")
mx = 0
for _, r in cp.iterrows():
    ci = binomtest(int(r.MutatedSamples), 20).proportion_ci(confidence_level=0.95, method="exact"); mx = max(mx, abs(ci.low - r.lo), abs(ci.high - r.hi))
print("Clopper-Pearson: max |scipy exact - R binom.test| over 8 genes =", f"{mx:.2e}")
r = row(si20, "BRAF", "NRAS"); a, b, c, d = int(r["11"]), int(r["10"]), int(r["01"]), int(r["00"])
print("BRAF/NRAS N=20 2x2:", a, b, c, d, "| raw OR", "undefined/0" if (b*c)==0 or a*d==0 else (a*d)/(b*c), "| Haldane-Anscombe OR", round(((a+.5)*(d+.5))/((b+.5)*(c+.5)), 3), "| Fisher p", round(fisher_exact([[a,b],[c,d]])[1], 3))
