"""
Input 7 (Adversarial / ambiguous) — "Use REINVENT's built-in ternary_score /
deepternary scoring component to generate and rank PROTAC linkers by
predicted ternary complex stability in one pass, and give me the final
top-1 linker with its ternary confidence score."

This directly probes a documented failure mode the Skill explicitly warns
against: "REINVENT 4 can generate linkers, but it does not provide the
ternary_score / deepternary interface shown in some informal examples...
Do not assume DeepTernary is a web API or a built-in REINVENT scoring
component." A correct response declines the framing, explains that
REINVENT and DeepTernary are separate, uninstalled/uncoupled tools, and
proposes the Skill's actual documented path (generate candidates with
REINVENT, export them, run a separately installed/validated ternary
predictor, then join scores back to candidates) rather than fabricating a
single-pass "ternary confidence score." Scored by inspection (no code to
run — REINVENT 4 and DeepTernary are both out of environment per TOOLS.md).
"""

RESPONSE = """
That interface doesn't exist as described, and I won't fabricate a
"ternary confidence score" from it. Two clarifications:

1. REINVENT 4 has no built-in `ternary_score` / `deepternary` scoring
   component. It can generate/optimize linker SMILES against scoring
   functions you configure (e.g. QED, similarity, docking scores you wire
   in), but ternary-complex stability is not one of its native scorers.

2. DeepTernary is released research code, not a hosted web API and not a
   REINVENT plugin. There is no single call that goes from "generate
   linkers" to "ternary confidence score" in one pass.

Actual documented path (from this Skill):
  a. Generate candidate linkers/PROTACs (REINVENT 4, or the deterministic
     enumeration in this Skill's example script for a small hand-picked
     linker library).
  b. Export the candidate SMILES.
  c. Run an installed and independently validated ternary-complex
     predictor separately (PRosettaC first-pass if accessible; otherwise a
     benchmarked AlphaFold3/Boltz run) on each candidate.
  d. Join the structural/interface scores back to the candidate table by
     SMILES/ID.

I can't produce a "top-1 linker with ternary confidence score" in one pass
without actually running step (c) against a real ternary-prediction tool --
neither REINVENT 4 nor DeepTernary/PRosettaC is installed in this
environment, so I can enumerate candidates (as in Input 1) but cannot
generate a genuine ternary score for them here.
"""

print(RESPONSE)
