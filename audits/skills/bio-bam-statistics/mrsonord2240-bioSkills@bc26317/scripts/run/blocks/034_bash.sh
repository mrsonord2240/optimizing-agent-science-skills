   # --SVDPrefix must include the .dat suffix of the panel files (e.g. 1000g.phase3.10k.b38.vcf.gz.dat)
   verifybamid2 --SVDPrefix panel.vcf.gz.dat --Reference ref.fa --BamFile input.bam --Output sample_vb
   # FREEMIX is in sample_vb.selfSM

   somalier extract -s sites.vcf.gz -f ref.fa -d extracted/ input.bam    # FASTA must contain the sites' contigs
   somalier relate extracted/*.somalier
