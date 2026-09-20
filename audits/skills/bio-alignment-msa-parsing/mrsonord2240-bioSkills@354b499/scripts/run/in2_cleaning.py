"""Input 2 (Variant A): 'Remove columns with >50% gaps, drop sequences with too many gaps, remove duplicates, keep IDs matching a
pattern, and save the cleaned alignment.'  REAL Pfam seed + SYNTHETIC syn_small.fasta with hand-known answers."""
import os, re, sys, subprocess, shutil
import numpy as np
from Bio import AlignIO
from common import *
import skill_md_funcs as F

aln = AlignIO.read(PFAM_STO, 'stockholm')
arr = np.array([list(str(r.seq)) for r in aln])
gapfrac = (arr == '-').mean(axis=0)

# 1. remove_gappy_columns on real data vs independent numpy mask
cl = F.remove_gappy_columns(aln, 0.5)
keep = np.flatnonzero(gapfrac < 0.5)
print('real: kept cols', cl.get_alignment_length(), 'of 141; gappy (>=50%) removed:', 141 - cl.get_alignment_length())
check('remove_gappy_columns(0.5): kept column count == numpy mask count', cl.get_alignment_length() == len(keep))
check('remove_gappy_columns: kept column CONTENT identical to arr[:, keep]', all(str(r.seq) == ''.join(arr[i, keep]) for i, r in enumerate(cl)))
check('sequence order and IDs preserved', [r.id for r in cl] == [r.id for r in aln])
check('cleaned alignment is rectangular (all rows same length)', len({len(r.seq) for r in cl}) == 1)
lost = [k for k in aln[0].annotations] 
check('per-record annotations (accession/start/end) survive cleaning [defect if FAIL: new SeqRecord drops annotations]', bool(cl[0].annotations), f"before={list(aln[0].annotations)} after={list(cl[0].annotations)}")
check('column_annotations (GC:seq_cons) survive cleaning [defect if FAIL]', bool(getattr(cl, 'column_annotations', {})), f"before={list(aln.column_annotations)} after={list(cl.column_annotations)}")

# 2. filter_by_gap_content on real
for mx in (0.1, 0.2):
    f = F.filter_by_gap_content(aln, mx)
    ind = [r.id for r in aln if str(r.seq).count('-') / 141 <= mx]
    check(f'filter_by_gap_content({mx}) keeps the same IDs as independent count ({len(ind)} of 73)', [r.id for r in f] == ind)
# Empty result edge: max_gap_fraction=0.0 on real data
try:
    f0 = F.filter_by_gap_content(aln, 0.0)
    print('0.0 ->', len(f0), 'seqs'); 
    try: L = f0.get_alignment_length(); print('len', L)
    except Exception as e: print('get_alignment_length on empty ->', type(e).__name__, e)
    check('filter to zero sequences returns an object without crashing', True, f'{len(f0)} seqs')
except Exception as e:
    check('filter to zero sequences returns an object without crashing', False, f'{type(e).__name__}: {e}')

# 3. remove_duplicates + filter_by_id on SYNTHETIC syn_small (A == E)
syn = AlignIO.read(os.path.join(HERE, 'data', 'syn_small.fasta'), 'fasta')
dd = F.remove_duplicates(syn)
check('SYNTH remove_duplicates drops exactly species_E (exact copy of A)', [r.id for r in dd] == ['species_A', 'species_B', 'species_C', 'species_D'])
fid = F.filter_by_id(syn, r'species_[AB]$')
check('SYNTH filter_by_id regex keeps A,B only', [r.id for r in fid] == ['species_A', 'species_B'])
# real data: duplicates
rd = F.remove_duplicates(aln)
check('REAL remove_duplicates: no exact duplicate rows in Pfam seed (73 kept)', len(rd) == 73)
fh = F.filter_by_id(aln, r'^GLB')
print('IDs starting GLB:', [r.id for r in fh][:5], len(fh))
check('REAL filter_by_id(^GLB) equals independent startswith', [r.id for r in fh] == [r.id for r in aln if r.id.startswith('GLB')])

# 4. SYNTHETIC gappy column hand-check: col 3 (0-based) has gap in A,C,D,E => 4/5 = 0.8 gaps
gp = F.gaps_per_column(syn)
print('gaps per col syn:', gp)
exp = [0,0,0,4,0,0,0,0,0,1,1,0]   # hand: A,C,D,E gap at col3; D gaps at cols 9,10
check('SYNTH gaps_per_column == hand-computed', gp == exp, str(gp))
sc = F.remove_gappy_columns(syn, 0.5)
check('SYNTH remove_gappy_columns(0.5) drops only col 3 => 11 cols', sc.get_alignment_length() == 11 and str(sc[0].seq) == 'MKVLLAAGTWH', str(sc[0].seq))
check('SYNTH find_gappy_columns(0.5) == [3]', F.find_gappy_columns(syn, 0.5) == [3])
# threshold boundary: 0.8 gap fraction column and threshold 0.8 -> removed (>=)
check('boundary: column with gap fraction == threshold is removed (0.8 vs col3)', 3 in F.find_gappy_columns(syn, 0.8) and 3 not in F.find_gappy_columns(syn, 0.81))
ug = F.extract_ungapped_regions(syn, ref_idx=0)   # reference A has gap at col 3
check('SYNTH extract_ungapped_regions(ref=A) drops col 3 => 11 cols; A ungapped', ug.get_alignment_length() == 11 and '-' not in str(ug[0].seq))
ugB = F.extract_ungapped_regions(syn, ref_idx=1)  # B has no gap => keeps everything
check('extract_ungapped_regions(ref=B, no gaps) is identity (12 cols)', ugB.get_alignment_length() == 12)

# 5. shipped example clean_alignment.py from a COPY on real FASTA
ex = os.path.join(HERE, 'ex2'); shutil.rmtree(ex, ignore_errors=True); shutil.copytree(SKILL_EX, ex)
shutil.copy(PFAM_FA, os.path.join(ex, 'alignment.fasta'))
p = subprocess.run([sys.executable, 'clean_alignment.py'], cwd=ex, capture_output=True, text=True, encoding='utf-8', env={**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONDONTWRITEBYTECODE': '1'})
print(p.stdout, p.stderr[-300:])
nseq_after_col = 73
m = re.findall(r'(\d+) sequences, (\d+) columns', p.stdout)
check('clean_alignment.py rc=0 and wrote cleaned_alignment.fasta', p.returncode == 0 and os.path.exists(os.path.join(ex, 'cleaned_alignment.fasta')))
if os.path.exists(os.path.join(ex, 'cleaned_alignment.fasta')):
    out = AlignIO.read(os.path.join(ex, 'cleaned_alignment.fasta'), 'fasta')
    # independent expected: column trim @0.5 then drop seqs with >20% gaps in the trimmed alignment
    trimmed = arr[:, keep]
    exp_ids = [aln[i].id for i in range(73) if (trimmed[i] == '-').mean() <= 0.2]
    print('example output shape', len(out), out.get_alignment_length(), '| expected', len(exp_ids), len(keep))
    check('clean_alignment.py output shape/IDs == independent pipeline (col trim 0.5 then seq gap<=0.2)', [r.id for r in out] == exp_ids and out.get_alignment_length() == len(keep))
summary()
