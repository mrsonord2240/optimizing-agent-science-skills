"""Export finished bio-derived Skills from the optimized shelf into bioSkills-Improved.

Contract (Sam, 2026-09-28 and 2026-09-30):

* ``optimized-scientific-skills`` stays the sole editing source. ``bioSkills-Improved`` is a
  bioSkills-shaped fork generated one way from it and is never edited directly.
* A Skill is exported when its committed PROVENANCE.json row is deployable, has no open P0, has a
  finished fix pass, and needs no re-audit. Marketplace holds do not apply to the fork.
* ``skills/<id>`` on the shelf lands at the row's ``upstream_path`` in the fork. The Skill tree is
  moved as Git objects, so the fork receives the exact committed bytes, and files the shelf
  dropped are dropped from the fork. Fork Skills with no finished row are left alone.
* The shelf is committed from Windows and carries no executable bits, so a file the fork already
  marks executable stays executable and a mode-only difference is not a change.
* Without ``--apply`` nothing is written. ``--apply`` forms one fork commit, or none when the fork
  already matches. ``--push`` publishes that commit.
"""

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

OUT = Path("F:/optimized-scientific-skills")
FORK = Path("F:/OpenScience/bioSkills-Improved")
FORK_URL = "https://github.com/mrsonord2240/bioSkills-Improved.git"
PROVIDER_REF = "main"
FORK_BRANCH = "main"
PROVIDER_NAME = "optimized-scientific-skills"
FORK_PATH = re.compile(r"[a-z0-9][a-z0-9-]*/[a-z0-9][a-z0-9-]*")


def _git(repo, *args, check=True):
    result = subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, encoding="utf-8",
        errors="replace", check=False,
    )
    if check and result.returncode:
        raise SystemExit(
            f"git -C {repo} {' '.join(args)} failed ({result.returncode}): {result.stderr.strip()}"
        )
    return result


