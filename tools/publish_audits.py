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
                    [--specialist ID=viable | --specialist ID=not-viable:<failing gate>]

Afterwards regenerate the index: npm run audits:index

Re-running is safe: each version folder is replaced.

AUDITS and SPECIALIST_SRC are the live working area on F: where auditors run — raw outputs and
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
PRE_FIX_RE = re.compile(r"^_pre-fix-20\d\d-?\d\d-?\d\d$")
FIXES = os.path.join(REPO_ROOT, "fixes")
SPECIALIST_SRC = os.environ.get("OASS_SPECIALIST_SRC", "F:/OpenScience/specialist-src")

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
UPSTREAM_CLONE = os.environ.get("OASS_UPSTREAM_CLONE", "F:/OpenScience/external/GPTomics__bioSkills")
CLONES = {"GPTomics/bioSkills": UPSTREAM_CLONE, "mrsonord2240/bioSkills": FORK_CLONE}
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
    if not base or not os.path.isdir(os.path.join(FORK_CLONE, ".git")):
        return None
    result = subprocess.run(
        ["git", "diff", "--quiet", base["commit"], source["commit"], "--", source["path"]],
        cwd=FORK_CLONE, capture_output=True)
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


def header(skill_id, source, report):
    lines = [
        f"> **Audit record for `{skill_id}`**",
        f"> - Skill authored by [{source['author']}]({source['author_url']}); audited version "
        f"[{source['repository']}@{source['commit'][:7]}]({source['url']}) ({source['license']}).",
    ]
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
        f"> - Performed on {report.get('meta', {}).get('evaluated_on')} by {PERFORMED_BY}, commissioned by "
        f"{COMMISSIONED_BY}. Not reviewed or endorsed by the Skill's authors.",
        "> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. "
        "Local paths below refer to the auditor's workstation.",
        "",
    ]
    return "\n".join(lines)


def publish_version(repo, skill_id, folder, report_name, script_dirs, supersedes, fixes_path, scripts_folder=None,
                    script_window=(None, None)):
    report_path = os.path.join(folder, report_name)
    report = read_json(report_path)
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
    if fixes_present:
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

    record = {
        "skill_id": skill_id,
        "version": name,
        "source": source,
        "audit": {
            "method": AUDIT_METHOD,
            "evaluator_version": report.get("meta", {}).get("evaluator_version"),
            "audited_on": report.get("meta", {}).get("evaluated_on"),
            "performed_by": PERFORMED_BY,
            "commissioned_by": COMMISSIONED_BY,
            "test_data": "synthetic",
        },
        "supersedes": supersedes,
        "files": {"report": "report.json", "viewer": "viewer.md", "fixes": "fixes.md" if fixes_present else None,
                  "scripts": len(scripts) + carried},
    }
    write_text(os.path.join(target, "record.json"), json.dumps(record, indent=2) + "\n")
    return name, len(scripts) + carried


def find_archive(skill_id, report_name, current):
    """The pre-fix report this audit supersedes, or None if this is the Skill's first audit.

    Each fix round archives the reports it is about to replace under its own `_pre-fix-<date>/`, so
    the folder to read is the newest one holding a report for this Skill that audits a different
    commit from the current one. Pinning a single date here meant a later round published its
    re-audits as first audits, with no `supersedes` link and no pre-fix record.
    """
    current_commit = parse_source(read_json(os.path.join(current, report_name)), current)["commit"]
    for archive in sorted((d for d in os.listdir(AUDITS) if PRE_FIX_RE.match(d)), reverse=True):
        archived = os.path.join(AUDITS, archive, skill_id)
        path = os.path.join(archived, report_name)
        if not os.path.isfile(path):
            continue
        if parse_source(read_json(path), archived)["commit"] != current_commit:
            return archived
        raise SystemExit(f"{skill_id}: {archive} and the current report audit the same commit")
    return None


def publish_skill(repo, skill_id):
    current = os.path.join(AUDITS, skill_id)
    report_name = f"eval_report_{skill_id}_result.json"
    archived = find_archive(skill_id, report_name, current)
    work_dirs = sorted(d for d in os.listdir(current)
                       if RUN_DIR_RE.match(d) and os.path.isdir(os.path.join(current, d)))
    data = ["data"] if os.path.isdir(os.path.join(current, "data")) else []
    fix_log = os.path.join(FIXES, f"{skill_id}.md")

    supersedes = None
    if archived:
        # The archive holds only the reports; both audits' run scripts are still in the live folder,
        # sometimes in one shared folder and sometimes in two. Split by modification time against the
        # archived report, which was copied after the first audit finished and before the re-audit
        # began — never by folder name. Auditors have used runs/ and run/ in different rounds, and a
        # name-based rule silently gave the superseded record no scripts at all.
        cutoff = os.path.getmtime(os.path.join(archived, report_name))
        pre_dirs = post_dirs = work_dirs + data
        pre_window, post_window = (cutoff, None), (None, cutoff)
        supersedes, _ = publish_version(repo, skill_id, archived, report_name, pre_dirs, None, None,
                                        scripts_folder=current, script_window=pre_window)
    else:
        # Nothing superseded, so this record is the only one: it carries every run folder.
        post_dirs = work_dirs + data
        post_window = (None, None)
    source = parse_source(read_json(os.path.join(current, report_name)), current)
    name, count = publish_version(repo, skill_id, current, report_name, post_dirs, supersedes,
                                  fix_log if source.get("fork_of") else None, script_window=post_window)
    return supersedes, name, count


def publish_specialist(repo, spec):
    specialist_id, _, verdict_text = spec.partition("=")
    verdict, _, gate = verdict_text.partition(":")
    if verdict not in ("viable", "not-viable"):
        raise SystemExit(f"--specialist {spec}: verdict must be viable or not-viable[:gate]")
    source_dir = os.path.join(SPECIALIST_SRC, specialist_id)
    target = os.path.join(repo, "audits", "specialists", specialist_id)
    os.makedirs(target, exist_ok=True)
    with open(os.path.join(source_dir, "AUDIT.md"), encoding="utf-8") as f:
        write_text(os.path.join(target, "AUDIT.md"), f.read().replace("\r\n", "\n"))
    recorded_on = None
    match = re.search(r"\b(20\d\d-\d\d-\d\d)\b", open(os.path.join(target, "AUDIT.md"), encoding="utf-8").read())
    if match:
        recorded_on = match.group(1)
    write_text(os.path.join(target, "verdict.json"), json.dumps({
        "specialist_id": specialist_id,
        "verdict": verdict.replace("-", " "),
        "failing_gate": gate or None,
        "recorded_on": recorded_on,
    }, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--skill", action="append", default=[])
    parser.add_argument("--specialist", action="append", default=[])
    args = parser.parse_args()
    for skill_id in args.skill:
        supersedes, name, count = publish_skill(args.repo, skill_id)
        print(f"{skill_id}: {name} ({count} scripts)" + (f", supersedes {supersedes}" if supersedes else ""))
    for spec in args.specialist:
        publish_specialist(args.repo, spec)
        print(f"specialist {spec}")


if __name__ == "__main__":
    main()
