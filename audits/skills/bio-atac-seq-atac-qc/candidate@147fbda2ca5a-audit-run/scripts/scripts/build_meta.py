import hashlib, os, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root = r'F:\OpenScience\wt\atac-atac-qc\skills\bio-atac-seq-atac-qc'
rows = []
for d, _, fs in os.walk(root):
    for f in fs:
        p = os.path.join(d, f); b = open(p, 'rb').read()
        rows.append((os.path.relpath(p, root).replace(chr(92), '/'), len(b), hashlib.sha256(b).hexdigest()))
rows.sort(key=lambda x: x[0].encode())
man = "\n".join(f"{a}\t{b}\t{c}" for a, b, c in rows).encode()
open(os.path.join(R, 'candidate-manifest.tsv'), 'wb').write(man)
ident = hashlib.sha256(man).hexdigest()
sid = {
 "schema": "scientific-skill-audit-source-identity-v1", "phase": "initial audit", "skill_id": "bio-atac-seq-atac-qc",
 "independent_auditor": False,
 "origin": {"repository": "GPTomics/bioSkills", "commit": "d91ed3d563019e649dc854c56ccd62551359488a", "path": "atac-seq/atac-qc", "license": "MIT"},
 "candidate": {"root": root, "worktree": r"F:\OpenScience\wt\atac-atac-qc", "branch": "fix/atac-atac-qc",
   "product_head": "3186916406e9cc6b0e6dc24ffe47880951fc0f93", "identity_scheme": "sha256-manifest-v1", "content_sha256": ident,
   "manifest_bytes": len(man), "file_count": len(rows),
   "manifest_recipe": "Ordinal POSIX relative paths; each UTF-8 line is path, TAB, byte count, TAB, lowercase file SHA-256; lines joined by LF without a trailing LF; SHA-256 over the manifest bytes.",
   "manifest_path": "candidate-manifest.tsv", "identity_before": ident, "identity_after": ident,
   "tree_status": "Candidate skill directory is untracked in the worktree; no candidate bytes were modified by this audit."},
 "tooling": {"tools_md": r"F:\OpenScience\audits\bio-atac-seq-atac-qc\TOOLS.md", "environment_lock_sha256": "e29e33c21ca3d6a660029311c4c9c7edbac105953734bd45b6a8f24799b009ac"},
 "rubric": {"zip": r"F:\optimizing-agent-science-skills\skill-auditor.zip", "evaluator_version": "skill-auditor@1.0"},
 "files": [{"path": a, "bytes": b, "sha256": c} for a, b, c in rows]}
json.dump(sid, open(os.path.join(R, 'source-identity.json'), 'w', encoding='utf-8'), indent=2)
cls = {"schema": "execution-classifications-v1", "skill_id": "bio-atac-seq-atac-qc", "candidate_sha256": ident, "surfaces": [
 {"surface": "scripts/library_complexity.py", "class": "executed", "evidence": "real GM12878 BAMs, planted BAMs, independent fragment comparison; findings ATAC-QC-001/002/009"},
 {"surface": "scripts/encode_tss_enrichment.py", "class": "executed", "evidence": "real bigWig, deepTools cross-check, planted-truth probes; ATAC-QC-004/005"},
 {"surface": "scripts/aggregate_qc.py", "class": "executed", "evidence": "threshold grading, MultiQC ingest; ATAC-QC-003"},
 {"surface": "scripts/atac_qc_metrics.R", "class": "executed", "evidence": "Windows-native R 4.4.3 / ATACseqQC 1.30.0 on real slice; plot re-rendered; ATAC-QC-007/008"},
 {"surface": "samtools flagstat/idxstats, Picard insert size, deepTools plotProfile/multiBamSummary/plotFingerprint, MultiQC", "class": "executed", "evidence": "TOOLS.md smoke_cli"},
 {"surface": "preseq c_curve/lc_extrap", "class": "executed", "evidence": "t_pre*.log; ATAC-QC-006"},
 {"surface": "mitochondrial fraction via samtools idxstats chrM", "class": "static-only", "evidence": "slice has no chrM; cannot be exercised on real data"},
 {"surface": "FRiP from freshly called MACS peaks; fastqc/macs2 MultiQC modules", "class": "static-only", "evidence": "ENCODE IDR peaks used; MACS not run"},
 {"surface": "sex-chromosome QC snippets (chrX XIST, chrY)", "class": "static-only", "evidence": "slice covers chr1:1-30Mb only"},
 {"surface": "spike-in, cell-cycle, replicate-correlation guidance", "class": "static-only", "evidence": "prose guidance without shipped runnable surface"}]}
json.dump(cls, open(os.path.join(R, 'execution-classifications.json'), 'w', encoding='utf-8'), indent=2)
print(ident)
