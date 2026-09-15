import assert from "node:assert/strict";
import { mkdir, mkdtemp, readFile, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  loadAudits,
  renderBacklog,
  renderIndex,
} from "../scripts/audit-index.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

test("generated audit index and backlog are up to date", async () => {
  const audits = await loadAudits(path.join(root, "audits"));
  for (const [name, render] of [
    ["INDEX.md", renderIndex],
    ["BACKLOG.md", renderBacklog],
  ]) {
    const current = (
      await readFile(path.join(root, "audits", name), "utf8")
    ).replace(/\r\n/g, "\n");
    assert.equal(
      current,
      render(audits),
      `audits/${name} is stale; run npm run audits:index`,
    );
  }
});

async function writeVersion(directory, skillId, version, options) {
  const base = path.join(directory, "skills", skillId, version);
  await mkdir(base, { recursive: true });
  const commit = "a".repeat(40);
  await writeFile(
    path.join(base, "record.json"),
    JSON.stringify({
      skill_id: skillId,
      version,
      source: {
        repository: "example/skills",
        commit,
        url: `https://github.com/example/skills/tree/${commit}/${skillId}`,
        author: "Example",
        author_url: "https://github.com/example",
      },
      audit: { audited_on: "2026-09-15" },
      supersedes: options.supersedes ?? null,
    }),
  );
  await writeFile(
    path.join(base, "report.json"),
    JSON.stringify({
      final: { score: options.score, grade: "Beta Only", deployable: false },
      recommendations: options.recommendations,
    }),
  );
}

const recommendation = (priority, title) => ({
  priority,
  title,
  observed_in: [1],
  problem: "p",
  root_cause: "r",
  fix: "f",
});

test("only the unsuperseded version's recommendations reach the backlog", async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), "audits-"));
  await writeVersion(directory, "skill-a", "old", {
    score: 70,
    recommendations: [recommendation("P1", "Old defect")],
  });
  await writeVersion(directory, "skill-a", "new", {
    score: 88,
    supersedes: "old",
    recommendations: [recommendation("P2", "New nit")],
  });
  const audits = await loadAudits(directory);
  assert.equal(audits.skills[0].latest.version, "new");
  const backlog = renderBacklog(audits);
  assert.match(backlog, /New nit/);
  assert.doesNotMatch(backlog, /Old defect/);
  assert.match(renderIndex(audits), /Superseded by/);
});

test("a Skill with two unsuperseded versions is rejected", async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), "audits-"));
  for (const version of ["one", "two"]) {
    await writeVersion(directory, "skill-b", version, {
      score: 80,
      recommendations: [],
    });
  }
  await assert.rejects(loadAudits(directory), /expected one latest version/);
});
