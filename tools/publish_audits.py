#!/usr/bin/env python3
"""Publish finished skill-auditor records into this repository.

Each audited Skill version lands in audits/skills/<skill-id>/<owner>-<repo>@<sha7>/ with:
  record.json  provenance: Skill source and author, audit method, who performed it, what it supersedes
  report.json  the skill-auditor report, unchanged
  viewer.md    the eval viewer, with a provenance header prepended
  fixes.md     for modified versions: the fix log for that version
  scripts/     the scripts the auditor wrote and ran (synthetic data and run outputs stay local)

Usage:
  publish_audits.py --repo F:/optimizing-agent-science-skills --skill ID [--skill ID ...]
  publish_audits.py --repo F:/optimizing-agent-science-skills --skill ID \
      --run-dir F:/OpenScience/audits/ID/initial-RUN \
      [--artifact run_cases.py --artifact data/input.tsv ...]

Afterwards regenerate the index: npm run audits:index

Re-running is safe: each version folder is replaced.

AUDITS is the live working area on F: where auditors run — raw outputs and
generated data stay there and are never published. FIXES is this repository's own fix logs.
"""
import argparse
import json
import os
import re
import shutil
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDITS = os.environ.get("OASS_AUDITS", "F:/OpenScience/audits")
# A second fix round on the same day archives under a letter suffix: _pre-fix-20260917b.
PRE_FIX_RE = re.compile(r"^_pre-fix-(20\d\d)-?(\d\d)-?(\d\d)([a-z]?)$")
FIXES = os.path.join(REPO_ROOT, "fixes")

SOURCE_RE = re.compile(r"^(?P<repository>[\w.-]+/[\w.-]+)@(?P<commit>[0-9a-f]{7,40}):(?P<path>.+)$")
UPSTREAM_BIOSKILLS = {"repository": "GPTomics/bioSkills", "commit": "d91ed3d563019e649dc854c56ccd62551359488a"}
REPOSITORIES = {
    "GPTomics/bioSkills": {"author": "GPTomics", "author_url": "https://github.com/GPTomics", "license": "MIT"},
    "mrsonord2240/bioSkills": {
        "author": "GPTomics",
        "author_url": "https://github.com/GPTomics",
        "license": "MIT",
        "modified_by": "Samuel Nord",
        "fork_of": UPSTREAM_BIOSKILLS,
    },
    "mrsonord2240/optimized-scientific-skills": {
        "author": "GPTomics",
        "author_url": "https://github.com/GPTomics",
        "license": "MIT",
        "modified_by": "Samuel Nord",
        "fork_of": UPSTREAM_BIOSKILLS,
    },
}
AUDIT_METHOD = {
    "name": "skill-auditor",
    "author": "AIPOCH",
    "repository": "aipoch/medical-research-skills",
    "commit": "f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26",
    "path": "skill-auditor",
    "license": "MIT",
}
AUDIT_METHOD["url"] = f"https://github.com/{AUDIT_METHOD['repository']}/tree/{AUDIT_METHOD['commit']}/{AUDIT_METHOD['path']}"
PERFORMED_BY = "Claude (Anthropic) auditor agents"
COMMISSIONED_BY = "Samuel Nord"
RUN_DIR_RE = re.compile(r"^(run|rerun|pass)\w*$")
FORK_CLONE = os.environ.get("OASS_FORK_CLONE", "F:/OpenScience/external/mrsonord2240__bioSkills")
UPSTREAM_CLONE = os.environ.get("OASS_UPSTREAM_CLONE", "F:/optimizing-agent-science-skills/external/GPTomics__bioSkills")
OPTIMIZED_CLONE = os.environ.get("OASS_OPTIMIZED_CLONE", "F:/optimized-scientific-skills")
CLONES = {
    "GPTomics/bioSkills": UPSTREAM_CLONE,
    "mrsonord2240/bioSkills": FORK_CLONE,
    "mrsonord2240/optimized-scientific-skills": OPTIMIZED_CLONE,
}
ALWAYS_MODIFIED_REPOSITORIES = {"mrsonord2240/optimized-scientific-skills"}
SCRIPT_EXTENSIONS = {".py", ".R", ".r", ".sh", ".ctl"}
MAX_SCRIPT_BYTES = 100_000


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def full_commit(repository, commit, where):
    """Expand an abbreviated commit to its full sha against the local clone.

    Auditors write the sha their dispatch gave them, which is often the 7-character form. Records are
    filed and cross-referenced by commit, so an abbreviation has to be resolved once, here, rather
    than left to mean two different things in two records.
    """
    if len(commit) == 40:
        return commit
    clone = CLONES.get(repository)
    if not clone or not os.path.isdir(os.path.join(clone, ".git")):
        raise SystemExit(f"{where}: source gives the abbreviated commit {commit} and there is no "
                         f"clone of {repository} to expand it against")
    result = subprocess.run(["git", "rev-parse", commit + "^{commit}"],
                            cwd=clone, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"{where}: {commit} is not a commit in {clone}")
    return result.stdout.strip()


