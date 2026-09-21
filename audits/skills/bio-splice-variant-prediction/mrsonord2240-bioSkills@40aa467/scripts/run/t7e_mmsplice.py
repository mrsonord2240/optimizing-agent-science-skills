import os, sys, warnings
sys.dont_write_bytecode = True
warnings.filterwarnings('ignore'); os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
S = '/mnt/openscience/as-spvp-reaudit-scratch'
from mmsplice.vcf_dataloader import SplicingVCFDataloader
from mmsplice import MMSplice, predict_save
dl = SplicingVCFDataloader(gtf=S + '/gencode.v45.chr7_17.basic.gtf', fasta_file=S + '/hg38_chr7_chr17.upper.fa', vcf_file='data/panel_new_grch38.vcf')
predict_save(MMSplice(), dl, 'out/mmsplice_new.csv', pathogenicity=True)
print('done')
