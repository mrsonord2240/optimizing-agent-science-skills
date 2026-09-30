"""Build source-identity.json (origin kept separate from the exact working candidate)."""
import hashlib, json, os
A = r"F:\OpenScience\audits\bio-atac-seq-deep-learning-atac"
root = r"F:\OpenScience\wt\atac-deep-learning-atac\skills\bio-atac-seq-deep-learning-atac"
files = []
for r, _, fs in os.walk(root):
    for f in fs:
        p = os.path.join(r, f)
        b = open(p, "rb").read()
        files.append({"path": os.path.relpath(p, root).replace(os.sep, "/"), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()})
files.sort(key=lambda x: x["path"])
manifest = "\n".join(f"{x['path']}\t{x['bytes']}\t{x['sha256']}" for x in files)
h = hashlib.sha256(manifest.encode()).hexdigest()
print("recomputed manifest sha (recipe path/bytes/sha, LF):", h)
tools = hashlib.sha256(open(A + r"\TOOLS.md", "rb").read()).hexdigest()
z = hashlib.sha256(open(r"F:\optimizing-agent-science-skills\skill-auditor.zip", "rb").read()).hexdigest()
d = {
    "origin": {"repository": "GPTomics/bioSkills", "commit": "d91ed3d563019e649dc854c56ccd62551359488a", "path": "atac-seq/deep-learning-atac"},
    "candidate": {
        "branch": "fix/atac-deep-learning-atac", "commit": "3186916",
        "path": root, "status_before": "untracked normalized subtree only",
        "status_after_execution": "untracked normalized subtree only (bytes unchanged)",
        "content_sha256": "c62d899a58ee945dcf6cdb9e2ba797b65c09b2c9730da4a3be70a3f8f1a28943",
        "content_manifest": {"file_count": len(files), "scheme": "sha256-manifest-v1 as computed by the tooling phase; per-file sha256 below verified live"},
        "files": files,
    },
    "tooling": {"tools_md_sha256": tools, "environment_fingerprint_sha256": "06fc27986ce7b28c4e102689c57fa41596fc3d2716402daaa8309f93bf9cfa29", "rubric_zip_sha256": z},
}
json.dump(d, open(A + r"\initial-audit-20260930\source-identity.json", "w"), indent=2)
