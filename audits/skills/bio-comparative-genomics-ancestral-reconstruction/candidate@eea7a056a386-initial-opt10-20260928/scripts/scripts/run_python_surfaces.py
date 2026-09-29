#!/usr/bin/env python3
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

ROOT = pathlib.Path('/mnt/openscience/audit-envs/bio-comparative-genomics-ancestral-reconstruction')
CAND = pathlib.Path('/mnt/openscience/wt/opt10-ancestral-reconstruction/skills/bio-comparative-genomics-ancestral-reconstruction')

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

provider = load('provider_asr', CAND/'scripts/ancestral_reconstruction.py')
codeml = load('codeml_asr', CAND/'scripts/codeml_asr.py')
iqstate = load('iqtree_state', CAND/'scripts/iqtree_state.py')
results = []

def record(name, status, **detail):
    results.append({'name': name, 'status': status, **detail})

demo = subprocess.run([sys.executable, str(CAND/'scripts/ancestral_reconstruction.py')], text=True, capture_output=True)
record('provider_demo', 'PASS' if demo.returncode == 0 and 'Reconstruction Quality: POOR' in demo.stdout else 'FAIL', returncode=demo.returncode, stdout=demo.stdout, stderr=demo.stderr)

with tempfile.TemporaryDirectory(dir=ROOT/'runs') as td:
    td = pathlib.Path(td)
    ctl = provider.write_asr_control('protein.phy', 'tree.nwk', 'asr.mlc', str(td))
    text = pathlib.Path(ctl).read_text()
    record('provider_control_writer', 'PASS' if 'RateAncestor = 1' in text and 'seqtype = 2' in text else 'FAIL', control=text)
    codon_ctl = codeml.write_codeml_ctl('codon.phy', 'tree.nwk', str(td), seqtype='codon')
    codon_text = pathlib.Path(codon_ctl).read_text()
    aa_ctl = codeml.write_codeml_ctl('protein.phy', 'tree.nwk', str(td), seqtype='protein')
    aa_text = pathlib.Path(aa_ctl).read_text()
    record('codeml_control_writer', 'PASS' if 'seqtype = 1' in codon_text and 'seqtype = 2' in aa_text else 'FAIL')

rst = ROOT/'data/parser-fixture.rst'
rst.write_text('''Prob distribution at node 9, by site\n  1 AAA: A(0.999) C(0.001)\n  2 CCC: C(0.750) T(0.250)\nProb distribution at node 10, by site\n  1 AAA: A(0.950) C(0.050)\n\nList of extant and reconstructed sequences\nnode #9\nAC\nnode #10\nAT\n''')
parsed = codeml.parse_rst_posteriors(rst)
summary = codeml.summarize_node_confidence(parsed)
record('codeml_parser_documented_fixture', 'PASS' if len(parsed) == 2 and summary[9]['n_ambiguous'] == 1 else 'FAIL', parsed=dict(parsed), summary=summary)
provider_anc = provider.parse_rst_ancestors(rst)
provider_probs = provider.extract_site_probabilities(rst)
record('provider_parser_documented_fixture', 'OBSERVED', ancestors=provider_anc, site_probabilities=provider_probs, note='fixture follows PAML-style A(probability) rows')

quality = provider.assess_reconstruction_quality([
    {'site': 1, 'state': 'A', 'probability': 0.95},
    {'site': 2, 'state': 'C', 'probability': 0.80},
    {'site': 3, 'state': 'G', 'probability': 0.79},
])
record('provider_threshold_boundaries', 'OBSERVED', quality=quality)
try:
    provider.summarize_asr_results({}, provider.assess_reconstruction_quality([]), [])
    empty = 'accepted'
except Exception as exc:
    empty = f'{type(exc).__name__}: {exc}'
record('provider_empty_probability_contract', 'OBSERVED', outcome=empty)

state = ROOT/'data/iqtree-parser-valid.state'
state.write_text('# comment\nNode\tSite\tState\tp_A\tp_C\tp_G\tp_T\nNode1\t1\tA\t0.97\t0.01\t0.01\t0.01\nNode1\t2\tC\t0.1\t0.7\t0.1\t0.1\n')
groups = iqstate.load_iqtree_state(state)
frame = groups.get_group('Node1')
record('iqtree_state_parser_valid', 'PASS' if list(frame.max_post) == [0.97, 0.7] else 'FAIL', columns=list(frame.columns), max_post=list(frame.max_post))

bad = ROOT/'data/iqtree-parser-no-probabilities.state'
bad.write_text('Node\tSite\tState\nNode1\t1\tA\n')
try:
    bad_groups = iqstate.load_iqtree_state(bad)
    bad_frame = bad_groups.get_group('Node1')
    bad_outcome = {'accepted': True, 'max_post': [None if str(x) == 'nan' else float(x) for x in bad_frame.max_post]}
except Exception as exc:
    bad_outcome = {'accepted': False, 'error': f'{type(exc).__name__}: {exc}'}
record('iqtree_state_parser_missing_probability_columns', 'OBSERVED', outcome=bad_outcome)

(ROOT/'evidence/python-surfaces.json').write_text(json.dumps(results, indent=2, sort_keys=True))
assert all(r['status'] != 'FAIL' for r in results)

