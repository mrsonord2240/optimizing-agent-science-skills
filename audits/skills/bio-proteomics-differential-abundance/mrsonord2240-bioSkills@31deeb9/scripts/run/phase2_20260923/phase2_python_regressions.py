"""Fresh Phase-2 Python evidence: Inputs 4, 7, and 13."""
import importlib.util, pathlib, sys
import pandas as pd
if len(sys.argv) != 4: raise SystemExit("usage: phase2_python_regressions.py <skill> <data> <out>")
skill, data, out = map(pathlib.Path, sys.argv[1:])
spec = importlib.util.spec_from_file_location("da", skill/"examples"/"differential_abundance.py")
mod = importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(mod)
print("=== INPUT 4 Python Welch+BH and untestable table ===")
pg = pd.read_csv(data/"proteinGroups.txt", sep="\t", low_memory=False); cols = [x for x in pg if x.startswith("LFQ intensity")]
m = pg[cols].copy(); m.index = pg["Majority protein IDs"]; m.columns = [x.replace("LFQ intensity ","") for x in cols]
res, unt = mod.differential_abundance(mod.preprocess(m),[x for x in m if x.startswith("T")],[x for x in m if x.startswith("C")])
print(f"tested={len(res)} untestable={len(unt)} calls={(res.padj<.05).sum()} columns={list(unt.columns)}"); assert list(unt.columns)==["protein","n_case","n_ctrl"]
try: mod.differential_abundance(pd.DataFrame([[1,2]],index=["x"],columns=["C","T"]),["T"],["C"])
except ValueError as e: print("no-testable guard:",e)
else: raise AssertionError("missing no-testable guard")
print("=== INPUT 6 scope-boundary refusal verification ===")
sk=(skill/"SKILL.md").read_text(encoding="utf-8"); guide=(skill/"usage-guide.md").read_text(encoding="utf-8")
for x in ("single-sample (n=1) comparisons", "diagnosis or treatment decisions for an individual patient"):
 print(f"scope_exclusion={x!r} present={x in sk}"); assert x in sk
print("=== INPUT 7 source/guide consistency ===")
for x in ("manufactures systematic false positives","collapsed within-group variance",">50%"):
 print(f"obsolete={x!r} skill={x in sk} guide={x in guide}"); assert x not in sk and x not in guide
assert "examples/limma_analysis.R" in sk and "examples/differential_abundance.py" in sk and "references/feature_level.md" in sk and "msqrob2" in guide
print("=== INPUT 13 new large-n Python planted-truth check ===")
plasma=pd.read_csv(data/"plasma_12v12.csv",index_col=0); truth=pd.read_csv(data/"plasma_truth.csv").set_index("protein"); r13,u13=mod.differential_abundance(mod.preprocess(plasma),[x for x in plasma if x.startswith("case")],[x for x in plasma if x.startswith("ctrl")]); sig=r13[r13.padj<.05]; fp=int((truth.reindex(sig.protein)["class"]=="null").sum()); fdr=fp/max(1,len(sig)); print(f"large_n tested={len(r13)} untestable={len(u13)} calls={len(sig)} fp={fp} fdr={fdr:.3f}"); assert len(r13)>100 and len(u13)>0 and list(u13.columns)==["protein","n_case","n_ctrl"] and fdr<=.05; r13.to_csv(out/"python_input13_results.csv",index=False)
print("ALL_PY_ASSERTIONS_PASS")
