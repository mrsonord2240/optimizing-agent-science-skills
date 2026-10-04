"""Reconcile published-shelf metadata without rewriting published Skill bytes.

Consolidated contract (Sam, 2026-09-27):

* ``GPTomics/bioSkills@d91ed3d`` is a read-only upstream used only for provenance.
* ``optimized-scientific-skills`` is the provider and the sole source of shipped bytes.
* Existing provenance rows are carried forward. A provider Skill without a provenance row is
  appended only when its latest *published records-repo audit* is deployable, has no open P0 or
  veto, names a provider commit on the ancestry of provider ``main``, and the Skill tree at
  ``main`` exactly matches the audited commit.
* ``--apply`` writes only PROVENANCE.json, REMAINING.json, and REMAINING.md. It never copies,
  deletes, or rebuilds ``skills/``.

The marketplace gate remains metadata-only. This tool never writes release manifests, submission
state, marketplace intake trees, or provider ``authoring/`` content.
"""

import argparse
import atexit
import copy
import difflib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

REC = Path("F:/optimizing-agent-science-skills")
UPSTREAM = REC / "external" / "GPTomics__bioSkills"
UPSTREAM_COMMIT = "d91ed3d563019e649dc854c56ccd62551359488a"
OUT = Path("F:/optimized-scientific-skills")
PROVIDER_REF = "main"
PROVIDER_REPOSITORY = "mrsonord2240/optimized-scientific-skills"
MARKETPLACE_HOLDS = REC / "config" / "marketplace_submission_holds.json"
USAGE = Path("catalog") / "usage.json"

VALID_CATEGORIES = {
    "Evidence Insight",
    "Protocol Design",
    "Data Analysis",
    "Academic Writing",
    "Other",
}
DECLARATION_LINES = {
    "license: MIT",
    "author: GPTomics",
    *(f"category: {category}" for category in VALID_CATEGORIES),
}


class PromotionResult:
    def __init__(self, provenance, remaining, remaining_md, messages, added):
        self.provenance = provenance
        self.remaining = remaining
        self.remaining_md = remaining_md
        self.messages = messages
        self.added = added


def grade_for_score(score):
    """Return the canonical AIPOCH MedSkillAudit release disposition."""
    if score >= 85:
        return "Production Ready"
    if score >= 75:
        return "Limited Release"
    if score >= 60:
        return "Beta Only"
    return "Reject"


def load_marketplace_holds(path=MARKETPLACE_HOLDS):
    """Read deliberate marketplace submission holds, failing closed when malformed."""
    path = Path(path)
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"cannot load marketplace holds from {path}: {exc}") from exc
    if document.get("schema_version") != 1 or not isinstance(document.get("holds"), list):
        raise SystemExit(f"{path}: expected schema_version 1 and a holds array")
    holds = {}
    required_scope = {"marketplace_submission", "marketplace_intake"}
    for hold in document["holds"]:
        if not isinstance(hold, dict):
            raise SystemExit(f"{path}: every hold must be an object")
        sid, reason, scope = hold.get("id"), hold.get("reason"), hold.get("scope")
        if (not isinstance(sid, str) or not sid or not isinstance(reason, str) or not reason
                or not isinstance(scope, list) or not required_scope.issubset(scope)):
            raise SystemExit(f"{path}: holds need id, reason, and both marketplace scopes")
        if sid in holds:
            raise SystemExit(f"{path}: duplicate hold for {sid}")
        holds[sid] = hold
    return holds


def set_marketplace_status(row, hold, source_category_ready=True):
    """Apply the existing marketplace gate without touching submission or release state."""
    row["marketplace_ready"] = (
        row.get("grade") == "Production Ready"
        and row.get("fix_pass") == "done"
        and row.get("reaudit") == "not needed"
        and source_category_ready
        and hold is None
    )
    if hold:
        row["marketplace_hold"] = copy.deepcopy(hold)
    else:
        row.pop("marketplace_hold", None)


