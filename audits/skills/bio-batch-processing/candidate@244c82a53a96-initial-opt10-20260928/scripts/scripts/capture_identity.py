#!/usr/bin/env python3
"""Capture exact candidate/origin identity without mutating either tree."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path


if os.name == "nt":
    AUDIT = Path(r"F:\OpenScience\audits\bio-batch-processing\initial-opt10-20260928")
    CANDIDATE_REPO = Path(r"F:\OpenScience\wt\opt10-batch-processing")
    ORIGIN_REPO = Path(r"F:\optimizing-agent-science-skills\external\GPTomics__bioSkills")
    TOOLS_ROOT = Path(r"F:\OpenScience\audit-envs\bio-batch-processing")
    RUBRIC_ZIP = Path(r"F:\optimizing-agent-science-skills\skill-auditor.zip")
else:
    AUDIT = Path("/mnt/openscience/audits/bio-batch-processing/initial-opt10-20260928")
    CANDIDATE_REPO = Path("/mnt/openscience/wt/opt10-batch-processing")
    ORIGIN_REPO = Path("/mnt/openscience/optimizing-agent-science-skills/external/GPTomics__bioSkills")
    TOOLS_ROOT = Path("/mnt/openscience/audit-envs/bio-batch-processing")
    RUBRIC_ZIP = Path("/mnt/openscience/optimizing-agent-science-skills/skill-auditor.zip")
CANDIDATE = CANDIDATE_REPO / "skills" / "bio-batch-processing"
ORIGIN_COMMIT = "d91ed3d563019e649dc854c56ccd62551359488a"
ORIGIN_PATH = "sequence-io/batch-processing"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", repo, *args], text=True, stderr=subprocess.STDOUT
    ).strip()


def manifest(root: Path) -> tuple[list[dict[str, object]], str]:
    paths = sorted(
        (path for path in root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(root).as_posix().casefold(),
    )
    rows = []
    for path in paths:
        rel = path.relative_to(root).as_posix()
        digest = sha256(path)
        rows.append(
            {
                "path": rel,
                "bytes": path.stat().st_size,
                "sha256": digest,
                "git_blob": subprocess.check_output(
                    ["git", "hash-object", "--no-filters", path], text=True
                ).strip(),
            }
        )
    identity_rows = [
        rf"{row['path']}\t{row['bytes']}\t{row['sha256']}" for row in rows
    ]
    content_digest = hashlib.sha256(r"\n".join(identity_rows).encode("utf-8")).hexdigest()
    return rows, content_digest


files, content_digest = manifest(CANDIDATE)
cache_artifacts = sorted(
    str(path.relative_to(CANDIDATE)).replace("\\", "/")
    for path in CANDIDATE.rglob("*")
    if path.is_file() and (path.suffix in {".pyc", ".pyo"} or "__pycache__" in path.parts)
)
payload = {
    "origin": {
        "repository": "GPTomics/bioSkills",
        "commit": git(ORIGIN_REPO, "rev-parse", "HEAD"),
        "path": ORIGIN_PATH,
        "subtree": git(ORIGIN_REPO, "rev-parse", f"{ORIGIN_COMMIT}:{ORIGIN_PATH}"),
        "checkout": str(ORIGIN_REPO),
        "status": git(ORIGIN_REPO, "status", "--short") or "clean",
    },
    "candidate": {
        "branch": git(CANDIDATE_REPO, "branch", "--show-current"),
        "commit": git(CANDIDATE_REPO, "rev-parse", "HEAD"),
        "content_sha256": content_digest,
        "identity_recipe": "case-insensitive relative POSIX-path sort; each row is path\\\\tbytes\\\\tsha256; rows joined by literal \\\\n; SHA-256 over UTF-8",
        "path": str(CANDIDATE),
        "status": git(CANDIDATE_REPO, "status", "--short"),
    },
    "files": files,
    "tooling": {
        "tools_md_sha256": sha256(TOOLS_ROOT / "TOOLS.md"),
        "environment_fingerprint_sha256": sha256(TOOLS_ROOT / "environment-fingerprint.json"),
        "environment_lock_sha256": sha256(TOOLS_ROOT / "environment-explicit.lock"),
        "rubric_zip_sha256": sha256(RUBRIC_ZIP),
    },
    "candidate_cache_artifacts_after_execution": cache_artifacts,
}
(AUDIT / "source-identity.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps({"candidate_content_sha256": content_digest, "cache_count": len(cache_artifacts)}))
