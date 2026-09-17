# Input 3 (regression) -- Edge: blocking on a near-noise factor with only 2 blocks
# Prompt: "My technician wants to block by cage even though there's basically no cage-to-cage
# variability, and I only have 2 cages (3 ctrl/3 treat each). Should I block on cage? What's
# the risk with only 2 blocks?"
set.seed(2026091703)
cage <- rep(c('cage1', 'cage2'), each = 6)
condition <- rep(rep(c('ctrl', 'treat'), each = 3), 2)
cage_effect <- setNames(rnorm(2, 0, 0.05), c('cage1', 'cage2'))  # ~0 true cage variance
y <- 0.4 * (condition == 'treat') + cage_effect[cage] + rnorm(12, 0, 1)
df <- data.frame(cage = factor(cage), condition = factor(condition), y = y)

unblocked <- lm(y ~ condition, data = df)
blocked   <- lm(y ~ cage + condition, data = df)
p_unblocked <- coef(summary(unblocked))['conditiontreat', 'Pr(>|t|)']
p_blocked   <- coef(summary(blocked))['conditiontreat', 'Pr(>|t|)']
cat(sprintf('Unblocked p(condition) = %.3f\nBlocked   p(condition) = %.3f\n', p_unblocked, p_blocked))
print(anova(blocked))
