#!/usr/bin/env python3
"""Rebuild the final-pass tracker from worktree, git, checkpoint, and report evidence.

The old ``_final_pass.json`` was a dispatch aid, not evidence.  This command deliberately
does not read its phase marks.  It discovers candidate Skills from the staging repository's
registered ``fix/*`` worktrees, identifies the Skill each branch changed after 2026-09-21,
and writes one evidence row per frontmatter ``name``.

Run from anywhere::

    python tools/build_phase2_manifest.py

The defaults are the Phase 2 recovery locations in ``HANDOFF-codex-phase2.md``.  All writes
are atomic.  The pre-recovery tracker is copied once and never overwritten when the existing
backup is valid JSON.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# A date-only Git --since expression inherits the current clock time.  The recovery
# boundary is the entire Pacific calendar day, so keep the offset explicit.
SINCE = "2026-09-21T00:00:00-07:00"
DEFAULT_STAGING = Path(r"F:\OpenScience\external\mrsonord2240__bioSkills")
DEFAULT_WT_ROOT = Path(r"F:\OpenScience\wt")
DEFAULT_AUDITS_ROOT = Path(r"F:\OpenScience\audits")
DEFAULT_ENVS_ROOT = Path(r"F:\OpenScience\audit-envs")


@dataclass(frozen=True)
class Worktree:
    path: Path
    branch: str
    tip_commit: str


def run_git(repo: Path, *args: str, check: bool = True) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    if check and completed.returncode:
        raise RuntimeError(
            f"git {' '.join(args)} failed in {repo}: {completed.stderr.strip()}"
        )
    return completed.stdout


def registered_worktrees(staging: Path, wt_root: Path) -> list[Worktree]:
    """Read Git's worktree registry; directory enumeration is intentionally not trusted."""
    blocks = run_git(staging, "worktree", "list", "--porcelain").strip().split("\n\n")
    result: list[Worktree] = []
    wt_root_norm = str(wt_root.resolve()).replace("\\", "/").lower().rstrip("/") + "/"
    for block in blocks:
        values: dict[str, str] = {}
        for line in block.splitlines():
            key, _, value = line.partition(" ")
            values[key] = value
        raw_path = values.get("worktree")
        raw_branch = values.get("branch", "")
        if not raw_path or not raw_branch.startswith("refs/heads/fix/"):
            continue
        path = Path(raw_path)
        path_norm = str(path.resolve()).replace("\\", "/").lower().rstrip("/") + "/"
        if not path_norm.startswith(wt_root_norm):
            continue
        result.append(
            Worktree(
                path=path,
                branch=raw_branch.removeprefix("refs/heads/"),
                tip_commit=values["HEAD"],
            )
        )
    return sorted(result, key=lambda worktree: str(worktree.path).lower())


def parse_frontmatter_name(skill_file: Path) -> str | None:
    try:
        text = skill_file.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    if not text.startswith("---"):
        return None
    closing = re.search(r"^---\s*$", text[3:], re.MULTILINE)
    if closing is None:
        return None
    frontmatter = text[3 : 3 + closing.start()]
    match = re.search(r"^name:\s*['\"]?([^'\"\r\n#]+?)['\"]?\s*(?:#.*)?$", frontmatter, re.MULTILINE)
    return match.group(1).strip() if match else None


def commits_and_paths(staging: Path, branch: str, since: str) -> list[tuple[str, list[Path]]]:
    """Return commits and their changed paths after ``since`` on one branch."""
    output = run_git(
        staging,
        "log",
        f"--since={since}",
        "--format=%H",
        "--name-only",
        f"main..{branch}",
    )
    commits: list[tuple[str, list[Path]]] = []
    current: str | None = None
    paths: list[Path] = []
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        if re.fullmatch(r"[0-9a-f]{40}", line):
            if current is not None:
                commits.append((current, paths))
            current, paths = line, []
        elif current is not None:
            paths.append(Path(line))
    if current is not None:
        commits.append((current, paths))
    return commits


