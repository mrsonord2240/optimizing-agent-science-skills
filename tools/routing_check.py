"""Routing check for a router-shaped Skill: does a cheap agent open the right route and run its command?

One case per route. A bash-only agent in a network-less Docker container gets the Skill, the case's input
files and a one-line request. The input must be real or cut down from real: an agent that finds empty
files stops to report them instead of following the route. The run stops at the first command that names the route's script; that
command is never executed, so the container needs none of the Skill's packages. No truth data is involved:
the check reads only which files the agent opened and which command it issued.

A repeat passes when the expected route file is the first route file the agent opens (no other route and
no `routes/*` glob before it) and the agent then runs the expected script or opens the expected reference.
A case passes when most of its repeats pass.

Cases file (JSON list), written by the tooling worker and kept beside TOOLS.md:
  {"route": "routes/pseudobulk.md",           route file, relative to the Skill
   "request": "...",                          what a user would type; must not name a route or a script
   "data": "F:/OpenScience/.../small-input",  directory copied to /work/data; keep it under a few MB
   "expect": "scripts/pseudobulk_de.R"}       optional; default is the first scripts/ path the route names.
                                              A scripts/ path must be run; any other path (a reference the
                                              route sends this request to) must be opened.

   "allow_before": ["routes/qc.md"]           optional; routes the Skill itself orders ahead of this one (a
                                              pipeline's QC step). Opening or running them first is not a miss.

Every route in the first table of SKILL.md needs a case; later tables (after-the-run routes) are optional.

Usage:
  routing_check.py SKILL_DIR CASES.json --out DIR [--reps 3] [--routes a.md,b.md] [--model SLUG] [--image NAME]

--routes reruns only the named cases, after an infrastructure error; the cases file must still cover every route.

The OpenRouter key comes from $OPENROUTER_API_KEY or --env-file and is never logged. Exit status is 1
when any case fails or an infrastructure error leaves a case undecided.
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, os.path.dirname(__file__))
from skill_preflight import frontmatter, identity  # noqa: E402

OR_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-v4.1-flash"  # the model the layout evals ran on
PROVIDERS = ["GMICloud", "DeepInfra"]
ENV_FILE = r"F:\Bio-Evals\runner\.env"
IMAGE = "bioeval-env"
MAX_STEPS = 10      # the layout evals reached the script by step 4 or 5
STEPS_PER_EARLIER_ROUTE = 5
MAX_TOKENS = 8000
CMD_TIMEOUT_S = 60
OBS_LIMIT = 8000

SYSTEM = """You are an autonomous data-analysis agent working in a Linux sandbox with no internet access.
Your working directory is /work. The user's files are in /work/data.

You have one tool: a bash shell. On each turn reply with your reasoning and EXACTLY ONE bash code block:

```bash
<commands>
```

You will receive the output. When you are finished, reply without a bash block.

A reference Skill is available as the directory /work/skills/{name}/ containing SKILL.md and further files.
Read it before you start.