def parse_source(report, where):
    raw = report.get("source") or report.get("meta", {}).get("source")
    match = SOURCE_RE.match(raw or "")
    if not match:
        raise SystemExit(f"{where}: unrecognised source {raw!r}")
    source = match.groupdict()
    if source["repository"] not in REPOSITORIES:
        raise SystemExit(f"{where}: no author/license known for {source['repository']}")
    source["commit"] = full_commit(source["repository"], source["commit"], where)
    source.update(REPOSITORIES[source["repository"]])
    source["url"] = f"https://github.com/{source['repository']}/tree/{source['commit']}/{source['path']}"
    return source


def version_name(source):
    return f"{source['repository'].replace('/', '-')}@{source['commit'][:7]}"


def fork_modifies(source):
    """Does the audited fork commit actually change this Skill's files from its upstream base?

    A fix log on disk does not answer this: it may describe fixes committed *after* the commit that
    was audited, in which case the audited content is still upstream's. Returns None when the fork
    clone is unavailable, leaving the caller to fall back on the fix log.
    """
    base = source.get("fork_of")
    if source["repository"] in ALWAYS_MODIFIED_REPOSITORIES:
        # The published shelf was created with independent history and normalized
        # `skills/<id>` paths, so its commit cannot be diffed against the upstream
        # repository's original path. Every shelf record is intentionally treated
        # as a modified derivative and retains its upstream attribution below.
        return True
    clone = CLONES.get(source["repository"])
    if not base or not clone or not os.path.isdir(os.path.join(clone, ".git")):
        return None
    result = subprocess.run(
        ["git", "diff", "--quiet", base["commit"], source["commit"], "--", source["path"]],
        cwd=clone, capture_output=True)
    if result.returncode == 0:
        return False
    if result.returncode == 1:
        return True
    return None


def resolve_identity(source, fixes_present):
    """The version a record is filed under.

    A Skill whose audited fork commit does not change its files is byte-identical to upstream at the
    fork's base commit, so the audited *content* is upstream's. Filing it under the fork commit
    would claim a modification that does not exist, so it is filed under upstream and the fork
    checkout it was read from is recorded separately.
    """
    modified = fork_modifies(source)
    if not source.get("fork_of") or (fixes_present if modified is None else modified):
        return source, version_name(source)
    base = source["fork_of"]
    upstream = dict(source)
    upstream.pop("fork_of", None)
    upstream.pop("modified_by", None)
    upstream["repository"] = base["repository"]
    upstream["commit"] = base["commit"]
    upstream["url"] = f"https://github.com/{base['repository']}/tree/{base['commit']}/{source['path']}"
    upstream["audited_from"] = {
        "repository": source["repository"],
        "commit": source["commit"],
        "url": source["url"],
        "unchanged_from_upstream": True,
    }
    return upstream, version_name(upstream)


def collect_scripts(folder, subdirectories, modified_before=None, modified_after=None):
    found = []
    for sub in subdirectories:
        base = os.path.join(folder, sub)
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = sorted(d for d in dirnames if d != "__pycache__")
            for name in sorted(filenames):
                path = os.path.join(dirpath, name)
                if os.path.splitext(name)[1] not in SCRIPT_EXTENSIONS or os.path.getsize(path) > MAX_SCRIPT_BYTES:
                    continue
                mtime = os.path.getmtime(path)
                if modified_before is not None and mtime >= modified_before:
                    continue
                if modified_after is not None and mtime < modified_after:
                    continue
                found.append((os.path.relpath(path, folder).replace(os.sep, "/"), path))
    return found


