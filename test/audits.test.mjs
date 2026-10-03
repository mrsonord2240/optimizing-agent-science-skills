import assert from "node:assert/strict";
import { mkdir, mkdtemp, readFile, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  buildCorpusFromProvider,
  buildStatus,
  gradeForScore,
  loadAudits,
  loadCorpus,
  renderBacklog,
  renderIndex,
  renderStatus,
} from "../scripts/audit-index.mjs";
import { renderStatusDashboard } from "../scripts/status-dashboard.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

test("generated audit views are up to date", async () => {
  const audits = await loadAudits(path.join(root, "audits"));
  const corpus = await loadCorpus(path.join(root, "audits", "CORPUS.json"));
  for (const [name, render] of [
    ["INDEX.md", renderIndex],
    ["BACKLOG.md", renderBacklog],
    ["STATUS.md", (data) => renderStatus(buildStatus(data, corpus))],
    [
      "STATUS.html",
      (data) => renderStatusDashboard(buildStatus(data, corpus)),
    ],
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
      final: {
        score: options.score,
        grade: options.grade ?? "Beta Only",
        deployable: options.deployable ?? false,
      },
      meta: { category: options.category ?? "Data Analysis" },
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

test("AIPOCH release grades follow the score thresholds", async () => {
  assert.equal(gradeForScore(85), "Production Ready");
  assert.equal(gradeForScore(84), "Limited Release");
  assert.equal(gradeForScore(60), "Beta Only");
  assert.equal(gradeForScore(59), "Reject");

  const directory = await mkdtemp(path.join(os.tmpdir(), "audits-"));
  await writeVersion(directory, "skill-c", "current", {
    score: 93,
    grade: "Production Ready (self-audited)",
    deployable: true,
    recommendations: [],
  });
  await assert.rejects(loadAudits(directory), /requires grade Production Ready/);
});

test("status separates ready, untouched, and out-of-scope Skills", async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), "audits-"));
  await writeVersion(directory, "skill-ready", "current", {
    score: 90,
    grade: "Production Ready",
    deployable: true,
    recommendations: [],
    category: "Data Analysis",
  });
  await writeVersion(directory, "skill-excluded", "current", {
    score: 70,
    recommendations: [recommendation("P1", "Needs work")],
    category: "Protocol Design",
  });
  const audits = await loadAudits(directory);
  const corpus = {
    schema_version: 1,
    source: { upstream: "example/skills@abc" },
    skills: [
      {
        id: "skill-ready",
        upstream_path: "data/ready",
        category: "Data Analysis",
        state: "ready",
      },
      {
        id: "skill-excluded",
        upstream_path: "protocol/excluded",
        category: null,
        state: "excluded",
      },
      {
        id: "skill-new",
        upstream_path: "unknown/new",
        category: null,
        state: "remaining",
      },
      {
        id: "installer",
        upstream_path: "installer",
        category: null,
        state: "out_of_scope",
      },
    ],
  };
  const status = buildStatus(audits, corpus);
  assert.deepEqual(status.totals, {
    known: 4,
    audited: 2,
    untouched: 1,
    ready: 1,
    outOfScope: 1,
  });
  const rendered = renderStatus(status);
  assert.match(rendered, /Audit coverage: \*\*2 \/ 3 \(66\.7%\)\*\*/);
  assert.match(rendered, /\| Protocol Design \| 1 \| 1 \| 0 \| 0 \| 0 \|/);
  assert.match(rendered, /\| Unclassified \| 2 \| 0 \| 1 \| 0 \| 1 \|/);
  assert.match(rendered, /`skill-excluded`/);
  assert.match(rendered, /\| Area \| Done \| Started \| Untouched \| Excluded \| Total \|/);
  assert.match(rendered, /\| installer \| 0 \| 0 \| 0 \| 1 \| 1 \|/);
  assert.match(rendered, /\| \*\*Total\*\* \| \*\*1\*\* \| \*\*0\*\* \| \*\*1\*\* \| \*\*2\*\* \| \*\*4\*\* \|/);

  const dashboard = renderStatusDashboard(status);
  assert.match(dashboard, /^<!doctype html>/);
  assert.match(dashboard, /66\.7%/);
  assert.match(dashboard, /skill-excluded/);
  assert.match(dashboard, /Protocol Design/);
  assert.match(dashboard, /href="skills\/skill-excluded\/current\/viewer\.md"/);
  assert.doesNotMatch(dashboard, /Lorem ipsum/);
});

test("provider-ready Skills require a published audit", () => {
  assert.throws(
    () =>
      buildStatus(
        { skills: [] },
        {
          schema_version: 1,
          source: { upstream: "example/skills@abc" },
          skills: [
            {
              id: "missing-audit",
              upstream_path: "data/missing-audit",
              category: "Data Analysis",
              state: "ready",
            },
          ],
        },
      ),
    /provider-ready Skill\(s\) missing a published audit: missing-audit/,
  );
});

test("provider inventory refresh is deterministic and fail-closed", async () => {
  const provider = await mkdtemp(path.join(os.tmpdir(), "provider-"));
  await writeFile(
    path.join(provider, "PROVENANCE.json"),
    JSON.stringify({
      generated: "2026-09-28",
      sources: {
        example: {
          provider_repository: "https://github.com/example/optimized",
          provider_ref: "main",
          provider_skills_tree: "tree",
        },
      },
      skills: [
        {
          id: "skill-ready",
          upstream_path: "data/ready",
          category: "Data Analysis",
          score: 95,
          grade: "Production Ready",
          deployable: true,
          open_p0: 0,
          fix_pass: "done",
          reaudit: "not needed",
        },
        {
          id: "skill-refined",
          upstream_path: "data/refined",
          category: "Data Analysis",
          score: 80,
          grade: "Limited Release",
          deployable: true,
          open_p0: 0,
          fix_pass: "done",
          reaudit: "not needed",
        },
      ],
    }),
  );
  await writeFile(
    path.join(provider, "REMAINING.json"),
    JSON.stringify({
      generated: "2026-09-28",
      source: "example/source@abc",
      reconciliation: { skills_in_source_tree: 4 },
      remaining: [{ id: "skill-new", upstream_path: "data/new" }],
      excluded: [],
      out_of_scope: [{ id: "installer", upstream_path: "installer" }],
    }),
  );
  const corpus = await buildCorpusFromProvider(provider);
  assert.deepEqual(
    corpus.skills.map(({ id, state }) => [id, state]),
    [
      ["installer", "out_of_scope"],
      ["skill-new", "remaining"],
      ["skill-ready", "ready"],
      ["skill-refined", "refined"],
    ],
  );

  await writeFile(
    path.join(provider, "REMAINING.json"),
    JSON.stringify({
      source: "example/source@abc",
      reconciliation: { skills_in_source_tree: 4 },
      remaining: [{ id: "skill-ready", upstream_path: "data/duplicate" }],
      excluded: [],
      out_of_scope: [{ id: "installer", upstream_path: "installer" }],
    }),
  );
  await assert.rejects(
    buildCorpusFromProvider(provider),
    /provider inventory has duplicate IDs: skill-ready/,
  );
});
