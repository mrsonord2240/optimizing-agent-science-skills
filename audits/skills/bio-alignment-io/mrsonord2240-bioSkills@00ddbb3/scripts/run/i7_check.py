"""INPUT 7 assertions on the tool outputs written by i7_tools.sh (RAxML-NG 1.2.2 + 2.0.3, PhyML 3.3.20260528 + 3.3.20220408, IQ-TREE 3.1.3, MrBayes 3.2.7).
Each claim of the round-2 SKILL ('PHYLIP-Relaxed Dialect Mismatches' table, IQ-TREE paragraph, MrBayes paragraph, Version line) is judged by output text."""
import os, re
from common import *
d = DATA/'tools'; os.chdir(d)
rd = lambda f: open(f, encoding='utf-8', errors='replace').read()
print('=== Row 1 (corrected): RAxML-NG "*" in a nucleotide alignment -> Invalid character ...: *  ; protein accepts "*" as undetermined')
for v, name in [('1', '1.2.2'), ('2', '2.0.3')]:
    t = rd(f'a7_rxd{v}.out'); ok(re.search(r'ERROR: Invalid character in sequence 5 at position 4: \*', t) is not None, f'RAxML-NG {name} DNA + "*": {[l for l in t.splitlines() if "Invalid" in l][:1]}')
    ll = {k: re.search(r'Final LogLikelihood: (-[\d.]+)', rd(f'a7_rxs{v}_pf12_star{k}.out')) for k in ['', '_dash', '_X']}
    ok(all(ll.values()), f'RAxML-NG {name} protein --search1 with "*" completes: lnL {ll[""].group(1) if ll[""] else None}')
    ok(ll[''] and ll['_dash'] and ll['_X'] and ll[''].group(1) == ll['_dash'].group(1) == ll['_X'].group(1), f'RAxML-NG {name}: lnL with "*" == with "-" == with "X" ({[m.group(1) for m in ll.values()]}) -> "*" is treated as undetermined and not scored (SKILL parenthetical)')
print('=== Row 3 (replaced): PhyML rejects ":" and "," ; accepts "(" ")" and writes them into the Newick; 138-char names kept')
ok("Character ':' is not permitted in sequence name (GLB:1)" in rd('a7_ph_colon.out'), 'PhyML 3.3.20260528 ":" -> "Character \':\' is not permitted in sequence name"')
ok("Character ',' is not permitted in sequence name (GLB,1)" in rd('a7_ph_comma.out'), 'PhyML "," -> "Character \',\' is not permitted in sequence name" (SKILL: "same for ,")')
ok(os.path.getsize('a7_phyml_colon_tree.txt') == 0 and os.path.getsize('a7_phyml_comma_tree.txt') == 0, 'no tree is produced for those two')
t = rd('a7_phyml_paren_tree.txt'); ok('GLB(1)' in t and os.path.getsize('a7_phyml_paren_tree.txt') > 400, 'PhyML accepts "GLB(1)" and writes it verbatim into the Newick (SKILL: "accepts ( ) but writes them into the Newick tree"): ' + re.search(r'GLB\(1\)[^,)]*', t).group(0))
for tag, ver in [('new', '3.3.20260528'), ('old', '3.3.20220408')]:
    tr = rd(f'a7_phyml_{tag}_tree.txt'); names = re.findall(r'[(,]([^(),:]+):', tr)
    ok(len(names) == 12 and set(len(n) for n in names) == {138}, f'PhyML {ver}: all 12 names kept at 138 characters (SKILL: "138-character names are kept intact")')
print('=== Row 4: RAxML-NG rejects : , ( in names')
for v, name in [('1', '1.2.2'), ('2', '2.0.3')]:
    for c, ch in [('colon', 'GLB:1'), ('comma', 'GLB,1'), ('paren', 'GLB(1)')]:
        if v == '1' and c != 'colon': continue
        t = rd(f'a7_rxc{v}_pf12_name_{c}.out'); ok(f'ERROR: Following taxon name contains invalid characters: {ch}' in t, f'RAxML-NG {name} rejects {ch}: "Following taxon name contains invalid characters"')
ok('successfully read' in rd('a7_rxc2_pf12_longnames.out') and 'successfully read' in rd('a7_rxc1_pf12_longnames.out') if os.path.exists('a7_rxc1_pf12_longnames.out') else False, 'RAxML-NG 1.2.2 and 2.0.3 accept the 138-character names')
ok('Alignment has 12 sequences with 141 columns' in rd('a7_iq_pf12_longnames.out'), 'IQ-TREE 3.1.3 accepts the 138-character names (SKILL: "RAxML-NG and IQ-TREE accept ... 138 characters")')
print('=== Probes beyond the SKILL text (gaps in the sanitiser advice)')
t = rd('a7_rxc2_pf12_name_bracket.out'); print('RAxML-NG 2.0.3 on GLB[1]:', [l for l in t.splitlines() if 'ERROR' in l][:1])
ok('invalid characters: GLB[1]' in t, 'RAxML-NG also rejects "[" in a name; the SKILL sanitiser regex [():,] does not include [ or ]')
ph = rd('a7_ph_bracket.out'); print('PhyML on GLB[1]: tail:', ph.strip()[-90:].replace('\n', ' '))
ok('Time used' not in ph, 'PhyML on a name with "[" never reaches "Time used" (it crashed: exit 139 in i7_tools.out) - the SKILL sanitiser [():,] leaves "[" through')
print('=== IQ-TREE validation paragraph')
ok('Alignment has 12 sequences with 141 columns' in rd('a7_iq_pf12_relaxed.out'), "iqtree3 -s f.phy -n 0 -m LG -redo -pre check prints 'Alignment has N sequences with M columns'")
ok(re.search(r'ERROR: Line \d+: Sequence \S+ has wrong sequence length', rd('a7_iq_pf12_wronglen.out')) is not None, 'wrong-length foreign file: "ERROR: Line N: Sequence X has wrong sequence length"')
ok('Invalid "--check" option' in rd('a7_iq_chk.out'), 'IQ-TREE 3.1.3: --check is an invalid option')
t = rd('a7_iq_pf12_name_colon.out'); ok('Some sequence names are changed' in t, 'IQ-TREE 3.1.3 on ":" in a name: "WARNING: Some sequence names are changed" (Row 2)')
print('=== Biopython relaxed writer rewriting (Row 2 parenthetical): checked in i3_phylip.py ("a:1"->"a|1", "b(2)"->"b2", "c,3"->"c3")')
print('=== MrBayes paragraph')
t = rd('a7_mb_pf12.out'); ok("Instead found ''' in command 'Matrix'" in t, "MrBayes 3.2.7 on Biopython's NEXUS with quoted Pfam ids: Instead found ''' in command 'Matrix' (as the SKILL says)")
t = rd('a7_mb_pf12_recipe.out'); ok('Analysis completed' in t, 'MrBayes 3.2.7 loads the recipe-sanitised NEXUS and completes the mcmc run')
summary()
