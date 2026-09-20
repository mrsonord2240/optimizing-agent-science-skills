"""Input 2 (Variant A, regression of first-audit input 2): 'Clean this alignment: drop columns that are 50% gaps or more, drop
sequences with more than 20% gaps, remove exact duplicates, keep only IDs starting with GLB, and save the cleaned alignment.
Keep the Stockholm annotations.'
REAL Pfam PF00042 seed (73 x 141, has record annotations accession/start/end, GC seq_cons, GR pAS/active_site) + a SYNTHETIC 5 x 12
protein alignment with hand-computed gaps. Code = SKILL.md blocks exec'd from the file; clean_alignment.py run from the copy."""
import io, os, subprocess, sys
from collections import Counter
import numpy as np
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from common import *
import skillns

ns, log = skillns.load()
aln = AlignIO.read(PFAM_STO, 'stockholm')
raw = {}
for line in open(PFAM_STO, encoding='utf-8'):
    if line.startswith('#') or line.startswith('//') or not line.strip(): continue
    n, s = line.split(); raw[n] = s
arr = np.array([list(s) for s in raw.values()]); isgap = arr == '.'
N, L = arr.shape

# ---- remove_gappy_columns vs independent mask -------------------------------------------------------------------------
keep = [j for j in range(L) if isgap[:, j].mean() < 0.5]
cl = ns['remove_gappy_columns'](aln, 0.5)
print(f'kept {cl.get_alignment_length()} of {L} columns (independent mask keeps {len(keep)})')
check('remove_gappy_columns(0.5): same columns as an independent mask, content identical to raw-file columns',
      cl.get_alignment_length() == len(keep) == 118 and all(str(r.seq).upper().replace('.', '-') == ''.join(arr[i, keep]).replace('.', '-') for i, r in enumerate(cl)))
check('sequence order and IDs preserved; alignment is rectangular', [r.id for r in cl] == [r.id for r in aln] and len({len(r.seq) for r in cl}) == 1)

# ---- annotations survive (the first audit's FAIL) ---------------------------------------------------------------------------
before_rec = aln[0].annotations
print('record annotations before/after:', dict(aln[0].annotations), dict(cl[0].annotations))
check('per-record annotations (accession/start/end) survive cleaning, for all 73 records', all(dict(a.annotations) == dict(b.annotations) and len(b.annotations) >= 3 for a, b in zip(aln, cl)))
gc = aln.column_annotations
print('column_annotations keys:', list(gc), '->', list(cl.column_annotations))
check('column annotation GC seq_cons survives and equals the ORIGINAL string sliced at the kept columns',
      list(cl.column_annotations) == list(gc) and all(cl.column_annotations[k] == ''.join(gc[k][j] for j in keep) for k in gc))
la_keys = {k for r in aln for k in r.letter_annotations}
print('letter_annotation keys on the real seed:', la_keys)
ok_la = True
for a, b in zip(aln, cl):
    for k, v in a.letter_annotations.items():
        want = ''.join(v[j] for j in keep) if isinstance(v, str) else [v[j] for j in keep]
        ok_la &= (b.letter_annotations.get(k) == want)
check('letter_annotations (GR lines) sliced to the kept columns for every record that has them', ok_la and len(la_keys) > 0, str(la_keys))
buf = io.StringIO(); AlignIO.write(cl, buf, 'stockholm'); out = buf.getvalue()
buf0 = io.StringIO(); AlignIO.write(aln, buf0, 'stockholm'); out0 = buf0.getvalue()
back = AlignIO.read(io.StringIO(out), 'stockholm'); back0 = AlignIO.read(io.StringIO(out0), 'stockholm')
cnt = lambda t, tag: sum(l.startswith(tag) for l in t.splitlines())
print(f'Stockholm write, ORIGINAL vs CLEANED: #=GS {cnt(out0, "#=GS")}/{cnt(out, "#=GS")}, #=GR {cnt(out0, "#=GR")}/{cnt(out, "#=GR")}, #=GC {cnt(out0, "#=GC")}/{cnt(out, "#=GC")}')
print("NOTE (Biopython 1.88 writer, see probes/probe_sto_roundtrip.py): the Pfam-specific tags GC seq_cons and GR pAS are held in memory but the Stockholm WRITER drops them for the uncleaned alignment too.")
act0 = {r.id: r.letter_annotations['active_site'] for r in back0 if 'active_site' in r.letter_annotations}
act1 = {r.id: r.letter_annotations['active_site'] for r in back if 'active_site' in r.letter_annotations}
check('written Stockholm after cleaning loses nothing that Biopython writes for the ORIGINAL: same #=GS/#=GR counts, active_site GR line present and sliced to the kept columns; 73 x 118 on re-read',
      cnt(out, '#=GS') == cnt(out0, '#=GS') and cnt(out, '#=GR') == cnt(out0, '#=GR') >= 1 and back.get_alignment_length() == 118
      and set(act0) == set(act1) and all(act1[k] == ''.join(act0[k][j] for j in keep) for k in act0), f'{len(act1)} record(s) with active_site')

