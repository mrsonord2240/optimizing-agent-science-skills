import importlib.util
import json
import pathlib
import sys

sys.dont_write_bytecode = True
root = pathlib.Path('/mnt/openscience/audit-envs/bio-comparative-genomics-ancestral-reconstruction')
cand = pathlib.Path('/mnt/openscience/wt/opt10-ancestral-reconstruction/skills/bio-comparative-genomics-ancestral-reconstruction')
out = pathlib.Path('/mnt/openscience/audits/bio-comparative-genomics-ancestral-reconstruction/reaudit-opt10-20260928/evidence')
sys.path.insert(0, str(cand / 'scripts'))

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

provider = load('provider', cand / 'scripts/ancestral_reconstruction.py')
codeml = load('codeml', cand / 'scripts/codeml_asr.py')
iqtree = load('iqtree', cand / 'scripts/iqtree_state.py')
checks = []

for label in ('provider', 'extracted'):
    rst = root / f'runs/paml-{label}/rst'
    ancestors = provider.parse_rst_ancestors(rst)
    probabilities = provider.extract_site_probabilities(rst)
    nodes = codeml.parse_rst_posteriors(rst)
    assert len(ancestors) == 7 and all(len(s) == 110 for s in ancestors.values())
    assert len(probabilities) == 770 and len(nodes) == 7
    assert all(len(sites) == 110 for sites in nodes.values())
    checks.append({'surface': f'real_paml_{label}_protein_rst', 'nodes': len(ancestors),
                   'sites_per_node': 110, 'probability_records': len(probabilities), 'status': 'PASS'})

quality = provider.assess_reconstruction_quality([])
summary = provider.summarize_asr_results({}, quality, [])
assert quality['status'] == 'no_data' and quality['total_sites'] == 0
checks.append({'surface': 'empty_no_data_summary', 'status': 'PASS', 'quality': quality, 'summary': summary})

state = root / 'runs/iqtree-candidate/asr_iqtree.state'
groups = iqtree.load_iqtree_state(state)
all_rows = sum(len(frame) for _, frame in groups)
assert all_rows == 660 and len(groups) == 6
checks.append({'surface': 'real_iqtree_state', 'status': 'PASS', 'rows': all_rows,
               'nodes': len(groups), 'columns': list(groups.get_group('Node1').columns)})

fixtures = {
    'missing_columns': 'Node\tSite\tState\nNode1\t1\tA\n',
    'empty': 'Node\tSite\tState\tp_A\tp_C\n',
    'bad_sum': 'Node\tSite\tState\tp_A\tp_C\nNode1\t1\tA\t0.7\t0.1\n',
    'bad_argmax': 'Node\tSite\tState\tp_A\tp_C\nNode1\t1\tC\t0.9\t0.1\n',
    'nan': 'Node\tSite\tState\tp_A\tp_C\nNode1\t1\tA\tnan\t0.1\n',
}
for label, content in fixtures.items():
    path = out / f'iqtree-{label}.state'
    path.write_text(content, encoding='utf-8')
    try:
        iqtree.load_iqtree_state(path)
    except ValueError as exc:
        checks.append({'surface': f'iqtree_reject_{label}', 'status': 'PASS', 'error': str(exc)})
    else:
        raise AssertionError(f'IQ-TREE parser accepted malformed {label} fixture')

demo = __import__('subprocess').run([sys.executable, str(cand / 'scripts/ancestral_reconstruction.py')],
                                    capture_output=True, text=True)
assert demo.returncode == 0 and 'Reconstruction Quality: POOR' in demo.stdout
checks.append({'surface': 'shipped_python_demo', 'status': 'PASS', 'returncode': demo.returncode,
               'simulated_demo_output': demo.stdout, 'stderr': demo.stderr})
(out / 'python-results.json').write_text(json.dumps(checks, indent=2), encoding='utf-8')
print(json.dumps(checks, indent=2))
