// Two mechanical frontmatter fixes across the bioSkills corpus:
//
//   1. 13 Skills have an unquoted `description` containing ": ", which YAML reads as a nested
//      mapping. The frontmatter does not parse at all, so `name` and `description` are invisible to
//      anything that reads frontmatter — the marketplace's intake, and the Skill loader itself.
//      Fixed by double-quoting the scalar. Verified beforehand that no description in the 13 contains
//      a double quote or a backslash, so no escaping is needed; the script re-checks per file anyway.
//
//   2. No Skill declares `license`. The marketplace treats a missing declaration as needing a
//      reviewed "Unknown" exception with an evidence explanation. bioSkills is MIT (LICENSE at the
//      repo root), so declaring it removes that review friction.
//
// Line endings are preserved per file. The parsed description is asserted equal to the original text
// afterwards, so a quoting change can never silently alter a description.

import { readFileSync, writeFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { parseDocument } from "file:///F:/openscience-specialists/node_modules/yaml/dist/index.js";

const ROOT = "F:/optimizing-agent-science-skills/skills/bioSkills";
const APPLY = process.argv.includes("--apply");

const FM_RE = /^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/;
let quoted = 0, licensed = 0, untouched = 0;
const changes = [], refusals = [];

for (const folder of readdirSync(ROOT)) {
  const fp = join(ROOT, folder);
  if (!statSync(fp).isDirectory()) continue;
  for (const skill of readdirSync(fp)) {
    const sd = join(fp, skill);
    if (!statSync(sd).isDirectory()) continue;
    const p = join(sd, "SKILL.md");
    let raw;
    try { raw = readFileSync(p, "utf8"); } catch { continue; }

    const m = raw.match(FM_RE);
    if (!m) { refusals.push([`${folder}/${skill}`, "no frontmatter block"]); continue; }
    const eol = raw.includes("\r\n") ? "\r\n" : "\n";
    let fmText = m[1];
    const before = parseDocument(fmText);
    const wasBroken = before.errors.length > 0;
    let didQuote = false, didLicense = false;

    // 1. quote a description that breaks the parse
    if (wasBroken) {
      const lines = fmText.split(/\r?\n/);
      const i = lines.findIndex((l) => /^description:\s/.test(l));
      if (i === -1) { refusals.push([`${folder}/${skill}`, "broken but no description: line"]); continue; }
      const value = lines[i].replace(/^description:\s*/, "");
      if (value.includes('"') || value.includes("\\")) {
        refusals.push([`${folder}/${skill}`, "description contains a quote or backslash; needs a human"]);
        continue;
      }
      if (/^["'>|]/.test(value)) {
        refusals.push([`${folder}/${skill}`, "description already uses a YAML scalar style"]);
        continue;
      }
      lines[i] = `description: "${value}"`;
      fmText = lines.join(eol === "\r\n" ? "\r\n" : "\n");
      didQuote = true;
    }

    // 2. declare the licence
    const parsed = parseDocument(fmText);
    if (parsed.errors.length) {
      refusals.push([`${folder}/${skill}`, `still unparseable: ${parsed.errors[0].message.split("\n")[0]}`]);
      continue;
    }
    const data = parsed.toJS({ maxAliasCount: 50 });
    if (!Object.hasOwn(data, "license") && !Object.hasOwn(data.metadata ?? {}, "license")) {
      fmText = fmText.replace(/\s*$/, "") + (eol === "\r\n" ? "\r\n" : "\n") + "license: MIT";
      didLicense = true;
    }

    if (!didQuote && !didLicense) { untouched++; continue; }

    // verify before writing: parses, keeps name, and the description is byte-identical in meaning
    const after = parseDocument(fmText);
    if (after.errors.length) {
      refusals.push([`${folder}/${skill}`, "edit would not parse"]);
      continue;
    }
    const ad = after.toJS({ maxAliasCount: 50 });
    if (typeof ad.name !== "string" || !ad.name.trim()) {
      refusals.push([`${folder}/${skill}`, "edit lost the name"]);
      continue;
    }
    if (typeof ad.description !== "string" || !ad.description.trim()) {
      refusals.push([`${folder}/${skill}`, "edit lost the description"]);
      continue;
    }
    if (didQuote) {
      const original = m[1].split(/\r?\n/).find((l) => /^description:\s/.test(l)).replace(/^description:\s*/, "");
      if (ad.description !== original) {
        refusals.push([`${folder}/${skill}`, "description text changed — refusing"]);
        continue;
      }
    }
    if (ad.license !== "MIT" && didLicense) {
      refusals.push([`${folder}/${skill}`, "licence did not round-trip"]);
      continue;
    }

    const out = raw.replace(FM_RE, (full) => {
      const tail = full.endsWith("\n") ? (full.endsWith("\r\n") ? "\r\n" : "\n") : "";
      return `---${eol}${fmText}${eol}---${tail}`;
    });
    if (APPLY) writeFileSync(p, out, "utf8");
    if (didQuote) quoted++;
    if (didLicense) licensed++;
    changes.push([`${folder}/${skill}`, [didQuote && "quoted-description", didLicense && "license: MIT"].filter(Boolean).join(" + ")]);
  }
}

console.log(APPLY ? "APPLIED" : "DRY RUN (pass --apply to write)");
console.log(`descriptions quoted : ${quoted}`);
console.log(`licence declared    : ${licensed}`);
console.log(`already fine        : ${untouched}`);
console.log(`refused             : ${refusals.length}`);
for (const [p, why] of refusals) console.log(`  REFUSED ${p}: ${why}`);
