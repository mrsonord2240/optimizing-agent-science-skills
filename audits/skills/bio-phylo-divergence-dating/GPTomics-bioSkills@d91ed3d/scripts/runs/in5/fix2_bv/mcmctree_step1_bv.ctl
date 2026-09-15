seed = -1
seqfile = alignment.phy
treefile = calibrated_tree.nwk
outfile = step1.out

ndata = 1
usedata = 3
clock = 2
RootAge = <1.0

model = 4
alpha = 0.5
ncatG = 4
cleandata = 0

BDparas = 1 1 0.1 m
kappa_gamma = 6 2
alpha_gamma = 1 1
rgene_gamma = 2 20 1
sigma2_gamma = 1 10 1

print = 1
burnin = 5000
sampfreq = 50
nsample = 5000
