"""Mechanical preflight for scientific Skill directories: identity, hygiene, frontmatter and Marketplace ID collisions.

Runs before any agent is dispatched and again before a batch closes, so that agents never spend tokens
on checks a script decides. It never edits a Skill.

Checks per Skill directory:
  identity   sha256-manifest-v1: files sorted by ordinal UTF-8 relative path, one `path\\tbytes\\tsha256`
             line each, LF-joined without a trailing LF; the identity is the sha256 of that text
  hygiene    CRLF or UTF-8 BOM in text files, __pycache__ / *.pyc, LICENSE below the Skill root,
             symlinks, dot-prefixed path segments (Marketplace publication drops them)
  frontmatter name equals the directory name; description and author nonempty; exactly one category
             from the Marketplace's five labels (fail); license declaration or Skill-root LICENSE absent (warn)
  collisions ID already in the live Marketplace catalog, differing from one only by a `bio-` prefix,
             or present in the Marketplace's third-party review queue (fail); IDs sharing most
             name tokens with a live or queued ID (warn: a maintainer checks semantic duplicates)
  shape      only with --shape, the router layout normalization produces: description is a `Use when`
             trigger; a route table within 15 lines of the title; routes/ exists and every route is named
             by SKILL.md or another route; every routes/, scripts/ or references/ path an instruction
             file names exists; no literature citation in SKILL.md or a route (fail); a script no
             instruction file or other script names (warn)

Usage:
  skill_preflight.py SKILL_DIR [SKILL_DIR ...] [--shape] [--offline] [--marketplace PATH] [--json]

--offline skips the live catalog and queue checks. --marketplace names the local Marketplace clone whose
fetched origin/main supplies the review queue (default: marketplace/intake/openscience-skill-marketplace).
Exit status is 1 when any Skill has a failure; warnings alone exit 0.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from marketplace_manifests import VALID_CATEGORIES, marketplace_ids  # noqa: E402

DEFAULT_MARKETPLACE = os.path.normpath(os.path.join(
    os.path.dirname(__file__), "..", "marketplace", "intake", "openscience-skill-marketplace"))
TEXT_SUFFIXES = {".md", ".py", ".r", ".sh", ".txt", ".json", ".yaml", ".yml", ".tsv", ".csv", ".toml",
                 ".cfg", ".ini", ".wdl", ".nf", ".smk", ".ipynb", ".js", ".ts", ".html", ".css", ".sql"}


def identity(root):
    rows = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in filenames:
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            with open(path, "rb") as fh:
                data = fh.read()
            rows.append((rel, data))
    rows.sort(key=lambda r: r[0].encode("utf-8"))
    manifest = "\n".join(f"{rel}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}" for rel, data in rows)
    return hashlib.sha256(manifest.encode("utf-8")).hexdigest(), rows

TITLE_TO_TABLE = 15  # lines from the title to the first route-table row
OWN_PATH = re.compile(r"(?<![\w./-])((?:routes|scripts|references)/[\w.-]+(?:/[\w.-]+)*)")
CITATION = re.compile(
    r"\bet al\b|\bdoi\b|\bPMID\b|^#+\s*(?:References|Citations|Bibliography)\s*$"
    r"|\b[A-Z][a-z]+ (?:and|&) [A-Z][a-z]+,? \(?(?:19|20)\d\d"
    r"|\([A-Z][A-Za-z-]+,? (?:19|20)\d\d[a-z]?\)"
    r"|\b(?:Nat(?:ure)? (?:Methods|Biotechnol\w*|Commun\w*|Genet\w*)|Genome Biol\w*|Nucleic Acids Res\w*)\b")


def shape(rows, fm):
    """Router-layout checks on (rel, bytes) rows; returns (fails, warns)."""
    fails, warns = [], []
    text = {rel: data.decode("utf-8", errors="replace") for rel, data in rows
            if os.path.splitext(rel)[1].lower() in TEXT_SUFFIXES}
    names = {rel for rel, _ in rows}
    dirs = {rel.rsplit("/", 1)[0] for rel in names if "/" in rel}
    instructions = {rel: body for rel, body in text.items()
                    if rel == "SKILL.md" or (rel.startswith("routes/") and rel.endswith(".md"))}
    routes = sorted(rel for rel in instructions if rel != "SKILL.md")
    if fm is not None and not fm.get("description", [""])[0].startswith("Use when "):
        fails.append("description is not a `Use when ...` trigger")
    lines = instructions.get("SKILL.md", "").splitlines()
    title = next((i for i, line in enumerate(lines) if line.startswith("# ")), None)
    if title is None:
        fails.append("SKILL.md has no `# ` title")
    elif not any(line.startswith("|") for line in lines[title + 1:title + 1 + TITLE_TO_TABLE]):
        fails.append(f"no route table within {TITLE_TO_TABLE} lines of the title")
    if not routes:
        fails.append("no routes/*.md files")
    named = set()
    for rel, body in sorted(instructions.items()):
        for n, line in enumerate(body.splitlines(), 1):
            for path in OWN_PATH.findall(line):
                path = path.rstrip(".")
                named.add(path)
                if path not in names and path not in dirs:
                    fails.append(f"routed path missing: {path} ({rel}:{n})")
            if CITATION.search(line):
                fails.append(f"literature citation in an instruction file: {rel}:{n}")
    for rel in routes:
        if rel not in named:
            fails.append(f"route not named by SKILL.md or another route: {rel}")
    for rel in sorted(n for n in names if n.startswith("scripts/")):
        base = rel.rsplit("/", 1)[1]
        if rel not in named and not any(base in body for other, body in text.items()
                                        if other.startswith("scripts/") and other != rel):
            warns.append(f"script no instruction file or script names: {rel}")
    return fails, warns


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        if line and not line[0].isspace() and ":" in line:
            key, value = line.split(":", 1)
            fields.setdefault(key.strip(), []).append(value.strip().strip("\"'"))
    return fields


def tokens(sid):
    return set((sid[4:] if sid.startswith("bio-") else sid).split("-"))


def review_queue(marketplace):
    r = subprocess.run(["git", "show", "origin/main:authoring/submissions/index.json"], cwd=marketplace,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise SystemExit(f"{marketplace}: cannot read origin/main review queue; run `git fetch origin` there")
    return {s["skill_id"] for s in json.loads(r.stdout)["submissions"]}


def check(root, live, queue, router=False):
    fails, warns = [], []
    sid = os.path.basename(os.path.normpath(root))
    ident, rows = identity(root)
    for rel, data in rows:
        parts = rel.split("/")
        full = os.path.join(root, *parts)
        if os.path.islink(full):
            fails.append(f"symlink: {rel}")
        if any(p.startswith(".") for p in parts):
            fails.append(f"dot-prefixed path: {rel}")
        if "__pycache__" in parts or rel.endswith(".pyc"):
            fails.append(f"bytecode cache: {rel}")
        if parts[-1].upper().startswith("LICENSE") and len(parts) > 1:
            fails.append(f"nested license file: {rel}")
        if os.path.splitext(rel)[1].lower() in TEXT_SUFFIXES or parts[-1] in ("LICENSE", "NOTICE"):
            if data.startswith(b"\xef\xbb\xbf"):
                fails.append(f"UTF-8 BOM: {rel}")
            if b"\r\n" in data:
                fails.append(f"CRLF line endings: {rel}")
    names = [rel for rel, _ in rows]
    if "LICENSE" not in names:
        warns.append("no Skill-root LICENSE (the manifest must then cite repository license evidence)")
    skill_md = next((data for rel, data in rows if rel == "SKILL.md"), None)
    fm = frontmatter(skill_md.decode("utf-8", errors="replace")) if skill_md is not None else None
    if fm is None:
        fails.append("SKILL.md missing or without YAML frontmatter")
    else:
        if fm.get("name", [""])[0] != sid:
            fails.append(f"frontmatter name {fm.get('name', [''])[0]!r} != directory {sid!r}")
        for key in ("description", "author"):
            if not fm.get(key, [""])[0]:
                fails.append(f"frontmatter {key} missing or empty")
        if not fm.get("license", [""])[0]:
            warns.append("frontmatter license absent (intake routes this to manual Unknown-license review)")
        cats = fm.get("category", [])
        if len(cats) != 1 or cats[0] not in VALID_CATEGORIES:
            fails.append(f"frontmatter category must be exactly one of {sorted(VALID_CATEGORIES)}; got {cats}")
    if router:
        shape_fails, shape_warns = shape(rows, fm)
        fails += shape_fails
        warns += shape_warns
    if live is not None:
        alias = sid[4:] if sid.startswith("bio-") else sid
        stripped = {i[4:] if i.startswith("bio-") else i for i in live}
        if sid in live:
            fails.append("ID already in the live Marketplace catalog")
        elif alias in stripped:
            fails.append("ID differs from a live Marketplace ID only by a bio- prefix")
        if sid in queue or alias in queue:
            fails.append("ID already in the Marketplace third-party review queue")
        mine = tokens(sid)
        for other in sorted((live | queue) - {sid, alias}):
            theirs = tokens(other)
            if len(mine & theirs) >= 2 and len(mine & theirs) / len(mine | theirs) >= 0.5:
                warns.append(f"near-duplicate name: {other}")
    return {"id": sid, "path": root.replace(os.sep, "/"), "identity": ident, "files": len(rows),
            "bytes": sum(len(d) for _, d in rows), "fail": fails, "warn": warns}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skills", nargs="+")
    ap.add_argument("--shape", action="store_true")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--marketplace", default=DEFAULT_MARKETPLACE)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    live = queue = None
    if not args.offline:
        live, queue = marketplace_ids(), review_queue(args.marketplace)
    results = [check(os.path.abspath(s), live, queue, args.shape) for s in args.skills]
    if args.json:
        json.dump(results, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        for r in results:
            status = "FAIL" if r["fail"] else "PASS"
            print(f"{status} {r['id']} {r['identity']} files={r['files']} bytes={r['bytes']}")
            for f in r["fail"]:
                print(f"  fail: {f}")
            for w in r["warn"]:
                print(f"  warn: {w}")
    sys.exit(1 if any(r["fail"] for r in results) else 0)


if __name__ == "__main__":
    main()
