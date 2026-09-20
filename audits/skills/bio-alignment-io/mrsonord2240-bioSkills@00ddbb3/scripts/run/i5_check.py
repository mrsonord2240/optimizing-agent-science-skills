"""INPUT 5 assertions on the tool outputs written by i5_tools.sh (MrBayes 3.2.7, IQ-TREE 3.1.3, RAxML-NG 2.0.3, PAML codeml 4.10.10) - judged by output text."""
import os, re
from common import *
d = DATA/'e2e'; os.chdir(d)
rd = lambda f: open(f, encoding='utf-8', errors='replace').read()
print('=== MrBayes 3.2.7: NEXUS as the shipped example wrote it (real ids, no recipe) vs after the SKILL recipe')
for f in ['hbb6_example', 'hbb6_recipe', 'globins8_example', 'globins8_recipe']:
    t = rd(f'mb_{f}.out'); done = 'Analysis completed' in t; err = [l.strip() for l in t.splitlines() if 'Error' in l or 'Instead found' in l][:2]
    print(f'{f}: analysis completed={done}; errors={err}')
ok('Analysis completed' in rd('mb_hbb6_recipe.out') and 'datatype=dna' in rd('hbb6_recipe.nex').lower(), 'MrBayes loads the DNA NEXUS produced with the SKILL recipe (datatype=dna) and completes a 200-generation run')
ok('Analysis completed' in rd('mb_globins8_recipe.out') and 'datatype=protein' in rd('globins8_recipe.nex').lower(), 'MrBayes loads the protein NEXUS produced with the SKILL recipe (datatype=protein) and completes a run')
m = re.search(r'Average standard deviation of split frequencies: ([\d.]+)', rd('mb_hbb6_recipe.out')); print('hbb6 recipe run: ASDSF', m.group(1) if m else None)
t = rd('mb_hbb6_example.out'); ok("Unrecognized DNA/RNA character '|'" in t and 'Analysis completed' not in t, "MrBayes REJECTS the NEXUS the shipped example wrote for real NCBI ids ('lcl|NM_000518.5'): \"Unrecognized DNA/RNA character '|'\" (not the quoted-id error the SKILL describes; the SKILL's recipe removes it)")
t = rd('mb_globins8_example.out'); ok("Unrecognized Protein character '|'" in t and 'Analysis completed' not in t, "MrBayes REJECTS the example's NEXUS for real UniProt ids ('sp|P02185|MYG_PHYMC'): Unrecognized Protein character '|'")
ok("'" not in rd('hbb6_example.nex') and "'" not in rd('globins8_example.nex'), "Biopython did NOT quote these '|' ids (so the SKILL's quoted-id explanation does not describe this failure; its replace-everything recipe still fixes it)")
print('=== IQ-TREE 3.1.3 zero-iteration check on the example PHYLIP-relaxed')
t = rd('iq_hbb6.out'); ok('Alignment has 6 sequences with 444 columns' in t, 'IQ-TREE reads hbb6_relaxed.phy (ids with "|"): Alignment has 6 sequences with 444 columns')
t = rd('iq_globins8.out'); ok('Alignment has 8 sequences with 155 columns' in t, 'IQ-TREE reads globins8_relaxed.phy: Alignment has 8 sequences with 155 columns')
print('=== RAxML-NG 2.0.3 --check on PHYLIP-relaxed with "|" in ids')
for f in ['hbb6', 'globins8', 'hbb6_recipe']:
    t = rd(f'rx_{f}.out'); print(f, [l.strip() for l in t.splitlines() if 'ERROR' in l or 'successfully' in l or 'invalid' in l.lower()][:2])
ok('successfully read' in rd('rx_hbb6.out') and 'successfully read' in rd('rx_globins8.out'), 'RAxML-NG accepts Biopython phylip-relaxed with real ids containing "|" and "." (DNA and AA)')
ok('successfully read' in rd('rx_hbb6_recipe.out'), 'RAxML-NG accepts the recipe-sanitised ids too')
print('=== codeml')
for tag in ['seq', 'rel']:
    mlc = rd(f'codeml_{tag}/mlc') if os.path.exists(f'codeml_{tag}/mlc') else ''
    so = rd(f'codeml_{tag}/stdout.txt'); om = re.search(r'omega \(dN/dS\) =\s+([\d.]+)', mlc); ll = re.search(r'lnL\(ntime:[^)]*\):\s+(-[\d.]+)', mlc)
    print(tag, 'omega', om.group(1) if om else None, 'lnL', ll.group(1) if ll else None, '| stdout tail:', so.strip().splitlines()[-1][:120] if so.strip() else '')
mlc = rd('codeml_seq/mlc'); om = re.search(r'omega \(dN/dS\) =\s+([\d.]+)', mlc)
ok(om is not None and 0.05 < float(om.group(1)) < 1.0, f'codeml on phylip-sequential HBB codon alignment: omega {om.group(1) if om else None} (purifying selection, plausible for beta-globin)')
ok('Error in sequence data file' in rd('codeml_rel/stdout.txt') + (rd('codeml_rel/mlc') if os.path.exists('codeml_rel/mlc') else ''), 'codeml rejects the phylip-relaxed file with "Error in sequence data file" (SKILL table row)')
so = rd('codeml_rel/stdout.txt'); print([l for l in so.splitlines() if 'separate' in l or 'Error' in l][:2])
summary()