# ---- sequence filters -----------------------------------------------------------------------------------------------------
fr = isgap.mean(1)
kept20 = [i for i in range(N) if fr[i] <= 0.2]
f20 = ns['filter_by_gap_content'](aln, 0.2)
check('filter_by_gap_content(0.2) keeps the same IDs as independent (44 of 73)', [r.id for r in f20] == [list(raw)[i] for i in kept20] and len(f20) == 44)
try:
    ns['filter_by_gap_content'](aln, 0.0); raised = None
except ValueError as e:
    raised = str(e)
print('filter_by_gap_content(0.0) ->', raised)
check('over-strict filter raises ValueError naming the threshold and the lowest gap fraction (was an empty alignment)',
      raised is not None and 'max_gap_fraction=0.0' in raised and f'{fr.min():.2f}' in raised and 'removes all 73' in raised)
try:
    ns['filter_by_id'](aln, '^zzz'); r2 = None
except ValueError as e:
    r2 = str(e)
check("filter_by_id('^zzz') raises ValueError instead of returning an empty alignment", r2 is not None and 'removes all 73' in r2, r2)
glb = ns['filter_by_id'](aln, '^GLB')
check('filter_by_id(^GLB) == independent startswith (32 IDs)', [r.id for r in glb] == [n for n in raw if n.startswith('GLB')] and len(glb) == 32)
check('filtered alignment keeps column_annotations and per-record annotations', glb.column_annotations == aln.column_annotations and all(g.annotations == a.annotations for g, a in zip(glb, [r for r in aln if r.id.startswith('GLB')])))
try:
    ns['filter_by_id'](aln, '['); rx = None
except Exception as e:
    rx = type(e).__name__
check('malformed user regex "[" fails loudly (re.error), no silent empty result', rx == 'error', str(rx))
dup = ns['remove_duplicates'](aln)
check('remove_duplicates on the real seed keeps all 73 (no exact duplicates; independent set count)', len(dup) == 73 == len({s for s in raw.values()}))

# ---- synthetic 5 x 12 with hand-known answers ---------------------------------------------------------------------------------
syn_txt = """MKV-LLAAGTWH
MKVALLAAGTWH
MKI-LLSAGTWQ
MRV-LLAAG--H
MKV-LLAAGTWH
"""
ids = ['species_A', 'species_B', 'species_C', 'species_D', 'species_E']
syn = MultipleSeqAlignment([SeqRecord(Seq(s), id=i, description='') for i, s in zip(ids, syn_txt.split())])
# hand: gaps per column = col3 four gaps (A,C,D,E), col9 one (D), col10 one (D); species_D has 3 gaps of 12
check('SYNTH gaps_per_column == hand-computed [0,0,0,4,0,0,0,0,0,1,1,0]', ns['gaps_per_column'](syn) == [0, 0, 0, 4, 0, 0, 0, 0, 0, 1, 1, 0])
c5 = ns['remove_gappy_columns'](syn, 0.5)
check('SYNTH remove_gappy_columns(0.5) drops only column 3 (4/5 gaps) and col 9,10 stay (1/5): 11 columns, row A = MKVLLAAGTWH', c5.get_alignment_length() == 11 and str(c5[0].seq) == 'MKVLLAAGTWH')
check('SYNTH boundary: a column with gap fraction exactly equal to the threshold is removed (0.8 threshold removes col 3)', ns['find_gappy_columns'](syn, 0.8) == [3] and ns['find_gappy_columns'](syn, 0.81) == [])
check('SYNTH remove_duplicates drops exactly species_E', [r.id for r in ns['remove_duplicates'](syn)] == ids[:4])
check('SYNTH extract_ungapped_regions(ref=species_A) drops column 3 only', ns['extract_ungapped_regions'](syn, 0).get_alignment_length() == 11)
check('SYNTH filter_by_gap_content(0.2): D (3/12 = 0.25 gaps) and A,C,E (1/12) -> A,B,C,E kept', [r.id for r in ns['filter_by_gap_content'](syn, 0.2)] == ['species_A', 'species_B', 'species_C', 'species_E'])

# ---- shipped clean_alignment.py from the copy, on the real .sto ---------------------------------------------------------------
work = os.path.join(DATA, 'in2_work'); os.makedirs(work, exist_ok=True)
p = subprocess.run([sys.executable, os.path.join(EX, 'clean_alignment.py'), PFAM_STO], cwd=work, capture_output=True, text=True,
                   env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONIOENCODING': 'utf-8'})
print(p.stdout, p.stderr[-300:])
written = AlignIO.read(os.path.join(work, 'cleaned_alignment.fasta'), 'fasta')
exp_ids = [list(raw)[i] for i in range(N) if (isgap[i, keep].mean() <= 0.2)]
check('clean_alignment.py rc 0; output FASTA equals the independent pipeline (columns < 50% gaps, then rows <= 20% gaps): IDs and sequences',
      p.returncode == 0 and [r.id for r in written] == exp_ids and all(str(r.seq) == ''.join(arr[list(raw).index(r.id), keep]).replace('.', '-') for r in written),
      f'{len(written)} x {written.get_alignment_length()}')
check("clean_alignment.py output FASTA uses '-' gaps only (no '.')", all('.' not in str(r.seq) for r in written))
summary()
