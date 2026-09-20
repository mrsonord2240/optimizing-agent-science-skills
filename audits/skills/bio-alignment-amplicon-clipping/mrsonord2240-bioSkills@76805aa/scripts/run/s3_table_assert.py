"""Assert every cell of SKILL.md's synthetic single-read outcome table (samtools 1.24). cwd = out/i3.
Expected values are typed from SKILL.md ("Choosing the Clip Mode", second table); U = untouched (= original pos:CIGAR)."""
import sys
def load(tag):
    d = {}
    for l in open(f"{tag}.tsv"):
        n, flag, pos, cig = l.rstrip("\n").split("\t"); d[n] = f"{pos}:{cig}"
    return d
modes = ["default", "strand", "both", "both_strand"]
res = {m: load(m) for m in modes}
orig = {}
for l in open("orig.tsv"):
    n, flag, pc = l.rstrip("\n").split("\t"); orig[n] = pc
U = "U"
# read name -> (SKILL row label, [none, --strand, --both-ends, --both-ends --strand])
table = {
    "c1_rev_5end_inside_plusprimer":  ("rev 251-310", ["251:50M10S", U, "251:50M10S", U]),
    "c4_fwd_3end_inside_minusprimer": ("fwd 251-330", [U, U, "251:50M30S", "251:75M5S"]),
    "c5_fwd_3end_inside_plusprimer":  ("fwd 251-315", [U, U, "251:50M15S", U]),
    "c7_rev_3end_inside_minusprimer": ("rev 331-400", [U, U, "351:20S50M", U]),
}
ok = bad = 0
for n, (label, exp) in table.items():
    for m, e in zip(modes, exp):
        want = orig[n] if e == U else e
        got = res[m][n]
        flag = "ok" if got == want else "MISMATCH"
        ok += flag == "ok"; bad += flag != "ok"
        print(f"{label:12s} {m:12s} expected {want:12s} got {got:12s} {flag}")
print(f"SKILL table cells: {ok} match, {bad} mismatch (of {ok + bad})")
