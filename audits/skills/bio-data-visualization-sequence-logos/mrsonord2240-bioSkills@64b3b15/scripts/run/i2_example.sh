#!/bin/bash
# Input 2: shipped example examples/seqlogo_phd.R, (a) as shipped from a clean dir, (b) with the missing inputs supplied
RUN=/f/OpenScience/audits/bio-data-visualization-sequence-logos/run
R=/f/OpenScience/audit-envs/data-visualization/r.sh
rm -rf $RUN/scratch_ex2 && mkdir -p $RUN/scratch_ex2/a $RUN/scratch_ex2/b
cp $RUN/skill/data-visualization/sequence-logos/examples/seqlogo_phd.R $RUN/scratch_ex2/a/
cp $RUN/skill/data-visualization/sequence-logos/examples/seqlogo_phd.R $RUN/scratch_ex2/b/
cd $RUN/scratch_ex2/a && echo "== (a) as shipped, no inputs ==" && bash $R seqlogo_phd.R 2>&1 | grep -v -e '^ℹ' -e 'Please report' | head -20
cd $RUN/scratch_ex2/b
awk '{print ">s"NR; print $0}' $RUN/data/dna_n200.txt > aligned_motif.fa
awk '{print ">p"NR; print $0}' $RUN/data/prot_n200.txt > phospho_aligned.fa
# the example never defines ctcf_seqs/rest_seqs/gata1_seqs: define them in a prelude
cat > prelude.R <<'PR'
rd <- function(f) readLines(file.path("F:/OpenScience/audits/bio-data-visualization-sequence-logos/run/data", f))
ctcf_seqs <- rd("dna_n200.txt"); rest_seqs <- rd("dna_n20.txt"); gata1_seqs <- rd("dna_gcrich_n500.txt")
PR
echo "== (b1) with fasta inputs but WITHOUT ctcf_seqs etc. (as shipped otherwise) =="
bash $R seqlogo_phd.R 2>&1 | grep -v -e '^ℹ' -e 'Please report' | head -20
cat prelude.R seqlogo_phd.R > seqlogo_phd_with_inputs.R
echo "== (b2) with all inputs supplied =="
bash $R seqlogo_phd_with_inputs.R 2>&1 | grep -v -e '^ℹ' -e 'Please report' | head -40
ls -la
