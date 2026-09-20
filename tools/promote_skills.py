"""Assemble the optimized-scientific-skills repository.

Contents, per Sam 2026-09-17:
  - every Skill whose latest audit is deployable with no open P0, whatever its score, with
    `fix_pass: needed` marking those not yet through a fix pass
  - a list of what remains, limited for now to the rest of GPTomics/bioSkills

Layout is flat, `skills/<skill-id>/`, so the directory name equals the frontmatter `name` and equals
the marketplace submission `id`. The upstream path is not encoded in the tree; it is recorded per
Skill in PROVENANCE.json, which is the only place provenance should be read from.

Source of Skill bytes is the fork at the pinned commit, not the working tree.
"""
import atexit
import json
import os
import re
import shutil
import subprocess
import sys
import time

REC = "F:/optimizing-agent-science-skills"
FORK = "F:/OpenScience/external/mrsonord2240__bioSkills"
UPSTREAM_COMMIT = "d91ed3d563019e649dc854c56ccd62551359488a"
FORK_COMMIT = "85a3e4de9a56ad5b24911ee7c21a039eb57ef216"
AUDITS = "F:/OpenScience/audits"
OUT = "F:/optimized-scientific-skills"

# Present in the source tree but not candidates for refinement. Recorded in REMAINING.json with the
# reason rather than silently filtered, so the remaining count always reconciles with the tree.
OUT_OF_SCOPE = {
    "clawhub-installer": "upstream's own corpus installer, not a science Skill; declares "
                         "os: darwin/linux only and exists to install the other Skills",
}


def git(args, cwd=FORK):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def staging_tree():
    """Every path in the staging repo at the pinned commit. Never the working tree.

    Reading a working tree here is how the export/source mix-up happens: the tree on disk can be
    ahead of, behind, or unrelated to the commit this promotion claims to be from.
    """
    out = git(["ls-tree", "-r", "--name-only", FORK_COMMIT]).stdout or ""
    return [p for p in out.splitlines() if p]


def skill_index():
    """frontmatter name -> path in the staging repo, read at the pinned commit."""
    idx = {}
    for path in staging_tree():
        if not path.endswith("/SKILL.md"):
            continue
        head = (git(["show", f"{FORK_COMMIT}:{path}"]).stdout or "")[:2000]
        m = re.search(r"^name:\s*(.+)$", head, re.M)
        if m:
            idx[m.group(1).strip().strip("\"'")] = path[: -len("/SKILL.md")]
    return idx


def audits():
    out = {}
    for d in sorted(os.listdir(AUDITS)):
        if d.startswith("_"):
            continue
        p = os.path.join(AUDITS, d, f"eval_report_{d}_result.json")
        if os.path.exists(p):
            out[d] = json.load(open(p, encoding="utf-8"))
    return out


