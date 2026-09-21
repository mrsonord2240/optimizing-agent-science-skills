"""Run the shipped example examples/lollipop_phd.R with minimal path substitutions only, in three variants, and record how far it gets.
V1: verbatim except 'cohort.maf' -> synthetic MAF path and the undefined `clinical` -> the synthetic clinical table.
V2: V1 with proteinID = 'P04637' removed (the argument the Skill recommends).
V3: V2 on a cleaned MAF (no unparsable HGVSp, no class outside the 7-colour palette) to see whether the rest produces correct output.
Driven from Python only to do the text substitution with explicit utf-8; R runs through r.sh."""
import os, re, subprocess, csv, shutil
BASE = r"F:\OpenScience\audits\bio-data-visualization-lollipop-protein-maps"
src = open(BASE + r"\run\skill\examples\lollipop_phd.R", encoding="utf-8").read()
DATA = (BASE + r"\data").replace("\\", "/")
RUN = BASE + r"\run\out\ex"
os.makedirs(RUN, exist_ok=True)

# cleaned MAF for V3
rows = list(csv.reader(open(BASE + r"\data\synthetic_lollipop.maf", encoding="utf-8"), delimiter="\t"))
hdr, body = rows[0], rows[1:]
ih, ic = hdr.index("HGVSp_Short"), hdr.index("Variant_Classification")
ok_classes = {"Missense_Mutation","Nonsense_Mutation","Frame_Shift_Del","Frame_Shift_Ins","Splice_Site","In_Frame_Del","In_Frame_Ins"}
clean = [r for r in body if re.match(r"^p\.[A-Z]\d+", r[ih]) and r[ic] in ok_classes]
with open(RUN + r"\clean.maf", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t"); w.writerow(hdr); w.writerows(clean)
print("clean MAF rows:", len(clean), "of", len(body))

def make(name, maf_path, drop_proteinid):
    s = src.replace("maf = 'cohort.maf', clinicalData = clinical",
                    "maf = '%s', clinicalData = data.table::fread('%s/synthetic_clinical.tsv')" % (maf_path, DATA))
    if drop_proteinid:
        s = s.replace(",\n             proteinID = 'P04637')", ")")
    s = s.replace("library(maftools)", "library(maftools); library(data.table)", 1)
    p = RUN + "\\" + name + ".R"
    open(p, "w", encoding="utf-8").write(s)
    return p

for name, maf, drop in [("V1_verbatim", DATA + "/synthetic_lollipop.maf", False),
                        ("V2_no_proteinID", DATA + "/synthetic_lollipop.maf", True),
                        ("V3_clean_no_proteinID", (RUN + r"\clean.maf").replace("\\", "/"), True)]:
    print("wrote", make(name, maf, drop))
# then run: for v in V1_verbatim V2_no_proteinID V3_clean_no_proteinID; do (cd out/ex && ../../../../../audit-envs/... r.sh $v.R > $v.log 2>&1); done  (see 10_run_examples.sh)