def _git(repo, *args, check=True, binary=False):
    result = subprocess.run(
        ["git", *args], cwd=repo, capture_output=True,
        text=not binary, encoding=None if binary else "utf-8",
        errors=None if binary else "replace",
        check=False,
    )
    if check and result.returncode:
        stderr = result.stderr.decode("utf-8", "replace") if binary else result.stderr
        raise SystemExit(
            f"git -C {repo} {' '.join(args)} failed ({result.returncode}): {stderr.strip()}"
        )
    return result


def _resolve(repo, ref):
    return _git(repo, "rev-parse", "--verify", ref).stdout.strip()


def tree_fingerprint(repo, ref, path):
    """Return the exact Git tree/blob object id at ``ref:path``."""
    result = _git(repo, "rev-parse", f"{ref}:{path}", check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def _tree_bytes(repo, ref, prefix):
    """Return relative path -> blob bytes for a committed subtree."""
    listed = _git(repo, "ls-tree", "-r", "--name-only", "-z", ref, "--", prefix,
                  binary=True).stdout
    paths = [part.decode("utf-8") for part in listed.split(b"\0") if part]
    normalized_prefix = prefix.rstrip("/") + "/"
    blobs = {}
    for path in paths:
        if not path.startswith(normalized_prefix):
            continue
        relative = path[len(normalized_prefix):]
        blobs[relative] = _git(repo, "show", f"{ref}:{path}", binary=True).stdout
    return blobs


def _declarations_only(upstream, provider):
    try:
        before = upstream.decode("utf-8").splitlines()
        after = provider.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        return False
    for line in difflib.ndiff(before, after):
        if line.startswith("- "):
            return False
        if line.startswith("+ ") and line[2:].strip() not in DECLARATION_LINES:
            return False
    return True


def classify_across_repositories(provider_repo, provider_ref, provider_path,
                                 upstream_repo, upstream_commit, upstream_path):
    """Classify committed provider bytes relative to pinned upstream across repositories."""
    provider = _tree_bytes(provider_repo, provider_ref, provider_path)
    upstream = _tree_bytes(upstream_repo, upstream_commit, upstream_path)
    if not provider:
        raise SystemExit(f"{provider_repo}:{provider_ref}:{provider_path}: empty Skill tree")
    if not upstream:
        raise SystemExit(f"{upstream_repo}:{upstream_commit}:{upstream_path}: empty upstream tree")
    changed = sorted(path for path in set(provider) | set(upstream)
                     if provider.get(path) != upstream.get(path))
    if not changed:
        return "unmodified", []
    if changed == ["SKILL.md"] and _declarations_only(
            upstream["SKILL.md"], provider["SKILL.md"]):
        return "declarations-only", changed
    return "modified", changed


def _read_json(path, label):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"cannot load {label} from {path}: {exc}") from exc


def load_latest_audits(records_repo=REC):
    """Load the one unsuperseded audit per Skill from canonical records-repo evidence."""
    root = Path(records_repo) / "audits" / "skills"
    latest = {}
    if not root.is_dir():
        return latest
    for skill_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        versions = {}
        for version_dir in sorted(path for path in skill_dir.iterdir() if path.is_dir()):
            record_path = version_dir / "record.json"
            report_path = version_dir / "report.json"
            if not record_path.is_file() or not report_path.is_file():
                continue
            record = _read_json(record_path, "audit record")
            report = _read_json(report_path, "audit report")
            version = record.get("version")
            if record.get("skill_id") != skill_dir.name or version != version_dir.name:
                raise SystemExit(
                    f"{version_dir}: record identifies {record.get('skill_id')}/{version}"
                )
            versions[version] = {
                "skill_id": skill_dir.name,
                "version": version,
                "record": record,
                "report": report,
            }
        if not versions:
            continue
        superseded = set()
        for version, entry in versions.items():
            predecessor = entry["record"].get("supersedes")
            if predecessor:
                if predecessor not in versions:
                    raise SystemExit(
                        f"{skill_dir}/{version}: supersedes missing version {predecessor}"
                    )
                superseded.add(predecessor)
        candidates = [entry for version, entry in versions.items() if version not in superseded]
        if len(candidates) != 1:
            raise SystemExit(
                f"{skill_dir}: expected one latest audit, found {len(candidates)}"
            )
        latest[skill_dir.name] = candidates[0]
    return latest


