#!/usr/bin/env python3
"""Capture exact candidate, origin, tooling, and rubric identity read-only."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path


if os.name == "nt":
    AUDIT = Path(r"F:\OpenScience\audits\bio-batch-processing\reaudit-opt10-20260928")
    REPO = Path(r"F:\OpenScience\wt\opt10-batch-processing")
    ORIGIN = Path(r"F:\optimizing-agent-science-skills\external\GPTomics__bioSkills")
    TOOLS = Path(r"F:\OpenScience\audit-envs\bio-batch-processing")
    RUBRIC = Path(r"F:\optimizing-agent-science-skills\skill-auditor.zip")
else:
    AUDIT = Path("/mnt/openscience/audits/bio-batch-processing/reaudit-opt10-20260928")
    REPO = Path("/mnt/openscience/wt/opt10-batch-processing")
    ORIGIN = Path("/mnt/openscience/optimizing-agent-science-skills/external/GPTomics__bioSkills")
    TOOLS = Path("/mnt/openscience/audit-envs/bio-batch-processing")
    RUBRIC = Path("/mnt/openscience/optimizing-agent-science-skills/skill-auditor.zip")

CANDIDATE = REPO / "skills" / "bio-batch-processing"
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
        ["git", "-C", str(repo), *args], text=True, stderr=subprocess.STDOUT
    ).strip()


def manifest(root: Path):
    paths = sorted(
        (path for path in root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(root).as_posix().casefold(),
    )
    rows = []
    for path in paths:
        relative = path.relative_to(root).as_posix()
        rows.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "git_blob": subprocess.check_output(
                    ["git", "hash-object", "--no-filters", str(path)], text=True
                ).strip(),
            }
        )
    identity_rows = [
        rf"{row['path']}\t{row['bytes']}\t{row['sha256']}" for row in rows
    ]
    digest = hashlib.sha256(r"\n".join(identity_rows).encode("utf-8")).hexdigest()
    return rows, digest


files, content_digest = manifest(CANDIDATE)
cache_artifacts = sorted(
    path.relative_to(CANDIDATE).as_posix()
    for path in CANDIDATE.rglob("*")
    if path.is_file() and (path.suffix in {".pyc", ".pyo"} or "__pycache__" in path.parts)
)
payload = {
    "phase": "independent reaudit-scientific-skill",
    "independence": {
        "performed_initial_audit": False,
        "performed_candidate_fix": False,
        "performed_tooling_delta": False,
        "candidate_bytes_modified": False,
    },
    "origin": {
        "repository": "GPTomics/bioSkills",
        "commit": git(ORIGIN, "rev-parse", "HEAD"),
        "path": ORIGIN_PATH,
        "subtree": git(ORIGIN, "rev-parse", f"{ORIGIN_COMMIT}:{ORIGIN_PATH}"),
        "checkout": str(ORIGIN),
        "status": git(ORIGIN, "status", "--short") or "clean",
    },
    "candidate": {
        "path": str(CANDIDATE),
        "branch": git(REPO, "branch", "--show-current"),
        "commit": git(REPO, "rev-parse", "HEAD"),
        "status": git(REPO, "status", "--short"),
        "content_sha256": content_digest,
        "identity_recipe": "case-insensitive relative POSIX-path sort; each row is path\\tbytes\\tsha256; rows joined by literal \\n; SHA-256 over UTF-8",
    },
    "files": files,
    "tooling": {
        "tools_md_sha256": sha256(TOOLS / "TOOLS.md"),
        "environment_fingerprint_sha256": sha256(TOOLS / "environment-fingerprint.json"),
        "environment_lock_sha256": sha256(TOOLS / "environment-explicit.lock"),
        "rubric_zip_sha256": sha256(RUBRIC),
    },
    "candidate_cache_artifacts": cache_artifacts,
}
(AUDIT / "source-identity.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps({"candidate_content_sha256": content_digest, "files": len(files), "cache": cache_artifacts}))