def header(skill_id, source, report, candidate=None):
    performed_by = report.get("meta", {}).get("performed_by", PERFORMED_BY)
    lines = [
        f"> **Audit record for `{skill_id}`**",
    ]
    if candidate:
        lines += [
            f"> - Audited working candidate `{candidate['identity']}`; exact candidate provenance is in "
            "[source-identity.json](source-identity.json).",
            f"> - Derived from [{source['repository']}@{source['commit'][:7]}]({source['url']}), authored by "
            f"[{source['author']}]({source['author_url']}) ({source['license']}).",
        ]
    else:
        lines.append(
            f"> - Skill authored by [{source['author']}]({source['author_url']}); audited version "
            f"[{source['repository']}@{source['commit'][:7]}]({source['url']}) ({source['license']})."
        )
    if source.get("fork_of"):
        base = source["fork_of"]
        lines.append(
            f"> - Modified by {source['modified_by']} from "
            f"[{base['repository']}@{base['commit'][:7]}](https://github.com/{base['repository']}/tree/{base['commit']}); "
            "every change is listed in [fixes.md](fixes.md)."
        )
    elif source.get("audited_from"):
        fork = source["audited_from"]
        lines.append(
            f"> - Read from [{fork['repository']}@{fork['commit'][:7]}]({fork['url']}), a fork in which this "
            "Skill's files are unchanged from upstream; the audited content is upstream's."
        )
    lines += [
        f"> - Audit method: [{AUDIT_METHOD['name']}]({AUDIT_METHOD['url']}) by {AUDIT_METHOD['author']} "
        f"({AUDIT_METHOD['license']}), {report.get('meta', {}).get('evaluator_version', 'skill-auditor')}.",
        f"> - Performed on {report.get('meta', {}).get('evaluated_on')} by {performed_by}, commissioned by "
        f"{COMMISSIONED_BY}. Not reviewed or endorsed by the Skill's authors.",
        "> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. "
        "Local paths below refer to the auditor's workstation.",
        "",
    ]
    return "\n".join(lines)


def _modular_source(identity, where):
    origin = identity.get("origin")
    if not isinstance(origin, dict):
        raise SystemExit(f"{where}: source-identity.json has no origin object")
    repository = origin.get("repository")
    commit = origin.get("commit")
    path = origin.get("path")
    if repository not in REPOSITORIES:
        raise SystemExit(f"{where}: no author/license known for {repository!r}")
    if not re.fullmatch(r"[0-9a-f]{40}", str(commit or "")):
        raise SystemExit(f"{where}: origin commit must be a full 40-character SHA")
    if not isinstance(path, str) or not path.strip():
        raise SystemExit(f"{where}: origin path is missing")
    source = {"repository": repository, "commit": commit, "path": path}
    source.update(REPOSITORIES[repository])
    source["url"] = f"https://github.com/{repository}/tree/{commit}/{path}"
    if origin.get("subtree"):
        source["subtree"] = origin["subtree"]
    return source


def _modular_candidate(identity, where):
    raw = identity.get("candidate")
    if not isinstance(raw, dict):
        raise SystemExit(f"{where}: source-identity.json has no candidate object")
    value = raw.get("content_sha256") or raw.get("sha256") or raw.get("digest") or raw.get("subtree")
    value = str(value or "").lower()
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", value):
        raise SystemExit(
            f"{where}: candidate needs a 40-character tree id or 64-character content SHA-256"
        )
    candidate = {
        "identity": value,
        "identity_kind": "git-tree" if len(value) == 40 else "sha256-manifest",
    }
    for key in ("branch", "commit", "subtree", "content_sha256", "path"):
        if raw.get(key) is not None:
            candidate[key] = raw[key]
    files = identity.get("files")
    if isinstance(files, list):
        candidate["files"] = files
    return candidate


def _latest_published_version(repo, skill_id):
    root = os.path.join(repo, "audits", "skills", skill_id)
    if not os.path.isdir(root):
        return None
    records = {}
    superseded = set()
    for version in sorted(os.listdir(root)):
        record_path = os.path.join(root, version, "record.json")
        if not os.path.isfile(record_path):
            continue
        record = read_json(record_path)
        if record.get("skill_id") != skill_id or record.get("version") != version:
            raise SystemExit(f"{record_path}: record identity does not match its directory")
        records[version] = record
        if record.get("supersedes"):
            superseded.add(record["supersedes"])
    latest = [version for version in records if version not in superseded]
    if len(latest) > 1:
        raise SystemExit(f"{root}: expected at most one latest version, found {len(latest)}")
    return latest[0] if latest else None


