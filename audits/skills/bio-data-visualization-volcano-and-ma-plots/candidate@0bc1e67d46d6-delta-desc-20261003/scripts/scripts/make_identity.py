#!/usr/bin/env python3
"""Usage: make_identity.py <skill-id> <upstream-name> <candidate-path> <worktree> <out-source-identity.json>"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

skill_id, upstream, cand, wt, out = sys.argv[1:6]
REPO = Path(r"F:\optimizing-agent-science-skills")
pre = json.loads(subprocess.run([sys.executable, str(REPO / "tools/skill_preflight.py"), "--offline", "--json", cand],
                                capture_output=True, text=True, cwd=REPO).stdout)[0]
assert pre["id"] == skill_id and not pre["fail"], pre
base = Path(cand)
files = []
for p in sorted(base.rglob("*")):
    if p.is_file():
        b = p.read_bytes()
        files.append({"path": p.relative_to(base).as_posix(), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()})
ext = REPO / "external" / "GPTomics__bioSkills"
commit = "d91ed3d563019e649dc854c56ccd62551359488a"
sub = subprocess.run(["git", "-C", str(ext), "rev-parse", f"{commit}:data-visualization/{upstream}"], capture_output=True, text=True).stdout.strip()
branch = subprocess.run(["git", "-C", wt, "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True).stdout.strip()
head = subprocess.run(["git", "-C", wt, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
status = subprocess.run(["git", "-C", wt, "status", "--short"], capture_output=True, text=True).stdout.strip().replace("\n", "; ")
zsha = hashlib.sha256((REPO / "skill-auditor.zip").read_bytes()).hexdigest()
doc = {
    "origin": {"repository": "GPTomics/bioSkills", "commit": commit, "path": f"data-visualization/{upstream}",
               "subtree": sub, "checkout": str(ext)},
    "candidate": {"branch": branch, "commit": head, "path": cand.replace("/", "\\"), "content_sha256": pre["identity"],
                  "identity_kind": "sha256-manifest-v1", "status_after_execution": status,
                  "content_manifest": {"file_count": pre["files"], "bytes": pre["bytes"]}},
    "files": files,
    "tooling": {"rubric_zip_sha256": zsha, "preflight_warn": pre["warn"]},
    "candidate_cache_artifacts_after_execution": [str(p.relative_to(base)) for p in base.rglob("__pycache__")],
}
Path(out).write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
print(pre["identity"], len(files), "pycache:", doc["candidate_cache_artifacts_after_execution"])
