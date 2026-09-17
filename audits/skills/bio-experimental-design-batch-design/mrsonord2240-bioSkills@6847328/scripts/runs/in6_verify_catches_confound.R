# Batch-design Input 6 (NEW, targets the P2 fix "no verification step after optimization"):
# "My core just handed back this plate map -- can you sanity-check it before we run it?" where
# the handed-back map is GENUINELY confounded (a whole condition is missing from one batch), the
# way a suboptimal or hand-edited layout could be. This tests whether the new verification block
# (b02_verify, same code used in Input 1 and inside b03_bridge) is a REAL gate that halts on a
# confounded layout, not just a table that gets printed and ignored.
# v2: fixes two bugs in the first version of this script (not in the Skill) -- the "balanced
# layout should NOT halt" check re-read a stale `assignment` object instead of the balanced one,
# and the bridge-plex condition vector did not sum to 60 rows.
.libPaths(c('F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/R-lib', .libPaths()))
BB <- 'F:/OpenScience/audits/bio-experimental-design-batch-design'

# --- Test A: a layout with a real confound: batch 3 has zero controls (all case). This is the
# exact failure mode SKILL.md's stopifnot message names.
assignment <- data.frame(
  id = sprintf('S%02d', 1:24),
  condition = c(rep(c('ctrl','treat'), 8), rep('treat', 8)),
  batch = rep(c('B1','B2','B3'), each = 8)
)
cat('Test A -- handed-back layout deliberately confounded in B3:\n')
print(table(assignment$condition, assignment$batch))
resA <- tryCatch({
  sys.source(file.path(BB, 'runs', 'blocks', 'b02_verify.R'), envir = globalenv())
  'NO ERROR -- verification passed silently (BAD: this layout IS confounded)'
}, error = function(e) paste('stopifnot HALTED:', conditionMessage(e)))
cat('[Test A: b02_verify on a confounded hand-back]', resA, '\n\n')

# --- Test B: the SAME block on a genuinely balanced layout must NOT halt.
assignment <- data.frame(
  id = sprintf('S%02d', 1:24),
  condition = rep(c('ctrl','treat'), each = 12),
  batch = rep(c('B1','B2','B3'), 8)
)
cat('Test B -- balanced layout:\n')
print(table(assignment$condition, assignment$batch))
resB <- tryCatch({
  invisible(capture.output(sys.source(file.path(BB, 'runs', 'blocks', 'b02_verify.R'), envir = globalenv())))
  'NO ERROR -- verification passed (expected on a balanced layout)'
}, error = function(e) paste('stopifnot HALTED (unexpected):', conditionMessage(e)))
cat('[Test B: b02_verify on a balanced layout]', resB, '\n\n')

# --- Test C: the bridge-channel verification's confounding line (same pattern, standalone) --
# a plex missing a whole condition should also halt there. 60 samples, plex 1 is all-case.
cond60 <- c(rep('case', 15), rep(c('case','ctrl'), length.out = 45))
stopifnot(length(cond60) == 60)
assignment3 <- data.frame(id = sprintf('S%02d', 1:60), condition = cond60, plex = rep(1:4, each = 15))
tab3 <- table(assignment3$condition, assignment3$plex)
cat('Test C -- bridge-layout hand-back (plex 1 deliberately all-case):\n'); print(tab3)
resC <- tryCatch({ stopifnot(all(tab3 > 0)); 'NO ERROR' }, error = function(e) paste('stopifnot HALTED:', conditionMessage(e)))
cat('[Test C: bridge confounding check]', resC, '\n')
