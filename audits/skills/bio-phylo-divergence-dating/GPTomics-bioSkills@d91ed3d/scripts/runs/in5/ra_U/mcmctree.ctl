seed = 1234
seqfile = loc1.phy
treefile = tree.nwk
mcmcfile = mcmc.txt
outfile = out.txt

ndata = 1
seqtype = 0
usedata = 0
clock = 2
RootAge = U(1.0)

model = 4
alpha = 0.5
ncatG = 5
cleandata = 0

BDparas = 1 1 0.1 m
kappa_gamma = 6 2
alpha_gamma = 1 1
rgene_gamma = 2 8 1
sigma2_gamma = 1 10 1

print = 1
burnin = 20000
sampfreq = 20
nsample = 10000