Available skills:
- {name}: {description}"""

BASH_RE = re.compile(r"```(?:bash|sh)\s*\n(.*?)```", re.S)
# Some models answer in their native tool-call markup instead of a fenced block; take its command the same way.
INVOKE_RE = re.compile(r'invoke name="bash">.*?parameter name="command"[^>]*>(.*?)</[^>]*parameter>', re.S)
ROUTE_RE = re.compile(r"routes/([\w.*?-]+)")
RUNNER = r"(?:Rscript|python3?|bash|sh|source\(|\./)[^\n;|&]*"  # an interpreter, then the script on the same command
SCRIPT_RE = re.compile(r"scripts/[\w.-]+")


def load_key(env_file):
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key.strip()
    if os.path.exists(env_file):
        for line in open(env_file, encoding="utf-8"):
            if line.startswith("OPENROUTER_API_KEY="):
                return line.split("=", 1)[1].strip().strip("\"'")
    raise SystemExit(f"No OpenRouter key: set OPENROUTER_API_KEY or put it in {env_file}")


def chat(model, key, messages):
    body = {"model": model, "messages": messages, "max_tokens": MAX_TOKENS, "usage": {"include": True},
            "provider": {"order": PROVIDERS, "allow_fallbacks": True}}
    for attempt in range(4):
        try:
            r = requests.post(OR_URL, json=body, timeout=(10, 180), headers={"Authorization": f"Bearer {key}"})
            r.raise_for_status()
            j = r.json()
            return j["choices"][0]["message"].get("content") or "", float((j.get("usage") or {}).get("cost") or 0)
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)


def docker(*args, timeout):
    return subprocess.run(["docker", *args], capture_output=True, text=True, encoding="utf-8", errors="replace",
                          timeout=timeout, stdin=subprocess.DEVNULL)


def first_table_routes(skill_md):
    """Route files named in the first table under the title."""
    routes, in_table = [], False
    for line in skill_md.splitlines():
        if line.startswith("|"):
            in_table = True
            routes += ["routes/" + m for m in ROUTE_RE.findall(line)]
        elif in_table:
            break
    return routes


def routes_named(cmd, route_files):
    """Route files a command touches, in order: `routes/x.md`, a `routes/*` glob, or `cd routes; cat x.md`."""
    hits = [(m.start(), m.group(1)) for m in ROUTE_RE.finditer(cmd)]
    if "routes" in cmd:
        hits += [(m.start(), name) for name in route_files for m in re.finditer(r"(?<![\w/.-])" + re.escape(name), cmd)]
    return [name for _, name in sorted(hits)]


def load_cases(skill, path):
    cases = json.loads(Path(path).read_text(encoding="utf-8"))
    scripts = {p.name for p in (skill / "scripts").glob("*")} if (skill / "scripts").is_dir() else set()
    problems = []
    for case in cases:
        route = skill / case["route"]
        if not route.is_file():
            problems.append(f"no such route: {case['route']}")
            continue
        named = SCRIPT_RE.findall(route.read_text(encoding="utf-8"))
        case.setdefault("expect", named[0] if named else None)
        leak = [w for w in ["routes/", "scripts/", Path(case["route"]).name, *scripts] if w in case["request"]]
        if leak:
            problems.append(f"request for {case['route']} names {leak}; a user would not")
        files = [f for f in Path(case.get("data") or "").rglob("*") if f.is_file()] if case.get("data") else []
        if not files or any(f.stat().st_size == 0 for f in files):
            problems.append(f"case for {case['route']} needs a data directory with no empty file")
    covered = {case["route"] for case in cases}
    for route in first_table_routes((skill / "SKILL.md").read_text(encoding="utf-8")):
        if route not in covered:
            problems.append(f"no case for first-table route {route}")
    if problems:
        raise SystemExit("cases file rejected:\n  " + "\n  ".join(problems))
    return cases


def run_case(skill, fm, case, rep, out, model, key, image):
    """One agent run. Returns the verdict plus the commands it issued."""
    name = f"{Path(case['route']).stem}-r{rep}"
    ws = out / "ws" / name
    shutil.copytree(skill, ws / "skills" / skill.name)
    shutil.copytree(case["data"], ws / "data")
    system = SYSTEM.format(name=skill.name, description=fm["description"][0])
    messages = [{"role": "system", "content": system}, {"role": "user", "content": case["request"]}]
    route_files = sorted(p.name for p in (skill / "routes").glob("*.md"))
    result = {"route": case["route"], "rep": rep, "expect": case["expect"], "routes_opened": [], "commands": [],
              "command_issued": False, "cost_usd": 0.0, "error": None}
    cid, bad_format = "", 0
    try:
        # No bind mount: Docker Desktop asks the user to approve every new host directory it is given.
        started = docker("run", "-d", "--rm", "--network", "none", "--cpus", "1", "--memory", "2g",
                         "-w", "/work", image, "sleep", "3600", timeout=120)
        cid = started.stdout.strip()
        if not cid:
            raise RuntimeError(f"could not start container: {started.stderr.strip()[:200]}")
        copied = docker("cp", f"{ws}{os.sep}.", f"{cid}:/work", timeout=300)
        if copied.returncode != 0:
            raise RuntimeError(f"could not copy inputs into the container: {copied.stderr.strip()[:200]}")
        # Each route the Skill orders first is real work the agent does on the way (reading it, running QC).
        for _ in range(MAX_STEPS + STEPS_PER_EARLIER_ROUTE * len(case.get("allow_before", []))):
            text, cost = chat(model, key, messages)
            result["cost_usd"] += cost
            messages.append({"role": "assistant", "content": text})
            block = BASH_RE.search(text) or INVOKE_RE.search(text)
            if not block:
                bad_format += 1
                if "```" not in text and "invoke" not in text or bad_format > 2:
                    break  # a plain-prose reply is the agent finishing
                messages.append({"role": "user", "content": "Format error: reply with exactly one ```bash block."})
                continue
            cmd = block.group(1)
            result["commands"].append(cmd)
            for route in routes_named(cmd, route_files):
                if route not in result["routes_opened"]:
                    result["routes_opened"].append(route)
            target = case["expect"] and re.escape(Path(case["expect"]).name)
            if target and re.search(RUNNER + target if case["expect"].startswith("scripts/") else target, cmd):
                result["command_issued"] = True  # reading a script with cat or head is not running it
                break
            try:
                p = docker("exec", cid, "timeout", str(CMD_TIMEOUT_S), "bash", "-c", cmd, timeout=CMD_TIMEOUT_S + 30)
                obs = ((p.stdout or "") + (p.stderr or ""))[:OBS_LIMIT] or "(no output)"
            except subprocess.TimeoutExpired:
                obs = "[command timed out]"
            messages.append({"role": "user", "content": obs})
    except Exception as e:  # API or Docker failure: undecided, never a silent fail of the Skill
        result["error"] = f"{type(e).__name__}: {str(e)[:200]}"
    finally:
        if cid:
            docker("rm", "-f", cid, timeout=60)
        shutil.rmtree(ws, ignore_errors=True)
    allowed = {Path(r).name for r in case.get("allow_before", [])}
    opened = [r for r in result["routes_opened"] if r not in allowed]
    result["route_first"] = bool(opened) and opened[0] == Path(case["route"]).name
    result["passed"] = result["route_first"] and (result["command_issued"] or not case["expect"])
    result["cost_usd"] = round(result["cost_usd"], 5)
    (out / f"{name}.json").write_text(json.dumps({"result": result, "messages": messages}, indent=1), encoding="utf-8")
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skill")
    ap.add_argument("cases")
    ap.add_argument("--out", required=True)
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--routes", default="")
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--image", default=IMAGE)
    ap.add_argument("--parallel", type=int, default=3)
    ap.add_argument("--env-file", default=ENV_FILE)
    args = ap.parse_args()
    skill, out = Path(args.skill).resolve(), Path(args.out).resolve()
    fm = frontmatter((skill / "SKILL.md").read_text(encoding="utf-8"))
    cases = load_cases(skill, args.cases)
    wanted = {r if r.startswith("routes/") else "routes/" + r for r in args.routes.split(",") if r}
    cases = [c for c in cases if not wanted or c["route"] in wanted]
    key = load_key(args.env_file)
    out.mkdir(parents=True, exist_ok=True)
    jobs = [(case, rep) for case in cases for rep in range(1, args.reps + 1)]
    with cf.ThreadPoolExecutor(args.parallel) as ex:
        runs = list(ex.map(lambda j: run_case(skill, fm, j[0], j[1], out, args.model, key, args.image), jobs))
    shutil.rmtree(out / "ws", ignore_errors=True)
    summary, failed = [], False
    for case in cases:
        mine = [r for r in runs if r["route"] == case["route"]]
        errors = [r for r in mine if r["error"]]
        passes = sum(r["passed"] for r in mine if not r["error"])
        decided = len(mine) - len(errors)
        status = "ERROR" if errors and passes * 2 <= len(mine) else "PASS" if passes * 2 > decided else "FAIL"
        failed |= status != "PASS"
        summary.append({"route": case["route"], "status": status, "passed": passes, "decided": decided,
                        "errors": len(errors)})
        print(f"{status} {case['route']} {passes}/{decided}" + (f" ({len(errors)} errored)" if errors else ""))
        for r in mine:
            if not r["passed"] and not r["error"]:
                why = "command not issued" if r["route_first"] else f"opened {r['routes_opened'] or 'no route'} first"
                print(f"  r{r['rep']}: {why}")
    report = {"skill": skill.name, "identity": identity(str(skill))[0], "model": args.model, "reps": args.reps,
              "cost_usd": round(sum(r["cost_usd"] for r in runs), 4), "cases": summary,
              "runs": [{k: v for k, v in r.items() if k != "commands"} for r in runs]}  # commands stay in the per-run files
    (out / "routing.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"{skill.name} {report['identity']} cost=${report['cost_usd']}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
