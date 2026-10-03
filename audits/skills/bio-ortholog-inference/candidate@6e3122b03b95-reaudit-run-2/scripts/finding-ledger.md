# Finding dispositions: bio-ortholog-inference

Prior rejected identity `aa32b51586699da5ed4708ce63e6cbc9eb19751ed79f94b5ff5d73208e252495`; re-audited `6e3122b03b95f6b9666a03f538ff5e07657ad733c2f0b9a2c7f1de1749993bbb`.

| ID | Priority | Disposition | Evidence |
|---|---|---|---|
| OI-01..OI-08 | P1/P2 | verified-fixed, no regression | run_reaudit.txt rerun on new bytes (null-safe OrthoDB, retry stub, group verification, /tab, PANTHER, licence) |
| OI-09 | P2 | verified-fixed | SKILL.md line 86 species form; route.txt 200 vs 404 |
| OI-10 | P2 | verified-fixed | stub.txt three statuses; compara.txt per-symbol outcome and PARTIAL BATCH flag |
| eggNOG note | P2 | verified-fixed | SKILL.md line 103, usage-guide.md line 74 |
| B2 eggNOG | blocker | still blocked | not executed |
| OI-11 | P2 | new | statuses undocumented in SKILL.md; snippet drops failed symbols |
| OI-12 | P2 | new | unknown symbol labelled request failed (HTTP 400) |
