#!/usr/bin/env python3
import importlib.util
import json
import pathlib
import shutil
import subprocess

import sys
sys.dont_write_bytecode = True

from Bio import AlignIO, Phylo

ROOT=pathlib.Path('/mnt/openscience/audit-envs/bio-comparative-genomics-ancestral-reconstruction')
CAND=pathlib.Path('/mnt/openscience/wt/opt10-ancestral-reconstruction/skills/bio-comparative-genomics-ancestral-reconstruction')
ENV=ROOT/'conda-env'

def load(name, path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

provider=load('provider', CAND/'scripts/ancestral_reconstruction.py')
extracted=load('extracted', CAND/'scripts/codeml_asr.py')
alignment=AlignIO.read(ROOT/'data/cytochrome-c-aligned.fasta','fasta')
rename={r.id:f'T{i:02d}' for i,r in enumerate(alignment,1)}
for r in alignment: r.id=rename[r.id]; r.name=r.id; r.description=''
tree=Phylo.read(ROOT/'data/cytochrome-c-rooted.nwk','newick')
for t in tree.get_terminals(): t.name=rename[t.name]

results=[]
for label, writer in [('provider', lambda run: provider.write_asr_control('alignment.phy','tree.nwk','mlc',str(run))),
                      ('extracted', lambda run: extracted.write_codeml_ctl('alignment.phy','tree.nwk',str(run),seqtype='protein'))]:
    run=ROOT/'runs'/f'paml-{label}'
    if run.exists(): shutil.rmtree(run)
    run.mkdir(parents=True)
    AlignIO.write(alignment,run/'alignment.phy','phylip-sequential')
    tmp_tree=run/'tree.raw.nwk'
    Phylo.write(tree,tmp_tree,'newick')
    (run/'tree.nwk').write_text(f"8 1\n{tmp_tree.read_text().strip()}\n")
    tmp_tree.unlink()
    shutil.copy2(ENV/'dat/lg.dat',run/'lg.dat')
    ctl=writer(run)
    proc=subprocess.run([ENV/'bin/codeml', pathlib.Path(ctl).name],cwd=run,text=True,capture_output=True,timeout=180)
    rst=run/'rst'
    row={'surface':label,'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,
         'rst_exists':rst.exists(),'mlc_exists':(run/'mlc').exists()}
    if rst.exists():
        row['rst_bytes']=rst.stat().st_size
        row['provider_ancestors']=provider.parse_rst_ancestors(rst)
        row['provider_probabilities']=provider.extract_site_probabilities(rst)
        parsed=extracted.parse_rst_posteriors(rst)
        row['extracted_node_counts']={str(k):len(v) for k,v in parsed.items()}
        row['rst_probability_headers']=sum('Prob distribution at node' in line for line in rst.read_text(errors='replace').splitlines())
    results.append(row)

(ROOT/'evidence/paml-surfaces.json').write_text(json.dumps(results,indent=2,sort_keys=True))
assert all(r['returncode']==0 and r['rst_exists'] and r['mlc_exists'] for r in results)

