# Extracted verbatim from SKILL.md "Verify the optimized layout before trusting it"
# (post-fix SKILL.md; commit 6847328). Requires `assignment` in scope.
tab <- table(assignment$condition, assignment$batch)
print(tab)

# Hard fail: a whole condition missing from a batch means condition and batch are confounded in
# this layout, not merely unbalanced -- the design must not be used as-is.
stopifnot(
  "condition is confounded with batch in this layout (a batch has zero samples of some condition)" =
    all(tab > 0)
)

# Soft check: flag an avoidable imbalance so the agent iterates instead of shipping a sub-optimal
# split (see Input 2 above: 7/7/7/9 was accepted when 7/8/7/8 was achievable).
imbalance <- max(tab) - min(tab)
if (imbalance > 1) {
  warning(sprintf(
    'Largest cell minus smallest cell in condition x batch = %d; re-run optimize_design() with a
higher max_iter or a different random seed before accepting this layout.', imbalance))
}
