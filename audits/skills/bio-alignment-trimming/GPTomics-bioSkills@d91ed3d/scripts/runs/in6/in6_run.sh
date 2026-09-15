# Input 6 (Scope Boundary) -- SYNTHETIC 10-taxon codon alignment (AliSim GY codon model, protein-guided MAFFT + PAL2NAL).
# User wants it "cleaned" for a codeml branch-site test and then wants the positively selected genes called.
# Skill: do NOT aggressively trim; TCS/GUIDANCE2 masking; MACSE frameshift post-processing; codeml belongs elsewhere.
set -u
export PATH=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/bin:/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts:$PATH
T=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools
cd "$(dirname "$0")"
cp ../../data/cds10_codon_aln.fasta codon.fasta
echo "== What column trimming would do (to justify NOT trimming): ClipKIT smart-gap without and with --codon"
clipkit codon.fasta -m smart-gap -o codon_smartgap.fasta > cs.out 2>&1; echo "exit $?"; grep -E "Original length|Number of sites kept" cs.out
clipkit codon.fasta -m smart-gap --codon -o codon_smartgap_codon.fasta > csc.out 2>&1; echo "exit $?"; grep -E "Number of sites kept" csc.out
PYTHONIOENCODING=utf-8 python -c "
from Bio import AlignIO
for f in ['codon.fasta','codon_smartgap.fasta','codon_smartgap_codon.fasta']:
    L=AlignIO.read(f,'fasta').get_alignment_length(); print(f, L, 'divisible by 3:', L%3==0)
"
echo "== MACSE frameshift post-processing (Skill commands) on a copy with an injected frameshift '!' and internal stop"
PYTHONIOENCODING=utf-8 python in6_inject.py
sed -e 's/!/-/g' macse_like.fasta > aligned_paml.fasta; echo "sed exit $?; '!' left: $(grep -v '>' aligned_paml.fasta | grep -c '!')"
java -jar $T/macse_v2.07.jar -prog exportAlignment -align macse_like.fasta \
    -codonForFinalStop --- -codonForInternalStop NNN \
    -out_NT aligned_hyphy.fasta -out_AA aligned_hyphy_aa.fasta > macse_export.out 2>&1; echo "MACSE exportAlignment exit $?"
tail -5 macse_export.out; grep -v '>' aligned_hyphy.fasta | grep -o -E '!|TAA|TAG|TGA' | sort | uniq -c | head
echo "== codeml check of the Skill claim that codeml reads '!' as missing data (M0, fixed tree)"
for v in bang dash; do
  mkdir -p codeml_$v; cp ../../data/cds10_true.nwk codeml_$v/tree.nwk
  if [ $v = bang ]; then cp macse_like_nostop.fasta codeml_$v/aln.fasta; else sed -e 's/!/-/g' macse_like_nostop.fasta > codeml_$v/aln.fasta; fi
  printf "seqfile = aln.fasta\ntreefile = tree.nwk\noutfile = mlc\nnoisy = 0\nverbose = 0\nrunmode = 0\nseqtype = 1\nCodonFreq = 2\nmodel = 0\nNSsites = 0\nicode = 0\nfix_kappa = 0\nkappa = 2\nfix_omega = 0\nomega = 0.4\ncleandata = 0\n" > codeml_$v/codeml.ctl
  (cd codeml_$v && timeout 300 codeml codeml.ctl > run.out 2>&1; echo "codeml $v exit $?"; tail -3 run.out; grep -E "^lnL|omega \(dN/dS\)" mlc 2>/dev/null)
done
echo "== T-Coffee: no Windows build -> TCS commands NOT executed (flag check against T-Coffee docs in runs/flagcheck)"
