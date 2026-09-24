"""
Round-3 re-audit, Input 1 (Canonical, REGRESSION) + Input 6 (NEW).

Regression-tests the round-3 fix's headline claim (SKILL.md, mrsonord2240/bioSkills@9d31109,
"Chronos (Dempster 2021)" section, comment on negative_control_sgrnas): omitting
negative_control_sgrnas makes chronos.Chronos(...) CONSTRUCTION raise
  ValueError("excess_variance was passed as dict without key for <library>: {}")
before train() is ever called -- NOT UnboundLocalError('prior_variance') at train(), which is
what SKILL.md said before this fix (and what the round-2 re-audit's Input 4 caught as a
documentation bug, now supposedly fixed).

Also (Input 6, NEW -- not run by either prior audit): passes negative_control_sgrnas as an
EXPLICIT EMPTY dict {'screen': []} rather than omitting the argument entirely. The fix log
claims this produces a *different* ValueError ("set of negative_control_sgrnas is empty") but
that claim was never independently verified by an audit -- it is the fixer's own unverified
aside. SKILL.md's Common Errors table only documents the omitted-argument case; if the
empty-dict case produces something else, that is a real documentation gap this audit would be
the first to catch.

Real single-line HAP1 TKOv3 data (planted ERBB2 amplicon), reused from the round-2 audit.
"""
import sys
import pandas as pd

sys.path.insert(0, "F:/OpenScience/audit-envs/crispr-screen-analyst/tools/chronos-venv/Lib/site-packages")
import chronos

counts = pd.read_csv("../../data/hap1_tkov3_planted_erbb2amp_counts.txt", sep="\t")

guide_gene_map = counts[["sgRNA", "gene"]].drop_duplicates().rename(columns={"sgRNA": "sgrna"})

readcounts = counts.set_index("sgRNA")[["HAP1_T0", "HAP1_T18A", "HAP1_T18B", "HAP1_T18C"]].T
readcounts.index.name = "sequence_ID"

sequence_map = pd.DataFrame({
    "sequence_ID": ["HAP1_T0", "HAP1_T18A", "HAP1_T18B", "HAP1_T18C"],
    "cell_line_name": ["pDNA", "HAP1", "HAP1", "HAP1"],
    "days": [0, 18, 18, 18],
    "pDNA_batch": ["batch1", "batch1", "batch1", "batch1"],
})

print("=== Input 1 (regression): negative_control_sgrnas OMITTED entirely ===")
try:
    model = chronos.Chronos(
        sequence_map={"screen": sequence_map},
        guide_gene_map={"screen": guide_gene_map},
        readcounts={"screen": readcounts},
    )
    print("Chronos(...) construction SUCCEEDED without negative_control_sgrnas -- unexpected, "
          "SKILL.md's claim that construction raises would be wrong.")
    print("Proceeding to train() to see if the OLD documented UnboundLocalError happens there instead...")
    try:
        model.train(nepochs=5)
        print("train() also SUCCEEDED -- neither documented failure occurred.")
    except UnboundLocalError as e:
        print(f"train() raised UnboundLocalError: {e} -- matches the OLD (pre-round-3) SKILL.md text, "
              f"contradicts the round-3 fix's claim that this happens at construction.")
    except Exception as e:
        print(f"train() raised {type(e).__name__}: {e}")
except ValueError as e:
    print(f"Chronos(...) construction raised ValueError: {e}")
    msg = str(e)
    expected_substr = "excess_variance was passed as dict without key for"
    if expected_substr in msg:
        print(f'>>> MATCHES SKILL.md\'s round-3 claim verbatim (contains "{expected_substr}").')
    else:
        print(f'>>> Exception type matches (ValueError) but message text does NOT contain the '
              f'documented substring "{expected_substr}" -- partial match only.')
except UnboundLocalError as e:
    print(f"Chronos(...) construction raised UnboundLocalError directly: {e} -- this would mean "
          f"the internal catch-and-reraise SKILL.md describes does NOT happen, contradicting the fix.")
except Exception as e:
    print(f"Chronos(...) construction raised an unexpected exception type {type(e).__name__}: {e}")

print()
print("=== Input 6 (NEW): negative_control_sgrnas passed as an EXPLICIT EMPTY dict {'screen': []} ===")
try:
    model2 = chronos.Chronos(
        sequence_map={"screen": sequence_map},
        guide_gene_map={"screen": guide_gene_map},
        readcounts={"screen": readcounts},
        negative_control_sgrnas={"screen": []},
    )
    print("Chronos(...) construction SUCCEEDED with an empty negative_control_sgrnas list -- "
          "unexpected if the fix log's aside claim is right.")
    try:
        model2.train(nepochs=5)
        print("train() also SUCCEEDED with an empty negative-control list.")
    except Exception as e:
        print(f"train() raised {type(e).__name__}: {e}")
except ValueError as e:
    print(f"Chronos(...) construction raised ValueError: {e}")
    if "empty" in str(e).lower():
        print('>>> Message mentions "empty" -- consistent with the fix log\'s unverified aside '
              '("set of negative_control_sgrnas is empty"), now independently confirmed.')
    else:
        print(">>> ValueError raised, but message text differs from the fix log's aside -- "
              "worth noting exact wording for the report.")
except Exception as e:
    print(f"Chronos(...) construction raised {type(e).__name__}: {e}")

print("\nDONE")
