"""Rank the pinned upstream Skills by two usage proxies and snapshot the result.

Nothing records how often a Skill is actually used, so this ranks on what can be measured:

  downloads        conda downloads of the Skill's frontmatter ``primary_tool``: the larger of its
                   Bioconda and conda-forge all-time totals
  workflow_fan_in  how many upstream workflow Skills list the Skill under ``depends_on``

``score`` is 0-100: half from log10(downloads) against the most-downloaded tool, half from
log2(1 + fan-in) against the highest fan-in. A tool with no conda package scores 0 on the first half
and is listed under ``unresolved``; add it to ALIASES when it has a package under another name.

Conda totals undercount tools installed mostly through pip or CRAN and favour old tools, so read
the score as an ordering hint, not a measurement.

The snapshot is ``catalog/usage.json``. ``promote_skills.py`` reads it when rendering REMAINING.md
and never fetches anything itself. Only this tool touches the network.

Usage:
  usage_rank.py            print the ranking
  usage_rank.py --apply    also write catalog/usage.json
"""
import argparse
import datetime
import json
import math
import re
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from promote_skills import REC, UPSTREAM, UPSTREAM_COMMIT, _atomic_write, _git, _resolve

BIOCONDA_TOTALS = (
    "https://raw.githubusercontent.com/bioconda/bioconda-stats/data/"
    "package-downloads/anaconda.org/bioconda/packages.tsv"
)
CONDA_FORGE_PACKAGE = "https://api.anaconda.org/package/conda-forge/{name}"

# primary_tool -> conda packages to try instead of the derived names. An empty list means the tool
# has no conda package, or only an unrelated package of the same name.
ALIASES = {
    "ALE": [],  # bioconda/ale is the assembly evaluator, not the reconciliation tool
    "AMRFinderPlus": [("bioconda", "ncbi-amrfinderplus")],
    "ASAP": [],
    "ASTRAL-III": [("bioconda", "astral-tree")],
    "AmpliconArchitect": [("bioconda", "ampliconsuite")],
    "BLAST+": [("bioconda", "blast")],
    "CAFE5": [("bioconda", "cafe")],
    "CLIPper": [("bioconda", "clipper")],  # not bioconductor-clipper
    "GATK": [("bioconda", "gatk4")],
    "GATK Mutect2": [("bioconda", "gatk4")],
    "IQ-TREE2": [("bioconda", "iqtree")],
    "MAGMA": [],  # conda-forge/magma is the GPU linear-algebra library
    "MARVEL": [],  # bioconda/marvel is a phage binner
    "Milo": [("bioconda", "bioconductor-milor")],
    "Monocle3": [("bioconda", "r-monocle3")],
    "PGS Catalog Calculator": [("bioconda", "pgscatalog.calc")],
    "R-scape": [("bioconda", "rscape")],
    "ROSE": [],  # conda-forge/r-rose is random over-sampling
    "Ribo-TISH": [("bioconda", "ribotish")],
    "SCENIC+": [("bioconda", "scenicplus")],
    "STAMP": [],  # bioconda/stamp is the metagenomics statistics tool
    "ShapeMapper2": [("bioconda", "shapemapper")],
    "Signac": [("bioconda", "r-signac"), ("conda-forge", "r-signac")],
    "TwoSampleMR": [("conda-forge", "r-twosamplemr")],
    "VEP": [("bioconda", "ensembl-vep")],
    "WGCNA": [("bioconda", "r-wgcna"), ("conda-forge", "r-wgcna")],
    "boruta": [("conda-forge", "boruta_py"), ("conda-forge", "r-boruta")],
    "cobrapy": [("bioconda", "cobra"), ("conda-forge", "cobra")],
    "featureCounts": [("bioconda", "subread")],
    "gatk": [("bioconda", "gatk4")],
    "ichorCNA": [("bioconda", "r-ichorcna")],
    "metaFlye": [("bioconda", "flye")],
    "miRge3.0": [("bioconda", "mirge3")],
    "modkit": [("bioconda", "ont-modkit")],
    "obitools3": [("bioconda", "obitools")],
    "pyComBat": [("bioconda", "inmoose")],
    "rMATS-turbo": [("bioconda", "rmats")],
    "scipy.sparse": [("conda-forge", "scipy")],
    "sklearn": [("conda-forge", "scikit-learn")],
}


def _fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "usage-rank"})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def load_bioconda_totals():
    rows = _fetch(BIOCONDA_TOTALS).decode("utf-8").splitlines()[1:]
    return {name: int(total) for name, total in (row.split("\t") for row in rows if row)}


def conda_forge_total(name):
    try:
        package = json.loads(_fetch(CONDA_FORGE_PACKAGE.format(name=name)))
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise
    return sum(item.get("ndownloads", 0) for item in package.get("files", []))


def candidates(tool, tool_types):
    """Return (channel, package) guesses for a primary_tool used by Skills of ``tool_types``."""
    if tool in ALIASES:
        return list(ALIASES[tool])
    if tool == "BioPython" or tool.startswith("Bio."):
        return [("conda-forge", "biopython")]
    lowered = tool.lower()
    names = list(dict.fromkeys(
        [lowered, re.sub(r"[ _.]+", "-", lowered), re.sub(r"[ _.]+", "_", lowered)]
    ))
    guesses = [(channel, name) for name in names for channel in ("bioconda", "conda-forge")]
    if tool_types & {"r", "mixed"}:
        guesses += [("bioconda", f"bioconductor-{lowered}"), ("conda-forge", f"r-{lowered}")]
    return [(channel, name) for channel, name in guesses if re.fullmatch(r"[a-z0-9._+-]+", name)]