def classify(path):
    """How this Skill differs from the archived upstream, at the pinned fork commit."""
    if git(["diff", "--quiet", UPSTREAM_COMMIT, FORK_COMMIT, "--", path]).returncode == 0:
        return "unmodified", []
    out = git(["diff", "-U0", UPSTREAM_COMMIT, FORK_COMMIT, "--", path]).stdout or ""
    changed = [l for l in out.splitlines()
               if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    files = sorted({l.split("/")[-1] for l in out.splitlines() if l.startswith("+++ b/")})
    if all(l == "+license: MIT" for l in changed):
        return "licence-declaration-only", files
    return "modified", files


def audited_bytes_differ(source, path):
    """True when the bytes at FORK_COMMIT are not the bytes the audit ran on.

    A Skill fixed after its audit but not yet re-audited must not be promoted on the old score. The
    `license: MIT` line added corpus-wide at 558aea5 is the one tolerated difference.
    """
    m = re.match(r"^[\w.-]+/[\w.-]+@([0-9a-f]{7,40}):", source or "")
    if not m:
        return True
    out = git(["diff", "-U0", m.group(1), FORK_COMMIT, "--", path]).stdout or ""
    changed = [l for l in out.splitlines() if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    return any(l != "+license: MIT" for l in changed)


def audit_source_commit(source):
    """The fork commit an audit record was run against, or None for an upstream-sourced record."""
    m = re.match(r"^mrsonord2240/bioSkills(?:-Improved)?@([0-9a-f]{7,40}):", source or "")
    return m.group(1) if m else None


def unmerged_records(rep, idx):
    """Records audited on a fork commit that never landed on the path to FORK_COMMIT.

    Distinct from ordinary staleness (`audited_bytes_differ`, where the fork simply moved on since a
    passing audit — safe to promote with `reaudit: needed`). Here the record's own commit is not an
    ancestor of FORK_COMMIT at all: a re-audit that scored a fix worktree, then declined to land it
    (still failing, or landed by a run that hasn't pushed yet), leaves that better score sitting in
    the canonical report while the Skill's actual bytes at FORK_COMMIT are whatever they were before
    — often not deployable. Promoting on that record's `deployable` flag would ship the old, rejected
    content under the new score. Caught by hand once (bio-geo-data, 2026-09-19); this closes it.
    """
    bad = []
    for sid, r in rep.items():
        if sid not in idx:
            continue
        commit = audit_source_commit(r.get("source") or r.get("meta", {}).get("source"))
        if commit is None:
            continue
        if git(["merge-base", "--is-ancestor", commit, FORK_COMMIT]).returncode != 0:
            bad.append((sid, commit))
    return bad


def acquire_promote_lock(out_dir=OUT, timeout=600, poll=2):
    """Atomic mkdir lock so two concurrent `--apply` runs never race the same rmtree/rebuild of
    `skills/`. Several agents hit this collision by hand on 2026-09-19 (crash mid-rmtree, or one
    run's output silently clobbered by another's) before recovering manually each time. Blocks up
    to `timeout` seconds, then fails loudly rather than racing anyway. Released via atexit so a
    raised SystemExit (e.g. a blob-hash mismatch) still frees it for the next run.
    """
    os.makedirs(out_dir, exist_ok=True)
    lock_dir = os.path.join(out_dir, ".promote.lock")
    waited = 0
    while True:
        try:
            os.mkdir(lock_dir)
            break
        except FileExistsError:
            if waited >= timeout:
                raise SystemExit(
                    f"{lock_dir}: another promote_skills.py --apply run holds this lock "
                    f"(waited {timeout}s). Retry once it finishes, or rmdir it by hand if it's "
                    "stale (its owner crashed without cleaning up).")
            time.sleep(poll)
            waited += poll
    atexit.register(lambda: shutil.rmtree(lock_dir, ignore_errors=True))


def main():
    # Every Skill whose latest audit is deployable with no open P0 is promoted, whatever its score
    # (Sam, 2026-09-17). Skills that have not yet been through a fix pass are promoted too, and are
    # flagged `fix_pass: needed` in PROVENANCE.json and listed in REMAINING.md.
    apply = "--apply" in sys.argv
    if apply:
        acquire_promote_lock()
    idx = skill_index()
    rep = audits()
    fixlogs = {f[:-3] for f in os.listdir(os.path.join(REC, "fixes")) if f.endswith(".md")}

    # Records whose own commit never landed on the path to FORK_COMMIT: skip them entirely this run
    # rather than promoting (or rejecting) on a score that does not describe the published bytes.
    # Everything else still promotes normally. See unmerged_records()'s docstring.
    unmerged = dict(unmerged_records(rep, idx))
    if unmerged:
        for sid, c in unmerged.items():
            print(f"skipping  : {sid} (audited at {c[:8]}, not an ancestor of {FORK_COMMIT[:8]} "
                  "-- that fix has not landed; record does not describe the published bytes)")
        rep = {sid: r for sid, r in rep.items() if sid not in unmerged}

    finished, excluded = [], []
    for sid, r in rep.items():
        if sid not in idx:
            continue
        fin = r["final"]
        p0 = [x for x in r.get("recommendations", []) if str(x.get("priority", "")).upper() == "P0"]
        row = {
            "id": sid,
            "upstream_path": idx[sid],
            "score": fin["score"],
            "grade": fin["grade"],
            "deployable": fin["deployable"],
            "open_p0": len(p0),
            "audited_on": r.get("meta", {}).get("evaluated_on"),
            "fix_log": f"fixes/{sid}.md" if sid in fixlogs else None,
            "fix_pass": "done" if sid in fixlogs else "needed",
        }
        # Changed since its audit (e.g. the 2026-09-16 P2 backlog round, fixed without a re-audit):
        # still promoted, but flagged so the score is never read as describing these bytes.
        row["reaudit"] = ("needed" if audited_bytes_differ(
            r.get("source") or r.get("meta", {}).get("source"), idx[sid]) else "not needed")
        (finished if fin["deployable"] and not p0 else excluded).append(row)

    for row in finished:
        kind, files = classify(row["upstream_path"])
        row["relative_to_upstream"] = kind
        row["changed_files"] = files

    finished.sort(key=lambda r: r["id"])
    excluded.sort(key=lambda r: r["id"])
    remaining = sorted(set(idx) - {r["id"] for r in finished} - {r["id"] for r in excluded}
                       - set(OUT_OF_SCOPE))
    needs_fix = [r for r in finished if r["fix_pass"] == "needed"]

    print(f"finished  : {len(finished)}")
    for k in ("modified", "licence-declaration-only", "unmodified"):
        print(f"   {k:26s} {sum(1 for r in finished if r['relative_to_upstream'] == k)}")
    print(f"   fix pass done              {len(finished) - len(needs_fix)}")
    print(f"   fix pass needed            {len(needs_fix)}")
    print(f"excluded  : {len(excluded)}  {[r['id'] for r in excluded]}")
    stale = [r for r in finished if r["reaudit"] == "needed"]
    print(f"   re-audit needed            {len(stale)}")
    print(f"remaining : {len(remaining)}")

    if not apply:
        print("\nDRY RUN — pass --apply to write the repository")
        return

    os.makedirs(OUT, exist_ok=True)
    sk = os.path.join(OUT, "skills")
    if os.path.isdir(sk):
        shutil.rmtree(sk)
    os.makedirs(sk)
    # Extract from the staging repo at the pinned commit, then verify every promoted file against
    # that commit's blob hashes. A promotion that cannot prove what it copied is not a promotion.
    tree = staging_tree()
    blobs = {}
    for line in (git(["ls-tree", "-r", FORK_COMMIT]).stdout or "").splitlines():
        meta, path = line.split("\t", 1)
        blobs[path] = meta.split()[2]
    promoted = 0
    for row in finished:
        prefix = row["upstream_path"] + "/"
        members = [p for p in tree if p.startswith(prefix)]
        if not members:
            raise SystemExit(f"{row['id']}: nothing at {prefix} in {FORK_COMMIT[:8]}")
        for path in members:
            dst = os.path.join(sk, row["id"], *path[len(prefix):].split("/"))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            data = subprocess.run(["git", "show", f"{FORK_COMMIT}:{path}"], cwd=FORK,
                                  capture_output=True).stdout
            with open(dst, "wb") as f:
                f.write(data)
            actual = subprocess.run(["git", "hash-object", "--stdin"], cwd=FORK,
                                    input=data, capture_output=True, text=False).stdout.decode().strip()
            if actual != blobs[path]:
                raise SystemExit(f"{path}: promoted bytes do not match {FORK_COMMIT[:8]}")
            promoted += 1
    print(f"promoted {promoted} files, each verified against {FORK_COMMIT[:8]} by blob hash")

    json.dump({
        "schema_version": 1,
        "generated": "2026-09-17",
        "note": "Provenance is per Skill. The tree is flat by Skill id; upstream_path records where "
                "each Skill came from in its source repository.",
        "sources": {
            "gptomics-bioskills": {
                "upstream_repository": "https://github.com/GPTomics/bioSkills",
                "upstream_commit": UPSTREAM_COMMIT,
                "upstream_licence": "MIT",
                "upstream_status": "archived 2026-08-15; accepts no issues or pull requests",
                "staging_repository": "https://github.com/mrsonord2240/bioSkills-Improved",
                "staging_commit": FORK_COMMIT,
            }
        },
        "skills": finished,
    }, open(os.path.join(OUT, "PROVENANCE.json"), "w", encoding="utf-8", newline="\n"), indent=2)

    json.dump({"schema_version": 1, "generated": "2026-09-17",
               "source": "GPTomics/bioSkills@" + UPSTREAM_COMMIT,
               "reconciliation": {
                   "skills_in_source_tree": len(idx),
                   "refined": len(finished),
                   "audited_and_excluded": len(excluded),
                   "out_of_scope": len(OUT_OF_SCOPE),
                   "remaining": len(remaining),
               },
               "remaining": [{"id": i, "upstream_path": idx[i]} for i in remaining],
               "excluded": excluded,
               "out_of_scope": [{"id": i, "upstream_path": idx.get(i), "reason": why}
                                for i, why in sorted(OUT_OF_SCOPE.items())]},
              open(os.path.join(OUT, "REMAINING.json"), "w", encoding="utf-8", newline="\n"), indent=2)
    by = {}
    for r in remaining:
        by.setdefault(idx[r].split("/")[0], []).append(r)
    done = {}
    for s in finished:
        done[s["upstream_path"].split("/")[0]] = done.get(s["upstream_path"].split("/")[0], 0) + 1
    L = ["# Remaining Skills", "",
         "Not yet refined. Scope is deliberately limited to the rest of",
         "[GPTomics/bioSkills](https://github.com/GPTomics/bioSkills) at commit",
         f"`{UPSTREAM_COMMIT}`; other source corpora are out of scope for now.", "",
         f"**{len(remaining)} remaining** across {len(by)} folders. {len(finished)} are already "
         "refined and live in `skills/`.", "",
         "The source tree holds "
         f"{len(idx)} Skills: {len(finished)} refined, {len(excluded)} audited and excluded, "
         f"{len(OUT_OF_SCOPE)} out of scope, {len(remaining)} remaining.", "",
         "| folder | remaining | refined |", "| --- | ---: | ---: |"]
    for f in sorted(by, key=lambda f: (-len(by[f]), f)):
        L.append(f"| {f} | {len(by[f])} | {done.get(f, 0)} |")
    L += ["", "## Promoted, fix pass still needed", "",
          "These Skills are in `skills/` because their audit found them deployable with no open P0.",
          "They have not yet been through a fix pass, however high they scored. Their open findings",
          "are in the audit record. `fix_pass` in PROVENANCE.json carries the same flag.", "",
          "| skill | score | grade |", "| --- | ---: | --- |"]
    for r in needs_fix:
        L.append(f"| `{r['id']}` | {r['score']} | {r['grade']} |")
    L += ["", "## Promoted, re-audit still needed", "",
          "Changed in staging after their latest audit, so the score below describes earlier bytes.",
          "`reaudit` in PROVENANCE.json carries the same flag.", "",
          "| skill | score at last audit | audited on |", "| --- | ---: | --- |"]
    for r in stale:
        L.append(f"| `{r['id']}` | {r['score']} | {r['audited_on']} |")
    L += ["", "## Audited and excluded", "",
          "Audited and did not pass. Not pending — rejected until the defects behind the score are",
          "fixed.", "", "| skill | score | grade | open P0 |", "| --- | ---: | --- | ---: |"]
    for e in excluded:
        L.append(f"| `{e['id']}` | {e['score']} | {e['grade']} | {e['open_p0']} |")
    L += ["", "## Out of scope", "", "| skill | reason |", "| --- | --- |"]
    for i, why in sorted(OUT_OF_SCOPE.items()):
        L.append(f"| `{i}` | {why} |")
    L += ["", "## The list", ""]
    for f in sorted(by):
        L += [f"### {f}", ""]
        L += [f"- `{i}` — `{idx[i]}`" for i in sorted(by[f])]
        L.append("")
    with open(os.path.join(OUT, "REMAINING.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L))
    print(f"\nwrote {OUT}")


main()
