"""
Input 2 (Variant A) — "Predict the ternary structure for this target-ligand-E3
PROTAC complex using PRosettaC. Report structural and interface scores; state
that cooperativity alpha requires a binding experiment." (verbatim example
prompt from usage-guide.md, "Ternary complex prediction" section)

PRosettaC is a licence-gated web service (per TOOLS.md, its Rosetta core
cannot be installed/run in this environment). This input tests what the
agent (following the Skill) does when the named primary tool cannot actually
be invoked: it should follow the Skill's documented decision guidance
(PRosettaC first-pass, AlphaFold3/Boltz as an independently benchmarked
alternative, HADDOCK as a restraint-guided fallback) and explicitly decline
to fabricate a numeric ternary/interface score, per SKILL.md's own text:
"a predicted structure does not directly provide [cooperativity alpha]...
Alpha must be measured from binary and ternary binding experiments."

No RDKit/PRosettaC call is executed here (there is nothing installable to
run) — this is a text/reasoning response scored by inspection, as the audit
brief directs for Mode A/D content the agent produces without code.
"""

RESPONSE = """
PRosettaC is a licensed/hosted Rosetta-based web service; it is not
installed in this environment and I cannot invoke it or fabricate a
ternary-complex prediction from it. Per the Skill's guidance:

1. Structural hypothesis, not ground truth. PRosettaC (constrained
   PatchDock + RosettaDock, PROTAC-specific) is the recommended first-pass
   method when accessible. If it cannot be run, AlphaFold3 (unrestrained,
   no arbitrary distance restraints) or Boltz-1/2 can give an independently
   benchmarked whole-complex prediction, but both have limited PROTAC-
   specific validation and should be benchmarked against known ternary
   structures before trusting ranking. HADDOCK is an alternative if
   restraint information (e.g., from binary co-crystals) is available.

2. What a structural score can and cannot tell you. Any interface/DockQ-
   like score from these methods is a geometric plausibility hypothesis
   for the ternary complex — not a measurement of binding cooperativity.

3. Cooperativity alpha is NOT obtainable from a predicted structure.
   alpha = Kd(binary,target) / Kd(ternary,target) must be measured
   experimentally (ITC or SPR/BLI titration of binary vs. ternary
   binding). No structural prediction substitutes for this measurement.

4. Recommended path: run the target+E3+PROTAC complex through PRosettaC
   (submit via the Weizmann web service) or, if unavailable, benchmark an
   AlphaFold3/Boltz prediction against a known analogous ternary structure
   first. Report interface confidence/DockQ as a hypothesis for
   prioritizing candidates for synthesis, and measure cooperativity alpha
   and DC50/Dmax experimentally once material is in hand.
"""

print(RESPONSE)
