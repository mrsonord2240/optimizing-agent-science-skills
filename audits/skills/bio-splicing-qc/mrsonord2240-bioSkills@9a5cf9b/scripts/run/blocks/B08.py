import sys; sys.path.insert(0, 'examples')
from splicing_qc import score_splice_sites

# 5'ss: 9 nt (3 exon + 6 intron). 3'ss: 23 nt (20 intron + 3 exon); the intron must end in AG.
donors = ['CAGGTAAGT', 'CAGATAAGT']
acceptors = ['TTTTTTTTTTTTTTCCTTAGGAG']          # 11.58; 'T'*20 + 'CAG' has no AG and scores -7.20
s5, s3 = score_splice_sites(donors, acceptors)   # one score per input; NaN for invalid input
print(s5, s3)                                     # [10.86, 2.68] [11.58]
