#!/bin/bash
# Make REAL tool-produced alignments (WSL, env alignment). Run: wsl_run.sh 'bash /mnt/openscience/audits/bio-alignment-msa-statistics/run/s01_wsl_make_data.sh'
set -u
cd /mnt/openscience/audits/bio-alignment-msa-statistics/run/data
# 1. MAFFT default output (does it emit lowercase?) on 8 UniProt globins
mafft --auto --quiet globins_uniprot.fasta > globins_mafft_default.fa </dev/null
# 2. MAFFT with --preservecase (input is uppercase so stays uppercase)
mafft --auto --quiet --preservecase globins_uniprot.fasta > globins_mafft_upper.fa </dev/null
# 3. clean 6 HBB CDS (drop record 7 = internal stop) -> nucleotide MAFFT
python - <<'EOF'
from Bio import SeqIO
recs = list(SeqIO.parse('hbb_cds_mammals.fasta','fasta'))
print('hbb records', len(recs), [len(r.seq) for r in recs])
SeqIO.write(recs[:6], 'hbb6.fa', 'fasta')
EOF
mafft --auto --quiet hbb6.fa > hbb6_mafft_default.fa </dev/null
# 4. HMMER: build a profile from the Pfam seed and align the 8 globins -> A2M (lowercase inserts, '.' gaps)
hmmbuild --amino --informat stockholm hmm_globin.hmm PF00042_seed.sto > /dev/null </dev/null
hmmalign --amino --outformat A2M hmm_globin.hmm globins_uniprot.fasta > globins_hmmalign.a2m </dev/null
hmmalign --amino --outformat afa hmm_globin.hmm globins_uniprot.fasta > globins_hmmalign.afa </dev/null
# 5. Clustal Omega (uppercase) for comparison
clustalo -i globins_uniprot.fasta --outfmt=fa --force -o globins_clustalo.fa </dev/null
# 6. Pfam seed (gap-stripped) via MAFFT default -> lowercase, 73 seq
python - <<'EOF'
from Bio import SeqIO
recs = []
for r in SeqIO.parse('PF00042_seed.sto','stockholm'):
    from Bio.SeqRecord import SeqRecord
    recs.append(SeqRecord(r.seq.replace('-','').replace('.',''), id=r.id.replace('/','_'), description=''))
SeqIO.write(recs,'seed_ungapped.fa','fasta')
EOF
mafft --auto --quiet seed_ungapped.fa > seed_mafft_default.fa </dev/null
for f in globins_mafft_default.fa globins_mafft_upper.fa hbb6_mafft_default.fa globins_hmmalign.a2m globins_hmmalign.afa globins_clustalo.fa seed_mafft_default.fa; do
  echo "== $f: seqs=$(grep -c '>' $f) bytes=$(wc -c < $f)"; sed -n '2p' $f | cut -c1-70
done
mafft --version 2>&1 | head -1
