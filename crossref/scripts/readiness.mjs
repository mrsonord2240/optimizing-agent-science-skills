// Check every bioSkill against the Open-Science Skill Marketplace intake gates.
//
// Gates from authoring/README.md and skills/README.md in aipoch/openscience-skill-marketplace,
// and from the failures that repo records against its own members: four YAML syntax failures,
// one missing description, five missing license declarations, one Skill over the size limits.
//
// Uses the same `yaml` parser the marketplace tooling uses, so a YAML verdict here matches theirs.

import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { parseDocument } from "file:///F:/openscience-specialists/node_modules/yaml/dist/index.js";

const ROOT = "F:/optimizing-agent-science-skills/skills/bioSkills";
const KEBAB = /^[a-z0-9]+(-[a-z0-9]+)*$/;
const SKILL_MAX = 128 * 1024 * 1024;
const FILE_MAX = 50 * 1024 * 1024;

function walk(dir) {
  let total = 0;
  const big = [];
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    if (e.name === "__pycache__") continue;
    const p = join(dir, e.name);
    if (e.isDirectory()) {
      const r = walk(p);
      total += r.total;
      big.push(...r.big);
    } else {
      const n = statSync(p).size;
      total += n;
      if (n > FILE_MAX) big.push(e.name);
    }
  }
  return { total, big };
}

const rows = [];
const fails = new Map();
const bump = (k) => fails.set(k, (fails.get(k) ?? 0) + 1);

for (const folder of readdirSync(ROOT)) {
  const fp = join(ROOT, folder);
  if (!statSync(fp).isDirectory()) continue;
  for (const skill of readdirSync(fp)) {
    const sd = join(fp, skill);
    if (!statSync(sd).isDirectory()) continue;
    let raw;
    try {
      raw = readFileSync(join(sd, "SKILL.md"), "utf8");
    } catch {
      continue;
    }
    // Mirrors inspectFrontmatter() in the marketplace's scripts/lib/catalog.mjs, plus the
    // authoring.mjs limits. `license` is optional there: when absent the submission needs a
    // reviewed "Unknown" exception with an evidence explanation, which is friction, not a failure.
    const problems = [];
    const soft = [];
    const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
    let fm = null;
    let syntaxErrors = [];
    if (!m) problems.push("missing-YAML-frontmatter");
    else {
      const doc = parseDocument(m[1]);
      syntaxErrors = doc.errors.map((x) => x.message.split("\n")[0]);
      if (syntaxErrors.length) problems.push("yaml-syntax-error");
      try {
        fm = doc.toJS({ maxAliasCount: 50 });
      } catch (e) {
        problems.push("yaml-toJS-error");
      }
      if (!fm || typeof fm !== "object" || Array.isArray(fm)) {
        problems.push("frontmatter-not-mapping");
        fm = null;
      }
    }
    let name = "", desc = "", lic = "";
    if (fm) {
      name = typeof fm.name === "string" ? fm.name.trim() : "";
      desc = typeof fm.description === "string" ? fm.description.trim() : "";
      const rawLic = Object.hasOwn(fm, "license") ? fm.license : fm.metadata?.license;
      lic = typeof rawLic === "string" ? rawLic.trim() : "";
      if (!name) problems.push("frontmatter-requires-a-name");
      else if (!KEBAB.test(name)) problems.push("id-not-kebab-case");
      else if (name.length > 128) problems.push("id-too-long");
      if (!desc) problems.push("frontmatter-requires-a-description");
      else if (desc.length > 10000) problems.push("description-over-10000");
      if (rawLic !== undefined && !lic) problems.push("license-declared-but-empty");
      if (rawLic === undefined) soft.push("no-frontmatter-license (needs reviewed Unknown exception)");
      const author = fm.author ?? fm.metadata?.author ?? fm.metadata?.["skill-author"];
      if (typeof author === "string" && author.length > 500) problems.push("author-over-500");
    }
    const { total, big } = walk(sd);
    if (total > SKILL_MAX) problems.push("skill-over-128MiB");
    if (big.length) problems.push("file-over-50MiB");
    for (const p of problems) bump(p);
    for (const s of soft) bump(`SOFT: ${s}`);
    rows.push({ path: `${folder}/${skill}`, name, problems, soft, syntaxErrors, bytes: total, descLen: desc.length });
  }
}

const ok = rows.filter((r) => r.problems.length === 0);
console.log(`bioSkills checked : ${rows.length}`);
console.log(`PASS all gates    : ${ok.length}`);
console.log(`with problems     : ${rows.length - ok.length}`);
console.log("\n=== failures by gate ===");
for (const [k, v] of [...fails].sort((a, b) => b[1] - a[1])) {
  console.log(`  ${String(v).padStart(4)}  ${k}`);
}
const bad = rows.filter((r) => r.problems.length);
if (bad.length) {
  console.log("\n=== first 12 affected ===");
  for (const r of bad.slice(0, 20)) console.log(`  ${r.path.padEnd(48)} ${r.problems.join(", ")}  ${(r.syntaxErrors[0]||"").slice(0,60)}`);
}
const sizes = rows.map((r) => r.bytes).sort((a, b) => a - b);
console.log(
  `\nskill size: median ${(sizes[sizes.length >> 1] / 1024).toFixed(0)} KiB, max ${(sizes.at(-1) / 1048576).toFixed(1)} MiB`,
);
const dl = rows.map((r) => r.descLen).sort((a, b) => a - b);
console.log(`description length: median ${dl[dl.length >> 1]}, min ${dl[0]}, max ${dl.at(-1)}`);
