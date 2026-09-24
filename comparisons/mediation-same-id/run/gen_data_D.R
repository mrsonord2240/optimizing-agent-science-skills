# Dataset D: exposure-mediator interaction planted. Y = 0.2 G + 0.6 M + 0.4 G*M + e ; M = 0.5 G + e(0.8). No confounding.
# VanderWeele 4-way truth (a=1, a*=0, m*=0, E[M|G=0]=0): CDE 0.2, INTref 0, INTmed 0.4*0.5=0.2, PIE 0.6*0.5=0.3, TE 0.7.
set.seed(99); n <- 2000
D <- data.frame(genotype = rbinom(n, 2, 0.3), age = rnorm(n, 55, 10), sex = rbinom(n, 1, 0.5))
D$expression <- 0.5*D$genotype + rnorm(n, 0, 0.8)
D$y_cont <- 0.2*D$genotype + 0.6*D$expression + 0.4*D$genotype*D$expression + rnorm(n)
write.csv(D, 'F:/OpenScience/comparisons/mediation-same-id/data/D_interaction.csv', row.names = FALSE)
