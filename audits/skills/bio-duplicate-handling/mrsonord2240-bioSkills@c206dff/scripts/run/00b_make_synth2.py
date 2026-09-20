"""SYNTHETIC BAMs #2 for the duplicate-handling audit (written to run/data/).
3. synth_samelib_2rg.bam : 2 read groups (rgA1, rgA2) BOTH in library libA (e.g. two lanes of one library). 30 pairs at identical
   coordinates, one pair per RG. Truth: same library -> they ARE duplicates (30 pairs). SKILL.md claims --use-read-groups keys on RG ID
   (would NOT mark) whereas Picard keys on LB (marks 30).
4. synth_amplicon.bam    : PE 100bp amplicon panel: 10 amplicons x 100 pairs, every pair with the identical start/end (primer-anchored).
   Truth: 1000 pairs = 10 distinct molecules by coordinate; any coordinate-based marker flags 990 pairs (1980 reads).
"""
import pysam, random
exec(open("/mnt/openscience/audits/bio-duplicate-handling/run/00_make_synth.py").read().split("# ---- 1. optical")[0])
# reuse header()/mk_pair()/write() from script 1 (top part)
h = header([{"ID": "rgA1", "LB": "libA", "SM": "s", "PL": "ILLUMINA"}, {"ID": "rgA2", "LB": "libA", "SM": "s", "PL": "ILLUMINA"}])
recs = []
for i in range(30):
    p1 = 2000 + i * 400
    recs += mk_pair(h, f"A00001:10:FC1:1:1101:{1000+i}:{2000+i}", p1, p1 + 180, "rgA1", 900 + i)
    recs += mk_pair(h, f"A00001:10:FC1:2:1101:{3000+i}:{4000+i}", p1, p1 + 180, "rgA2", 900 + i)
write(f"{D}/synth_samelib_2rg.bam", h, recs)

h = header([{"ID": "rg1", "LB": "libA", "SM": "s", "PL": "ILLUMINA"}])
recs = []
for a in range(10):
    p1 = 1000 + a * 2000
    for k in range(100):
        recs += mk_pair(h, f"A00001:10:FC1:1:{1101+k}:{1000+k*13}:{2000+a*7}", p1, p1 + 150, "rg1", 3000 + a)
write(f"{D}/synth_amplicon.bam", h, recs)
print("wrote synth_samelib_2rg.bam (60 pairs) and synth_amplicon.bam (1000 pairs)")
