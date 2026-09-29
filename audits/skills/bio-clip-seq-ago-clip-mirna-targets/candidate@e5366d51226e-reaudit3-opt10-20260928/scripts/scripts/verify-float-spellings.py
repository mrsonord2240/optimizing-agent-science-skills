#!/usr/bin/env python3
"""Exercise Python's accepted non-finite float spellings against the parser."""
from __future__ import annotations
import csv, json, os, subprocess, sys, tempfile
from pathlib import Path

candidate = Path("/mnt/openscience/wt/opt10-ago-clip/skills/bio-clip-seq-ago-clip-mirna-targets")
parser = candidate / "scripts/consensus_hyb.py"
high = "MIMAT1_MirBase_miR-1_microRNA"
low = "MIMAT2_MirBase_miR-2_microRNA"
def row(read_id: str, mirna: str) -> str:
    return "\t".join([read_id,"ACGT"*10,".","ENST1_gene_mRNA","23","40","101","118","2e-4",mirna,"1","22","1","22","1e-4",""]) + "\n"

spellings = ["NaN","nan","NAN","+NaN","-NaN","Inf","inf","+Inf","-Inf","Infinity","infinity","+Infinity","-Infinity"]
with tempfile.TemporaryDirectory(prefix="ago009-float-spellings-") as temp:
    root = Path(temp)
    hyb = root / "replicate.hyb"
    hyb.write_text(row("above",high)+row("below",low),encoding="utf-8")
    def invoke(expr: Path, threshold: str, name: str):
        out = root/name
        out.mkdir()
        outputs = [out/x for x in ("sites.tsv","targets.tsv","excluded.tsv","support.tsv","manifest.json")]
        cmd=[sys.executable,str(parser),"--hyb",str(hyb),str(hyb),"--sites",str(outputs[0]),"--targets",str(outputs[1]),"--excluded",str(outputs[2]),"--support",str(outputs[3]),"--manifest",str(outputs[4]),"--reads",str(hyb),"--expression",str(expr),f"--expression-threshold={threshold}","--hyb-commit","fixture","--hyb-db","fixture","--run-id",name]
        result=subprocess.run(cmd,capture_output=True,text=True,env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"})
        return result, outputs
    finite = root/"finite.tsv"
    finite.write_text("mirna_id\texpression_value\texpression_unit\texpression_source\n"+f"{high}\t+1.5e2\tTPM\tfixture\n{low}\t5e1\tTPM\tfixture\n",encoding="utf-8")
    accepted, files=invoke(finite,"1e2","finite-spellings")
    assert accepted.returncode == 0, accepted.stderr
    sites=list(csv.DictReader(files[0].open(encoding="utf-8"),delimiter="\t"))
    excluded=list(csv.DictReader(files[2].open(encoding="utf-8"),delimiter="\t"))
    assert [x["read_id"] for x in sites]==["above"] and excluded[0]["reason"]=="below_expression_threshold"
    value_results=[]; threshold_results=[]
    for i,value in enumerate(spellings):
        expr=root/f"bad-value-{i}.tsv"
        expr.write_text("mirna_id\texpression_value\texpression_unit\texpression_source\n"+f"{high}\t{value}\tTPM\tfixture\n",encoding="utf-8")
        result,out=invoke(expr,"100",f"bad-value-{i}")
        absent=all(not p.exists() for p in out)
        assert result.returncode != 0 and "expression_value must be finite" in result.stderr and absent,(value,result.stderr,absent)
        value_results.append({"value":value,"rejected":True,"outputs_absent":absent})
        result,out=invoke(finite,value,f"bad-threshold-{i}")
        absent=all(not p.exists() for p in out)
        assert result.returncode != 0 and "expression threshold must be finite" in result.stderr and absent,(value,result.stderr,absent)
        threshold_results.append({"value":value,"rejected":True,"outputs_absent":absent})
    print(json.dumps({"finite_values":{"accepted_expression":"+1.5e2","below_threshold_expression":"5e1","finite_threshold":"1e2","accepted_ids":[x["read_id"] for x in sites],"exclusion_reason":excluded[0]["reason"]},"python_float_nonfinite_spellings":spellings,"expression_values":value_results,"thresholds":threshold_results,"assertions_passed":1+len(value_results)+len(threshold_results)},indent=2,sort_keys=True))
