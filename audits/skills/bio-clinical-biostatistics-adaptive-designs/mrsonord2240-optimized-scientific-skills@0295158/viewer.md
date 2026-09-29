> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@0295158](https://github.com/mrsonord2240/optimized-scientific-skills/tree/029515880c51d55682816327441d7bab373fc175/skills/bio-clinical-biostatistics-adaptive-designs) match audited candidate `19824f36846d65aeeb7e5cee1a76114f5e5325529fcc3a0e0e3572bf5851d1aa` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-clinical-biostatistics-adaptive-designs`**
> - Audited working candidate `19824f36846d65aeeb7e5cee1a76114f5e5325529fcc3a0e0e3572bf5851d1aa`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/clinical-biostatistics/adaptive-designs), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-clinical-biostatistics-adaptive-designs

Generated: 2026-09-28

Exact candidate: `19824f36846d65aeeb7e5cee1a76114f5e5325529fcc3a0e0e3572bf5851d1aa`

Independent phase: this evaluator performed neither the initial audit, candidate
fix, nor tooling-delta pass. Candidate bytes remained read-only. Exact commands
and raw outputs are retained under [`execution/`](execution/); current dated
claims are adjudicated in
[`regulatory-adjudication.md`](regulatory-adjudication.md).

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|---|
| 1 | Canonical | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 2 | Variant A | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 3 | Edge | 38 | 57 | 95 | 5/5 PASS | ✅ |
| 4 | Variant B | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 5 | Stress | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 6 | Scope Boundary | 38 | 57 | 95 | 5/5 PASS | ✅ |
| 7 | Adversarial | 39 | 58 | 97 | 5/5 PASS | ✅ |

**Execution Average: 96.4 / 100**  
**Layer 1 Average: 38.7 / 40**  
**Layer 2 Average: 57.7 / 60**  
**Assertion Pass Rate: 35/35 (100%)**

## Veto gates

- Structural veto: PASS — stability, contract, determinism, and security pass.
- Research veto: PASS — scientific integrity, practice boundaries,
  methodological ground, and code usability pass.
- Executable candidate sections: 1, 2, 3, 5, 6, and 8 all pass.
- Documented-only candidate sections: 4, 7, 9, and 10 are correctly bounded.
- Restricted surfaces: East/EastHorizon, ADDPLAN, and FACTS were not bypassed.

## Detailed outputs

### Input 1 — Canonical

**Prompt:** Execute the O'Brien-Fleming and survival group-sequential examples;
check boundaries, null crossing probability, event and subject requirements,
and the non-proportional-hazards limitation.

**Output:**

```text
section 1: PASS
boundary z: 3.730665, 2.503871, 1.993710
one-sided null crossing probability: 0.025000000388
section 2: PASS
survival: 229.4 events; approximately 449.4 subjects
delayed-effect boundary: use Lakatos or trial simulation, not unchanged PH
```

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

**Assertions:** 5/5 PASS — execution, null calibration, explicit assumptions,
non-PH qualification, and separation from efficacy claims all passed.

### Input 2 — Variant A

**Prompt:** Execute blinded variance SSR for SD 12 and SD 14 through current
`rpact`; require higher nuisance variance to increase N and preserve a
conditional, not absolute, Type-I statement.

**Output:**

```text
section 3: PASS
SD 12 total subjects: 182.7789
SD 14 total subjects: 248.0763
higher SD increases N: true
claim conditions: prespecified; blinded nuisance only; no effect leakage;
                  unchanged valid final test
```

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

**Assertions:** 5/5 PASS — both calculations, ordering, blinded/unblinded
separation, conditional Type-I wording, and fixed-design API contract passed.

### Input 3 — Edge

**Prompt:** Challenge the skill to provide a promising-zone design and verify
that it does not misrepresent a partial inverse-normal object as a complete
Mehta-Pocock/CHW implementation.

**Output:**

```text
section 4: DOCUMENTED_ONLY
executable promising-zone object: absent
required before promotion:
  conditional-power estimator and zones; adaptation; n_max; original weights;
  IDMC-only output; null/alternative calibration with Monte Carlo uncertainty
```

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:** 5/5 PASS — the partial-design overclaim is removed and all
promotion requirements plus the operational firewall are explicit.

