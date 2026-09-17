# Input 3 (Edge/boundary) — blocking on a near-noise factor with very few blocks
# Prompt: "My technician insists on blocking by cage even though there's basically no
#  cage-to-cage variability, and I only have 2 cages total (3 mice each, split evenly
#  control/treat). Should I block on cage? What's the risk with only 2 blocks?"
# SYNTHETIC data: cage effect deliberately set to ~0 (noise factor), only 2 blocks.

set.seed(2026091703)
n_cages <- 2
per_cage <- 6  # 3 ctrl, 3 treat

df <- expand.grid(cage = paste0('C', 1:n_cages), rep = 1:per_cage)
df$condition <- rep(c('ctrl', 'ctrl', 'ctrl', 'treat', 'treat', 'treat'), times = n_cages)
cage_effect <- setNames(rnorm(n_cages, 0, 0.02), paste0('C', 1:n_cages))  # ~0 real cage variance
df$response <- cage_effect[df$cage] + ifelse(df$condition == 'treat', 0.4, 0) + rnorm(nrow(df), 0, 1)

cat('=== Unblocked model: response ~ condition (2 df error saved) ===\n')
m0 <- lm(response ~ condition, data = df)
print(anova(m0))

cat('\n=== Blocked model: response ~ cage + condition (spends 1 df on cage) ===\n')
m1 <- lm(response ~ cage + condition, data = df)
print(anova(m1))

cat('\n=== ASSERTION CHECK ===\n')
p0 <- anova(m0)['condition', 'Pr(>F)']
p1 <- anova(m1)['condition', 'Pr(>F)']
cage_ss <- anova(m1)['cage', 'Sum Sq']
resid_ss0 <- anova(m0)['Residuals', 'Sum Sq']
cat('Blocking on cage removes negligible variance (cage SS small relative to residual):',
    cage_ss / resid_ss0 < 0.05, ' (cage SS=', round(cage_ss,3), ', unblocked resid SS=', round(resid_ss0,3), ')\n')
cat('Blocked-model p-value for condition is >= unblocked p-value (blocking on noise costs power):',
    p1 >= p0, ' (unblocked p=', signif(p0,3), ', blocked p=', signif(p1,3), ')\n')
cat('Only 2 blocks available -> blocking spends 1 of very few error df (n=12 total):',
    n_cages == 2, '\n')