def _modular_artifacts(run_dir, artifacts):
    selected = []
    root = os.path.realpath(run_dir)
    for relative in artifacts:
        normalized = relative.replace("\\", "/").lstrip("/")
        if not normalized or normalized == ".." or normalized.startswith("../") or "/../" in normalized:
            raise SystemExit(f"{run_dir}: unsafe artifact path {relative!r}")
        path = os.path.realpath(os.path.join(root, *normalized.split("/")))
        try:
            inside = os.path.commonpath([root, path]) == root
        except ValueError:
            inside = False
        if not inside or not os.path.isfile(path):
            raise SystemExit(f"{run_dir}: artifact is missing or outside the run root: {relative!r}")
        if os.path.getsize(path) > MAX_SCRIPT_BYTES:
            raise SystemExit(f"{path}: artifact exceeds {MAX_SCRIPT_BYTES} bytes")
        selected.append((normalized, path))
    if len({relative for relative, _ in selected}) != len(selected):
        raise SystemExit(f"{run_dir}: duplicate --artifact path")
    return selected


def _same_bytes(first, second):
    with open(first, "rb") as left, open(second, "rb") as right:
        return left.read() == right.read()


def publish_modular(repo, skill_id, run_dir, artifacts):
    """Publish one explicit modular audit run without rewriting its strict report schema."""
    run_dir = os.path.abspath(run_dir)
    report_path = os.path.join(run_dir, "report.json")
    viewer_path = os.path.join(run_dir, "viewer.md")
    identity_path = os.path.join(run_dir, "source-identity.json")
    for path in (report_path, viewer_path, identity_path):
        if not os.path.isfile(path):
            raise SystemExit(f"{run_dir}: required modular audit file missing: {os.path.basename(path)}")

    report = read_json(report_path)
    meta = report.get("meta", {})
    if meta.get("skill_name") != skill_id:
        raise SystemExit(
            f"{report_path}: report names {meta.get('skill_name')!r}, expected {skill_id!r}"
        )
    identity = read_json(identity_path)
    source = _modular_source(identity, identity_path)
    candidate = _modular_candidate(identity, identity_path)
    label = re.sub(r"[^A-Za-z0-9._-]+", "-", os.path.basename(run_dir)).strip("-")
    if not label:
        raise SystemExit(f"{run_dir}: cannot derive a safe run label")
    version = f"candidate@{candidate['identity'][:12]}-{label}"
    target = os.path.join(repo, "audits", "skills", skill_id, version)

    selected = _modular_artifacts(run_dir, artifacts)
    if os.path.isdir(target):
        existing_report = os.path.join(target, "report.json")
        existing_identity = os.path.join(target, "source-identity.json")
        if (
            os.path.isfile(existing_report)
            and os.path.isfile(existing_identity)
            and _same_bytes(existing_report, report_path)
            and _same_bytes(existing_identity, identity_path)
        ):
            record = read_json(os.path.join(target, "record.json"))
            return version, record.get("files", {}).get("scripts", 0)
        raise SystemExit(f"{target}: existing modular record differs; refusing to overwrite")

    supersedes = _latest_published_version(repo, skill_id)
    os.makedirs(target)
    with open(viewer_path, encoding="utf-8") as f:
        viewer = f.read().replace("\r\n", "\n")
    write_text(os.path.join(target, "viewer.md"), header(skill_id, source, report, candidate) + "\n" + viewer)
    shutil.copyfile(report_path, os.path.join(target, "report.json"))
    shutil.copyfile(identity_path, os.path.join(target, "source-identity.json"))
    for relative, path in selected:
        destination = os.path.join(target, "scripts", *relative.split("/"))
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.copyfile(path, destination)

    performed_by = meta.get("performed_by", PERFORMED_BY)
    audit_record = {
        "method": AUDIT_METHOD,
        "evaluator_version": meta.get("evaluator_version"),
        "audited_on": meta.get("evaluated_on"),
        "performed_by": performed_by,
        "commissioned_by": COMMISSIONED_BY,
        "test_data": "see published scripts and inputs",
    }
    if "auditor_independent" in meta:
        audit_record["auditor_independent"] = meta["auditor_independent"]
    record = {
        "skill_id": skill_id,
        "version": version,
        "source": source,
        "candidate": candidate,
        "audit": audit_record,
        "supersedes": supersedes,
        "files": {
            "report": "report.json",
            "viewer": "viewer.md",
            "source_identity": "source-identity.json",
            "fixes": None,
            "scripts": len(selected),
        },
    }
    write_text(os.path.join(target, "record.json"), json.dumps(record, indent=2) + "\n")
    return version, len(selected)


