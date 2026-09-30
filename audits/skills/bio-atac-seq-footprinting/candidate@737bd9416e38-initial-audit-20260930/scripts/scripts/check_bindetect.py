"""Assert biology on BINDetect output. Usage: check_bindetect.py bindetect_results.txt [cond1 cond2]"""
import csv, sys
f=sys.argv[1]; c1,c2=(sys.argv[2],sys.argv[3]) if len(sys.argv)>3 else ("cond1","cond2")
rows=list(csv.DictReader(open(f),delimiter="\t")); by={}
for r in rows: by.setdefault(r["name"],[]).append(r)
ch=lambda n: sum(float(x[f"{c1}_{c2}_change"]) for x in by[n])/len(by[n])
print("cols:",list(rows[0])); print("motifs:",sorted(by))
for n in by: print(n, "change=%.3f"%ch(n), "total_tfbs=",by[n][0]["total_tfbs"])
ok={"GATA1 more bound in K562 (change<0)":"GATA1" in by and ch("GATA1")<0,
    "IRF4 more bound in GM12878 (change>0)":"IRF4" in by and ch("IRF4")>0,
    "EBF1 more bound in GM12878 (change>0)":"EBF1" in by and ch("EBF1")>0,
    "CTCF >500 sites":"CTCF" in by and max(int(x["total_tfbs"]) for x in by["CTCF"])>500}
for k,v in ok.items(): print("PASS" if v else "FAIL",k)
sys.exit(0 if all(ok.values()) else 1)
