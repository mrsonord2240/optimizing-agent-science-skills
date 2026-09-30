import json,sys
r=json.load(open('report.json',encoding='utf-8'));bad=[]
assert set(r)=={"meta","veto_gates","static_score","dynamic_score","final","key_strengths","recommendations"}
c=r["static_score"]["categories"];mx=dict(functional_suitability=12,reliability=12,performance_context=8,agent_usability=16,human_usability=8,security=12,maintainability=12,agent_specific=20)
assert set(c)==set(mx)
for k,v in c.items(): assert 0<=v["score"]<=mx[k]==v["max"] and v["note"]
assert sum(v["score"] for v in c.values())==r["static_score"]["subtotal"]
d=r["dynamic_score"];ins=d["inputs"];assert len(ins)==r["meta"]["n_inputs"]
for i in ins:
    assert i["basic"]+i["specialized"]==i["total"] and 3<=len(i["assertions"])<=5
    assert i["assertions_passed"]==sum(a["result"]=="PASS" for a in i["assertions"]) and i["assertions_total"]==len(i["assertions"])
    assert i["status_flag"]==("✅" if i["status"]=="COMPLETED" and i["total"]>=75 else "⚠️")
assert d["execution_avg"]==round(sum(i["total"] for i in ins)/len(ins),1)
f=r["final"];assert f["static_weighted"]==round(r["static_score"]["subtotal"]*.4,1) and f["dynamic_weighted"]==round(d["execution_avg"]*.6,1)
assert f["score"]==round(f["static_weighted"]+f["dynamic_weighted"])
assert 2<=len(r["key_strengths"])<=5
p=[x["priority"] for x in r["recommendations"]];assert all(x in("P0","P1","P2") for x in p) and p==sorted(p)
for x in r["recommendations"]: assert len(x["title"])<=60 and set(x)=={"priority","title","observed_in","problem","root_cause","fix"},x["title"]
print("schema checklist OK",f["score"],f["grade"])
