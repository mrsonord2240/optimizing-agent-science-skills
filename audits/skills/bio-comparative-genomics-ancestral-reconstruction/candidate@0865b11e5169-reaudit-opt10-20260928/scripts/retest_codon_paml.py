import importlib.util
import json
import pathlib
import subprocess
import sys

sys.dont_write_bytecode = True
root = pathlib.Path('/mnt/openscience/audit-envs/bio-comparative-genomics-ancestral-reconstruction')
cand = pathlib.Path('/mnt/openscience/wt/opt10-ancestral-reconstruction/skills/bio-comparative-genomics-ancestral-reconstruction')
out = pathlib.Path('/mnt/openscience/audits/bio-comparative-genomics-ancestral-reconstruction/reaudit-opt10-20260928/evidence')
run = out / 'codon-paml'
run.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(cand / 'scripts'))

from Bio import AlignIO, Phylo
from Bio.Seq import Seq
from Bio.Data import CodonTable

spec = importlib.util.spec_from_file_location('codeml_candidate', cand / 'scripts/codeml_asr.py')
codeml = importlib.util.module_from_spec(spec); spec.loader.exec_module(codeml)
alignment = AlignIO.read(root / 'data/cytochrome-c-aligned.fasta', 'fasta')
tree = Phylo.read(root / 'data/cytochrome-c-rooted.nwk', 'newick')
codon_table = CodonTable.unambiguous_dna_by_name['Standard']
codons_by_aa = {}
for codon, aa in codon_table.forward_table.items(): codons_by_aa.setdefault(aa, []).append(codon)
name_map = {}
for i, record in enumerate(alignment, 1):
    old = record.id
    name_map[old] = f'T{i:02d}'
    codons = []
    for site, aa in enumerate(str(record.seq).upper()):
        if aa == '-':
            codons.append('---')
            continue
        if aa not in codons_by_aa:
            raise ValueError(f'No codon mapping for residue {aa!r} in {old}')
        choices = sorted(codons_by_aa[aa])
        codons.append(choices[(i + site) % len(choices)])
    record.id = name_map[old]; record.name = record.id; record.description = ''
    record.seq = Seq(''.join(codons))
for tip in tree.get_terminals():
    tip.name = name_map[tip.name]
for node in tree.find_clades():
    if node.branch_length is not None and node.branch_length < 0.005:
        node.branch_length = 0.005
aln_path = run / 'alignment.phy'
AlignIO.write(alignment, aln_path, 'phylip-sequential')
tree_text = (run / 'tree.raw.nwk')
Phylo.write(tree, tree_text, 'newick')
(run / 'tree.nwk').write_text(f'8 1\n{tree_text.read_text().strip()}\n', encoding='ascii')
tree_text.unlink()
(run / 'tree.nwk').write_text((run / 'tree.nwk').read_text().replace('\n', '\n'), encoding='ascii')

env = root / 'conda-env'
codeml.write_codeml_ctl('alignment.phy', 'tree.nwk', str(run), seqtype='codon')
ctl = run / 'codeml.ctl'
# The candidate writes absolute output paths but relative input names; PAML runs in the fixture directory.
proc = subprocess.run([str(env / 'bin/codeml'), ctl.name], cwd=run, text=True,
                      capture_output=True, timeout=300)
rst = run / 'rst'
if proc.returncode != 0 or not rst.exists():
    raise RuntimeError(f'codeml failed: rc={proc.returncode}; stdout={proc.stdout}; stderr={proc.stderr}')
try:
    parsed = codeml.parse_rst_posteriors(rst)
except Exception as exc:
    first_row = next((line for line in rst.read_text(encoding='utf-8', errors='replace').splitlines()
                      if line.lstrip().startswith('1      1')), None)
    result = {'status':'FAIL_REAL_CODON_RST_PARSER', 'paml_version':'4.10.10',
              'codeml_returncode':proc.returncode, 'rst_bytes':rst.stat().st_size,
              'parser_error':f'{type(exc).__name__}: {exc}', 'first_codon_marginal_row':first_row,
              'stdout':proc.stdout, 'stderr':proc.stderr}
else:
    assert len(parsed) == 7 and all(len(rows) == 110 for rows in parsed.values())
    result = {'status':'PASS_REAL_CODON_RST', 'paml_version':'4.10.10', 'returncode':proc.returncode,
              'rst_bytes':rst.stat().st_size, 'nodes':len(parsed), 'sites_per_node':110,
              'probability_records':sum(map(len, parsed.values())),
              'state_widths':sorted({len(row['state']) for rows in parsed.values() for row in rows}),
              'stdout':proc.stdout, 'stderr':proc.stderr}
(out / 'paml-codon-results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
