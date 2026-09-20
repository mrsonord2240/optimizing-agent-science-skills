"""Input 5c (Stress, real data): SKILL's PAML claim. Alignment of 6 real HBB CDS (MAFFT) -> AlignIO -> phylip-sequential / phylip-relaxed -> run codeml M0 (WSL) and compare."""
import pathlib, subprocess, sys, re, shutil
from Bio import AlignIO
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m)
here = pathlib.Path(__file__).parent; d = here/'data'
aln = AlignIO.read(d/'hbb6_aln.fa', 'fasta'); L = aln.get_alignment_length()
print('alignment', len(aln), 'x', L, '| multiple of 3:', L % 3 == 0)
print('--- A. SKILL route with the ORIGINAL NCBI ids (what a user has): write phylip-sequential')
try:
    AlignIO.write(aln, d/'hbb_long.phy', 'phylip-sequential'); ok(True, 'written')
except Exception as e:
    ok(False, f'phylip-sequential with real NCBI headers: {type(e).__name__}: {e}')
print('--- B. ids shortened by me (human, chimp, cow, pig, macaque, horse) then write both layouts')
names = ['human', 'chimp', 'cow', 'pig', 'macaque', 'horse']
for r, n in zip(aln, names): r.id = n; r.name = n; r.description = ''
AlignIO.write(aln, d/'hbb_seq.phy', 'phylip-sequential'); AlignIO.write(aln, d/'hbb_rel.phy', 'phylip-relaxed')
print(open(d/'hbb_seq.phy').read()[:120].replace('\n', ' | '))
print(open(d/'hbb_rel.phy').read()[:120].replace('\n', ' | '))
# star-ish user tree
tree = '((human,chimp),macaque,((cow,pig),horse));'
PASS = sys.argv[1] if len(sys.argv) > 1 else '1'
for tag in ['seq', 'rel']:
    w = d/f'codeml_{tag}'
    if PASS == '2': pass
    else: shutil.rmtree(w, ignore_errors=True); w.mkdir()
    if PASS == '1': shutil.copy(d/f'hbb_{tag}.phy', w/'aln.phy'); (w/'tree.nwk').write_text(tree+'\n')
    (w/'codeml.ctl').write_text('seqfile = aln.phy\ntreefile = tree.nwk\noutfile = mlc\nnoisy = 0\nverbose = 0\nrunmode = 0\nseqtype = 1\nCodonFreq = 2\nmodel = 0\nNSsites = 0\nicode = 0\nfix_kappa = 0\nkappa = 2\nfix_omega = 0\nomega = 0.4\ncleandata = 0\n', encoding='utf-8')
    (w/'run.sh').write_text('cd /mnt/openscience/audits/bio-alignment-io/run/data/codeml_%s\ncodeml codeml.ctl </dev/null > stdout.txt 2>&1\ntail -3 stdout.txt\n' % tag, encoding='utf-8', newline='\n')
    # codeml is run by i5c_run_codeml.sh (WSL); this script only prepares inputs (pass 1) and parses mlc (pass 2)
    mlc = w/'mlc'
    if mlc.exists():
        t = mlc.read_text(errors='replace'); m = re.search(r'omega \(dN/dS\) =\s+([\d.]+)', t); l = re.search(r'lnL\(ntime:.*?\):\s+(-[\d.]+)', t)
        print(f'[{tag}] omega={m.group(1) if m else None} lnL={l.group(1) if l else None}')
        globals()[f'res_{tag}'] = (m.group(1) if m else None)
    else: print(f'[{tag}] no mlc output'); globals()[f'res_{tag}'] = None
ok(res_seq is not None, f'codeml on phylip-sequential produced omega={res_seq}')
ok(res_rel is not None, f'codeml on phylip-relaxed produced omega={res_rel} (SKILL claims codeml fails with relaxed: "cannot read sequences")')
