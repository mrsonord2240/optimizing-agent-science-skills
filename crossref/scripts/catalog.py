"""Catalog every Skill across the cloned source corpora, then measure duplication.

Three kinds of duplication, cheapest first:
  1. identical  - same content sha256, byte for byte
  2. id-collision - same frontmatter `name`, different bytes (the Skill-conflict risk)
  3. near-duplicate - high Jaccard on normalized word shingles

Frontmatter `description` is often a folded multi-line YAML scalar, so the parser reads until the
next top-level key rather than assuming one line.
"""
import hashlib
import json
import os
import re
from collections import defaultdict

ROOT = "F:/OpenScience/external"
OUT = "F:/OpenScience/catalog"

# Excluded from the catalog, with the reason recorded in the report.
EXCLUDE = {
    "GPTomics__bioSkills": "superseded by our fork mrsonord2240__bioSkills (same 562 skills, plus audit-evidenced fixes)",
    "K-Dense-AI__scientific-agent-skills": "byte-identical to K-Dense-AI__claude-scientific-skills (verified: same 164 paths, same content)",
    "InternScience__Awesome-Scientific-Skills": "submodule aggregator of ~30 other repos, not a corpus of its own",
    "Agnuxo1__PaperClaw": "no SKILL.md files",
}

LISTED = set()
for line in open("F:/optimizing-agent-science-skills/skill_lists.md", encoding="utf-8"):
    line = line.strip()
    if line.startswith("http"):
        owner, name = line.split()[0].rstrip("/").split("/")[-2:]
        LISTED.add(f"{owner}__{name}")
LISTED.add("mrsonord2240__bioSkills")  # our fork stands in for GPTomics/bioSkills

KEY_RE = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*)$")


def frontmatter(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return {}
    out, key, buf = {}, None, []
    for line in m.group(1).splitlines():
        km = KEY_RE.match(line)
        if km:
            if key:
                out[key] = " ".join(buf).strip()
            key, buf = km.group(1), [km.group(2)]
        elif key and line.strip():
            buf.append(line.strip())
    if key:
        out[key] = " ".join(buf).strip()
    return {k: v.strip().strip('"\'').strip() for k, v in out.items()}


def licence_of(repo_dir):
    for cand in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "MIT License.md"):
        p = os.path.join(repo_dir, cand)
        if os.path.isfile(p):
            head = open(p, encoding="utf-8", errors="replace").read(800).lower()
            for name, pat in [("MIT", "mit license"), ("Apache-2.0", "apache license"),
                              ("BSD-3", "bsd 3-clause"), ("BSD-2", "bsd 2-clause"),
                              ("GPL-3", "gnu general public"), ("CC-BY", "creative commons")]:
                if pat in head:
                    return name
            return "other"
    return "none-in-repo"


STOP = set("""use when a an the and or for to of in with from that this it its on by is are be as at
into your you can not no if then than each per via using used run running build built make makes
skill skills guide guidance workflow workflows step steps file files data output outputs result
results analysis analyze analyzing user users need needs should must may also more most other""".split())


def shingles(text, n=3):
    words = [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP and len(w) > 2]
    return {" ".join(words[i:i + n]) for i in range(max(0, len(words) - n + 1))}


def main():
    os.makedirs(OUT, exist_ok=True)
    skills, skipped = [], []
    for repo in sorted(os.listdir(ROOT)):
        rd = os.path.join(ROOT, repo)
        if not os.path.isdir(rd):
            continue
        if repo in EXCLUDE:
            skipped.append({"repo": repo, "reason": EXCLUDE[repo]})
            continue
        lic = licence_of(rd)
        for base, dirs, fns in os.walk(rd):
            dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "__pycache__")]
            if "SKILL.md" not in fns:
                continue
            p = os.path.join(base, "SKILL.md")
            raw = open(p, "rb").read()
            text = raw.decode("utf-8", errors="replace")
            fm = frontmatter(text)
            rel = os.path.relpath(base, rd).replace("\\", "/")
            skills.append({
                "repo": repo,
                "listed": repo in LISTED,
                "licence": lic,
                "path": rel,
                "dir_name": os.path.basename(base),
                "name": fm.get("name") or os.path.basename(base),
                "description": fm.get("description", ""),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw),
            })

    # 1. identical content
    by_hash = defaultdict(list)
    for s in skills:
        by_hash[s["sha256"]].append(s)
    identical = [v for v in by_hash.values() if len(v) > 1]

    # 2. same declared name, different bytes
    by_name = defaultdict(list)
    for s in skills:
        by_name[s["name"].lower()].append(s)
    collisions = []
    for name, group in by_name.items():
        repos = {g["repo"] for g in group}
        if len(repos) > 1 and len({g["sha256"] for g in group}) > 1:
            collisions.append({"name": name, "members": group})

    # 3. near-duplicates, compared only inside a candidate bucket keyed on shared rare words,
    #    so this stays linear-ish instead of ~1.8M pairwise comparisons.
    sig = {}
    for i, s in enumerate(skills):
        sig[i] = shingles(s["name"].replace("-", " ") + " " + s["description"])
    buckets = defaultdict(set)
    for i, sh in sig.items():
        for tok in list(sh)[:40]:
            buckets[tok].add(i)
    seen, near = set(), []
    for members in buckets.values():
        if len(members) > 60:
            continue
        ms = sorted(members)
        for a in range(len(ms)):
            for b in range(a + 1, len(ms)):
                i, j = ms[a], ms[b]
                if (i, j) in seen:
                    continue
                seen.add((i, j))
                if skills[i]["sha256"] == skills[j]["sha256"]:
                    continue
                A, B = sig[i], sig[j]
                if not A or not B:
                    continue
                jac = len(A & B) / len(A | B)
                if jac >= 0.30:
                    near.append({"jaccard": round(jac, 3), "a": i, "b": j})
    near.sort(key=lambda x: -x["jaccard"])

    json.dump({"skills": skills, "skipped": skipped, "identical": identical,
               "collisions": collisions, "near": near[:4000]},
              open(os.path.join(OUT, "catalog.json"), "w", encoding="utf-8"), indent=1)

    print(f"skills cataloged      : {len(skills)}")
    print(f"repos excluded        : {len(skipped)}")
    print(f"identical-content sets: {len(identical)} covering {sum(len(v) for v in identical)} files")
    print(f"name collisions       : {len(collisions)}")
    print(f"near-duplicate pairs  : {len(near)} at Jaccard >= 0.30")
    print()
    per_repo = defaultdict(int)
    for s in skills:
        per_repo[(s["repo"], s["licence"], s["listed"])] += 1
    print(f"{'repo':52s} {'skills':>6}  {'licence':12s} listed")
    for (r, l, li), n in sorted(per_repo.items(), key=lambda x: -x[1]):
        print(f"{r:52s} {n:>6}  {l:12s} {'yes' if li else '-'}")


main()
