import sys, pysam
bam=sys.argv[1]; lab=sys.argv[2]
# microexon exons: 1801-1810 -> junctions (1300,1800) and (1810,2400) (0-based half-open intron coords)
J1=(1300,1800); J2=(1810,2400); JS=(1300,2400)
c={"inc_total":0,"inc_with_micro":0,"inc_skipped_form":0,"inc_other":0,"skip_total":0,"skip_ok":0,"skip_with_micro":0}
for r in pysam.AlignmentFile(bam):
    if r.is_unmapped or r.is_secondary or r.is_supplementary: continue
    pos=r.reference_start; jn=[]
    for op,ln in r.cigartuples:
        if op==3: jn.append((pos,pos+ln)); pos+=ln
        elif op in (0,2,7,8): pos+=ln
    inc="_Minc_" in r.query_name
    has=(J1 in jn and J2 in jn); skp=(JS in jn)
    if inc:
        c["inc_total"]+=1
        if has: c["inc_with_micro"]+=1
        elif skp: c["inc_skipped_form"]+=1
        else: c["inc_other"]+=1
    else:
        c["skip_total"]+=1
        if skp: c["skip_ok"]+=1
        elif has: c["skip_with_micro"]+=1
print("%-52s microexon-including reads: %3d/%3d kept the 10-nt exon (%.0f%%), %3d aligned as exon-skipping, %3d other | skip reads correct %d/%d"%(lab,c["inc_with_micro"],c["inc_total"],100*c["inc_with_micro"]/max(c["inc_total"],1),c["inc_skipped_form"],c["inc_other"],c["skip_ok"],c["skip_total"]))
