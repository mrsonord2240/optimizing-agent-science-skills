#!/usr/bin/env python3
"""Bind an immutable candidate audit to byte-identical committed provider bytes.

The scientific report is copied unchanged.  A separate binding record proves
that every committed provider file matches the audited candidate worktree and
makes the provider commit the latest audit identity used by readiness tooling.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess


PROVIDER_REPOSITORY = "mrsonord2240/optimized-scientific-skills"
ORIGIN_REPOSITORY = "GPTomics/bioSkills"
ORIGIN_COMMIT = "d91ed3d563019e649dc854c56ccd62551359488a"


def _git(repo: Path, *args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
    )
    return result.stdout


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"cannot read {path}: {exc}") from exc


def _write_json(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _local_files(root: Path) -> dict[str, bytes]:
    if not root.is_dir():
        raise SystemExit(f"candidate path is not a directory: {root}")
    files: dict[str, bytes] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if path.suffix in {".pyc", ".pyo"} or "__pycache__" in path.parts:
            raise SystemExit(f"candidate contains cache artifact: {relative}")
        files[relative] = path.read_bytes()
    if not files:
        raise SystemExit(f"candidate path has no files: {root}")
    return files


def _provider_files(repo: Path, commit: str, prefix: str) -> dict[str, bytes]:
    listed = _git(repo, "ls-tree", "-r", "--name-only", "-z", commit, "--", prefix, binary=True)
    assert isinstance(listed, bytes)
    paths = [part.decode("utf-8") for part in listed.split(b"\0") if part]
    normalized = prefix.rstrip("/") + "/"
    files: dict[str, bytes] = {}
    for path in paths:
        if not path.startswith(normalized):
            continue
        relative = path[len(normalized):]
        blob = _git(repo, "show", f"{commit}:{path}", binary=True)
        assert isinstance(blob, bytes)
        files[relative] = blob
    if not files:
        raise SystemExit(f"provider commit has no files under {prefix}")
    return files


def _manifest(files: dict[str, bytes]) -> tuple[str, list[dict]]:
    rows = []
    lines = []
    for relative in sorted(files, key=lambda value: value.encode("utf-8")):
        blob = files[relative]
        digest = hashlib.sha256(blob).hexdigest()
        rows.append({"path": relative, "bytes": len(blob), "sha256": digest})
        lines.append(f"{relative}\t{len(blob)}\t{digest}")
    manifest = "\n".join(lines).encode("utf-8")
    return hashlib.sha256(manifest).hexdigest(), rows


def _insert_binding_note(viewer: str, note: str) -> str:
    lines = viewer.splitlines()
    if lines and lines[0].startswith("# "):
        lines[1:1] = ["", note]
        return "\n".join(lines) + "\n"
    return note + "\n\n" + viewer.replace("\r\n", "\n")


def bind_candidate_audit(
    records: Path,
    provider: Path,
    skill_id: str,
    candidate_version: str,
    provider_commit: str,
) -> tuple[str, Path]:
    if not re.fullmatch(r"[0-9a-f]{40}", provider_commit):
        raise SystemExit("provider commit must be a full lowercase 40-character SHA")
    resolved = str(_git(provider, "rev-parse", f"{provider_commit}^{{commit}}")).strip()
    if resolved != provider_commit:
        raise SystemExit(f"provider commit resolved unexpectedly: {resolved}")

    source_dir = records / "audits" / "skills" / skill_id / candidate_version
    record_path = source_dir / "record.json"
    report_path = source_dir / "report.json"
    viewer_path = source_dir / "viewer.md"
    identity_path = source_dir / "source-identity.json"
    for path in (record_path, report_path, viewer_path, identity_path):
        if not path.is_file():
            raise SystemExit(f"candidate audit is missing {path.name}: {source_dir}")
    record = _read_json(record_path)
    if record.get("skill_id") != skill_id or record.get("version") != candidate_version:
        raise SystemExit(f"candidate record identity does not match {skill_id}/{candidate_version}")
    candidate = record.get("candidate")
    if not isinstance(candidate, dict) or not candidate.get("identity"):
        raise SystemExit("candidate audit record has no exact candidate identity")
    candidate_path = Path(str(candidate.get("path", "")))
    local_files = _local_files(candidate_path)
    provider_path = f"skills/{skill_id}"
    committed_files = _provider_files(provider, provider_commit, provider_path)
    if set(local_files) != set(committed_files):
        missing = sorted(set(local_files) - set(committed_files))
        extra = sorted(set(committed_files) - set(local_files))
        raise SystemExit(f"provider/candidate file sets differ; missing={missing}, extra={extra}")
    mismatches = sorted(path for path in local_files if local_files[path] != committed_files[path])
    if mismatches:
        raise SystemExit("provider/candidate bytes differ: " + ", ".join(mismatches))

    manifest_sha256, files = _manifest(committed_files)
    tree = str(_git(provider, "rev-parse", f"{provider_commit}:{provider_path}")).strip()
    version = f"mrsonord2240-optimized-scientific-skills@{provider_commit[:7]}"
    target = records / "audits" / "skills" / skill_id / version
    if target.exists():
        existing = _read_json(target / "binding.json") if (target / "binding.json").is_file() else {}
        if (
            existing.get("provider_commit") == provider_commit
            and existing.get("candidate_version") == candidate_version
            and existing.get("manifest_sha256") == manifest_sha256
        ):
            return version, target
        raise SystemExit(f"provider binding already exists with different content: {target}")

    shutil.copytree(source_dir, target)
    provider_url = (
        f"https://github.com/{PROVIDER_REPOSITORY}/tree/"
        f"{provider_commit}/{provider_path}"
    )
    source = record.get("source", {})
    origin_repository = source.get("repository", ORIGIN_REPOSITORY)
    origin_commit = source.get("commit", ORIGIN_COMMIT)
    bound_record = dict(record)
    bound_record["version"] = version
    bound_record["source"] = {
        "repository": PROVIDER_REPOSITORY,
        "commit": provider_commit,
        "path": provider_path,
        "author": source.get("author", "GPTomics"),
        "author_url": source.get("author_url", "https://github.com/GPTomics"),
        "license": source.get("license", "MIT"),
        "modified_by": "Samuel Nord",
        "fork_of": {"repository": origin_repository, "commit": origin_commit},
        "url": provider_url,
    }
    bound_record["supersedes"] = candidate_version
    bound_record["candidate"] = dict(candidate)
    bound_record["candidate"]["provider_commit"] = provider_commit
    bound_record["candidate"]["provider_tree"] = tree
    bound_record["files"] = dict(record.get("files", {}))
    bound_record["files"]["provider_binding"] = "binding.json"
    binding = {
        "schema_version": 1,
        "skill_id": skill_id,
        "candidate_version": candidate_version,
        "candidate_identity": candidate["identity"],
        "provider_repository": PROVIDER_REPOSITORY,
        "provider_commit": provider_commit,
        "provider_path": provider_path,
        "provider_tree": tree,
        "verification": "every committed provider file compared byte-for-byte with the audited candidate worktree",
        "manifest_recipe": "relative POSIX path, byte count, lowercase SHA-256; UTF-8 LF joins; ordinal UTF-8 byte ordering; no trailing LF",
        "manifest_sha256": manifest_sha256,
        "file_count": len(files),
        "files": files,
        "report_reexecuted": False,
        "report_rewritten": False,
    }
    _write_json(target / "record.json", bound_record)
    _write_json(target / "binding.json", binding)
    viewer = (target / "viewer.md").read_text(encoding="utf-8")
    note = (
        f"> - Provider binding: exact committed bytes at "
        f"[{PROVIDER_REPOSITORY}@{provider_commit[:7]}]({provider_url}) match audited candidate "
        f"`{candidate['identity']}` byte for byte. The scientific report was neither re-executed nor rewritten."
    )
    (target / "viewer.md").write_text(
        _insert_binding_note(viewer, note), encoding="utf-8", newline="\n"
    )
    return version, target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", required=True, type=Path)
    parser.add_argument("--provider", required=True, type=Path)
    parser.add_argument("--skill", required=True)
    parser.add_argument("--candidate-version", required=True)
    parser.add_argument("--provider-commit", required=True)
    args = parser.parse_args()
    version, target = bind_candidate_audit(
        args.records.resolve(),
        args.provider.resolve(),
        args.skill,
        args.candidate_version,
        args.provider_commit,
    )
    print(json.dumps({"version": version, "path": str(target)}))


if __name__ == "__main__":
    main()
