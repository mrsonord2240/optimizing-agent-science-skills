"""Build the SYNTHETIC test MAFs (seeded) and the independent ground-truth tables.
Everything here is synthetic: sample ids, coordinates and counts are made up. Truth is computed with a
regex parser written here, NOT with any Skill code."""
import random, re, json, csv
random.seed(20260920)
OUT = r"F:\OpenScience\audits\bio-data-visualization-lollipop-protein-maps\data" + "\\"

COLS = ["Hugo_Symbol","Entrez_Gene_Id","Center","NCBI_Build","Chromosome","Start_Position","End_Position","Strand",
        "Variant_Classification","Variant_Type","Reference_Allele","Tumor_Seq_Allele1","Tumor_Seq_Allele2",
        "Tumor_Sample_Barcode","HGVSp_Short","Protein_Change"]
rows = []
def add(gene, samp, vc, hgvsp, vt="SNP", chrom="17", start=7670000):
    ref, alt = ("C","T") if vt=="SNP" else (("CT","-") if vt=="DEL" else ("-","A"))
    rows.append([gene,0,"SYN","GRCh38",chrom,start+len(rows),start+len(rows),"+",vc,vt,ref,ref,alt,samp,hgvsp,hgvsp])

sid = [0]
def new_sample():
    sid[0]+=1; return "SYN-%04d" % sid[0]

# ---- TP53: planted hotspots + variant-class mix ----
for _ in range(45): add("TP53", new_sample(), "Missense_Mutation", "p.R175H")
for _ in range(38): add("TP53", new_sample(), "Missense_Mutation", "p.R248Q")
for _ in range(12): add("TP53", new_sample(), "Missense_Mutation", "p.R248W")   # same residue, other AA
for _ in range(29): add("TP53", new_sample(), "Missense_Mutation", "p.R273H")
for _ in range(8):  add("TP53", new_sample(), "Nonsense_Mutation", "p.R342*")
for _ in range(5):  add("TP53", new_sample(), "Frame_Shift_Del", "p.E286Kfs*9", "DEL")
for _ in range(4):  add("TP53", new_sample(), "Frame_Shift_Ins", "p.P72Lfs*3", "INS")
for _ in range(6):  add("TP53", new_sample(), "Splice_Site", "p.X125_splice")
for _ in range(4):  add("TP53", new_sample(), "In_Frame_Del", "p.K381del", "DEL")
for _ in range(3):  add("TP53", new_sample(), "In_Frame_Ins", "p.E298_S299insG", "INS")
# off-domain noise: N-terminal 8-40 and C-terminal 372-390, singletons
for pos in [8,12,17,22,26,33,40,372,377,380,385,390]:
    add("TP53", new_sample(), "Missense_Mutation", "p.%s%dA" % (random.choice("RKEDSTP"), pos))
# scattered singletons everywhere
for _ in range(40):
    pos = random.randint(45, 370)
    add("TP53", new_sample(), "Missense_Mutation", "p.%s%dV" % (random.choice("RKEDSTGL"), pos))
# multi-hit: sample already carrying R175H gets a 2nd R175H-position hit (different AA), and a sample with two hits at 248
add("TP53", "SYN-0001", "Missense_Mutation", "p.R175C")            # same sample, same position, other AA
add("TP53", "SYN-0046", "Missense_Mutation", "p.R248W")            # SYN-0046 is an R248Q sample (first R248Q)
add("TP53", "SYN-0003", "Missense_Mutation", "p.R175H")            # exact duplicate row of a sample's R175H (two calls)
# HGVSp edge cases
add("TP53", new_sample(), "Translation_Start_Site", "p.M1?")
add("TP53", new_sample(), "Translation_Start_Site", "p.M1?")
add("TP53", new_sample(), "Nonstop_Mutation", "p.*394Wext*?")
for _ in range(3): add("TP53", new_sample(), "Silent", "p.=")
add("TP53", new_sample(), "Intron", "")
add("TP53", new_sample(), "Intron", "")
add("TP53", new_sample(), "Missense_Mutation", "p.Arg175His")        # 3-letter HGVSp (not Short)
# ---- KRAS ----
for _ in range(30): add("KRAS", new_sample(), "Missense_Mutation", "p.G12D", chrom="12", start=25200000)
for _ in range(25): add("KRAS", new_sample(), "Missense_Mutation", "p.G12V", chrom="12", start=25200000)
for _ in range(12): add("KRAS", new_sample(), "Missense_Mutation", "p.G13D", chrom="12", start=25200000)
for _ in range(8):  add("KRAS", new_sample(), "Missense_Mutation", "p.Q61H", chrom="12", start=25200000)
for pos in [2,5,90,120,146,150,177]:
    add("KRAS", new_sample(), "Missense_Mutation", "p.A%dT" % pos, chrom="12", start=25200000)
# Cohort tag for lollipopPlot2
random.shuffle(rows)
with open(OUT+"synthetic_lollipop.maf","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t"); w.writerow(COLS); w.writerows(rows)

# clinical: alternate subtype, but planted so R175H is mostly Luminal, R273H mostly Basal
samples = sorted({r[13] for r in rows})
sub = {}
for s in samples:
    sub[s] = "Luminal" if random.random() < 0.5 else "Basal"
for r in rows:
    if r[0]=="TP53" and r[14]=="p.R175H": sub[r[13]] = "Luminal"
    if r[0]=="TP53" and r[14]=="p.R273H": sub[r[13]] = "Basal"
with open(OUT+"synthetic_clinical.tsv","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t"); w.writerow(["Tumor_Sample_Barcode","Subtype"])
    for s in samples: w.writerow([s, sub[s]])

# ---- INDEPENDENT TRUTH (regex written here) ----
pat = re.compile(r"^p\.(?:[A-Z\*]|[A-Z][a-z]{2})(\d+)")   # 1- or 3-letter ref, then position
truth = {}
for r in rows:
    gene, samp, vc, h = r[0], r[13], r[8], r[14]
    m = pat.match(h)
    if not m: continue
    pos = int(m.group(1))
    if vc == "Silent": continue
    d = truth.setdefault(gene, {}).setdefault(pos, {"mutations":0,"samples":set(),"classes":{}, "changes":{}})
    d["mutations"] += 1; d["samples"].add(samp)
    d["classes"][vc] = d["classes"].get(vc,0)+1
    d["changes"][h] = d["changes"].get(h,0)+1
out = {g:{str(p):{"mutations":v["mutations"],"samples":len(v["samples"]),"classes":v["classes"],"changes":v["changes"]} for p,v in sorted(pp.items())} for g,pp in truth.items()}
json.dump(out, open(OUT+"synthetic_truth.json","w",encoding="utf-8"), indent=1)
top = sorted(out["TP53"].items(), key=lambda kv:-kv[1]["mutations"])[:6]
print("rows", len(rows), "samples", len(samples))
for p,v in top: print("TP53", p, v["mutations"], "mut /", v["samples"], "samples", v["classes"])
print("KRAS", {p:(v["mutations"],v["samples"]) for p,v in out["KRAS"].items() if v["mutations"]>1})