def publish_version(repo, skill_id, folder, report_name, script_dirs, supersedes, fixes_path, scripts_folder=None,
                    script_window=(None, None)):
    report_path = os.path.join(folder, report_name)
    report = read_json(report_path)
    performed_by = report.get("meta", {}).get("performed_by", PERFORMED_BY)
    source = parse_source(report, report_path)
    fixes_present = bool(fixes_path and os.path.isfile(fixes_path))
    source, name = resolve_identity(source, fixes_present)
    # Filed under upstream: the audited commit changes nothing here, so any fix log on disk
    # describes work that landed after this audit and does not belong to this record.
    fixes_present = fixes_present and bool(source.get("fork_of"))
    if name == supersedes:
        raise SystemExit(
            f"{skill_id}: {name} would overwrite the superseded record — the fork version is unchanged "
            "from upstream, so both resolve to the same version. Expected a fix log at "
            f"{fixes_path}."
        )
    target = os.path.join(repo, "audits", "skills", skill_id, name)
    # Republishing must not lose evidence. A superseded record's scripts frequently no longer exist
    # in the live audit folder, because the re-audit reused that folder and overwrote them, so
    # rebuilding the record purely from what is on F: today silently deletes the first audit's work.
    # Keep anything already published that this run cannot re-derive.
    published_before = {}
    existing_record = None
    existing_fixes = None
    existing_record_path = os.path.join(target, "record.json")
    existing_fixes_path = os.path.join(target, "fixes.md")
    if os.path.isfile(existing_record_path):
        existing_record = read_json(existing_record_path)
    if os.path.isfile(existing_fixes_path):
        with open(existing_fixes_path, "rb") as f:
            existing_fixes = f.read()
    previous_scripts = os.path.join(target, "scripts")
    if os.path.isdir(previous_scripts):
        for dirpath, _, filenames in os.walk(previous_scripts):
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                relative = os.path.relpath(path, previous_scripts).replace(os.sep, "/")
                with open(path, "rb") as f:
                    published_before[relative] = f.read()
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)

    viewer_path = os.path.join(folder, f"eval_viewer_{skill_id}.md")
    with open(viewer_path, encoding="utf-8") as f:
        viewer = f.read().replace("\r\n", "\n")
    write_text(os.path.join(target, "viewer.md"), header(skill_id, source, report) + "\n" + viewer)
    shutil.copyfile(report_path, os.path.join(target, "report.json"))
    if existing_fixes is not None:
        with open(os.path.join(target, "fixes.md"), "wb") as f:
            f.write(existing_fixes)
    elif fixes_present:
        with open(fixes_path, encoding="utf-8") as f:
            write_text(os.path.join(target, "fixes.md"), f.read().replace("\r\n", "\n"))

    scripts = collect_scripts(scripts_folder or folder, script_dirs, *script_window)
    republished = set()
    for relative, path in scripts:
        destination = os.path.join(target, "scripts", *relative.split("/"))
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.copyfile(path, destination)
        republished.add(relative)
    carried = 0
    for relative, blob in sorted(published_before.items()):
        if relative in republished:
            continue
        destination = os.path.join(target, "scripts", *relative.split("/"))
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        with open(destination, "wb") as f:
            f.write(blob)
        carried += 1

    audit_record = {
        "method": AUDIT_METHOD,
        "evaluator_version": report.get("meta", {}).get("evaluator_version"),
        "audited_on": report.get("meta", {}).get("evaluated_on"),
        "performed_by": performed_by,
        "commissioned_by": COMMISSIONED_BY,
        "test_data": "synthetic",
    }
    if "auditor_independent" in report.get("meta", {}):
        audit_record["auditor_independent"] = report["meta"]["auditor_independent"]
    record = {
        "skill_id": skill_id,
        "version": name,
        "source": source,
        "audit": audit_record,
        "supersedes": supersedes,
        "files": {"report": "report.json", "viewer": "viewer.md", "fixes": "fixes.md" if fixes_present else None,
                  "scripts": len(scripts) + carried},
    }
    if existing_record is not None:
        # Republishing an already-recorded version may recover scripts, but it
        # must not rewrite that historical version's provenance or chain edge.
        record["source"] = existing_record.get("source", record["source"])
        record["audit"] = existing_record.get("audit", record["audit"])
        record["supersedes"] = existing_record.get("supersedes")
    write_text(os.path.join(target, "record.json"), json.dumps(record, indent=2) + "\n")
    return name, len(scripts) + carried


