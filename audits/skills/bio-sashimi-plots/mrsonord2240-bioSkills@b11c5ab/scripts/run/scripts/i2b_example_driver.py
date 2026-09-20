#!/usr/bin/env python3
"""Input 2b: drive examples/plot_sashimi.py (from the run/skill COPY) on planted + real chrX data, including failure paths.
Run: micromamba run -n as-core python i2b_example_driver.py   (PATH must contain run/bin for the ggsashimi.py shim)."""
import os, sys, subprocess, json, pathlib, shutil, traceback
RUN = pathlib.Path('/mnt/openscience/audits/bio-sashimi-plots/run')
PUB = pathlib.Path('/mnt/openscience/audit-envs/alternative-splicing/public-data')
sys.path.insert(0, str(RUN / 'skill' / 'examples'))
sys.dont_write_bytecode = True
import plot_sashimi as ps  # noqa: E402

W = RUN / 'out' / 'i2b'
shutil.rmtree(W, ignore_errors=True)
W.mkdir(parents=True)
os.chdir(W)
results = {}


def check_labels(svg, region, tsv, M=1):
    r = subprocess.run(['micromamba', 'run', '-n', 'as-core', 'python', str(RUN / 'scripts' / 'jtruth.py'), region, tsv, '--M', str(M), '--svg', svg],
                       capture_output=True, text=True)
    return r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]


# ---- planted
bams = [str(PUB / 'planted' / f) for f in ('G1_rep1.bam', 'G1_rep2.bam', 'G1_rep3.bam', 'G2_rep1.bam', 'G2_rep2.bam', 'G2_rep3.bam')]
ps.create_grouping_file(bams, ['Control'] * 3 + ['Treatment'] * 3, 'planted_groups.tsv')
ps.write_palette(['#1f77b4', '#ff7f0e'], 'palette.txt')
print(open('planted_groups.tsv').read().splitlines()[0])
out = ps.plot_sashimi('planted_groups.tsv', 'chrP:1-1200', 'pl', str(PUB / 'planted' / 'planted.gtf'), options={'palette': 'palette.txt', 'format': 'svg'})
results['planted_svg'] = (out, check_labels('pl.svg', 'chrP:1-1200', 'planted_groups.tsv'))
out = ps.plot_sashimi('planted_groups.tsv', 'chrP:1-1200', 'pl', str(PUB / 'planted' / 'planted.gtf'), options={'palette': 'palette.txt', 'format': 'png', 'width': 6})
results['planted_png'] = out
print('planted:', results['planted_svg'])

# ---- batch on planted rMATS (start = 100-500 < 1)
try:
    ps.batch_plot_rmats_events(str(RUN / 'data/rmats_planted/SE.MATS.JC.txt'), 'planted_groups.tsv', str(PUB / 'planted' / 'planted.gtf'), 'batch_planted')
    results['batch_planted'] = sorted(os.listdir('batch_planted'))
except Exception as e:
    results['batch_planted'] = f'RAISED {type(e).__name__}: {e}'
print('batch planted:', results['batch_planted'])

# ---- real chrX: rMATS chrX vs BAM contig X
rb = [str(PUB / 'rnasplice/bam' / f'{s}.Aligned.out.bam') for s in ('ERR188383', 'ERR188428', 'ERR188454', 'ERR204916')]
ps.create_grouping_file(rb, ['GBR', 'GBR', 'YRI', 'YRI'], 'real_groups.tsv')
gtf = str(PUB / 'rnasplice/reference/genes_chrX.gtf')
print('match_contig(chrX) ->', ps.match_contig(rb, 'chrX'), '| (X) ->', ps.match_contig(rb, 'X'))
try:
    ps.batch_plot_rmats_events(str(RUN / 'data/rmats_real/SE.MATS.JC.txt'), 'real_groups.tsv', gtf, 'batch_real')
    results['batch_real'] = sorted(f'{f} {os.path.getsize("batch_real/" + f)}' for f in os.listdir('batch_real'))
except Exception as e:
    results['batch_real'] = f'RAISED {type(e).__name__}: {e}'
print('batch real:', results['batch_real'])

# labels on one real event via svg (PDZD11, minus strand)
reg = 'chrX:69508604-69510295'
try:
    out = ps.plot_sashimi('real_groups.tsv', reg, 'pdzd11', gtf, options={'palette': 'palette.txt', 'format': 'svg'})
    results['pdzd11_labels'] = check_labels('pdzd11.svg', 'X:69508604-69510295', 'real_groups.tsv')
except Exception as e:
    results['pdzd11_labels'] = f'RAISED {type(e).__name__}: {e}'
print('PDZD11:', results['pdzd11_labels'])

# plot_specific_event (-M 5, -A mean_j -O 3 -C 3)
try:
    r = ps.plot_specific_event('real_groups.tsv', gtf, 'chrX', 69509104, 69509795, 'specific_pdzd11', flank=500)
    results['specific'] = r
except Exception as e:
    results['specific'] = f'RAISED {type(e).__name__}: {e}'
print('specific:', results['specific'])

# ---- failure paths must raise, not silently succeed
fail = {}
for name, args in {
    'bad_contig': ('real_groups.tsv', 'chr99:1-1000', 'f1', gtf),
    'empty_region': ('planted_groups.tsv', 'chrP:2000-2500', 'f2', str(PUB / 'planted/planted.gtf')),
    'bad_region_str': ('planted_groups.tsv', 'chrP-1-1200', 'f3', str(PUB / 'planted/planted.gtf')),
}.items():
    try:
        ps.plot_sashimi(*args)
        fail[name] = 'NO ERROR (silent success)'
    except Exception as e:
        fail[name] = f'{type(e).__name__}: {str(e)[:110]}'
open('missing.tsv', 'w').write(f'a\t{PUB}/planted/G1_rep1.bam\tA\nb\t{PUB}/planted/NOPE.bam\tA\n')
try:
    ps.plot_sashimi('missing.tsv', 'chrP:1-1200', 'f4', str(PUB / 'planted/planted.gtf'))
    fail['missing_bam'] = 'NO ERROR'
except Exception as e:
    fail['missing_bam'] = f'{type(e).__name__}: {str(e)[:110]}'
open('badpal.txt', 'w').write('notacolour\nalsobad\n')
try:
    ps.plot_sashimi('planted_groups.tsv', 'chrP:1-1200', 'f5', str(PUB / 'planted/planted.gtf'), options={'palette': 'badpal.txt'})
    fail['bad_palette'] = 'NO ERROR'
except Exception as e:
    fail['bad_palette'] = f'{type(e).__name__}: {str(e)[:110]}'
# --shrink guard: -M above every junction
try:
    o = ps.plot_sashimi('planted_groups.tsv', 'chrP:1-1200', 'f6', str(PUB / 'planted/planted.gtf'), options={'min_junc': 100, 'format': 'png', 'width': 6})
    fail['shrink_guard_M100'] = f'figure written {o}'
except Exception as e:
    fail['shrink_guard_M100'] = f'{type(e).__name__}: {str(e)[:110]}'
results['failures'] = fail
for k, v in fail.items():
    print('FAIL-PATH', k, '->', v)
json.dump(results, open('results.json', 'w'), indent=1, default=str)
