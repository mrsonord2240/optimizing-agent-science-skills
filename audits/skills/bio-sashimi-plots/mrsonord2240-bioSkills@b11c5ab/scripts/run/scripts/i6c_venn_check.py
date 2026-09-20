"""Independent venn check: genes (Jutils compares GeneName) with p-value<=0.05 (Jutils default), q<=1, |dPSI|>=0.05 in each rMATS TSV (JC vs JCEC)."""
import pandas as pd
d = 'F:/OpenScience/audits/bio-sashimi-plots/run/out/i6_jutils_real/jutils_out/'
def s(f):
    x = pd.read_csv(d + f, sep='\t', comment='#')
    return set(x[(x['p-value'] <= 0.05) & (x['q-value'] <= 1.0) & (x['dPSI'].abs() >= 0.05)]['GeneName'])
A, B = s('rmats_JC_results.tsv'), s('rmats_JCEC_results.tsv')
print('JC only', len(A - B), '| both', len(A & B), '| JCEC only', len(B - A), '   (figure shows 5 / 19 / 9)')