def archive_order(name):
    year, month, day, suffix = PRE_FIX_RE.match(name).groups()
    return year + month + day, suffix


def find_archives(skill_id, report_name, current):
    """The pre-fix audits the current one supersedes, oldest first; empty for a Skill's first audit.

    Each fix round archives the audit it is about to replace under its own `_pre-fix-<date>/`, and a
    Skill can go through several rounds, so every archive holding a report for it is a link in one
    chain. Taking only the newest archive published a three-audit chain as two and silently dropped
    the middle record.
    """
    chain = [os.path.join(AUDITS, archive, skill_id)
             for archive in sorted((d for d in os.listdir(AUDITS) if PRE_FIX_RE.match(d)), key=archive_order)
             if os.path.isfile(os.path.join(AUDITS, archive, skill_id, report_name))]
    folders = chain + [current]
    commits = [parse_source(read_json(os.path.join(f, report_name)), f)["commit"] for f in folders]
    for earlier, later, folder in zip(commits, commits[1:], folders[1:]):
        if earlier == later:
            raise SystemExit(f"{skill_id}: {folder} audits the same commit as the audit it supersedes")
    return chain


def script_dirs(folder):
    dirs = sorted(d for d in os.listdir(folder) if RUN_DIR_RE.match(d) and os.path.isdir(os.path.join(folder, d)))
    return dirs + (["data"] if os.path.isdir(os.path.join(folder, "data")) else [])


def publish_skill(repo, skill_id):
    current = os.path.join(AUDITS, skill_id)
    report_name = f"eval_report_{skill_id}_result.json"
    chain = find_archives(skill_id, report_name, current)
    fix_log = os.path.join(FIXES, f"{skill_id}.md")
    live_dirs = script_dirs(current)

    supersedes = None
    after = None
    for folder in chain + [current]:
        if folder == current:
            # The live folder: split by time only if the audit before it left its scripts here.
            dirs, scripts_folder, window = live_dirs, current, (None, after)
        elif script_dirs(folder):
            # A whole-folder snapshot: that audit's scripts are exactly the ones archived with it. The
            # re-audit rewrites the live copies, so their times say nothing about the earlier audit.
            dirs, scripts_folder, window = script_dirs(folder), folder, (None, None)
            after = None
        else:
            # A reports-only archive: its scripts are still in the live folder, sometimes in one shared
            # folder and sometimes in two. Split by modification time against the archived report,
            # which was copied after that audit finished and before the next began — never by folder
            # name. Auditors have used runs/ and run/ in different rounds, and a name-based rule
            # silently gave the superseded record no scripts at all.
            cutoff = os.path.getmtime(os.path.join(folder, report_name))
            dirs, scripts_folder, window = live_dirs, current, (cutoff, after)
            after = cutoff
        source = parse_source(read_json(os.path.join(folder, report_name)), folder)
        name, count = publish_version(repo, skill_id, folder, report_name, dirs, supersedes,
                                      fix_log if source.get("fork_of") else None,
                                      scripts_folder=scripts_folder, script_window=window)
        previous, supersedes = supersedes, name
    return previous, name, count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--skill", action="append", default=[])
    parser.add_argument(
        "--run-dir",
        help="explicit modular audit root containing report.json, viewer.md, and source-identity.json",
    )
    parser.add_argument(
        "--artifact",
        action="append",
        default=[],
        help="run-root-relative saved script or input to publish (repeatable; modular mode only)",
    )
    args = parser.parse_args()
    if args.run_dir:
        if len(args.skill) != 1:
            parser.error("--run-dir requires exactly one --skill")
        name, count = publish_modular(args.repo, args.skill[0], args.run_dir, args.artifact)
        print(f"{args.skill[0]}: {name} ({count} scripts/inputs)")
        return
    if args.artifact:
        parser.error("--artifact requires --run-dir")
    for skill_id in args.skill:
        supersedes, name, count = publish_skill(args.repo, skill_id)
        print(f"{skill_id}: {name} ({count} scripts)" + (f", supersedes {supersedes}" if supersedes else ""))


if __name__ == "__main__":
    main()
