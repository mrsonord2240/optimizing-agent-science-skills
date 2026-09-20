"""INPUT 7 (NEW) assertions on the tool outputs written by i7_tools.sh / i7b_tools2.sh / i7c_tools3.sh (real RAxML-NG 1.2.2 + 2.0.3, PhyML 3.3.20260528 + 3.3.20220408,
IQ-TREE 3.1.3, MrBayes 3.2.7). Each SKILL claim in the 'PHYLIP-Relaxed Dialect Mismatches' table and the IQ-TREE validation paragraph is judged by output text."""
import os, re
from common import *
d = DATA/'tools'; os.chdir(d)
rd = lambda f: open(f, encoding='utf-8', errors='replace').read()
print('=== SKILL row 1: RAxML-NG "terminating with uncaught exception ... bad alphabet" for "*" in a protein alignment')
for v in ['1', '2']:
    t = rd(f'rx{v}_pf12_star.out'); ok('successfully read' in t and 'exception' not in t and 'bad alphabet' not in t, f'RAxML-NG v{"1.2.2" if v=="1" else "2.0.3"} --check accepts a protein alignment with "*" (no exception, no "bad alphabet"): claim NOT reproduced')
    t = rd(f'rxs{v}_pf12_star.out'); m = re.search(r'Final LogLikelihood: (-[\d.]+)', t); ok(bool(m), f'RAxML-NG v{v} full --search1 ML run on the "*" alignment completes: lnL {m.group(1) if m else None}')
for v in ['1', '2']:
    t = rd(f'rxd{v}.out'); ok('Invalid character in sequence 5 at position 4: *' in t, f'RAxML-NG v{v} on a NUCLEOTIDE alignment with "*": "ERROR: Invalid character ... *" (a different message, only for DNA)')
print('=== SKILL row 1 fix: replacing "*" with "X" is harmless')
ok('successfully read' in rd('rx2_pf12_starX.out'), 'RAxML-NG accepts the X-replaced protein alignment')
print('=== SKILL row 3: PhyML "silently truncated names / names >100 chars / truncates at 100 chars in current build"')
for tag, ver in [('new', '3.3.20260528'), ('old', '3.3.20220408')]:
    tr = rd(f'phyml_{tag}_tree.txt'); names = re.findall(r'[(,]([^(),:]+):', tr)
    print(f'PhyML {ver} tree taxon-name lengths:', sorted(set(len(n) for n in names)), 'n =', len(names))
    ok(len(names) == 12 and set(len(n) for n in names) == {138}, f'PhyML {ver} keeps all 12 names at full 138 chars: the "100-character truncation" claim is NOT reproduced')
print('=== SKILL: PhyML rejects colons in names')
ok("Character ':' is not permitted in sequence name" in rd('ph_pf12_foreign_colon.out'), 'PhyML 3.3.20260528: "Character \':\' is not permitted in sequence name (GLB:colon(1))"')
print('=== SKILL: RAxML-NG / IQ-TREE accept relaxed with long names; colon handling')
ok('successfully read' in rd('rx2_pf12_longnames.out') and 'successfully read' in rd('rx1_pf12_longnames.out'), 'RAxML-NG 1.2.2 and 2.0.3 accept 138-char names in Biopython phylip-relaxed')
ok('invalid characters: GLB:colon(1)' in rd('rx2_pf12_foreign_colon.out') and 'invalid characters' in rd('rx1_pf12_foreign_colon.out'), 'RAxML-NG rejects the colon/paren name (loud)  [SKILL says RAxML-NG and IQ-TREE accept relaxed; the colon case is only implied]')
t = rd('iq_pf12_foreign_colon.out'); ok('Some sequence names are changed' in t and 'Alignment has 12 sequences with 141 columns' in t, 'IQ-TREE 3.1.3 on a foreign file with ":" in a name: "WARNING: Some sequence names are changed" and proceeds (SKILL row 2)')
print('=== SKILL IQ-TREE validation paragraph')
t = rd('iq_pf12_relaxed.out'); ok('Alignment has 12 sequences with 141 columns' in t, "iqtree3 -s f.phy -n 0 -m LG -redo -pre check prints 'Alignment has N sequences with M columns'")
t = rd('iq_pf12_wronglen.out'); ok(re.search(r'ERROR: Line \d+: Sequence \S+ has wrong sequence length', t) is not None, 'wrong-length foreign file: "ERROR: Line N: Sequence X has wrong sequence length" (as SKILL states)')
ok('Invalid "--check" option' in rd('iq_chk.out'), 'IQ-TREE 3.1.3: --check is an invalid option (SKILL: "has no validate-only flag")')
print('=== MrBayes and the SKILL row "MrBayes | NEXUS | nexus"')
t = rd('mb_pf12.out'); print([l.strip() for l in t.splitlines() if 'Instead found' in l][:1])
ok("Instead found ''' in command 'Matrix'" in t, "MrBayes 3.2.7 REJECTS the NEXUS written by AlignIO with molecule_type='protein' for real Pfam ids (quoted names 'GLB2_LUMTE/31-141'): SKILL does not warn")
t = rd('mb_pf12_clean.out'); ok('Analysis completed' in t, 'the same NEXUS with ids sanitised (/ and - to _) loads and a 200-generation run completes in MrBayes 3.2.7')
head = [l for l in rd('pf12.nex').splitlines() if l.startswith("'")][:1]; print('Biopython NEXUS row start:', head[0][:40] if head else None)
summary()
