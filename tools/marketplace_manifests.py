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

# The marketplace has five fixed categories. Everything in bioSkills is computational analysis except
# the study-design folder. A maintainer may recategorise on review.
DEFAULT_CATEGORY = "Data Analysis"
FOLDER_CATEGORY = {"experimental-design": "Protocol Design"}


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
    rows = [r for r in prov["skills"] if r.get("marketplace_ready")]
    if args.skill:
        rows = [r for r in prov["skills"] if r["id"] in args.skill]
    live = marketplace_ids()
    stripped = {i[4:] if i.startswith("bio-") else i for i in live}

    if git("status", "--porcelain", "--", "skills"):
        raise SystemExit("the shelf has uncommitted changes under skills/; commit and push them first")
    on_main = set(git("rev-list", "origin/main").splitlines())

    written, refused = [], []
    for r in rows:
        sid = r["id"]
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
            "category": FOLDER_CATEGORY.get(r["upstream_path"].split("/")[0], DEFAULT_CATEGORY),
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
