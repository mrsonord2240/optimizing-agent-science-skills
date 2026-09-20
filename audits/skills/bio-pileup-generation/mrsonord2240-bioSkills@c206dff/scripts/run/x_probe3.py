import pysam
H="/mnt/openscience/audit-envs/alignment-files/public-data/human/"
D="/mnt/openscience/audits/bio-pileup-generation/run/data/"
bam=pysam.AlignmentFile(H+"test.paired_end.sorted.bam")
fa=pysam.FastaFile(H+"genome.fasta")
for kw in [dict(), dict(ignore_overlaps=False), dict(min_base_quality=30), dict(min_base_quality=30,ignore_overlaps=False), dict(stepper="samtools",fastafile=fa)]:
    for col in bam.pileup("chr22",2999,3000,truncate=True,**kw):
        print(kw.keys(), col.pos+1, "n",col.n,"nsegments",col.nsegments,"len(pileups)",len(col.pileups),"seqs",len(col.get_query_sequences()),"num_aligned",col.get_num_aligned() if hasattr(col,'get_num_aligned') else None)
print([a for a in dir(pysam.PileupColumn) if not a.startswith('_')])
# synthetic overlap
sb=pysam.AlignmentFile(D+"syn.bam")
for kw in [dict(), dict(ignore_overlaps=False)]:
    for col in sb.pileup("synA",929,930,truncate=True,**kw):
        print("syn overlap",kw,col.n,len(col.pileups),col.get_num_aligned(), col.get_query_sequences())
