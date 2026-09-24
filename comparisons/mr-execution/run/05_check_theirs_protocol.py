# Asserts on the theirs-side (prose-only) output: does it contain any data-derived number, and which named methods/warnings?
import re, io
t = io.open(r"F:\OpenScience\comparisons\mr-execution\run\04_theirs_protocol_output.md", encoding="utf-8").read()
resp = re.sub(r"\s+", " ", t.split("## A. Study framing")[1].split("# What this response contains")[0])
data_numbers = re.findall(r"\b0\.\d{2,}\b|\bp\s*=\s*[\d.e-]+\b(?!.*5e-8)", resp)
print("data-derived numbers in response body:", [x for x in data_numbers])
for k in ["IVW", "weighted median", "Egger", "MR-PRESSO", "leave-one-out", "Steiger", "directional pleiotropy", "F-statistic"]:
    print(f"{k:24s} named: {k.lower() in resp.lower()}")
print("executed_estimate_present:", bool(re.search(r"\bbeta\s*=\s*-?\d", resp)))