def identity_skill_dirs(worktree: Worktree) -> dict[Path, str]:
    """Resolve the intended Skill only from the ``fix/<worktree>`` identity.

    Every worktree is a complete checkout.  In particular, looking at arbitrary changed
    ``SKILL.md`` files can attribute unrelated commits to ``fix/entrez-fetch``.  We instead
    derive the expected folder from the branch name and validate just those candidate files.
    """
    short = worktree.branch.removeprefix("fix/").lower()
    files: set[Path] = set()
    direct = worktree.path / short / "SKILL.md"
    if direct.is_file():
        files.add(direct)
    # These older branch names predate the folder rename to pathway-analysis.  The
    # mapping is deliberately exact and one-way; it is not a fuzzy content search.
    if short.startswith("pathway-"):
        renamed = worktree.path / "pathway-analysis" / short.removeprefix("pathway-") / "SKILL.md"
        if renamed.is_file():
            files.add(renamed)
    for top in worktree.path.iterdir():
        if not top.is_dir() or top.name == ".git":
            continue
        prefix = top.name.lower() + "-"
        if short.startswith(prefix):
            candidate = top / short[len(prefix) :] / "SKILL.md"
            if candidate.is_file():
                files.add(candidate)
        # Bare branch names (for example fix/entrez-fetch) are resolved only as
        # exact child directory names, never by a fuzzy changed-file search.
        candidate = top / short / "SKILL.md"
        if candidate.is_file():
            files.add(candidate)
    result: dict[Path, str] = {}
    for skill_file in files:
        skill_id = parse_frontmatter_name(skill_file)
        if skill_id:
            result[skill_file.parent.relative_to(worktree.path)] = skill_id
    return result


def validate_checkpoint(checkpoint: Path, skill_id: str, worktree: Path) -> tuple[str, dict[str, Any]]:
    if not checkpoint.is_file():
        return "missing", {"reason": "CHECKPOINT.md does not exist"}
    text = checkpoint.read_text(encoding="utf-8", errors="replace")
    expected_title = f"# {skill_id} — final pass checkpoint"
    required_sections = [
        "## Fixed this phase",
        "## Still blocked (needs a decision)",
        "## Ran, not previously verified",
    ]
    reasons: list[str] = []
    if expected_title not in text.splitlines():
        reasons.append(f"missing exact title: {expected_title}")
    # The required template headings may have explanatory suffixes (for example,
    # "Ran, not previously verified this session") and a checkpoint may add a
    # Result/Commit summary.  Its three required sections must nevertheless occur
    # in template order.
    offsets = [text.find(section) for section in required_sections]
    missing = [section for section, offset in zip(required_sections, offsets) if offset < 0]
    if missing:
        reasons.append("missing required section(s): " + ", ".join(missing))
    elif offsets != sorted(offsets):
        reasons.append("required sections are not in template order")

    # The published template does not require a worktree line.  When one is supplied,
    # however, it must name this worktree rather than another Skill's worktree.
    mentioned = re.findall(r"(?:[A-Za-z]:)?[\\/][^\r\n`]*?[\\/]wt[\\/]([^\\/\s`]+)", text, re.IGNORECASE)
    expected_leaf = worktree.name.lower()
    wrong_worktrees = sorted({entry for entry in mentioned if entry.lower() != expected_leaf})
    if mentioned and expected_leaf not in {entry.lower() for entry in mentioned}:
        reasons.append("checkpoint names another worktree: " + ", ".join(wrong_worktrees))
    details = {
        "path": str(checkpoint),
        "worktree_reference": "matched" if expected_leaf in {entry.lower() for entry in mentioned} else (
            "not-stated" if not mentioned else "mismatched"
        ),
        "reasons": reasons,
    }
    return ("ok" if not reasons else "bad"), details


ENV_PREFERENCE_BY_TOP = {
    # These shared folders were tooled in several environments.  The first env listed
    # below has an explicit top-level Scope declaration and is the lane owner used here.
    "experimental-design": "crispr-screen-analyst",
    "pathway-analysis": "crispr-screen-analyst",
    "proteomics": "mass-spec-proteomics-analyst",
    "single-cell": "single-cell-transcriptomics-analyst",
}
ENV_PREFERENCE_BY_FOLDER = {
    "workflows/metabolomics-pipeline": "untargeted-metabolomics-analyst",
    "workflows/proteomics-pipeline": "mass-spec-proteomics-analyst",
}