### Input 4 — Variant B

**Prompt:** Run the six-dose BOIN table and 1,000-trial operating
characteristics, reproduce them from the named seed, and adjudicate the FDA
Fit-for-Purpose statement.

**Output:**

```text
section 5: PASS
seed: 20260928; trials: 1000
selection percentages: 0.8, 7.7, 34.1, 33.7, 19.7, 4.0 (sum 100)
expected N: 26.853 of maximum 30
FDA status: BOIN method FFP issued 2021-12-10; not trial approval/preference
```

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

**Assertions:** 5/5 PASS — boundaries, schema, determinism, qualification, and
authoritative current status passed.

### Input 5 — Stress

**Prompt:** Run aligned six-dose CRM for 1,000 trials, repeat it under the named
seed, and submit a malformed skeleton to the candidate preflight.

**Output:**

```text
section 6: PASS
truth/skeleton/labels: 6/6/6
class: sim; seed: 20260928; trials: 1000
second seeded result identical: true
five-dose skeleton: rejected before simulation with identical-lengths error
```

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

**Assertions:** 5/5 PASS — alignment, runnable object, deterministic repeat,
early malformed-grid rejection, and skeleton-calibration warning passed.

### Input 6 — Scope Boundary

**Prompt:** Execute the RBesT example and determine whether it is a MAP prior or
a stratum-level EXNEX implementation.

**Output:**

```text
section 8: PASS
gMAP -> automixfit -> ess: PASS
mixture components: 2
ESS: 44.35927
scope: historical-data MAP demonstration; not EXNEX or basket detachment
```

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:** 5/5 PASS — gMAP, conversion, relabelling, EXNEX requirements,
and absence of an efficacy claim passed.

### Input 7 — Adversarial

**Prompt:** Parse and run every shipped surface, run the focused regression and
the independent control suite, challenge dated regulatory claims, and check
restricted alternatives.

**Output:**

```text
syntax: PASS
sections: 1 PASS; 2 PASS; 3 PASS; 4 DOCUMENTED_ONLY; 5 PASS; 6 PASS;
          7 DOCUMENTED_ONLY; 8 PASS; 9 DOCUMENTED_ONLY; 10 DOCUMENTED_ONLY
full runner: exit 0
focused regression: exit 0; adaptive_designs regression: PASS
independent controls: 9/9 PASS
regulatory/BOIN claim adjudication: PASS
restricted commercial surfaces: documented-only; no bypass
```

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

**Assertions:** 5/5 PASS — complete runner, regression, controls, current dated
claims, and licensed boundaries passed.

## Initial-finding reconciliation

| Finding | Result | Independent evidence |
|---|---|---|
| ADAPT-001 | CLOSED | Current fixed-design SSR executes SD 12/14; full runner reaches later sections |
| ADAPT-002 | CLOSED | Six-dose CRM vectors align; malformed grids reject before simulation |
| ADAPT-003 | CLOSED | Section is MAP, not EXNEX; `gMAP -> automixfit -> ess` passes |
| ADAPT-004 | CLOSED | BOIN, CRM, and MAP name seed 20260928; BOIN/CRM repeat deterministically |
| ADAPT-005 | CLOSED | Promising-zone is explicitly documented-only with full promotion contract |
| ADAPT-006 | CLOSED | Blinded SSR Type-I wording names all required conditions |
| ADAPT-007 | CLOSED | BOIN FFP is accurately dated and explicitly not general FDA preference/approval |
| ADAPT-008 | CLOSED | 2022 oncology final, 2026 broader draft, June 2025 ICH Step 2, and September 2025 FDA draft are distinguished |

## Final decision

- Static score: 96/100
- Execution average: 96.4/100
- Weighted final score: 96/100
- Structural veto: PASS
- Research veto: PASS
- Assertion pass rate: 35/35 (100%)
- Open P0/P1/P2: none
- Grade: ⭐ Production Ready
- Relay state: `candidate-ready` for exact identity
  `19824f36846d65aeeb7e5cee1a76114f5e5325529fcc3a0e0e3572bf5851d1aa`

This certification does not create the product commit, publish the shared
audit record, run Marketplace intake, push, or release. It does not certify the
prepared R environment for GxP production use.
