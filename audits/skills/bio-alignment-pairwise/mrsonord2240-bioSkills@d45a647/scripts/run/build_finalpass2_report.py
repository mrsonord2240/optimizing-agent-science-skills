"""Write the Phase-2 report and viewer from fresh, saved regression/fresh-run logs."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
SOURCE = "mrsonord2240/bioSkills@d45a6478bc0f0450f101b6c394415998d7151899:alignment/pairwise-alignment"
PASS, FAIL = "PASS", "FAIL"

def checks(*rows):
    return [{"text": text, "result": result, "note": note} for result, text, note in rows]

inputs = [
    ("Canonical", "HBA/HBB global protein alignment and gap conventions", 38, 56,
     "Executed on real UniProt HBA/HBB using Biopython, independent Gotoh, parasail, EMBOSS, BLAST+, and pwalign; see input1*.py/.sh/.R logs.",
     checks((PASS,"Global BLOSUM62 -11/-1 equals independent Gotoh, parasail and needle","286.0 in all four"),(PASS,"EMBOSS-default -10/-0.5 score is reproduced","292.5"),(PASS,"BLASTP 11/1 maps to Biopython local -12/-1","raw 285 and identical HSP"),(PASS,"pwalign uses the documented BLAST convention","global 10/1=286; local 11/1=285"),(PASS,"Counts and explicit default-gap warning reproduce","65/75/9; 55/37 versus 9/5"))),
    ("Variant A", "Mutated HBB local DNA placement and strand recovery", 38, 56,
     "Executed on seeded synthetic flanks plus a real HBB fragment; see input2_local_dna.py log.",
     checks((PASS,"Local score equals independent Gotoh and planted-score arithmetic","268.0"),(PASS,"Coordinates and counts recover the planted segment","600..750; 142 identities, 5 mismatches, 3 gaps"),(PASS,"Parasail cross-check agrees","267 at 10/1"),(PASS,"Reverse-complement selection recovers the correct orientation","268.0 versus 34.5"))),
    ("Edge", "Semiglobal placement and invalid-input handling", 37, 56,
     "Executed with synthetic fragment/reference and real mammal CDS; see input3_edge_semiglobal.py log.",
     checks((PASS,"Both semiglobal recipes return score 40 and span 300..320","Deprecation warnings promoted to errors"),(PASS,"Argument-order warning is real","swapped order scores -279"),(PASS,"Documented invalid and accepted alphabets reproduce","lowercase/newline/J/U/empty reject; X/B/Z/SeqRecord accept"),(PASS,"Internal-stop check isolates rabbit HBB2","NM_001314043.1 only"),(PASS,"Strand distribution matches the final wording","300-pair median about 18; max 29"))),
    ("Variant B", "Empirical significance and dinucleotide shuffle", 38, 56,
     "Executed deterministic protein and DNA significance paths from the current copied example; see input4_significance.py log.",
     checks((PASS,"Seeded protein null is deterministic","three real pairs match on repeat"),(PASS,"Related and unrelated pairs separate by empirical p-value","0.001 versus 0.2478"),(PASS,"Karlin-Altschul check is consistent with BLAST","115.5 bits; fitted lambda 0.262"),(PASS,"Current pure-Python dinucleotide shuffle is available","current examples/empirical_pvalue.py copied before run"))),
    ("Stress", "Accelerated-library agreement and saturation", 37, 56,
     "Executed 4 kb/20 kb and 1,000-pair seeded synthetic cases; see input5_libs.py and finalpass2_allblocks_wsl.py logs.",
     checks((PASS,"parasail and edlib agree with independent scoring","1,000/1,000 comparisons"),(PASS,"Fixed-width parasail saturation is detected","0 plus saturated=True versus 35644"),(PASS,"Measured speed claims are plausible on this host","parasail 1.9-3.9x at 300 nt; edlib 714x at 20 kb"),(PASS,"Linux-only pywfa and mappy snippets execute","scores/locus cross-check in all-block harness"))),
    ("Scope Boundary", "Codon alignment, PAL2NAL trap, and database search", 37, 55,
     "Executed real HBB CDS, MAFFT/PAL2NAL in WSL, and MMseqs2 against eight real globins; see input6*.py/.sh logs.",
     checks((PASS,"Human/cow routing and protein-first codon alignment are frame-consistent","441 codon columns"),(PASS,"Documented PAL2NAL empty-output trap reproduces on the MAFFT rabbit route","exit 0, zero bytes, inconsistency error"),(PASS,"Clean control yields two PAL2NAL records","human/cow control"),(PASS,"Database-scale escape hatch executes","MMseqs2 finds HBA/HBB at 115 bits, E 3.096E-34"))),
    ("Adversarial", "PID definitions, deprecated APIs, exports, and examples", 37, 54,
     "Executed pairwise2/max_alignments/PID/IUPAC/export checks plus all five copied examples; see input7_adversarial.py, input7_R_biostrings.R, and run_examples.py logs.",
     checks((PASS,"pairwise2 deprecation and islice guidance are accurate","warning, AttributeError, OverflowError, and islice reproduce"),(PASS,"PID1-4 agree with EMBOSS and pwalign","43.6/46.4/45.8/45.0"),(FAIL,"Reference wording distinguishes the exact PID2 formula","the shown formula is exactly PID2, not merely 'similar to PID2'"),(PASS,"NUC.4.4, algorithm names, output formatting and exports reproduce","all checks pass"),(PASS,"All shipped examples run from the copied current source","five scripts complete without source bytecode writes"))),
    ("Variant B", "Fresh kinase-pair convention check", 39, 56,
     "Fresh real PKA/CDK2 pair not used in the HBA/HBB canonical input; see input8_kinase_conv.py, input8_ground_truth.sh, and input8_R_pwalign.R logs.",
     checks((PASS,"Global scores equal independent Gotoh and needle","124, 186.5, and 110 as configured"),(PASS,"BLAST mapping holds on a second protein family","local -12/-1=222 and identical HSP"),(PASS,"pwalign mapping holds on this pair","124/222/228"),(PASS,"Identity/significance advice fits a distant true homolog","29.1% PID2 and 90.1 bits"))),
    ("Edge", "Fresh mammal-CDS DNA alignment and unknown strand", 39, 56,
     "Fresh real six-mammal HBB CDS exercise; see input9_real_dna.py log.",
     checks((PASS,"NUC.4.4 global scores equal EMBOSS needle across five orthologs","all five agree"),(PASS,"Independent Gotoh agrees on human/cow","1666.5"),(PASS,"DNA-versus-protein routing threshold holds","minimum nucleotide PID1 85.2%"),(PASS,"Unknown-strand recipe recovers locus and score","183.0 and human span 126..246"))),
    ("Stress", "Fresh full-document code-fence execution", 39, 57,
     "Freshly extracted and executed all 16 Python fences from current SKILL.md plus all six reference files in WSL; see finalpass2_allblocks.py log.",
     checks((PASS,"Every current fenced Python block executes","16/16 with DeprecationWarning as error"),(PASS,"Semiglobal documented values are asserted","both return 40.0 and span 300..320"),(PASS,"parasail, edlib, pywfa and mappy comments are independently asserted","all four pass"),(PASS,"Export and substitution-count fences execute","FASTA/Clustal/PSL/SAM nonempty"),(PASS,"No source file was imported in place","audit copy used; source SHA-256 recorded"))),
    ("Variant A", "Fresh documented HHsearch command", 39, 57,
     "Fresh toy HH-suite profile database built from eight public globins, then current documented hhsearch command executed; see finalpass2_hhsearch.sh log.",
     checks((PASS,"Documented hhsearch flags execute against a real constructed database","query.a3m, -d toydb, -o query.hhr"),(PASS,"Result contains all eight ranked globin profiles","eight summary rows"),(PASS,"HBA query self-hit is strongly ranked","100.0 probability; E 1.8E-93"),(PASS,"Phylogenetic ordering is sensible","alpha, beta, then myoglobin profiles"))),
]

static = {
 "functional_suitability": (12,12,"All promised global, local, semiglobal, identity, strand, export, significance, library-routing and CLI paths executed."),
 "reliability": (11,12,"Explicit alphabet, empty-sequence, strand, internal-stop and PAL2NAL-empty-output traps are practical and reproduced."),
 "performance_context": (7,8,"SKILL.md is 299 lines and depth is routed to six focused references; the one index is concise."),
 "agent_usability": (15,16,"Goals, runnable patterns, configuration conventions, and observed failure modes are clear; some snippets intentionally rely on prior variables."),
 "human_usability": (8,8,"Frontmatter covers natural Needleman-Wunsch, Smith-Waterman, semiglobal, PID, strand, EMBOSS and BLAST requests."),
 "security": (11,12,"No credentials, dynamic execution, network calls, or destructive operations in shipped source; user FASTA paths remain caller-controlled."),
 "maintainability": (11,12,"Reference split, source examples and deterministic checks make updates localized; no formal automated test runner ships."),
 "agent_specific": (18,20,"Specific triggers, progressive disclosure, idempotent local computation and explicit handoffs to MMseqs2/HMMER/structure search are strong."),
}

def report_input(index, item):
    typ,label,basic,specialized,note,assertions = item
    return {"index": index, "type":typ, "label":label, "status":"COMPLETED", "status_flag":"✅", "note":note,
      "executed":True, "execution_note":note, "basic":basic, "specialized":specialized, "total":basic+specialized,
      "assertions_passed":sum(x["result"]==PASS for x in assertions), "assertions_total":len(assertions), "assertions":assertions}

rows=[report_input(i+1,x) for i,x in enumerate(inputs)]
avg=round(sum(x["total"] for x in rows)/len(rows),1)
passed=sum(x["assertions_passed"] for x in rows); total=sum(x["assertions_total"] for x in rows)
subtotal=sum(x[0] for x in static.values()); sw=round(subtotal*.4,1); dw=round(avg*.6,1); score=round(sw+dw)
report={
 "meta":{"skill_name":"bio-alignment-pairwise","description":"Perform pairwise sequence alignment using Biopython Bio.Align.PairwiseAligner for global, local, semiglobal, identity, strand and reproducibility workflows.","evaluated_on":"2026-09-23","evaluator_version":"skill-auditor@1.0","category":"Data Analysis","execution_mode":"A","complexity":"Complex","n_inputs":len(rows),"source":SOURCE,"reaudit_of":"F:\\OpenScience\\audits\\_phase1-20260922\\bio-alignment-pairwise (86, Production Ready)","fix_log":"F:\\optimizing-agent-science-skills\\fixes\\bio-alignment-pairwise.md (read; not evidence)","executed_inputs":f"{len(rows)}/{len(rows)}","auditor_independent":False,"note":"final pass: fixed and audited under one brief, see CHECKPOINT.md","environment":"alignment audit environment: Windows Biopython 1.88/parasail/edlib; WSL alignment Biopython 1.88, EMBOSS, BLAST+, MAFFT, PAL2NAL, MMseqs2, pywfa and mappy; WSL bio HH-suite 3.3.0; R pwalign 1.2.0.","execution_note":"Nine substantive Phase-1 inputs were rerun against the exact d45a647 source copy; inputs 10 and 11 are fresh all-fence and HHsearch tests. All reported evidence has a saved script and checked output."},
 "veto_gates":{"skill_veto":{"gate":"PASS","stability":"PASS","contract":"PASS","determinism":"PASS","security":"PASS"},"research_veto":{"applicable":True,"gate":"PASS","scientific_integrity":{"result":"PASS","detail":"Real public sequences, seeded synthetic perturbations, independent implementations and cross-tool checks support every scored numeric conclusion."},"practice_boundaries":{"result":"PASS","detail":"Sequence-comparison methods only; no individual diagnostic or treatment guidance."},"methodological_ground":{"result":"PASS","detail":"Gap conventions, null-based significance, codon-aware handling, database-scale escape hatches and strand logic passed fresh checks."},"code_usability":{"result":"PASS","detail":"16/16 current Python fences and all five shipped examples executed from an audit copy; current CLI blocks ran on real data."}}},
 "static_score":{"subtotal":subtotal,"max":100,"categories":{k:{"score":v[0],"max":v[1],"note":v[2]} for k,v in static.items()}},
 "dynamic_score":{"execution_avg":avg,"max":100,"assertion_pass_rate":{"passed":passed,"total":total},"inputs":rows},
 "final":{"static_weighted":sw,"dynamic_weighted":dw,"score":score,"max":100,"grade":"Production Ready","grade_symbol":"⭐","deployable":True,"veto_override":False},
 "key_strengths":["The gap-convention table was confirmed on two real protein families by independent Gotoh, EMBOSS, BLAST+ and pwalign.","The final reference split keeps SKILL.md concise while every current Python fence still executes.","The current pure-Python dinucleotide shuffle, PAL2NAL empty-output trap and HHsearch database command were exercised rather than assumed.","Clear boundaries route unsuitable pairwise work to MMseqs2, HMMER or structural search."],
 "recommendations":[{"priority":"P2","title":"Name the shown percent-identity formula PID2 exactly","observed_in":[7],"problem":"The formula identities/(identities+mismatches) is PID2 exactly, but references/percent-identity.md calls it only 'similar to PID2'.","root_cause":"The prose retains cautious wording after the formula was made explicit.","fix":"Replace 'similar to PID2' with 'PID2 (aligned residue pairs excluding gaps)' and retain the pointer to PID1-4."}]
}

# Schema and task-specific checks before emitting.
assert report["meta"]["auditor_independent"] is False and report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert subtotal==sum(x["score"] for x in report["static_score"]["categories"].values())
assert len(rows)==report["meta"]["n_inputs"] and all(x["executed"] and x["execution_note"] for x in rows)
assert all(3<=len(x["assertions"])<=5 and x["basic"]+x["specialized"]==x["total"] for x in rows)
assert all(x["assertions_passed"]==sum(a["result"]==PASS for a in x["assertions"]) for x in rows)
assert report["final"]["score"]==round(sw+dw)
(OUT / "eval_report_bio-alignment-pairwise_result.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

lines=["# Eval Viewer — bio-alignment-pairwise (final-pass Phase 2)","",f"Generated: 2026-09-23  |  Source: `{SOURCE}`","","> Final-pass exception: `auditor_independent: false`; fixed and audited under one brief, see `F:\\OpenScience\\audits\\_final_pass\\bio-alignment-pairwise\\CHECKPOINT.md`.","", "## Summary", "", "| Input | Type | Total | Assertions | Executed |", "|---|---|---:|---:|---|"]
for x in rows: lines.append(f"| {x['index']} | {x['type']} — {x['label']} | {x['total']}/100 | {x['assertions_passed']}/{x['assertions_total']} | true |")
lines += ["",f"Execution average: **{avg}/100**. Assertions: **{passed}/{total} ({passed/total*100:.1f}%)**. All **{len(rows)}/{len(rows)}** inputs executed.","",f"Static: **{subtotal}/100**. Final: **{score}/100 — ⭐ Production Ready**. Deployable: **true**. Veto: **PASS**.","", "## Evidence", "", "The pre-Phase-2 report was moved intact to `F:\\OpenScience\\audits\\_phase1-20260922\\bio-alignment-pairwise`. The audit source was copied from the exact current tip into `run/skill`; SHA-256 for current `SKILL.md` is `D97AB041A0A716DE9D4D0465F4C006A462F8AF61444B3DF58A9560FB375F6EDF`. All scripts and raw logs are in `run/`.","", "## Detailed Inputs", ""]
for x in rows:
    lines += [f"### Input {x['index']} — {x['label']}","",f"**Executed:** `{x['executed']}`. {x['execution_note']}","",f"**Score:** Basic {x['basic']}/40 | Specialized {x['specialized']}/60 | Total {x['total']}/100.","", "**Assertions:**"]
    lines += [f"- [{a['result']}] {a['text']} — {a['note']}" for a in x['assertions']]
    lines.append("")
lines += ["## Veto Gates", "", "Skill veto: PASS (stable current fences/examples; valid frontmatter; seeded or deterministic numerical paths; no credential/network/dynamic-code behavior).", "", "Research veto: PASS. The evidence is computational sequence analysis, uses public data or explicitly seeded synthetic data, and makes no diagnostic/prescriptive claims. Independent Gotoh, EMBOSS, BLAST+, pwalign, parasail, edlib, MMseqs2, PAL2NAL, HH-suite and cross-reference checks were used where applicable.", "", "## Recommendation", "", "- P2: Name the displayed `identities / (identities + mismatches)` formula exactly PID2 rather than only similar to PID2."]
(OUT / "eval_viewer_bio-alignment-pairwise.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
print(f"wrote score={score}, avg={avg}, assertions={passed}/{total}, inputs={len(rows)}")