def env_coverage(envs_root: Path, folder_path: Path) -> tuple[str | None, list[str]]:
    """Select an env only where its TOOLS.md names the Skill's top-level folder.

    A detailed exact-Skill mention wins.  The top-level folder's documented scope is the
    normal shared-env form (for example ``alignment-files`` covers ten Skills).
    """
    if not envs_root.is_dir():
        return None, []
    folder = "/".join(folder_path.parts).lower()
    top = folder_path.parts[0].lower()
    scored: list[tuple[int, str]] = []
    for tools_file in envs_root.glob("*/TOOLS.md"):
        text = tools_file.read_text(encoding="utf-8", errors="replace").lower().replace("\\", "/")
        scope = text[:3000]
        score = 0
        if re.search(rf"(?<![\w/-]){re.escape(folder)}(?=$|[\s`,:;.)])", text):
            score += 100
        # Coverage must appear in the TOOLS.md scope declaration, not merely in a
        # cross-reference or an installed-package table later in the document.
        if f"`{top}/*`" in scope or f"/{top}/" in scope or f" {top} audits" in scope:
            score += 10
        if score:
            scored.append((score, tools_file.parent.name))
    if not scored:
        return None, []
    best = max(score for score, _ in scored)
    candidates = sorted(name for score, name in scored if score == best)
    preferred = ENV_PREFERENCE_BY_FOLDER.get(folder, ENV_PREFERENCE_BY_TOP.get(top))
    if preferred in candidates:
        return preferred, candidates
    return (candidates[0] if len(candidates) == 1 else None), candidates


