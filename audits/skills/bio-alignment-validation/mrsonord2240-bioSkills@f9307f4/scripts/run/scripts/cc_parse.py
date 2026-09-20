"""Print 'RESULT LOD_SCORE' of the first CROSS-group row (LEFT_GROUP_VALUE != RIGHT_GROUP_VALUE) of a Picard
CrosscheckFingerprints metrics file.  Picard also writes self-comparison rows (group vs itself, always a match); if the only
rows are self rows (two files collapsed into one group) print 'SELFONLY <lod of the self row>'; NONE NA if no rows."""
import sys

rows = [l.rstrip("\n").split("\t") for l in open(sys.argv[1], encoding="utf-8") if l.strip() and not l.startswith("#")]
recs = [dict(zip(rows[0], r)) for r in rows[1:]]
cross = [r for r in recs if r["LEFT_GROUP_VALUE"] != r["RIGHT_GROUP_VALUE"]]
if cross:
    print(cross[0]["RESULT"], cross[0]["LOD_SCORE"])
elif recs:
    print("SELFONLY", recs[0]["LOD_SCORE"])
else:
    print("NONE NA")
