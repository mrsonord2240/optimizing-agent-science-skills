"""Adversarial/boundary: header-only rMATS files (zero events of a type), unsupported event_type, missing file, unsupported counts value."""
import sys, io, contextlib, traceback
SK = '/mnt/openscience/wt/norm-bio-splicing-quantification/skills/bio-splicing-quantification'
sys.path.insert(0, SK + '/scripts')
import quantify_splicing as q
P = '/mnt/openscience/audits/bio-splicing-quantification/run-reaudit-1/out/rmats_planted/out'


def attempt(label, fn):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            r = fn()
        print(f'{label}: OK rows={len(r)} cols={len(r.columns)} printed={buf.getvalue().strip()!r}')
    except Exception as e:
        print(f'{label}: {type(e).__name__}: {str(e)[:140]}')


for t in ('A5SS', 'A3SS', 'MXE', 'RI'):
    attempt(f'header-only planted {t} JC', lambda t=t: q.parse_rmats_output(P, t))
attempt('event_type=AFE', lambda: q.parse_rmats_output(P, 'AFE'))
attempt('missing dir', lambda: q.parse_rmats_output('/nonexistent', 'SE'))
attempt('counts=JCX', lambda: q.parse_rmats_output(P, 'SE', counts='JCX'))