def _skill_index(repo, ref):
    """Map frontmatter Skill ids to committed Skill paths."""
    result = _git(repo, "ls-tree", "-r", "--name-only", ref).stdout
    index = {}
    for path in result.splitlines():
        if not path.endswith("/SKILL.md"):
            continue
        head = _git(repo, "show", f"{ref}:{path}").stdout[:4000]
        match = re.search(r"^name:\s*(.+)$", head, re.MULTILINE)
        if not match:
            continue
        skill_id = match.group(1).strip().strip("\"'")
        skill_path = path[:-len("/SKILL.md")]
        if skill_id in index and index[skill_id] != skill_path:
            raise SystemExit(f"{repo}:{ref}: duplicate Skill id {skill_id}")
        index[skill_id] = skill_path
    return index


def _source_category(repo, ref, path, required=True):
    head = _git(repo, "show", f"{ref}:{path}/SKILL.md").stdout
    matches = re.findall(r"^category:\s*(.+)$", head, re.MULTILINE)
    if not matches and not required:
        return None
    if len(matches) != 1:
        raise SystemExit(f"{repo}:{ref}:{path}/SKILL.md: expected one category field")
    category = matches[0].strip().strip("\"'")
    if category not in VALID_CATEGORIES:
        raise SystemExit(f"{repo}:{ref}:{path}/SKILL.md: invalid category {category!r}")
    return category


def _open_p0(report):
    return sum(
        1 for recommendation in report.get("recommendations", [])
        if str(recommendation.get("priority", "")).upper() == "P0"
    )


def _veto_reason(report):
    gates = report.get("veto_gates")
    if not isinstance(gates, dict):
        return "missing veto gates"
    skill_gate = gates.get("skill_veto", {}).get("gate")
    research_gate = gates.get("research_veto", {}).get("gate")
    if skill_gate != "PASS":
        return f"skill veto gate is {skill_gate!r}"
    if research_gate not in {"PASS", "N/A", "NOT_APPLICABLE"}:
        return f"research veto gate is {research_gate!r}"
    return None


