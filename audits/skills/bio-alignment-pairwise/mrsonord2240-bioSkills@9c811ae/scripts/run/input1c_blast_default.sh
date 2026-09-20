#!/bin/bash
# Skill claim: "BLASTP's own default composition-based statistics change the reported score (286 here)". Run in WSL.
cd /mnt/openscience/audits/bio-alignment-pairwise/run/data
echo "--- blastp defaults (comp_based_stats 2), HBA vs HBB, raw score column"
blastp -query hba.fa -subject hbb.fa -outfmt '6 qseqid sseqid score bitscore evalue pident qstart qend sstart send' 2>&1 | head -3
