amplicon_bp = 460
read_pair_bp = 250 + 250
min_overlap = 12
slack = read_pair_bp - (amplicon_bp + min_overlap)
assert slack == 28
assert 230 + 230 < amplicon_bp + min_overlap
assert 250 + 222 == amplicon_bp + min_overlap
print(f'V3V4_BUDGET_PASS slack={slack}bp exact_boundary=250+222')
