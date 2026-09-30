#!/usr/bin/env python3
"""Build the delta report.json by carrying the prior certified report forward.
Frontmatter-only delta (category, author): no dimension or assertion is touched, so all
scores, assertions and recommendations carry forward unchanged; only the date moves.
Recomputes the final score from the rubric to confirm the carried numbers."""
import json, sys

prior_path, out_path, date = sys.argv[1], sys.argv[2], sys.argv[3]
r = json.load(open(prior_path, encoding="utf-8"))
r["meta"]["evaluated_on"] = date
assert r["meta"]["category"] == "Data Analysis"

static = sum(c["score"] for c in r["static_score"]["categories"].values())
assert static == r["static_score"]["subtotal"], static
ex = [i["total"] for i in r["dynamic_score"]["inputs"]]
avg = round(sum(ex) / len(ex), 1)
assert avg == r["dynamic_score"]["execution_avg"], avg
sw, dw = round(0.4 * static, 1), round(0.6 * avg, 1)
final = round(0.4 * static + 0.6 * avg)
assert (sw, dw, final) == (r["final"]["static_weighted"], r["final"]["dynamic_weighted"], r["final"]["score"]), (sw, dw, final)
p = sum(i["assertions_passed"] for i in r["dynamic_score"]["inputs"])
t = sum(i["assertions_total"] for i in r["dynamic_score"]["inputs"])
assert (p, t) == (r["dynamic_score"]["assertion_pass_rate"]["passed"], r["dynamic_score"]["assertion_pass_rate"]["total"])
assert all(x["priority"] in ("P0", "P1", "P2") for x in r["recommendations"])
json.dump(r, open(out_path, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
open(out_path, "a", encoding="utf-8", newline="\n").write("\n")
print(f"static={static} exec={avg} final={final} ({sw}+{dw}) grade={r['final']['grade']} "
      f"assertions={p}/{t} recs={[x['priority'] for x in r['recommendations']]}")
