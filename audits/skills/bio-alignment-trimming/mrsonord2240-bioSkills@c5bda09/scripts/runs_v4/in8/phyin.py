# PhyIN: Trimming DNA alignments by phylogenetic incompatibility among neighbouring sites

# Wayne Maddison
# This is translated from Java, so please forgive my accent

version = "1.0, November 2024"
# Distributed under an MIT License (see end of file)
# Look for new versions here: https://github.com/wmaddisn/PhyIN

#example command:
# python phyin.py -input alignment.fas -output trimmedAlignment.fas -b 10 -d 2 -p 0.5 -e -sot 0
# or
# python3 phyin.py -input alignment.fas -output trimmedAlignment.fas -b 10 -d 2 -p 0.5 -e -sot 0
#
# Requires python3
# Requires fasta formatted alignment files
# Requires nucleotide data


#============================= Setting up parameters ===================
inFileName = "infile.fas"
outFileName = "outfile.fas"

#PhyIN parameter defaults
blockLength = 10 # parameter b
propConflict = 0.5 # parameter p, proportion of neighbouring sites in conflict to trigger block selection
neighbourDistance = 2 # parameter d
gapsAsExtraState = True # parameter e, whether non-terminal gaps are treated as an extra state

#The following two parameters control site occupancy trimming, which is not formally part of PhyIN,  
# but which is provided as a convenience, because PhyIN does not otherwise filter for extreme gappiness
siteOccupancyThreshold = 0.0 # parameter sot, minimum site occupancy to keep site. A gappiness filter that is applied after PhyIN.
siteOccupancyTotalNumberTaxa = 0 # parameter sotnt, listing number of taxa assumed for whole dataset if sot>0. Used for pipeline processing so that individual files can have the filter applied as if for whole set of taxa for all loci

import argparse
parser = argparse.ArgumentParser("phyin")
parser.add_argument("-input", help="File to be read. Must be DNA/RNA data and in FASTA format, aligned.", default = "infile.fas")
parser.add_argument("-output", help="File to be written.", default = "outfile.fas")
parser.add_argument("-b", help="Length of blocks over which conflict proportions are assessed. Integer.", type=int, default = blockLength)
parser.add_argument("-d", help="Distance surveyed for conflict among neighbours. Integer.", type=int, default = neighbourDistance)
parser.add_argument("-p", help="Proportion of neighbouring sites in conflict to trigger block selection. Proportion (0 to 1)", type=float, default = propConflict)
parser.add_argument("-e", help="Treat gaps as an extra state.", action='store_true')
parser.add_argument("-not.e", help="Don't treat gaps as an extra state.", dest='e', action='store_false')
#The following two arguments add a site occupancy filter (not formally part of PhyIN). 
# If they are not included, site occupancy trimming is not done.  
parser.add_argument("-sot", help="Minimum site occupancy. (Optional.) Sites with proportion of non-gaps less than this will be removed. Proportion (0 to 1)", type=float, default = siteOccupancyThreshold)
parser.add_argument("-sotnt", help="Number of taxa assumed for site occupancy filter. If 0, then use number of taxa in input file. Integer.", type=int, default = siteOccupancyTotalNumberTaxa)
parser.set_defaults(e=True)
parser.add_argument("-v", help="Verbose.", action="store_true", default = False)
args = parser.parse_args()
inFileName = args.input
outFileName = args.output
blockLength = args.b
propConflict = args.p
gapsAsExtraState = args.e
neighbourDistance = args.d
verbose = args.v
siteOccupancyThreshold = args.sot
siteOccupancyTotalNumberTaxa = args.sotnt

numStates = 4 
if (gapsAsExtraState):
	numStates = 5 

if (verbose):
	print("\nPhyIN trimming of DNA sequence alignments (version", version, "), with parameters: ")
	print("   Length of blocks over which conflict proportions are assessed: ", args.b)
	print("   Proportion of neighbouring sites in conflict to trigger block selection: ", args.p)
	print("   Distance surveyed for conflict among neighbours: ", args.d)
	print("   Treat gaps as an extra state: ",  args.e)
	if (siteOccupancyThreashold>0):
		print("   Minimum site occupancy: ",  args.sot)
		if (args.sotnt > 0):
			print("   Number of taxa assumed for site occupancy filter: ",  args.sotnt)
			
	print("NOTE: PhyIN ignores ambiguity codes, and considers only A, a, C, c, G, g, T, t, U, u, and gaps (-).\n")
