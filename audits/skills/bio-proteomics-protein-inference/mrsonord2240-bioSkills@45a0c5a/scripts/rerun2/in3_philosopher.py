# Re-audit 2026-09-15 (batch C), Input 3 (Edge, NEW). The SKILL.md decision-tree row
# "FragPipe / TPP pipeline -> ProteinProphet inference + Philosopher/Philosopher-style FDR filtering"
# and the header line "CLI: ProteinProphet (TPP) ...; Philosopher filter for FragPipe FDR".
# Philosopher 5.1.0 is now installed. REAL data: PXD070049 DDA Condition_A, Comet 2026.02 pepXML.
# Every step is judged on its OUTPUT, never on its exit code.
import subprocess, os, re, glob

E = 'F:/OpenScience/audit-envs/mass-spec-proteomics-analyst'
PHIL = E + '/tools/philosopher/philosopher.exe'
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'phil')


def readlog(p):
    return open(os.path.join(W, p), encoding='utf-8', errors='replace').read()


def strip(s):
    return re.sub(r'\x1b\[[0-9;]*m', '', s)


print('=== step 1: philosopher peptideprophet (upstream of ProteinProphet) ===')
lg = strip(readlog('pepproph.log'))
print('  exit code recorded: 0')
print('  log says:', [l.strip() for l in lg.splitlines() if 'read in' in l][-1])
xml = open(os.path.join(W, 'interact-comet.pep.xml'), encoding='utf-8', errors='replace').read()
print(f'  OUTPUT CHECK -> spectrum_query elements: {xml.count("<spectrum_query")}; '
      f'peptideprophet_result elements: {xml.count("peptideprophet_result")}')
print('  verdict: SILENT FAILURE reproduced (exit 0, file written, zero probabilities modelled)')

print('\n=== step 2: philosopher proteinprophet, direct on Comet pepXML ===')
lg = strip(readlog('pp_direct.log'))
for l in lg.splitlines():
    if any(k in l for k in ('did not find', 'read in 0', 'WARNING', 'ERRO')):
        print('   ', l.strip())
print('  exit code recorded: 1')
print('  OUTPUT CHECK -> *.prot.xml written:', glob.glob(os.path.join(W, '*.prot.xml')))
print('  verdict: LOUD failure. The peptideprophet silent-failure class does NOT extend to ProteinProphet.')

print('\n=== step 3: philosopher proteinprophet on the interact-*.pep.xml from step 1 ===')
lg = strip(readlog('pp_chain.log'))
for l in lg.splitlines():
    if any(k in l for k in ('did not find', 'read in 0', 'WARNING', 'ERRO')):
        print('   ', l.strip())
print('  exit code recorded: 1; no .prot.xml produced -> loud failure again')

print('\n=== step 4: philosopher filter (the command SKILL.md actually names) ===')
lg = strip(readlog('filter.log'))
for l in lg.splitlines():
    if any(k in l for k in ('Charge profile', 'Database search results', 'Converged',
                            'Final report', 'razor option')):
        print('   ', ' '.join(l.split()))
print('  exit code recorded: 0')
for t in ('psm.tsv', 'peptide.tsv', 'ion.tsv'):
    p = os.path.join(W, t)
    n = sum(1 for _ in open(p, encoding='utf-8')) if os.path.exists(p) else None
    print(f'  OUTPUT CHECK -> {t}: {n} line(s) (1 = header only)')
print('  OUTPUT CHECK -> protein.tsv exists:', os.path.exists(os.path.join(W, 'protein.tsv')))
print('  verdict: SILENT FAILURE. exit 0 + "Converged to 0.00 % FDR" + empty tables + NO protein.tsv.')

print('\n=== step 5: is it Comet-specific? same PSMs re-serialised by OpenMS IDFileConverter ===')
lg = strip(readlog('f2/filter2.log'))
for l in lg.splitlines():
    if 'Database search results' in l or 'Converged to 0.00' in l:
        print('   ', ' '.join(l.split()))
        break
print('  verdict: identical 0-PSM read from an independently serialised pepXML ->'
      ' Philosopher pepXML ingestion is broken in this environment, not a Comet quirk.')

print('\n=== what the Skill gives the agent for this route ===')
sk = open('F:/OpenScience/external/mrsonord2240__bioSkills/proteomics/protein-inference/SKILL.md',
          encoding='utf-8').read()
for term in ('philosopher filter', 'Philosopher filter', 'ProteinProphet', 'peptideprophet',
             'prot.xml', 'protein.tsv', '--tag', 'check the output'):
    print(f'  {term!r:22s} occurrences in SKILL.md: {sk.count(term)}')
