"""Build source-identity.json for the audited candidate (file manifest from the live tree)."""
import hashlib
import json
import os
import subprocess

ROOT = 'F:/OpenScience/wt/recut-crispr-pipeline/skills/bio-workflows-crispr-screen-pipeline'
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = []
for dp, _, fn in os.walk(ROOT):
    for f in fn:
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
        b = open(p, 'rb').read()
        files.append({'path': rel,
                      'git_blob': subprocess.check_output(['git', 'hash-object', p]).decode().strip(),
                      'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)})
files.sort(key=lambda x: x['path'].encode())
ident = {
    'origin': {'repository': 'GPTomics/bioSkills', 'commit': 'd91ed3d563019e649dc854c56ccd62551359488a',
               'path': 'workflows/crispr-screen-pipeline', 'subtree': 'a69f1dad4a667e06a306b2794e121363ee35eef2',
               'checkout': 'F:\\optimizing-agent-science-skills\\external\\GPTomics__bioSkills', 'status': 'clean'},
    'candidate': {'branch': 'recut/crispr-screen-pipeline', 'commit': 'f162b3a9fd54e41c8f9e06bb969f86d079788518',
                  'base_note': 'commit is the worktree base; the candidate bytes are uncommitted',
                  'content_sha256': 'e242270b6fc053d495f12c86df5d2d8eb96f9b42fd3971d6435796c9bae5a71d',
                  'path': 'F:\\OpenScience\\wt\\recut-crispr-pipeline\\skills\\bio-workflows-crispr-screen-pipeline',
                  'status_before': 'uncommitted recut (normalize-phase changes)',
                  'status_after_execution': 'unchanged; skill_preflight --offline --shape re-verified the identity'},
    'files': files,
    'tooling': {'tools_md_sha256': '2315b89c95f49b170f79d65e5937dc8cc014a9c97b4c56379d1bfa8f5988983e',
                'rubric_zip_sha256': 'e54e9ff8b0c3677abcfe657ad6ed92ba34dbdb8ad205c7157ad881f25afcf0de',
                'routing_cases': 'audits/skills/bio-workflows-crispr-screen-pipeline/tooling/routing-cases.json'},
    'candidate_cache_artifacts_after_execution': [],
}
json.dump(ident, open(os.path.join(RUN, 'source-identity.json'), 'w'), indent=2)
print(len(files), 'files')
