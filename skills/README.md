# skills/

Fixed Skill trees, one directory per upstream source. These are the bytes a Specialist release
ships, so a release's `source` is this repository at a given commit.

```
skills/<upstream>/
  UPSTREAM.json    where it came from and how to get back there
  LICENSE          the upstream project's own licence, unmodified
  <folder>/<skill>/SKILL.md, usage-guide.md, examples/, scripts/
```

`UPSTREAM.json` records:

```json
{
  "repository": "https://github.com/GPTomics/bioSkills",
  "commit": "d91ed3d563019e649dc854c56ccd62551359488a",
  "license": "MIT",
  "author": "GPTomics",
  "fork": "https://github.com/mrsonord2240/bioSkills-Improved",
  "fork_branch": "openscience-fixes",
  "modified": true,
  "modified_by": "Samuel Nord (Claude agents)",
  "changes": "fixes/<skill-id>.md, and audits/<skill-id>/<version>/fixes.md"
}
```

Rules for this directory:

- A Skill's frontmatter `name` never changes. It is the Skill ID everything else keys on.
- Files change only where an audit demonstrated a defect. No restyling, no new sections.
- A Skill that passed with no findings stays byte-identical to its upstream commit.
- Fixes are made in a fork, never here; this directory is an export of that fork.
- Where the original upstream is still maintained, the fork is also the route for sending fixes
  back. `GPTomics/bioSkills` was archived on 2026-08-15 and takes no pull requests, so for those
  Skills the fork is the maintained line instead.
