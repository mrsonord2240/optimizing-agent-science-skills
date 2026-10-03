"""SUPPA2 path (SQ-06/07) with an independent oracle: PSI recomputed from the .ioe + TPM table in stdlib python.
Run in as-suppa: micromamba run -n as-suppa python 34_suppa_independent.py"""
import sys, os, csv, math, io, contextlib
import pandas as pd
SK = '/mnt/openscience/wt/norm-bio-splicing-quantification/skills/bio-splicing-quantification'
sys.path.insert(0, SK + '/scripts')
import quantify_splicing as q
AS = '/mnt/openscience/audit-envs/alternative-splicing/public-data'
P, R = AS + '/planted', AS + '/rnasplice'
OUT = '/mnt/openscience/audits/bio-splicing-quantification/run-reaudit-1/out/suppa'
os.makedirs(OUT, exist_ok=True)
os.chdir(OUT)
import statsmodels
print('pandas', pd.__version__, 'statsmodels', statsmodels.__version__)


def read_tpm(path):
    with open(path) as f:
        rows = [l.rstrip('\n').split('\t') for l in f]
    hdr = rows[0]
    return hdr, {r[0]: [float(x) for x in r[1:]] for r in rows[1:]}


def oracle_psi(ioe, tpm_path):
    hdr, t = read_tpm(tpm_path)
    out = {}
    with open(ioe) as f:
        rd = csv.reader(f, delimiter='\t')
        next(rd)
        for r in rd:
            alt = r[3].split(','); tot = r[4].split(',')
            vals = []
            if any(x not in t for x in alt + tot):   # SUPPA2 skips events with a transcript absent from the TPM table
                out[r[2]] = [None] * len(hdr)
                continue
            for k in range(len(hdr)):
                den = sum(t[x][k] for x in tot if x in t)
                num = sum(t[x][k] for x in alt if x in t)
                vals.append(num / den if den > 0 else None)
            out[r[2]] = vals
    return out


def compare(tag, gtf, tpm_path):
    with contextlib.redirect_stdout(io.StringIO()):
        files = q.run_suppa2_quantification(gtf, tpm_path, tag)
    print(tag, 'psi files', sorted(files))
    worst = 0.0
    for code, f in files.items():
        ora = oracle_psi(f'{tag}_{code}_strict.ioe', tpm_path)
        got = pd.read_csv(f, sep='\t', index_col=0)
        n = 0
        for ev, row in got.iterrows():
            o = ora[ev]
            for a, b in zip(row.values, o):
                if (b is None) != bool(pd.isna(a)):
                    worst = max(worst, 9.9)
                elif b is not None:
                    worst = max(worst, abs(a - b)); n += 1
        print(f'  {code}: events={len(got)} values compared={n}')
    print(f'  max |SUPPA2 psi - independent oracle| = {worst:.2e}')
    return files


# planted
tpm = pd.read_csv(P + '/planted_tpm.txt', sep='\t', index_col=0)
q.write_suppa_tpm(tpm, 'planted_tpm_suppa.tsv')
print('header line repr:', repr(open('planted_tpm_suppa.tsv').read().splitlines()[0]))
files = compare('planted', P + '/planted.gtf', 'planted_tpm_suppa.tsv')
print(pd.read_csv(files['SE'], sep='\t', index_col=0))
# header-trap negative: pandas default header must not be what the Skill writes
tpm.to_csv('planted_tpm_pandas.tsv', sep='\t')
print('pandas-default header repr:', repr(open('planted_tpm_pandas.tsv').readline()))
# chrX
m = pd.DataFrame({s: pd.read_csv(f'{R}/salmon/{s}/quant.sf', sep='\t', index_col=0)['TPM']
                  for s in ['ERR188383', 'ERR188428', 'ERR188454', 'ERR204916']})
q.write_suppa_tpm(m, 'chrX_tpm.tsv')
files = compare('chrX', R + '/reference/genes_chrX.gtf', 'chrX_tpm.tsv')
# filter_reliable_events vs independent hand count
print('filter_reliable_events (default psi_range 0.05-0.95, coverage>=0.5) vs hand count; custom range 0.1-0.9')
for code, f in files.items():
    rows = list(csv.reader(open(f), delimiter='\t'))[1:]
    def keep(lo, hi):
        c = 0
        for r in rows:
            v = [float(x) for x in r[1:] if x not in ('nan', 'NA', '')]
            if len(v) / (len(r) - 1) >= 0.5:
                mu = sum(v) / len(v)
                c += (lo < mu < hi)
        return c
    with contextlib.redirect_stdout(io.StringIO()):
        a = q.filter_reliable_events(f)
        b = q.filter_reliable_events(f, psi_range=(0.1, 0.9))
    print(f'  {code}: default skill={len(a)} hand={keep(0.05, 0.95)} | (0.1,0.9) skill={len(b)} hand={keep(0.1, 0.9)}',
          'OK' if (len(a) == keep(0.05, 0.95) and len(b) == keep(0.1, 0.9)) else 'FAIL')
