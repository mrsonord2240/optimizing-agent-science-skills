source /mnt/openscience/audits/bio-atac-seq-atac-qc/reaudit-run/scripts/env.sh; cd $O
python $R/mk_mism.py planted_pe.bam mism.bam && echo built; python $S/library_complexity.py mism.bam --exclude-contigs "" | tr -d '\n '; echo
python $S/library_complexity.py mism.bam | tr -d '\n '; echo
