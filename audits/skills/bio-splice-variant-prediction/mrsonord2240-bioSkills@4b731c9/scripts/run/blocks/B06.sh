curl -O https://ftp.ensembl.org/pub/current_variation/SpliceVault/SpliceVault_data_GRCh38.tsv.gz.tbi   # index only; rows stream over HTTP
python splicevault_lookup.py chr17 7674292 T C --transcript ENST00000269305 --tbi SpliceVault_data_GRCh38.tsv.gz.tbi
# ENST00000269305 Acceptor_loss at chr17:7674291; SpliceAI delta 1; out-of-frame Frameshift:3/4; 199336 samples
# Top1 CA +47 0.4% Frameshift | Top2 CA -50 0.08% Frameshift | Top3 ES 7 0.03% Frameshift | Top4 CA -70 0.03% inFrame
