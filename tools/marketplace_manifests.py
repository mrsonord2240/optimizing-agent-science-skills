"""Write Open Science marketplace `release.config.json` manifests for the promoted Skills, and check them.

The marketplace (aipoch/openscience-skill-marketplace, authoring/README.md) takes one manifest per Skill
that pins a public GitHub repository, a full commit SHA and a subdirectory. The payload stays in that
repository, so the pinned commit has to exist on the published shelf, `optimized-scientific-skills`.

Selects the Skills flagged `marketplace_ready` in the shelf's PROVENANCE.json (see promote_skills.py),
pins each to the shelf commit that last touched `skills/<id>/`, and refuses to write a manifest for:
  - a Skill whose pinned commit is not on origin/main (the marketplace cannot fetch it)
  - an id that already exists in the live marketplace, or differs from one only by a `bio-` prefix
    (their rules: registered ids are unique and disjoint from the original members; no renaming to
    dodge the check)

`config/marketplace_submission_holds.json` is an explicit maintainer-decision hold. Its entries are
never written or passed to `intake:skill`, even when an operator names one with `--skill`.

Usage:
  marketplace_manifests.py [--out DIR] [--version 1.0.0] [--skill ID ...]
                           [--intake PATH-TO-MARKETPLACE-CLONE]

--intake runs the marketplace's own `npm run intake:skill` over every manifest written, against the
shelf clone, and fails if it rejects any. A manifest that intake has not accepted is not evidence.
The output directory defaults to F:/OpenScience/marketplace-submissions and is not a repository.
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request

SHELF = "F:/optimized-scientific-skills"
SHELF_URL = "https://github.com/mrsonord2240/optimized-scientific-skills"
MARKETPLACE_JSON = "https://statics.aipoch.com/open-science/skill-marketplace/v1/marketplace.json"
MARKETPLACE_HOLDS = os.path.normpath(os.path.join(
    os.path.dirname(__file__), "..", "config", "marketplace_submission_holds.json"))

# The marketplace has five fixed categories. Classification is audit evidence, so manifest
# generation reads the declaration promoted with the Skill and never guesses from its folder.
VALID_CATEGORIES = {
    "Evidence Insight",
    "Protocol Design",
    "Data Analysis",
    "Academic Writing",
    "Other",
}


def skill_category(skill_id, shelf=None):
    shelf = shelf or SHELF
    path = os.path.join(shelf, "skills", skill_id, "SKILL.md")
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        raise SystemExit(f"{path}: cannot read Skill frontmatter: {exc}") from exc
    if not text.startswith("---"):
        raise SystemExit(f"{path}: missing YAML frontmatter")
    end = text.find("\n---", 3)
    if end < 0:
        raise SystemExit(f"{path}: unterminated YAML frontmatter")
    matches = [line.split(":", 1)[1].strip().strip("\"'")
               for line in text[3:end].splitlines() if line.startswith("category:")]
    if len(matches) != 1:
        raise SystemExit(f"{path}: expected exactly one category frontmatter field")
    category = matches[0]
    if category not in VALID_CATEGORIES:
        raise SystemExit(f"{path}: invalid marketplace category {category!r}")
    return category


def load_marketplace_holds(path=MARKETPLACE_HOLDS):
    """Read deliberate marketplace submission holds, failing closed on a malformed config."""
    with open(path, encoding="utf-8") as fh:
        document = json.load(fh)
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


def git(*args):
    r = subprocess.run(["git", *args], cwd=SHELF, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.stdout.strip()


def marketplace_ids():
    with urllib.request.urlopen(MARKETPLACE_JSON, timeout=60) as r:
        return {s["id"] for s in json.load(r)["skills"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="F:/OpenScience/marketplace-submissions")
    ap.add_argument("--version", default="1.0.0")
    ap.add_argument("--skill", action="append", default=[])
    ap.add_argument("--intake")
    args = ap.parse_args()

    prov = json.load(open(os.path.join(SHELF, "PROVENANCE.json"), encoding="utf-8"))
    marketplace_holds = load_marketplace_holds()
    rows = [r for r in prov["skills"] if r.get("marketplace_ready")]
    refused = []
    if args.skill:
        for sid in args.skill:
            hold = marketplace_holds.get(sid)
            if hold:
                refused.append((sid, "submission hold: " + hold["reason"]))
        rows = [r for r in prov["skills"]
                if r["id"] in args.skill and r["id"] not in marketplace_holds]
    else:
        rows = [r for r in rows if r["id"] not in marketplace_holds]
    live = marketplace_ids()
    stripped = {i[4:] if i.startswith("bio-") else i for i in live}

    if git("status", "--porcelain", "--", "skills"):
        raise SystemExit("the shelf has uncommitted changes under skills/; commit and push them first")
    on_main = set(git("rev-list", "origin/main").splitlines())

    written = []
    for r in rows:
        sid = r["id"]
        category = skill_category(sid)
        if r.get("category") != category:
            raise SystemExit(
                f"{sid}: PROVENANCE category {r.get('category')!r} does not match "
                f"SKILL.md category {category!r}")
        commit = git("log", "-1", "--format=%H", "--", f"skills/{sid}")
        alias = sid[4:] if sid.startswith("bio-") else sid
        if sid in live or alias in stripped:
            refused.append((sid, "id already in the marketplace"
                            if sid in live else "differs from a marketplace id only by a bio- prefix"))
            continue
        if commit not in on_main:
            refused.append((sid, f"pinned commit {commit[:8]} is not on origin/main"))
            continue
        if not git("ls-tree", commit, "LICENSE"):
            refused.append((sid, "no LICENSE at the pinned commit"))
            continue
        manifest = {
            "schema_version": 1,
            "id": sid,
            "version": args.version,
            "category": category,
            "source": {"repository": SHELF_URL, "commit": commit, "path": f"skills/{sid}"},
            "license_files": ["LICENSE"],
        }
        d = os.path.join(args.out, sid)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "release.config.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(manifest, f, indent=2)
            f.write("\n")
        written.append(sid)

    print(f"wrote {len(written)} manifests to {args.out}")
    for sid, why in refused:
        print(f"refused   : {sid}: {why}")

    if args.intake and written:
        # Chunked: 88 manifest/source pairs exceed the Windows command-line limit.
        accepted = {}
        for i in range(0, len(written), 15):
            cmd = ["npm", "run", "--silent", "intake:skill", "--"]
            for sid in written[i:i + 15]:
                cmd += ["--manifest", os.path.join(args.out, sid, "release.config.json"), "--source", SHELF]
            r = subprocess.run(cmd, cwd=args.intake, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", shell=(os.name == "nt"))
            if r.returncode != 0:
                print("INTAKE REJECTED a batch:")
                print((r.stderr or r.stdout)[-2000:])
                sys.exit(1)
            accepted.update(json.loads(r.stdout))
        print(f"intake accepted {len(accepted)} of {len(written)}")
        if len(accepted) != len(written):
            sys.exit(1)


if __name__ == "__main__":
    main()
