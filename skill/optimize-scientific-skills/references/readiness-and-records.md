# Readiness and records

Use the current `skill-auditor.zip` in the records repository as the canonical
rubric and report-schema source. Extract it only to a disposable run directory
when it is not already installed.

Unless the current rubric is stricter, `Production Ready` requires final score
at least 85, static score at least 80, execution average at least 85, Layer 1
at least 32, Layer 2 at least 48, assertion pass rate at least 90 percent, no
veto, no open P0, and no required accessible runnable surface left unexecuted
in final audit.

Use these states:

- `untouched`: no usable audit for the relevant source;
- `audited`: audit exists but final certification is incomplete;
- `candidate-ready`: exhaustive independent final audit passes for exact
  working bytes, but they have not entered the run-closing product commit;
- `ready`: exact audited bytes are committed on the optimized shelf with
  reconciled provider metadata;
- `done`: Marketplace intake accepted the exact optimized commit and path.

For every audit identity, preserve schema-valid `report.json`, `viewer.md`,
saved run scripts and inputs, command/output evidence, source identity, and
explicit execution classifications. Do not claim evidence that exists only in
chat.

After every audit, publish with the repository tooling when applicable:

```powershell
python tools/publish_audits.py --repo <provider-root> --skill <skill-id>
npm run audits:index
```

Regenerate the canonical index, backlog, and `audits/STATUS.md` from records.
`STATUS.md` groups the canonical known Skill inventory by category and shows at
least total known, audited, untouched, ready, and out-of-scope counts plus a
total row. `Audited` includes ready Skills. Derive:

- category, total known, ready, and out-of-scope states from
  `audits/CORPUS.json`;
- audited from the latest published audit records;
- untouched as in-scope known Skills with no published audit.

Never edit counts by hand. Run `npm run audits:index` after every published
audit. Run `npm run audits:inventory` after provider inventory, readiness, or
source metadata changes; it refreshes `audits/CORPUS.json` from the canonical
optimized provider and regenerates every audit view. If either generator
fails, resolve or report the concrete blocker before accepting the transition.