else:
	if (siteOccupancyThreshold > 0):
		if (args.sotnt > 0):
			print("PhyIN trimming (v.", version, "): b=", args.b, "p=", args.p, "d=", args.d, "e=",  args.e, "sot=", args.sot, "sotnt=", args.sotnt)
		else:
			print("PhyIN trimming (v.", version, "): b=", args.b, "p=", args.p, "d=", args.d, "e=",  args.e, "sot=", args.sot)
	else:
		print("PhyIN trimming (v.", version, "): b=", args.b, "p=", args.p, "d=", args.d, "e=",  args.e)

#============================= Reading the data ===================
# Read FASTA file
fastaFile = open(inFileName,'r')

# these are the lists that will hold the names and sequences.
names = [] # taxon names
sequences = [] # sequences

currentTaxon = 0
print("Reading file: ", inFileName)
for line in fastaFile: 
	line = line.strip() # strips end-of-line character
	if len(line)>0: #might not be needed, but in case there are blank lines, ignore them
		if line[0] == '>':  #The next taxon!
			names.append(line[1:]) #add this taxon name to the list of taxon names
			sequences.append("") #append an empty string to the list of sequences
			currentTaxon = len(sequences)-1 #remember what taxon number we're now on
			# print("Reading " + line[1:])
		else: 
			sequences[currentTaxon] += line #not a taxon, therefore sequence, therefore concatenate to the current taxon's sequence
fastaFile.close()

# Minimal error checking. 
if len(sequences) == 0:
	print("ERROR: No sequences read.")
	exit(42)

numChars = len(sequences[0]) #NUMBER OF CHARACTERS (sites, columns)
for x in sequences:
	if (len(x) != numChars):
		print("ERROR: This appears not to be an alignment; not all taxa have the same sequence length.")
		exit(43)
# perhaps put in here a check that it is DNA data? This is important because of assumption of 4 states + gap		
		
numTaxa = len(names) #NUMBER OF TAXA
print("Number of sequences (taxa): ", numTaxa, "; Number of sites: ", numChars)

# convert sequences as text to nucleotides as integer codes for quicker access later
def getStateAsNumber(s): #need to translate character in sequence to internal representation of states
	if s in ["A", "a"]:  
		return 0
	elif s in ["C", "c"]:
		return 1
	elif s in ["G", "g"]:
		return 2
	elif s in ["T", "t", "U", "u"]:
		return 3
	elif gapsAsExtraState and s == "-":
		return 4
	else: # NOTE: this ignores all ambiguous bases
		return -1

if (verbose):
	print("Finding conflict (incompatibilities) among neighbouring sites.")

#============================= Finding conflict (incompatibilities) among sites ===================
# Example with parameters b=10, d=1, p = 0.5
# AAATAAAAAACCAAAAAAAAAAA
# AAATTAAAACCAAAAAAAAAAAA
# AAAATAAAAAACAAAAAAAAAAA
# AAAAAAAAACAAAAAAAAAAAAA
#    ><
#          ><
#           ><
#    ©©    ©©©
#    ssssssssss
#    *********
# in the above, there are three pairs of conflicting neighbours (><). 
# These pass the simple binary version of the incompatibility criterion,
# in that all for combinations of states are present.
# The default is to look as well at two-away neighbours (d=2), but in this example
# there are no two-away neighbours that conflict.
#
# Thus, there are 5 conflicted characters (©).
# Thus, within the stretch of 10 shown by s, there are 5/10 conflicted characters, thus > 0.5 proportion.
# Thus, the stretch within that from first to last of the conflicted characters is selected (*).

#=============================

