"""Fetch the NEW real structures used by inputs 5, 8 and 9 (public RCSB / AlphaFold DB downloads, no authentication).
Windows or WSL python:  python scripts/49_fetch_new_data.py   (cwd = run/)
 - data/new/2HHB.pdb            deoxy human hemoglobin tetramer (second Hb tetramer for the multimer test)
 - data/new/2LZM.pdb, 181L.pdb  T4 lysozyme wild type and L99A point mutant (co-numbered, ~0.2 A)
 - data/new/complexes/*.pdb     60 real X-ray oligomer entries (2-6 protein chains, small) for the Foldseek-Multimer speed test
 - data/new/mse/*.pdb           real entries containing selenomethionine (MSE, a HETATM residue) for the Superimposer edge test
 - data/new/AF-*.pdb            AFDB v6 models of PKA (P17612) and CDK2 (P24941)
"""
import json, os, sys, urllib.request
os.makedirs('data/new/complexes', exist_ok=True); os.makedirs('data/new/mse', exist_ok=True)

def get(url, dest, data=None, headers=None):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return True
    try:
        req = urllib.request.Request(url, data=data, headers=headers or {})
        with urllib.request.urlopen(req, timeout=60) as r:
            open(dest, 'wb').write(r.read())
        return True
    except Exception as e:
        print('FAILED', url, e); return False

def search(query, rows):
    body = json.dumps({'query': query, 'return_type': 'entry', 'request_options': {'paginate': {'start': 0, 'rows': rows}, 'sort': [{'sort_by': 'rcsb_entry_info.resolution_combined', 'direction': 'asc'}]}}).encode()
    req = urllib.request.Request('https://search.rcsb.org/rcsbsearch/v2/query', data=body, headers={'Content-Type': 'application/json'})
    return [x['identifier'] for x in json.load(urllib.request.urlopen(req, timeout=60))['result_set']]

for pid in ('2HHB', '2LZM', '181L'):
    get(f'https://files.rcsb.org/download/{pid}.pdb', f'data/new/{pid}.pdb')
for acc in ('P17612', 'P24941'):
    get(f'https://alphafold.ebi.ac.uk/files/AF-{acc}-F1-model_v6.pdb', f'data/new/AF-{acc}-F1.pdb')

# 60 small oligomers: X-ray, 2-6 protein chains, <= 1500 residues total
q = {'type': 'group', 'logical_operator': 'and', 'nodes': [
    {'type': 'terminal', 'service': 'text', 'parameters': {'attribute': 'exptl.method', 'operator': 'exact_match', 'value': 'X-RAY DIFFRACTION'}},
    {'type': 'terminal', 'service': 'text', 'parameters': {'attribute': 'rcsb_entry_info.deposited_polymer_entity_instance_count', 'operator': 'range', 'value': {'from': 2, 'to': 6, 'include_lower': True, 'include_upper': True}}},
    {'type': 'terminal', 'service': 'text', 'parameters': {'attribute': 'rcsb_entry_info.deposited_polymer_monomer_count', 'operator': 'range', 'value': {'from': 300, 'to': 1500, 'include_lower': True, 'include_upper': True}}},
    {'type': 'terminal', 'service': 'text', 'parameters': {'attribute': 'rcsb_entry_info.nonpolymer_entity_count', 'operator': 'less_or_equal', 'value': 3}},
    {'type': 'terminal', 'service': 'text', 'parameters': {'attribute': 'rcsb_entry_info.polymer_entity_count_nucleic_acid', 'operator': 'equals', 'value': 0}},
]}
ids = search(q, 200)
n = 0
for pid in ids:
    if n >= 60: break
    dest = f'data/new/complexes/{pid}.pdb'
    if get(f'https://files.rcsb.org/download/{pid}.pdb', dest):
        n += 1
print('complexes downloaded:', len(os.listdir('data/new/complexes')))

# selenomethionine entries: MSE HETATM residues inside a single small protein chain
q = {'type': 'group', 'logical_operator': 'and', 'nodes': [
    {'type': 'terminal', 'service': 'text_chem', 'parameters': {'attribute': 'rcsb_chem_comp_container_identifiers.comp_id', 'operator': 'exact_match', 'value': 'MSE'}},
    {'type': 'terminal', 'service': 'text', 'parameters': {'attribute': 'rcsb_entry_info.deposited_polymer_entity_instance_count', 'operator': 'equals', 'value': 1}},
    {'type': 'terminal', 'service': 'text', 'parameters': {'attribute': 'rcsb_entry_info.deposited_polymer_monomer_count', 'operator': 'range', 'value': {'from': 100, 'to': 250, 'include_lower': True, 'include_upper': True}}},
    {'type': 'terminal', 'service': 'text', 'parameters': {'attribute': 'exptl.method', 'operator': 'exact_match', 'value': 'X-RAY DIFFRACTION'}},
]}
try:
    mids = search(q, 6)
except Exception as e:
    print('MSE search failed', e); mids = []
for pid in mids:
    get(f'https://files.rcsb.org/download/{pid}.pdb', f'data/new/mse/{pid}.pdb')
print('mse entries:', mids)
