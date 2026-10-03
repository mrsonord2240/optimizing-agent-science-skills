"""Hand-computed engineered tables for all 5 event types x JC/JCEC: NA cells, a low-read replicate in group 2 only,
a low-read replicate in group 1 only (reliability must look at BOTH groups, and mean must exclude IncLevelDifference)."""
import sys, tempfile, io, contextlib
SK = '/mnt/openscience/wt/norm-bio-splicing-quantification/skills/bio-splicing-quantification'
sys.path.insert(0, SK + '/scripts')
import quantify_splicing as q
cols = {
    'SE': ['exonStart_0base', 'exonEnd', 'upstreamES', 'upstreamEE', 'downstreamES', 'downstreamEE'],
    'A5SS': ['longExonStart_0base', 'longExonEnd', 'shortES', 'shortEE', 'flankingES', 'flankingEE'],
    'A3SS': ['longExonStart_0base', 'longExonEnd', 'shortES', 'shortEE', 'flankingES', 'flankingEE'],
    'MXE': ['1stExonStart_0base', '1stExonEnd', '2ndExonStart_0base', '2ndExonEnd', 'upstreamES', 'upstreamEE', 'downstreamES', 'downstreamEE'],
    'RI': ['riExonStart_0base', 'riExonEnd', 'upstreamES', 'upstreamEE', 'downstreamES', 'downstreamEE']}
# (ID, IJC1, SJC1, IJC2, SJC2, Inc1, Inc2, Diff) hand values
ev = [
    ('1', '30,30', '10,10', '25,25', '25,25', '0.9,0.7', '0.1,0.3', '0.6'),   # m1 .8, m2 .2, pooled .5, all reps >=40
    ('2', '30,30', '10,10', '25,5', '25,5', '0.9,0.7', '0.1,0.3', '0.6'),     # group2 rep2 only 10 reads
    ('3', '5,30', '5,10', '25,25', '25,25', '0.9,0.7', '0.1,0.3', '0.6'),     # group1 rep1 only 10 reads
    ('4', '30,0', '10,0', '25,25', '25,25', '0.9,NA', '0.1,0.3', '0.6'),      # NA replicate with 0 reads
]
fails = 0
for t, c in cols.items():
    for cnt in ('JC', 'JCEC'):
        d = tempfile.mkdtemp()
        hdr = ['ID', 'GeneID', 'geneSymbol', 'chr', 'strand'] + c + ['ID.1', 'IJC_SAMPLE_1', 'SJC_SAMPLE_1', 'IJC_SAMPLE_2', 'SJC_SAMPLE_2',
                                                                  'IncFormLen', 'SkipFormLen', 'PValue', 'FDR', 'IncLevel1', 'IncLevel2', 'IncLevelDifference']
        with open(f'{d}/{t}.MATS.{cnt}.txt', 'w') as f:
            f.write('\t'.join(hdr) + '\n')
            for e in ev:
                f.write('\t'.join([e[0], 'G', 'S', 'X', '+'] + ['1'] * len(c) + [e[0], e[1], e[2], e[3], e[4], '100', '50', 'NA', 'NA', e[5], e[6], e[7]]) + '\n')
        with contextlib.redirect_stdout(io.StringIO()):
            r = q.parse_rmats_output(d, t, min_junction_reads=20, counts=cnt)
            r0 = q.parse_rmats_output(d, t, min_junction_reads=0, counts=cnt)
        got = [int(i) for i in r['ID']]
        row = r.iloc[0]
        ok = (got == [1] and abs(row['mean_PSI'] - 0.5) < 1e-12 and abs(row['mean_PSI_group1'] - 0.8) < 1e-12
              and abs(row['mean_PSI_group2'] - 0.2) < 1e-12)
        r4 = r0[r0['ID'].astype(int) == 4].iloc[0]
        ok4 = (abs(r4['mean_PSI_group1'] - 0.9) < 1e-12 and abs(r4['mean_PSI'] - (0.9 + 0.1 + 0.3) / 3) < 1e-12 and len(r0) == 4)
        colsok = list(r.columns[5:5 + len(c)]) == c
        print(t, cnt, 'N=20 ids', got, 'OK' if ok else 'FAIL', '| N=0 NA handling', 'OK' if ok4 else 'FAIL', '| coord cols', colsok)
        fails += (not ok) + (not ok4) + (not colsok)
print('engineered fails', fails)
