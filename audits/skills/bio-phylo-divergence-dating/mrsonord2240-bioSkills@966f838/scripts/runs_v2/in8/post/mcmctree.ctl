seed = 1234
seqfile = species2loci.phy
treefile = calibrated.tre
mcmcfile = mcmc.txt
outfile = out.txt

ndata = 2
usedata = 2 in.BV
clock = 2
RootAge = <1.0

model = 4
alpha = 0.5
ncatG = 4
cleandata = 0

BDparas = 1 1 0.1 m
kappa_gamma = 6 2
alpha_gamma = 1 1
rgene_gamma = 2 8 1
sigma2_gamma = 1 10 1

print = 1
burnin = 50000
sampfreq = 50
nsample = 20000
