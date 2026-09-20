"""INPUT 4b (Variant B cont., regression + probes of the SKILL A2M / A3M section). REAL hmmalign A2M + REAL reformat.pl A3M/A2M from i4b_a2m.sh."""
import io, os, re
import pyhmmer
from Bio import AlignIO, SeqIO, Align
from common import *
d = DATA/'a2m'; os.chdir(d)
def rows(p):
    out, cur = {}, None
    for l in open(p):
        l = l.rstrip('\n')
        if l.startswith('>'): cur = l[1:].split()[0]; out[cur] = ''
        else: out[cur] += l
    return out
print('--- A. real hmmalign A2M is ragged (SKILL: ValueError on AlignIO fasta read)')
h = rows('globins_hmm.a2m'); print('row lengths', sorted(set(len(v) for v in h.values())), '| any "." padding:', any('.' in v for v in h.values()))
ok(len(set(len(v) for v in h.values())) > 1, 'hmmalign A2M rows have unequal lengths (ragged)')
try: AlignIO.read('globins_hmm.a2m', 'fasta'); ok(False, 'AlignIO.read ragged A2M unexpectedly worked')
except ValueError as e: ok('same length' in str(e), f'AlignIO.read(..., "fasta") -> ValueError: {e}')
print('--- B. SKILL SeqIO match-column snippet (verbatim), on ragged hmmalign A2M and on padded A2M')
code = block('A2M / A3M Conventions')
def run_snip(path):
    ns = {}; exec(code.replace("'hits.a2m'", repr(path)), ns); return ns['match_only_seqs']
m = run_snip('globins_hmm.a2m')
ok(len(m) == 8 and all(len(v) == 117 for v in m.values()), f'ragged hmmalign A2M: {len(m)} rows, match-column lengths {sorted(set(len(v) for v in m.values()))} == HMM LENG 117')
p = rows('pf.a2m'); ok(len(set(len(v) for v in p.values())) == 1, 'reformat.pl a3m->a2m output is rectangular (padded)')
pa = AlignIO.read('pf.a2m', 'fasta'); ok((len(pa), pa.get_alignment_length()) == (73, len(next(iter(p.values())))), f'padded A2M loads with AlignIO fasta: {len(pa)}x{pa.get_alignment_length()}')
m2 = run_snip('pf.a2m'); nm = sum(1 for c in next(iter(rows('pf.a3m').values())) if c.isupper() or c == '-')
ok(set(len(v) for v in m2.values()) == {nm}, f'padded A2M: all 73 rows reduce to {nm} match columns (= first A3M record match states)')
try: aa = Align.read('pf.a2m', 'a2m'); ok(aa.shape == (73, pa.get_alignment_length()), f'Align.read(padded A2M, "a2m") shape {aa.shape}')
except Exception as e: ok(False, f'Align.read padded a2m: {type(e).__name__}: {str(e)[:100]}')
try: ar = Align.read('globins_hmm.a2m', 'a2m'); print('Align.read(ragged hmmalign a2m) ->', ar.shape)
except Exception as e: print('Align.read(ragged hmmalign a2m) ->', type(e).__name__, str(e)[:100])
print('--- C. A3M has no reader in AlignIO / Bio.Align / pyhmmer (format table row)')
ok('a3m' not in Align.formats, 'a3m not in Bio.Align.formats: ' + str(Align.formats))
try: AlignIO.read('pf.a3m', 'a3m'); ok(False, 'AlignIO a3m worked')
except ValueError as e: ok('Unknown format' in str(e), f'AlignIO.read(..., "a3m") -> {e}')
try:
    with pyhmmer.easel.MSAFile('pf.a3m', format='a3m', digital=True) as f: f.read()
    ok(False, 'pyhmmer a3m worked')
except Exception as e: ok(True, f'pyhmmer format="a3m" -> {type(e).__name__}: {str(e)[:100]}')
with pyhmmer.easel.MSAFile('globins_hmm.a2m', format='a2m', digital=True) as f: mm = f.read()
ok(len(mm.sequences) == 8, f'pyhmmer reads real hmmalign A2M (format="a2m"): {len(mm.sequences)} sequences')
print('--- D. reformat.pl first-record pitfall (SKILL: first record is the match reference; different first record gives different padding)')
a_orig, a_re = rows('pf.a2m'), rows('pf_reordered.a2m')
common_ids = [k for k in a_orig if k in a_re]
diff = sum(1 for k in common_ids if a_orig[k] != a_re[k]); print('rows whose A2M differs after reordering:', diff, 'of', len(common_ids))
a3_same = all(rows('pf.a3m')[k] == rows('pf_reordered.a3m')[k] for k in rows('pf.a3m'))
ok(a3_same, 'the reordered A3M has byte-identical rows (only record order changed)')
letters = sum(1 for k in common_ids for x, y in zip(a_orig[k], a_re[k]) if x != y and not (x in '.-' and y in '.-'))
ok(diff > 0 and letters > 0, f'moving another record to first position changes the A2M residues (not just padding): {letters} residue positions differ (pitfall is real)')
print('--- E. SKILL: "hhfilter does not reorder records, so it is not a fix" (probe)')
o_ids = list(rows('pf_reordered.a3m')); f_ids = list(rows('pf_reordered_hhf.a3m'))
print('reordered a3m first id:', o_ids[0], '| after hhfilter -id 100 first id:', f_ids[0], '| records before/after:', len(o_ids), len(f_ids))
ok(o_ids[0] == f_ids[0], 'hhfilter keeps the first record in first position (no reordering)')
kept = [i for i in o_ids if i in f_ids]; ok(kept == f_ids, 'hhfilter output order is a subsequence of the input order (no reordering); it may drop records')
summary()