#Set up arrays with default values
hasConflict = [False for k in range(numChars)] # boolean array (numChars) of whether in conflict
taxonSequenceStart = [-1 for i in range(numTaxa)] # first non-gap site in taxon i
taxonSequenceEnd = [-1 for i in range(numTaxa)]  # last non-gap site in taxon i
statePairs = [[False for i in range(numStates)] for j in range(numStates)] # integer array i,j for compatibility test

#.............................
# determine first and last nucleotides of each sequence, since terminal gaps are forgiven
def getFirstInSequence(i):
	for k in range(numChars):
		if (sequences[i][k] != "-"):
			return k
	return -1
def getLastInSequence(i):
	for k in range(numChars):
		if (sequences[i][numChars-k-1] != "-"):
			return numChars-k-1
	return -1
numTaxaWithSequence = 0 # this records how many taxa have any sequence whatsoever (some could be entirely gaps!)
for i in range(numTaxa):
	taxonSequenceStart[i] = getFirstInSequence(i)
	taxonSequenceEnd[i] = getLastInSequence(i)
	if (taxonSequenceStart[i] >=0):
		numTaxaWithSequence += 1

#.............................
#Now let's check for incompatibilities

#The function to decide if two sites (columns) k1 and k2 are incompatible
def areIncompatible (k1, k2):
	#resetting record of state pairs present for the two sites
	for x in range(numStates):
		for y in range(numStates):
			statePairs[x][y] = False
	
	#harvest all patterns between the two columns k1 and k2
	for i in range(numTaxa):
		#Look only at taxa for which k1 and k2 are within their sequence (i.e. not in terminal gap region)
		if (taxonSequenceStart[i] >= 0 and k2 >= taxonSequenceStart[i] and k2 <= taxonSequenceEnd[i] and k2 >= taxonSequenceStart[i] and k2 <= taxonSequenceEnd[i]):
			state1 = getStateAsNumber(sequences[i][k1]) #state will be returned as 0, 1, 2, 3, 4, -1 (respectively: A, C, G, T, - (if extra state), other)
			state2 = getStateAsNumber(sequences[i][k2])
			if (state1 >=0 and state1<numStates and state2 >=0 and state2<numStates):
				statePairs[state1][state2] = True

	#To test for incompatibility, look for cycles in state to state occupancy graph (M. Steel)
	# If there is a cycle, it will be left behind after trimming terminal (single linked) edges from the graph
	#.............................
	def anyOtherConnectForward(s1, s2): # Is s1 paired only with s2, or with others as well?
		for m in range(numStates):
			if (s2 != m and statePairs[s1][m]):
				return True
		return False
	def anyOtherConnectBackward (s1, s2): # Is s2 paired only with s1, or with others as well?
		for m in range(numStates):
			if (s1 != m and statePairs[m][s2]):
				return True
		return False	
	def trimSingleConnects(): #Trim a state from the statePairs list if it has only one pairing, because it must be a singleton
		#That is, turn statePairs[i][k] to false if it is the only pairing among statePairs[i]
		for s1 in range(numStates):
			for s2 in range(numStates):
				if (statePairs[s1][s2]): #the pairing is present
					if (not anyOtherConnectForward(s1, s2)): 
						statePairs[s1][s2] = False #but it is the only one for s1, and so it is a singleton and should be trimmed
						return True
					if (not anyOtherConnectBackward(s1, s2)):
						statePairs[s1][s2] = False #but it is the only one for s2, and so it is a singleton and should be trimmed
						return True			
		return False	
	#.............................
	# Trim single links iteratively until there are no more
	stopper = 1000 #just in case something goes wrong!
	#trim state pair graph iteratively for single connections
	while trimSingleConnects() and stopper > 0:
		stopper -= 1
		if (stopper <= 1):
			print("ALERT SOMETHING WENT WRONG WITH THE PhyIN calculations (trimSingleConnects too many iterations)")
			exit(44)
	#.............................
	#OK, all single connects have been iteratively trimmed.
	#If any state pairs remain, there must have been a cycle, hence incompatibility
	for s1 in range(numStates):
		for s2 in range(numStates):
			if (statePairs[s1][s2]>0):
				return True

	return False
	#That was the incompatibility test for sites k1 and k2

