cd /mnt/openscience/audits/bio-alignment-io/run/data/codeml_seq
codeml codeml.ctl </dev/null > stdout.txt 2>&1
tail -3 stdout.txt