def resolve_tools(tools):
    """Map each primary_tool to its most-downloaded conda package, or None."""
    bioconda = load_bioconda_totals()
    guesses = {tool: candidates(tool, types) for tool, types in tools.items()}
    forge_names = sorted({name for rows in guesses.values()
                          for channel, name in rows if channel == "conda-forge"})
    with ThreadPoolExecutor(max_workers=8) as pool:
        forge = dict(zip(forge_names, pool.map(conda_forge_total, forge_names)))
    resolved = {}
    for tool, rows in guesses.items():
        hits = []
        for channel, name in rows:
            total = bioconda.get(name) if channel == "bioconda" else forge.get(name)
            if total is not None:
                hits.append((total, channel, name))
        if hits:
            total, channel, name = max(hits)
            resolved[tool] = {"channel": channel, "package": name, "downloads": total}
        else:
            resolved[tool] = None
    return resolved


def read_skills(upstream_repo, upstream_commit):
    """Return Skill id -> upstream path, primary tool, tool type and workflow dependencies."""
    listed = _git(upstream_repo, "ls-tree", "-r", "--name-only", upstream_commit).stdout
    skills = {}
    for path in listed.splitlines():
        if not path.endswith("/SKILL.md"):
            continue
        text = _git(upstream_repo, "show", f"{upstream_commit}:{path}").stdout
        front = re.match(r"---\r?\n(.*?)\r?\n---", text, re.DOTALL)
        if not front:
            continue
        front = front.group(1)

        def field(name):
            match = re.search(rf"^{name}:\s*(.+)$", front, re.MULTILINE)
            return match.group(1).strip().strip("\"'") if match else None

        depends = re.search(r"^depends_on:\s*\n((?:\s+-\s+.+\n?)+)", front, re.MULTILINE)
        skill_id = field("name")
        if not skill_id:
            continue
        skills[skill_id] = {
            "upstream_path": path[:-len("/SKILL.md")],
            "primary_tool": field("primary_tool"),
            "tool_type": field("tool_type"),
            "depends_on": re.findall(r"-\s+(\S+)", depends.group(1)) if depends else [],
        }
    return skills


def build_usage(upstream_repo=UPSTREAM, upstream_commit=UPSTREAM_COMMIT):
    upstream_commit = _resolve(upstream_repo, upstream_commit)
    skills = read_skills(upstream_repo, upstream_commit)
    by_path = {row["upstream_path"]: skill_id for skill_id, row in skills.items()}
    fan_in = dict.fromkeys(skills, 0)
    for skill_id, row in skills.items():
        for dependency in row["depends_on"]:
            if dependency not in by_path:
                raise SystemExit(f"{skill_id}: depends_on names unknown Skill path {dependency}")
            fan_in[by_path[dependency]] += 1

    tools = {}
    for row in skills.values():
        if row["primary_tool"]:
            tools.setdefault(row["primary_tool"], set()).add(row["tool_type"])
    resolved = resolve_tools(tools)

    top_downloads = max((hit["downloads"] for hit in resolved.values() if hit), default=0)
    top_fan_in = max(fan_in.values(), default=0)
    ranked = {}
    for skill_id, row in sorted(skills.items()):
        hit = resolved.get(row["primary_tool"])
        downloads = hit["downloads"] if hit else None
        popularity = math.log10(downloads + 1) / math.log10(top_downloads + 1) if downloads else 0
        reach = math.log2(1 + fan_in[skill_id]) / math.log2(1 + top_fan_in) if top_fan_in else 0
        ranked[skill_id] = {
            "upstream_path": row["upstream_path"],
            "primary_tool": row["primary_tool"],
            "downloads": downloads,
            "workflow_fan_in": fan_in[skill_id],
            "score": round(50 * popularity + 50 * reach, 1),
        }
    return {
        "schema_version": 1,
        "generated": datetime.date.today().isoformat(),
        "source": f"GPTomics/bioSkills@{upstream_commit}",
        "tools": {tool: resolved[tool] for tool in sorted(resolved) if resolved[tool]},
        "unresolved": sorted(tool for tool, hit in resolved.items() if not hit),
        "skills": ranked,
    }


def _report(usage):
    folders = {}
    for row in usage["skills"].values():
        folders.setdefault(row["upstream_path"].split("/", 1)[0], []).append(row["score"])
    print(f"{len(usage['skills'])} Skills, {len(usage['tools'])} tools resolved, "
          f"{len(usage['unresolved'])} unresolved")
    print("\nfolder                         skills  mean score")
    for folder in sorted(folders, key=lambda name: (-sum(folders[name]) / len(folders[name]), name)):
        scores = folders[folder]
        print(f"{folder:<30} {len(scores):>6}  {sum(scores) / len(scores):>10.1f}")
    print("\ntool -> package (downloads)")
    for tool, hit in usage["tools"].items():
        print(f"  {tool} -> {hit['channel']}/{hit['package']} ({hit['downloads']})")
    if usage["unresolved"]:
        print("\nunresolved: " + ", ".join(usage["unresolved"]))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write catalog/usage.json")
    parser.add_argument("--records", type=Path, default=REC)
    parser.add_argument("--upstream", type=Path, default=UPSTREAM)
    parser.add_argument("--upstream-commit", default=UPSTREAM_COMMIT)
    args = parser.parse_args(argv)
    usage = build_usage(args.upstream, args.upstream_commit)
    _report(usage)
    if args.apply:
        path = args.records / "catalog" / "usage.json"
        _atomic_write(path, json.dumps(usage, indent=2, ensure_ascii=False) + "\n")
        print(f"\nwrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
