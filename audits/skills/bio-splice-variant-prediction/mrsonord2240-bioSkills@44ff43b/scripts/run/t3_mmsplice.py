# INPUT 3: MMSplice exactly as SKILL.md block #2 (predict_save with pathogenicity=True) on plain VCF (as the Skill writes it), then on bgzip+tabix VCF.
import os, sys, warnings, traceback
sys.dont_write_bytecode = True
warnings.filterwarnings('ignore'); os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
AS = '/mnt/openscience/audit-envs/alternative-splicing'
gtf = AS + '/public-data/rnasplice/reference/genes_chrX.gtf'; fa = AS + '/public-data/derived/X.fa'
import mmsplice; print('mmsplice', mmsplice.__version__ if hasattr(mmsplice, '__version__') else '?')
from mmsplice.vcf_dataloader import SplicingVCFDataloader
from mmsplice import MMSplice, predict_save
mode = sys.argv[1]
vcf = {'plain': 'data/panel_grch37.vcf', 'gz': 'data/panel_grch37.vcf.gz'}[mode]
try:
    dl = SplicingVCFDataloader(gtf=gtf, fasta_file=fa, vcf_file=vcf)
    model = MMSplice()
    predict_save(model, dl, 'out/mmsplice_%s.csv' % mode, pathogenicity=True)
    print('predict_save finished OK for', mode)
except Exception as e:
    print('EXCEPTION for', mode, type(e).__name__, str(e)[:400]); traceback.print_exc(limit=3)
