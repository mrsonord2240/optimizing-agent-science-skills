import json, sys
p = "F:/OpenScience/audits/bio-experimental-design-sample-size/eval_report_bio-experimental-design-sample-size_result.json"
d = json.load(open(p, encoding="utf-8"))
err = []
def chk(c, m):
    if not c: err.append(m)
for k in ["meta","veto_gates","static_score","dynamic_score","final","key_strengths","recommendations"]:
    chk(k in d, f"missing top-level {k}")
m = d["meta"]
for k in ["skill_name","description","evaluated_on","evaluator_version","category","execution_mode","complexity","n_inputs","source","audit_type","executed_inputs"]:
    chk(k in m, f"meta missing {k}")
sv = d["veto_gates"]["skill_veto"]
chk(set(sv)=={"gate","stability","contract","determinism","security"}, f"skill_veto keys {set(sv)}")
rv = d["veto_gates"]["research_veto"]
chk(set(rv)=={"applicable","gate","scientific_integrity","practice_boundaries","methodological_ground","code_usability"}, f"research_veto keys {set(rv)}")
for k in ["scientific_integrity","practice_boundaries","methodological_ground","code_usability"]:
    chk(set(rv[k])=={"result","detail"}, f"{k} shape")
cats = d["static_score"]["categories"]
exp = {"functional_suitability":12,"reliability":12,"performance_context":8,"agent_usability":16,"human_usability":8,"security":12,"maintainability":12,"agent_specific":20}
chk(set(cats)==set(exp), f"category keys {set(cats)^set(exp)}")
tot=0
for k,mx in exp.items():
    v=cats[k]; chk(set(v)=={"score","max","note"}, f"{k} shape"); chk(v["max"]==mx, f"{k} max"); chk(isinstance(v["score"],int) and 0<=v["score"]<=mx, f"{k} range"); chk(v["note"], f"{k} note empty"); tot+=v["score"]
chk(tot==d["static_score"]["subtotal"], f"subtotal {d['static_score']['subtotal']} != {tot}")
ds = d["dynamic_score"]; ins = ds["inputs"]
chk(len(ins)==m["n_inputs"], f"inputs {len(ins)} != n_inputs {m['n_inputs']}")
tp=tt=0; tots=[]
for i in ins:
    chk(set(["index","type","label","status","status_flag","note","basic","specialized","total","assertions_passed","assertions_total","assertions","executed","execution_note"]) <= set(i), f"input {i.get('index')} keys missing {set(['index','type','label','status','status_flag','note','basic','specialized','total','assertions_passed','assertions_total','assertions','executed','execution_note'])-set(i)}")
    chk(i["basic"]+i["specialized"]==i["total"], f"input {i['index']} sum")
    a=i["assertions"]; chk(3<=len(a)<=5, f"input {i['index']} assertion count {len(a)}")
    np_=sum(1 for x in a if x["result"]=="PASS")
    chk(np_==i["assertions_passed"], f"input {i['index']} passed {i['assertions_passed']} != {np_}")
    chk(len(a)==i["assertions_total"], f"input {i['index']} total assertions")
    for x in a: chk(set(x)=={"text","result","note"}, f"input {i['index']} assertion shape"); chk(x["result"] in ("PASS","FAIL"), "assertion result")
    tp+=np_; tt+=len(a); tots.append(i["total"])
chk(ds["assertion_pass_rate"]=={"passed":tp,"total":tt}, f"assertion_pass_rate {ds['assertion_pass_rate']} vs {tp}/{tt}")
avg=round(sum(tots)/len(tots),1)
chk(abs(ds["execution_avg"]-avg)<1e-9, f"execution_avg {ds['execution_avg']} != {avg}")
f=d["final"]
sw=round(d["static_score"]["subtotal"]*0.4,1); dw=round(ds["execution_avg"]*0.6,1)
chk(f["static_weighted"]==sw, f"static_weighted {f['static_weighted']} != {sw}")
chk(f["dynamic_weighted"]==dw, f"dynamic_weighted {f['dynamic_weighted']} != {dw}")
chk(f["score"]==round(sw+dw), f"score {f['score']} != {round(sw+dw)}")
vf = sv["gate"]=="FAIL" or rv["gate"]=="FAIL"
chk(f["veto_override"]==vf, "veto_override"); chk(f["deployable"] is False if vf else True, "deployable")
chk(2<=len(d["key_strengths"])<=5, f"key_strengths {len(d['key_strengths'])}")
order={"P0":0,"P1":1,"P2":2}
pr=[order[r["priority"]] for r in d["recommendations"]]
chk(pr==sorted(pr), "recommendations not sorted")
for r in d["recommendations"]:
    chk(set(r)=={"priority","title","observed_in","problem","root_cause","fix"}, f"rec keys {set(r)}")
    chk(isinstance(r["observed_in"], list), f"observed_in not a list: {r['title']}")
    chk(len(r["title"])<=60, f"title too long ({len(r['title'])}): {r['title']}")
print("computed: subtotal=%d exec_avg=%.1f  sw=%.1f dw=%.1f score=%d  assertions=%d/%d  L1avg=%.1f L2avg=%.1f"
      % (tot, avg, sw, dw, round(sw+dw), tp, tt,
         sum(i["basic"] for i in ins)/len(ins), sum(i["specialized"] for i in ins)/len(ins)))
print("ERRORS:" if err else "ALL CHECKS PASSED")
for e in err: print("  -", e)
sys.exit(1 if err else 0)
