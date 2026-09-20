"""Bridge: hmmscan --domtblout (what the Skill says to run) -> pfam_scan.pl-style table (what analyzePFAM() parses).
Not part of the Skill. pfam_scan.pl is not installed in the audit env, and the Skill never says which format analyzePFAM needs.
analyzePFAM() only recognises the file when at least one row has a clan starting 'CL' (column 15), so a Pfam-A.clans.tsv lookup is needed too.
Usage: python 40c_domtbl_to_pfamscan.py domtbl.txt out.txt Pfam-A.clans.tsv.gz"""
import sys, io, gzip
src, dst, clans = sys.argv[1], sys.argv[2], sys.argv[3]
clan = {}
for l in gzip.open(clans, "rt", encoding="utf-8"):
    f = l.rstrip("\n").split("\t")
    if len(f) > 1 and f[1]:
        clan[f[0]] = f[1]
out = []
for line in io.open(src, encoding="utf-8"):
    if line.startswith("#") or not line.strip():
        continue
    f = line.split()
    hmm_name, hmm_acc, hmm_len, q = f[0], f[1], int(f[2]), f[3]
    ievalue, score = f[12], f[13]
    hmm_from, hmm_to, ali_from, ali_to, env_from, env_to = f[15], f[16], f[17], f[18], f[19], f[20]
    cl = clan.get(hmm_acc.split(".")[0], "No_clan")
    out.append("%s %6s %6s %6s %6s %s  %s  Domain %5s %5s %5d %8s %10s 1 %s  " % (q, ali_from, ali_to, env_from, env_to, hmm_acc, hmm_name, hmm_from, hmm_to, hmm_len, score, ievalue, cl))
io.open(dst, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("wrote", len(out), "domain rows to", dst)
