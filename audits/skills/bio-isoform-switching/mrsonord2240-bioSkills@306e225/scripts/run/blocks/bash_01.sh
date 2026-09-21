  hmmscan --cut_ga --domtblout pfam_domtbl.txt Pfam-A.hmm sequences/isoformSwitchAnalyzeR_isoform_AA.fasta > /dev/null
  curl -O https://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.clans.tsv.gz
  python examples/hmmscan_to_pfamscan.py pfam_domtbl.txt pfam_scanfmt.txt Pfam-A.clans.tsv.gz
  