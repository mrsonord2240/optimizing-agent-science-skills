"""Exact-commit re-audit of the previously repaired bio-alignment-multiple skill."""
from __future__ import annotations

import contextlib
import io
import os
import re
import shutil
import subprocess
from pathlib import Path

AUDITED = '966f838b0ba32918310bd223a34f71d78f190560'
COMMIT = '9d31109159d4d490ec375d4ae88c9b77570f3840'
FIXES = (
    '67499a0c5a0cc4065bfd80f8758c3fd8f02679ea',
    'e90210702462a6b08bf809e7caa68c7580771793',
    '8aa46939870db3a29e5f3fa42c8707b46d697584',
    'b67fab4b86d7f8ae563f8e92a221ce961415977b',
)
ROOT = Path(r'F:/OpenScience/worktrees/bio-alignment-multiple-reaudit')
SKILL = ROOT / 'alignment/multiple-alignment/SKILL.md'
AUDIT = Path(r'F:/OpenScience/audits/bio-alignment-multiple')
RUN = AUDIT / 'runs/exact-commit-9d31109'
MAFFT = Path(r'F:/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/mafft-win/mafft.bat')
MUSCLE = Path(r'F:/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/muscle.exe')


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f'PASS: {message}')


def git(*args: str) -> str:
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True).strip()


RUN.mkdir(parents=True, exist_ok=True)
require(git('rev-parse', 'HEAD') == COMMIT, f'exact source commit is {COMMIT}')
require(git('rev-parse', f'{AUDITED}:alignment/multiple-alignment/SKILL.md') !=
        git('hash-object', 'alignment/multiple-alignment/SKILL.md'),
        'current skill bytes differ from the audited source blob')
for fix in FIXES:
    require(subprocess.run(['git', '-C', str(ROOT), 'merge-base', '--is-ancestor', fix, 'HEAD']).returncode == 0,
            f'previous corrective commit {fix[:7]} is an ancestor of the exact source')

text = SKILL.read_text(encoding='utf-8')
require('muscle -align input.fasta -stratified -output ensemble.efa' in text,
        'MUSCLE ensemble uses -align rather than unsupported -super5 flags')
require('no direct `.efa`' in text and 'muscle -fa2efa replicates.txt -output ensemble.efa' in text,
        'large-set super5 ensemble workaround is documented')
require('| < 100 | < 3,000 | L-INS-i |' in text and '| >= 200,000 | >= 3,000 | PartTree' in text,
        'MAFFT auto table carries the audited count-and-length thresholds')
require('Homology/orientation pre-flight' in text and 'shuffled_max' in text,
        'homology/orientation pre-flight is runnable in the skill')
require('Strip the `_R_` prefix' in text and 'prompt to inspect further, not a verdict' in text,
        'orientation renaming and non-verdict gap guidance are explicit')
require((ROOT / 'alignment/multiple-alignment/references/specialist-tools.md').is_file() and
        (ROOT / 'alignment/multiple-alignment/references/tcoffee.md').is_file(),
        'specialist detail moved into linked reference files')

# Re-execute the repaired MUSCLE ensemble command and prove the obsolete command fails.
source_prot = AUDIT / 'runs/in1/prot15_unaligned.fa'
prot = RUN / 'prot15_unaligned.fa'
shutil.copy2(source_prot, prot)
ensemble = RUN / 'stratified.efa'
ok = subprocess.run([str(MUSCLE), '-align', str(prot), '-stratified', '-output', str(ensemble)],
                    cwd=RUN, text=True, capture_output=True)
require(ok.returncode == 0 and ensemble.is_file(), 'repaired MUSCLE -align stratified command executes')
efa = ensemble.read_text(encoding='utf-8')
require(len(re.findall(r'^<', efa, flags=re.M)) == 16 and len(re.findall(r'^>', efa, flags=re.M)) == 240,
        'stratified EFA has 16 replicate blocks and 240 records (16 x 15)')
bad = subprocess.run([str(MUSCLE), '-super5', str(prot), '-stratified', '-output', str(RUN / 'bad.efa')],
                     cwd=RUN, text=True, capture_output=True)
require(bad.returncode != 0 and 'not supported' in (bad.stderr + bad.stdout).lower(),
        'obsolete super5 stratified command is rejected as documented')

# Re-run two audited MAFFT --auto boundary cases and inspect the emitted strategy codes.
for name, expected in [('auto_sub90.fa', 'alg=L'), ('auto_sub150.fa', 'alg=X')]:
    fasta = AUDIT / 'runs/in5' / name
    out = RUN / f'{name}.out'
    with out.open('w', encoding='utf-8') as handle:
        proc = subprocess.run([str(MAFFT), '--auto', str(fasta)], cwd=RUN, stdout=handle,
                              stderr=subprocess.PIPE, text=True)
    (RUN / f'{name}.stderr').write_text(proc.stderr, encoding='utf-8')
    require(proc.returncode == 0 and expected in proc.stderr,
            f'MAFFT --auto {name} emits the documented {expected} strategy')

# Execute the exact source pre-flight fence on the audited mixed-orientation fixture.
mixed = AUDIT / 'runs/in3/mixed13.fa'
shutil.copy2(mixed, RUN / 'sequences.fa')
fences = re.findall(r'```python\n(.*?)```', text, flags=re.S)
preflight = next(f for f in fences if 'Homology/orientation pre-flight' in f)
capture = io.StringIO()
old_cwd = Path.cwd()
try:
    os.chdir(RUN)
    with contextlib.redirect_stdout(capture):
        exec(preflight, {})
finally:
    os.chdir(old_cwd)
preflight_output = capture.getvalue()
(RUN / 'preflight.log').write_text(preflight_output, encoding='utf-8')
require(preflight_output.count('NON-HOMOLOGOUS?') == 1,
        'pre-flight flags only the planted non-homologous contig')
require(preflight_output.count('reverse strand') == 3,
        'pre-flight identifies all three reverse-strand homologs')

# Confirm MAFFT produces the documented _R_ headers on the same mixed fixture.
adjusted = RUN / 'mixed_adjusted.fasta'
with adjusted.open('w', encoding='utf-8') as handle:
    directional = subprocess.run([str(MAFFT), '--adjustdirection', '--globalpair', '--maxiterate', '1000', str(mixed)],
                                 cwd=RUN, stdout=handle, stderr=subprocess.PIPE, text=True)
require(directional.returncode == 0 and adjusted.read_text(encoding='utf-8').count('>_R_') == 3,
        'MAFFT --adjustdirection produces three _R_ headers requiring downstream normalization')

print('ALL FOCUSED RE-AUDIT ASSERTIONS PASSED: 19/19')
