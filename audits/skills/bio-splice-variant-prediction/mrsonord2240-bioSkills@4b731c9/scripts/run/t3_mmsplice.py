# INPUT 3: MMSplice exactly as the SKILL.md block (SplicingVCFDataloader + predict_save(pathogenicity=True)).
# usage: python t3_mmsplice.py grch37|grch38   (env as-mmsplice)
import os, sys, warnings, traceback
sys.dont_write_bytecode = True
warnings.filterwarnings('ignore'); os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
AS = '/mnt/openscience/audit-envs/alternative-splicing'
G = '/mnt/openscience/as-spvp-scratch/g38'
build = sys.argv[1]
cfg = {'grch37': (AS + '/public-data/rnasplice/reference/genes_chrX.gtf', AS + '/public-data/derived/X.fa', 'data/panel_grch37.vcf'),
       'grch38': (G + '/gencode.v45.chr17_X.basic.gtf', G + '/hg38_chr17_chrX.upper.fa', 'data/panel_grch38_auditor.vcf')}[build]
gtf, fa, vcf = cfg
from mmsplice.vcf_dataloader import SplicingVCFDataloader
from mmsplice import MMSplice, predict_save
try:
    dl = SplicingVCFDataloader(gtf=gtf, fasta_file=fa, vcf_file=vcf)
    model = MMSplice()
    predict_save(model, dl, 'out/mmsplice_%s.csv' % build, pathogenicity=True)
    print('predict_save finished for', build)
except Exception as e:
    print('EXCEPTION', build, type(e).__name__, str(e)[:400]); traceback.print_exc(limit=3)