#.............................
# Now do the survey of sites to mark sites that are conflicted
# Mark sites in conflict. Currently looks only to immediate neighbour. 
for k in range(numChars): #For each site k
	for d in range(1, neighbourDistance+1): #Look whether neighbours at varying distances from 1 to neighbourDistance away from k are in conflict
		if (areIncompatible(k, k+d)): # site k+d is in conflict with k
				hasConflict[k] = True  #therefore mark k as having a conflict
				if (k+d<numChars):
					hasConflict[k+d] = True #if k is in conflict with k+d, reverse must be true as well
	if (verbose and ((k +1) % 100 == 0)):
		print(" ", k, " sites assessed.")

#At this point, individual sites having conflict are marked

#============================= Finding regions (blocks) with too much conflict ===================
# Scan for blocks with too much conflict. Selects only from conflicting to conflicting, even if that is less than blockLength

# This array will record whether the site is marked for deletion
toDelete = [False for k in range(numChars)]

#.............................
# Look to see if k is start of bad block. 
def selectBlockByProportion(k):
	if (not hasConflict[k]): #a bad block must start and end with a conflicting site
		return
	count = 0
	lastHit = numChars-1
	for b in range(blockLength):
		if (k+b>= numChars):
			break
		if (hasConflict[k+b]):
			count+=1
			lastHit = k+b

	if (1.0*count/blockLength >= propConflict):
		for k2 in range (k, lastHit+1):  #even though assessed over blockLength, delete only to last conflicted site
			toDelete[k2]= True

#Check all sites to see if they are the start of a bad block
for k in range(numChars):
	selectBlockByProportion(k)

# count how many are to be deleted (just for user's information)
numDeleted = 0
for k in range(numChars):
	if (toDelete[k]):
		numDeleted += 1

if (siteOccupancyThreshold<=0): #Just using PhyIN; therefore, time to report results
	if (verbose):
		print("Incompatibilities assessed. Total sites originally:", numChars, " Deleted by PhyIN:", numDeleted, "\n")
	else:
		print("Total sites originally:", numChars, " Deleted by PhyIN:", numDeleted, "Retained:", (numChars-numDeleted))

#============================= Performing optional site occupancy filter ===================
if (siteOccupancyThreshold>0):
	if (siteOccupancyTotalNumberTaxa>0):
		totalNumTaxa = siteOccupancyTotalNumberTaxa
	else:
		totalNumTaxa = numTaxa
	numTooSparse = 0
	retained = numChars
	for ic in range(numChars):
		occupancy = 0
		for it in range(numTaxa):
			if (sequences[it][ic] != "-"):
				occupancy+=1
		if (occupancy*1.0/totalNumTaxa < siteOccupancyThreshold): #/too little occupancy! (too many gaps)
			toDelete[ic] = True
			numTooSparse += 1
		if (toDelete[ic]):
			retained -= 1
	if (verbose):
		print("Incompatibilities & site occupancy assessed. Total sites originally:", numChars, " Deleted by PhyIN:", numDeleted, "Below occupancy threshold:", numTooSparse, "Total retained: ", retained, "\n")
	else:
		print("Total sites originally:", numChars, " Deleted by PhyIN:", numDeleted, "Deleted (too gappy):", numTooSparse, "Retained: ", retained)

#============================= Writing sequences without high conflict regions (trimmed) ===================
if (verbose):
	print("Writing trimmed sequences to file " + outFileName)
#Sites to delete have been found.  Now to write the output file without them
outputFile = open(outFileName,'w')

for i in range(numTaxa):
	outputFile.write(">")
	outputFile.write(names[i])
	outputFile.write("\n")
	lineLength = 0
	for k in range(numChars):
		if (not toDelete[k]):
			outputFile.write(sequences[i][k])
			lineLength += 1
			if (lineLength % 50 == 0):
				outputFile.write("\n")
	outputFile.write("\n") 
	
outputFile.close() 


# MIT License
# 
# Copyright (c) 2024 Wayne Maddison
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