def _tree(repo, ref, path):
    """Return the Git tree id at ``ref:path``, or None when the path is absent."""
    result = _git(repo, "rev-parse", "--verify", "--quiet", f"{ref}:{path}", check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def _files(repo, ref, path):
    """Return relative path -> (mode, blob id) for the files under ``ref:path``."""
    listed = _git(repo, "ls-tree", "-r", "-z", f"{ref}:{path}", check=False)
    files = {}
    for entry in filter(None, listed.stdout.split("\0")) if listed.returncode == 0 else ():
        meta, name = entry.split("\t", 1)
        mode, _, blob = meta.split()
        files[name] = (mode, blob)
    return files


def _blobs(files):
    return {name: blob for name, (_, blob) in files.items()}


def is_finished(row):
    return (
        row.get("deployable") is True
        and row.get("open_p0") == 0
        and row.get("fix_pass") == "done"
        and row.get("reaudit") == "not needed"
    )


def build_plan(provider_repo=OUT, provider_ref=PROVIDER_REF, fork_repo=FORK, fork_ref="HEAD"):
    """Return (changes, unchanged, skipped) for the finished Skills, writing nothing."""
    provider_repo, fork_repo = Path(provider_repo), Path(fork_repo)
    shown = _git(provider_repo, "show", f"{provider_ref}:PROVENANCE.json").stdout
    try:
        rows = json.loads(shown)["skills"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise SystemExit(f"{provider_repo}:{provider_ref}:PROVENANCE.json is unreadable: {exc}")
    changes, unchanged, skipped, claimed = [], [], [], {}
    for row in sorted(rows, key=lambda row: row.get("id", "")):
        skill_id, path = row.get("id"), row.get("upstream_path")
        if not skill_id:
            raise SystemExit("provenance row is missing id")
        if not is_finished(row):
            skipped.append(skill_id)
            continue
        if not isinstance(path, str) or not FORK_PATH.fullmatch(path):
            raise SystemExit(f"{skill_id}: upstream_path {path!r} is not <category>/<skill>")
        if path in claimed:
            raise SystemExit(f"{skill_id} and {claimed[path]} both map to {path}")
        claimed[path] = skill_id
        tree = _tree(provider_repo, provider_ref, f"skills/{skill_id}")
        if not tree:
            raise SystemExit(f"{skill_id}: no skills/{skill_id} at {provider_ref}")
        blobs = _blobs(_files(provider_repo, provider_ref, f"skills/{skill_id}"))
        current = _files(fork_repo, fork_ref, path)
        if _blobs(current) == blobs:
            unchanged.append(skill_id)
            continue
        changes.append({
            "id": skill_id, "path": path, "tree": tree, "blobs": blobs,
            "kind": "updated" if current else "added",
            "executable": sorted(name for name, (mode, _) in current.items()
                                 if mode == "100755" and name in blobs),
        })
    return changes, unchanged, skipped


def _assert_safe_fork(fork_repo, branch):
    if not (fork_repo / ".git").exists():
        raise SystemExit(f"{fork_repo}: no fork checkout; run git clone {FORK_URL} {fork_repo}")
    head = _git(fork_repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if head != branch:
        raise SystemExit(f"{fork_repo}: --apply requires checked-out {branch}; on {head}")
    status = _git(fork_repo, "status", "--porcelain=v1").stdout.strip()
    if status:
        raise SystemExit(f"{fork_repo}: --apply requires a clean fork checkout:\n{status}")
    _git(fork_repo, "fetch", "--quiet", "origin", branch)
    if _git(fork_repo, "rev-parse", "HEAD").stdout != _git(
            fork_repo, "rev-parse", f"origin/{branch}").stdout:
        raise SystemExit(f"{fork_repo}: {branch} differs from origin/{branch}; reconcile first")


def apply_plan(changes, provider_repo=OUT, provider_ref=PROVIDER_REF, fork_repo=FORK,
               trailers=()):
    """Stage every change as exact provider trees, verify them, and commit once."""
    provider_repo, fork_repo = Path(provider_repo), Path(fork_repo)
    commit = _git(provider_repo, "rev-parse", "--verify", provider_ref).stdout.strip()
    # The Skill trees have to exist in the fork's object store before read-tree can place them.
    _git(fork_repo, "fetch", "--quiet", "--no-tags", str(provider_repo), commit)
    for change in changes:
        _git(fork_repo, "rm", "-r", "-q", "--cached", "--ignore-unmatch", "--", change["path"])
        _git(fork_repo, "read-tree", f"--prefix={change['path']}/", change["tree"])
        for name in change["executable"]:
            # --chmod would rehash the stale working file; --cacheinfo keeps the shelf blob.
            _git(fork_repo, "update-index", "--cacheinfo",
                 f"100755,{change['blobs'][name]},{change['path']}/{name}")
    staged = _git(fork_repo, "write-tree").stdout.strip()
    for change in changes:
        if _blobs(_files(fork_repo, staged, change["path"])) != change["blobs"]:
            raise SystemExit(f"{change['id']}: staged fork tree differs from the shelf")
        shutil.rmtree(fork_repo / change["path"], ignore_errors=True)
    _git(fork_repo, "checkout-index", "--force", "--all")
    added = sum(1 for change in changes if change["kind"] == "added")
    subject = f"Update {len(changes)} skills from {PROVIDER_NAME}@{commit[:7]}"
    body = "\n".join(
        [f"{len(changes) - added} updated, {added} added. Exact bytes of skills/<id> at "
         f"{PROVIDER_NAME} {commit}.", ""]
        + [f"- {change['id']} -> {change['path']}" for change in changes]
    )
    args = ["commit", "--quiet", "-m", subject, "-m", body]
    for trailer in trailers:
        args += ["--trailer", trailer]
    _git(fork_repo, *args)
    return _git(fork_repo, "rev-parse", "HEAD").stdout.strip()


def _parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="commit the export in the fork")
    parser.add_argument("--push", action="store_true", help="push the fork after --apply")
    parser.add_argument("--provider", type=Path, default=OUT)
    parser.add_argument("--provider-ref", default=PROVIDER_REF)
    parser.add_argument("--fork", type=Path, default=FORK)
    parser.add_argument("--fork-branch", default=FORK_BRANCH)
    parser.add_argument("--trailer", action="append", default=[],
                        help="commit trailer, repeatable")
    return parser


def main(argv=None):
    args = _parser().parse_args(argv)
    if args.push and not args.apply:
        raise SystemExit("--push requires --apply")
    if args.apply:
        _assert_safe_fork(args.fork, args.fork_branch)
    changes, unchanged, skipped = build_plan(args.provider, args.provider_ref, args.fork)
    for change in changes:
        print(f"{change['kind']:7} {change['id']} -> {change['path']}")
    print(f"to export: {len(changes)}")
    print(f"unchanged: {len(unchanged)}")
    print(f"skipped  : {len(skipped)} {skipped}")
    if not args.apply:
        print("\nDRY RUN — fork untouched; pass --apply to commit, --push to publish")
        return
    if not changes:
        print("\nfork already matches the shelf; no commit made")
        return
    commit = apply_plan(changes, args.provider, args.provider_ref, args.fork, args.trailer)
    print(f"\ncommitted {commit[:12]} in {args.fork}")
    if args.push:
        _git(args.fork, "push", "--quiet", "origin", f"HEAD:{args.fork_branch}")
        print(f"pushed to origin/{args.fork_branch}")


if __name__ == "__main__":
    main()