def _candidate_eligibility(skill_id, entry, provider_repo, provider_ref):
    record, report = entry["record"], entry["report"]
    source = record.get("source", {})
    final = report.get("final", {})
    if source.get("repository") != PROVIDER_REPOSITORY:
        return False, f"latest audit is not a provider audit ({source.get('repository')!r})"
    commit = source.get("commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        return False, "latest provider audit has no full commit"
    expected_path = f"skills/{skill_id}"
    if source.get("path") != expected_path:
        return False, f"audit path is {source.get('path')!r}, expected {expected_path!r}"
    if final.get("deployable") is not True:
        return False, "latest audit is not deployable"
    if final.get("grade") != grade_for_score(final.get("score", -1)):
        return False, "latest audit grade does not match its score"
    p0 = _open_p0(report)
    if p0:
        return False, f"latest audit has {p0} open P0 recommendation(s)"
    veto = _veto_reason(report)
    if veto:
        return False, f"latest audit has a veto: {veto}"
    if _git(provider_repo, "cat-file", "-e", f"{commit}^{{commit}}", check=False).returncode:
        return False, f"audited provider commit {commit[:12]} is unavailable"
    if _git(provider_repo, "merge-base", "--is-ancestor", commit, provider_ref,
            check=False).returncode:
        return False, f"audited provider commit {commit[:12]} is not an ancestor of {provider_ref}"
    audited_tree = tree_fingerprint(provider_repo, commit, expected_path)
    current_tree = tree_fingerprint(provider_repo, provider_ref, expected_path)
    if not audited_tree or audited_tree != current_tree:
        return False, "current provider Skill bytes differ from the audited commit"
    return True, "eligible"


def _catalog_paths(provenance, remaining, upstream_index):
    catalog = {}
    groups = [
        provenance.get("skills", []),
        remaining.get("remaining", []),
        remaining.get("excluded", []),
        remaining.get("out_of_scope", []),
    ]
    for rows in groups:
        if not isinstance(rows, list):
            raise SystemExit("provider metadata arrays must be lists")
        for row in rows:
            skill_id, path = row.get("id"), row.get("upstream_path")
            if not skill_id:
                raise SystemExit("provider metadata row is missing id")
            if path:
                if skill_id in catalog and catalog[skill_id] != path:
                    raise SystemExit(f"conflicting upstream paths for {skill_id}")
                catalog[skill_id] = path
    for skill_id, path in upstream_index.items():
        catalog.setdefault(skill_id, path)
    return catalog


def _audit_date(row):
    value = row.get("audited_on")
    return value if isinstance(value, str) else ""


def _load_usage(records_repo):
    """Load the usage_rank.py snapshot as Skill id -> row, or {} when none has been written."""
    path = Path(records_repo) / USAGE
    if not path.is_file():
        return {}
    return _read_json(path, "usage snapshot")["skills"]


def _render_remaining(remaining, finished, catalog, usage=None):
    usage = usage or {}

    def score(skill_id):
        return usage.get(skill_id, {}).get("score", 0)

    pending = remaining["remaining"]
    excluded = remaining["excluded"]
    out_of_scope = remaining["out_of_scope"]
    by = {}
    for row in pending:
        folder = row["upstream_path"].split("/", 1)[0]
        by.setdefault(folder, []).append(row["id"])
    done = {}
    for row in finished:
        folder = row["upstream_path"].split("/", 1)[0]
        done[folder] = done.get(folder, 0) + 1
    needs_fix = [row for row in finished if row.get("fix_pass") == "needed"]
    stale = [row for row in finished if row.get("reaudit") == "needed"]
    source_commit = remaining["source"].split("@", 1)[-1]
    lines = [
        "# Remaining Skills", "",
        "Not yet refined. Scope is deliberately limited to the rest of",
        "[GPTomics/bioSkills](https://github.com/GPTomics/bioSkills) at commit",
        f"`{source_commit}`; other source corpora are out of scope for now.", "",
        f"**{len(pending)} remaining** across {len(by)} folders. {len(finished)} are already refined and live in `skills/`.", "",
        (
            f"The source tree holds {remaining['reconciliation']['skills_in_source_tree']} Skills: "
            f"{len(finished)} refined, {len(excluded)} audited and excluded, "
            f"{len(out_of_scope)} out of scope, {len(pending)} remaining."
        ), "",
    ]
    if usage:
        mean = {folder: sum(map(score, ids)) / len(ids) for folder, ids in by.items()}
        lines += [
            "Folders are ordered by `usage`, the mean score of their remaining Skills. A score is",
            "0-100: half conda downloads of the Skill's primary tool, half how many workflow Skills",
            "depend on it. It is a proxy from `tools/usage_rank.py` in the records repository, not",
            "measured use.", "",
            "| folder | remaining | refined | usage |", "| --- | ---: | ---: | ---: |",
        ]
        for folder in sorted(by, key=lambda name: (-mean[name], name)):
            lines.append(
                f"| {folder} | {len(by[folder])} | {done.get(folder, 0)} | {mean[folder]:.0f} |"
            )
    else:
        lines += ["| folder | remaining | refined |", "| --- | ---: | ---: |"]
        for folder in sorted(by, key=lambda name: (-len(by[name]), name)):
            lines.append(f"| {folder} | {len(by[folder])} | {done.get(folder, 0)} |")
    lines += [
        "", "## Promoted, fix pass still needed", "",
        "These Skills are in `skills/` because their audit found them deployable with no open P0.",
        "They have not yet been through a fix pass, however high they scored. Their open findings",
        "are in the audit record. `fix_pass` in PROVENANCE.json carries the same flag.", "",
        "| skill | score | grade |", "| --- | ---: | --- |",
    ]
    for row in needs_fix:
        lines.append(f"| `{row['id']}` | {row['score']} | {row['grade']} |")
    lines += [
        "", "## Promoted, re-audit still needed", "",
        "Changed in the provider after its latest audit, so the score describes earlier bytes.",
        "`reaudit` in PROVENANCE.json carries the same flag.", "",
        "| skill | score at last audit | audited on |", "| --- | ---: | --- |",
    ]
    for row in stale:
        lines.append(f"| `{row['id']}` | {row['score']} | {row.get('audited_on')} |")
    lines += [
        "", "## Audited and excluded", "",
        "Audited and did not pass. Not pending — rejected until the defects behind the score are",
        "fixed.", "", "| skill | score | grade | open P0 |",
        "| --- | ---: | --- | ---: |",
    ]
    for row in excluded:
        lines.append(
            f"| `{row['id']}` | {row.get('score')} | {row.get('grade')} | {row.get('open_p0')} |"
        )
    lines += ["", "## Out of scope", "", "| skill | reason |", "| --- | --- |"]
    for row in out_of_scope:
        lines.append(f"| `{row['id']}` | {row.get('reason')} |")
    lines += ["", "## The list", ""]
    for folder in sorted(by):
        lines += [f"### {folder}", ""]
        for skill_id in sorted(by[folder], key=lambda name: (-score(name), name)):
            line = f"- `{skill_id}` — `{catalog[skill_id]}`"
            row = usage.get(skill_id)
            if row:
                line += f" — usage {row['score']:.0f} ({row['primary_tool']}"
                if row["workflow_fan_in"]:
                    plural = "" if row["workflow_fan_in"] == 1 else "s"
                    line += f", in {row['workflow_fan_in']} workflow{plural}"
                line += ")"
            lines.append(line)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_metadata(records_repo=REC, provider_repo=OUT, upstream_repo=UPSTREAM,
                   upstream_commit=UPSTREAM_COMMIT, holds_path=MARKETPLACE_HOLDS,
                   provider_ref=PROVIDER_REF):
    """Build a deterministic metadata reconciliation plan without writing any repository."""
    records_repo = Path(records_repo)
    provider_repo = Path(provider_repo)
    upstream_repo = Path(upstream_repo)
    provenance_path = provider_repo / "PROVENANCE.json"
    remaining_path = provider_repo / "REMAINING.json"
    provenance = _read_json(provenance_path, "provider provenance")
    remaining = _read_json(remaining_path, "provider remaining inventory")
    if provenance.get("schema_version") != 1 or remaining.get("schema_version") != 1:
        raise SystemExit("provider metadata must use schema_version 1")

    _resolve(provider_repo, provider_ref)
    provider_skills_tree = tree_fingerprint(provider_repo, provider_ref, "skills")
    if not provider_skills_tree:
        raise SystemExit(f"{provider_repo}:{provider_ref}: provider has no skills tree")
    upstream_commit = _resolve(upstream_repo, upstream_commit)
    provider_index = _skill_index(provider_repo, provider_ref)
    upstream_index = _skill_index(upstream_repo, upstream_commit)
    existing_rows = copy.deepcopy(provenance.get("skills"))
    if not isinstance(existing_rows, list):
        raise SystemExit(f"{provenance_path}: skills must be an array")
    existing = {}
    for row in existing_rows:
        skill_id = row.get("id")
        if not skill_id or skill_id in existing:
            raise SystemExit(f"{provenance_path}: missing or duplicate Skill id {skill_id!r}")
        existing[skill_id] = row
    missing_provider = sorted(set(existing) - set(provider_index))
    if missing_provider:
        raise SystemExit("provenance Skill(s) missing from provider main: "
                         + ", ".join(missing_provider))

    latest = load_latest_audits(records_repo)
    holds = load_marketplace_holds(holds_path)
    unknown_holds = sorted(set(holds) - set(provider_index))
    if unknown_holds:
        raise SystemExit("marketplace hold(s) do not name provider Skills: "
                         + ", ".join(unknown_holds))
    catalog = _catalog_paths(provenance, remaining, upstream_index)
    messages, added = [], []
    rows = existing_rows
    for skill_id in sorted(set(provider_index) - set(existing)):
        entry = latest.get(skill_id)
        if entry is None:
            messages.append(f"skipping {skill_id}: no published audit record")
            continue
        eligible, reason = _candidate_eligibility(skill_id, entry, provider_repo, provider_ref)
        if not eligible:
            messages.append(f"skipping {skill_id}: {reason}")
            continue
        upstream_path = catalog.get(skill_id)
        if not upstream_path:
            raise SystemExit(f"{skill_id}: no upstream path in provider metadata or upstream tree")
        record, report = entry["record"], entry["report"]
        category = report.get("meta", {}).get("category")
        if category not in VALID_CATEGORIES:
            raise SystemExit(f"{skill_id}: audit has invalid category {category!r}")
        declared = _source_category(
            provider_repo, provider_ref, provider_index[skill_id], required=False
        )
        if declared is not None and declared != category:
            raise SystemExit(
                f"{skill_id}: provider category {declared!r} does not match audit {category!r}"
            )
        kind, files = classify_across_repositories(
            provider_repo, provider_ref, provider_index[skill_id],
            upstream_repo, upstream_commit, upstream_path,
        )
        final = report["final"]
        fix_log = records_repo / "fixes" / f"{skill_id}.md"
        row = {
            "id": skill_id,
            "upstream_path": upstream_path,
            "score": final["score"],
            "grade": final["grade"],
            "deployable": True,
            "open_p0": 0,
            "audited_on": record.get("audit", {}).get("audited_on")
                          or report.get("meta", {}).get("evaluated_on"),
            "fix_log": f"fixes/{skill_id}.md" if fix_log.is_file() else None,
            "fix_pass": "done" if fix_log.is_file() else "needed",
            "category": category,
            "reaudit": "not needed",
            "relative_to_upstream": kind,
            "changed_files": files,
        }
        rows.append(row)
        added.append(skill_id)
        messages.append(
            f"adding {skill_id}: audited {record['source']['commit'][:12]}, bytes match {provider_ref}"
        )

    # Existing rows, including their already-published marketplace disposition, are preserved.
    # A fix summary may land after the first provider-metadata reconciliation, so allow that
    # one-way records completion to move ``fix_pass`` from needed to done. Recomputing every
    # historical row would mutate the release state of already-pinned Marketplace submissions.
    for row in rows:
        hold = holds.get(row["id"])
        fix_log = records_repo / "fixes" / f"{row['id']}.md"
        completed_fix_record = row.get("fix_pass") == "needed" and fix_log.is_file()
        if completed_fix_record:
            row["fix_log"] = f"fixes/{row['id']}.md"
            row["fix_pass"] = "done"
            messages.append(f"completing fix-pass metadata for {row['id']}")
        if row["id"] not in added and not completed_fix_record:
            if hold:
                row["marketplace_ready"] = False
                row["marketplace_hold"] = copy.deepcopy(hold)
            continue
        declared = _source_category(
            provider_repo, provider_ref, provider_index[row["id"]], required=False
        )
        category_ready = declared == row.get("category")
        set_marketplace_status(row, hold, category_ready)
        if declared is None:
            messages.append(
                f"holding marketplace readiness for {row['id']}: provider frontmatter has no category"
            )
    rows.sort(key=lambda row: row["id"])
    finished_ids = {row["id"] for row in rows}

    new_provenance = copy.deepcopy(provenance)
    new_provenance["generated"] = max((_audit_date(row) for row in rows), default="")
    sources = new_provenance.setdefault("sources", {})
    source = copy.deepcopy(sources.get("gptomics-bioskills", {}))
    source.update({
        "upstream_repository": "https://github.com/GPTomics/bioSkills",
        "upstream_commit": upstream_commit,
        "upstream_licence": "MIT",
        "upstream_status": "archived 2026-08-15; accepts no issues or pull requests",
        "provider_repository": "https://github.com/mrsonord2240/optimized-scientific-skills",
        "provider_ref": provider_ref,
        # A tree id stays stable across later metadata-only commits, so repeated reconciliation is
        # idempotent while still pinning the exact shipped Skill bytes represented by this document.
        "provider_skills_tree": provider_skills_tree,
    })
    source.pop("staging_repository", None)
    source.pop("staging_commit", None)
    sources["gptomics-bioskills"] = source
    new_provenance["skills"] = rows

    new_remaining = copy.deepcopy(remaining)
    for key in ("remaining", "excluded", "out_of_scope"):
        values = new_remaining.get(key)
        if not isinstance(values, list):
            raise SystemExit(f"{remaining_path}: {key} must be an array")
        if key != "out_of_scope":
            values = [row for row in values if row.get("id") not in finished_ids]
        new_remaining[key] = sorted(values, key=lambda row: row["id"])
    new_remaining["generated"] = new_provenance["generated"]
    new_remaining["source"] = f"GPTomics/bioSkills@{upstream_commit}"
    new_remaining["reconciliation"] = {
        "skills_in_source_tree": len(upstream_index),
        "refined": len(rows),
        "audited_and_excluded": len(new_remaining["excluded"]),
        "out_of_scope": len(new_remaining["out_of_scope"]),
        "remaining": len(new_remaining["remaining"]),
    }
    accounted = (len(rows) + len(new_remaining["excluded"])
                 + len(new_remaining["out_of_scope"]) + len(new_remaining["remaining"]))
    if accounted != len(upstream_index):
        raise SystemExit(
            f"metadata accounts for {accounted} Skills but upstream has {len(upstream_index)}"
        )
    remaining_md = _render_remaining(new_remaining, rows, catalog, _load_usage(records_repo))
    return PromotionResult(new_provenance, new_remaining, remaining_md, messages, added)


def _atomic_write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def write_metadata(provider_repo, result):
    """Write exactly the three generated metadata files; never touch ``skills/``."""
    provider_repo = Path(provider_repo)
    _atomic_write(
        provider_repo / "PROVENANCE.json",
        json.dumps(result.provenance, indent=2, ensure_ascii=False) + "\n",
    )
    _atomic_write(
        provider_repo / "REMAINING.json",
        json.dumps(result.remaining, indent=2, ensure_ascii=False) + "\n",
    )
    _atomic_write(provider_repo / "REMAINING.md", result.remaining_md)


def acquire_promote_lock(provider_repo=OUT, timeout=600, poll=2):
    """Acquire an atomic metadata-reconciliation lock."""
    lock_dir = Path(provider_repo) / ".promote.lock"
    waited = 0
    while True:
        try:
            lock_dir.mkdir()
            break
        except FileExistsError:
            if waited >= timeout:
                raise SystemExit(
                    f"{lock_dir}: another promote_skills.py --apply holds this lock "
                    f"(waited {timeout}s)"
                )
            time.sleep(poll)
            waited += poll
    atexit.register(lambda: shutil.rmtree(lock_dir, ignore_errors=True))


def _assert_safe_apply_tree(provider_repo, provider_ref):
    head = _resolve(provider_repo, "HEAD")
    target = _resolve(provider_repo, provider_ref)
    if head != target:
        raise SystemExit(f"--apply requires checked-out {provider_ref}; HEAD is {head[:12]}")
    protected = ["skills", "PROVENANCE.json", "REMAINING.json", "REMAINING.md"]
    status = _git(provider_repo, "status", "--porcelain=v1", "--", *protected).stdout.strip()
    if status:
        raise SystemExit("--apply requires clean Skill and metadata paths:\n" + status)


def _parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write the three provider metadata files")
    parser.add_argument("--records", type=Path, default=REC)
    parser.add_argument("--provider", type=Path, default=OUT)
    parser.add_argument("--provider-ref", default=PROVIDER_REF)
    parser.add_argument("--upstream", type=Path, default=UPSTREAM)
    parser.add_argument("--upstream-commit", default=UPSTREAM_COMMIT)
    parser.add_argument("--holds", type=Path, default=MARKETPLACE_HOLDS)
    return parser


def main(argv=None):
    args = _parser().parse_args(argv)
    if args.apply:
        acquire_promote_lock(args.provider)
        _assert_safe_apply_tree(args.provider, args.provider_ref)
    result = build_metadata(
        args.records, args.provider, args.upstream, args.upstream_commit,
        args.holds, args.provider_ref,
    )
    for message in result.messages:
        print(message)
    print(f"refined  : {len(result.provenance['skills'])}")
    print(f"added    : {len(result.added)} {result.added}")
    print(f"excluded : {len(result.remaining['excluded'])}")
    print(f"remaining: {len(result.remaining['remaining'])}")
    ready = sum(1 for row in result.provenance["skills"] if row.get("marketplace_ready"))
    print(f"marketplace ready metadata: {ready}")
    if not args.apply:
        print("\nDRY RUN — no files written; pass --apply to write metadata only")
        return
    write_metadata(args.provider, result)
    print("\nwrote PROVENANCE.json, REMAINING.json, and REMAINING.md; skills/ was untouched")


if __name__ == "__main__":
    main()