def report_audits_tip(report: Path, tip_commit: str, folder_path: Path) -> bool:
    try:
        payload = json.loads(report.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return False
    meta = payload.get("meta") if isinstance(payload, dict) else None
    if not isinstance(meta, dict) or meta.get("auditor_independent") is not False:
        return False
    # AUDIT_BRIEF's current schema has source at the top level.  Early reports put
    # it in meta, so retain that compatibility only with the same strict identity
    # check.  A substring is not enough: it could be another branch or Skill.
    source = payload.get("source")
    if not isinstance(source, str):
        source = meta.get("source")
    if not isinstance(source, str):
        return False
    match = re.search(r"@([0-9a-fA-F]{7,40}):([^\s]+)$", source)
    if match is None:
        return False
    source_commit, source_folder = match.groups()
    tip = tip_commit.lower()
    return (
        len(source_commit) >= 7
        and tip.startswith(source_commit.lower())
        and source_folder.replace("\\", "/").rstrip("/") == folder_path.as_posix().rstrip("/")
    )


def phase2_reports(audits_root: Path, skill_id: str, tip_commit: str, folder_path: Path) -> list[Path]:
    report_dir = audits_root / skill_id
    if not report_dir.is_dir():
        return []
    return sorted(
        report
        for report in report_dir.glob("eval_report_*_result.json")
        if report_audits_tip(report, tip_commit, folder_path)
    )


def commit_timestamp(staging: Path, commit: str) -> int:
    raw = run_git(staging, "show", "-s", "--format=%ct", commit)
    try:
        return int(raw.strip())
    except ValueError:
        return 0


def choose_candidate(staging: Path, candidates: list[dict[str, Any]]) -> dict[str, Any]:
    """Deduplicate a frontmatter ID without hiding the competing worktrees."""
    return max(
        candidates,
        key=lambda item: (
            bool(item["phase2_report"]),
            len(item["phase1_commits"]),
            commit_timestamp(staging, item["tip_commit"]),
            item["worktree"].lower(),
        ),
    )


def atomic_json_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="\n", dir=path.parent, delete=False, suffix=".tmp"
    ) as handle:
        json.dump(value, handle, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    temporary.replace(path)


def is_valid_tracker(path: Path) -> bool:
    try:
        return isinstance(json.loads(path.read_text(encoding="utf-8")), list)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return False


def preserve_tracker_once(tracker: Path, backup: Path) -> str:
    if not tracker.exists():
        return "tracker-missing"
    if backup.exists():
        if is_valid_tracker(backup):
            return "backup-already-valid"
        raise RuntimeError(f"refusing to overwrite invalid existing backup: {backup}")
    if not is_valid_tracker(tracker):
        raise RuntimeError(f"refusing to back up invalid tracker JSON: {tracker}")
    shutil.copy2(tracker, backup)
    return "backup-created"


def build_manifest(args: argparse.Namespace) -> tuple[list[dict[str, Any]], str]:
    worktrees = registered_worktrees(args.staging, args.wt_root)
    by_skill: dict[str, list[dict[str, Any]]] = defaultdict(list)
    unresolved: list[dict[str, Any]] = []

    for worktree in worktrees:
        all_dirs = identity_skill_dirs(worktree)
        commits = commits_and_paths(args.staging, worktree.branch, args.since)
        if len(all_dirs) != 1:
            unresolved.append(
                {
                    "worktree": str(worktree.path),
                    "branch": worktree.branch,
                    "reason": "branch identity does not resolve exactly one valid SKILL.md",
                    "candidate_folder_paths": sorted(str(path) for path in all_dirs),
                }
            )
            continue
        folder_path = next(iter(all_dirs))
        skill_id = all_dirs[folder_path]
        # Restrict the commit list to this one Skill.  A branch with no recorded Phase 1
        # commit is purposely eligible for redo-p1, never inferred from the old tracker.
        phase1_commits = [
            commit
            for commit, paths in commits
            if any(changed == folder_path or folder_path in changed.parents for changed in paths)
        ]
        checkpoint_path = args.audits_root / "_final_pass" / skill_id / "CHECKPOINT.md"
        checkpoint, checkpoint_validation = validate_checkpoint(checkpoint_path, skill_id, worktree.path)
        env, env_candidates = env_coverage(args.envs_root, folder_path)
        env_resolution = (
            "missing-tools-coverage"
            if env is None and not env_candidates
            else ("single-scope" if len(env_candidates) == 1 else "shared-scope-preference")
        )
        reports = phase2_reports(args.audits_root, skill_id, worktree.tip_commit, folder_path)
        phase2_report = bool(reports)
        status = "p2-done" if phase2_report else (
            "ready" if checkpoint == "ok" and phase1_commits else "redo-p1"
        )
        by_skill[skill_id].append(
            {
                "skill_id": skill_id,
                "worktree": str(worktree.path),
                "branch": worktree.branch,
                "folder_path": folder_path.as_posix(),
                "tip_commit": worktree.tip_commit,
                "phase1_commits": phase1_commits,
                "env": env,
                "env_candidates": env_candidates,
                "env_resolution": env_resolution,
                "checkpoint": checkpoint,
                "checkpoint_validation": checkpoint_validation,
                "phase2_report": phase2_report,
                "phase2_report_paths": [str(report) for report in reports],
                "status": status,
            }
        )

    manifest: list[dict[str, Any]] = []
    for skill_id in sorted(by_skill):
        candidates = by_skill[skill_id]
        selected = choose_candidate(args.staging, candidates)
        if len(candidates) > 1:
            selected = dict(selected)
            selected["duplicate_worktrees"] = [
                {
                    "worktree": candidate["worktree"],
                    "branch": candidate["branch"],
                    "tip_commit": candidate["tip_commit"],
                    "phase1_commit_count": len(candidate["phase1_commits"]),
                }
                for candidate in sorted(candidates, key=lambda item: item["worktree"].lower())
                if candidate["worktree"] != selected["worktree"]
            ]
        manifest.append(selected)
    if unresolved:
        raise RuntimeError(
            "refusing to write a dispatch manifest with unresolved worktree identities:\n"
            + json.dumps(unresolved, indent=2)
        )
    return manifest, preserve_tracker_once(args.tracker, args.backup)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staging", type=Path, default=DEFAULT_STAGING)
    parser.add_argument("--wt-root", type=Path, default=DEFAULT_WT_ROOT)
    parser.add_argument("--audits-root", type=Path, default=DEFAULT_AUDITS_ROOT)
    parser.add_argument("--envs-root", type=Path, default=DEFAULT_ENVS_ROOT)
    parser.add_argument("--since", default=SINCE)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_WT_ROOT / "_phase2_manifest.json")
    parser.add_argument("--tracker", type=Path, default=DEFAULT_WT_ROOT / "_final_pass.json")
    parser.add_argument(
        "--backup", type=Path, default=DEFAULT_WT_ROOT / "_final_pass.pre-20260922.json"
    )
    args = parser.parse_args(argv)
    manifest, backup_action = build_manifest(args)
    atomic_json_write(args.manifest, manifest)
    # _final_pass is intentionally an operational projection of the manifest, not a source.
    atomic_json_write(args.tracker, manifest)
    counts: dict[str, int] = defaultdict(int)
    for row in manifest:
        if row.get("skill_id"):
            counts[row["status"]] += 1
    print(json.dumps({"backup": backup_action, "counts": dict(sorted(counts.items())), "rows": len(manifest)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
