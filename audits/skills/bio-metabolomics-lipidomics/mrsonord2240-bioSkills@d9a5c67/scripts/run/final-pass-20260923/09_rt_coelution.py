from statistics import median

def classify_lpc(lpc_rt, parent_pc_rt, tolerance=0.10):
    return "SUSPECT_IN_SOURCE_FRAGMENT" if abs(lpc_rt - parent_pc_rt) <= tolerance else "RETENTION_TIME_DISTINCT"

coeluting = classify_lpc(5.02, 5.00)
distinct = classify_lpc(3.21, 5.00)
assert coeluting == "SUSPECT_IN_SOURCE_FRAGMENT"
assert distinct == "RETENTION_TIME_DISTINCT"
print(f"coeluting_LPC={coeluting}; distinct_LPC={distinct}; tolerance=0.10 min")
print("PASS RT classifier distinguishes a parent-coeluting artifact from a chromatographically distinct LPC")
