#!/usr/local/python/python-2.5/bin/python2.5

################################################################################
# score_conservation.cgi - Copyright Tony Capra 2007 - Last Update: 7/23/07
#
# 7/23/07 - fixed shannon_entropy base bug
# 6/26/07 - fixed read_clustal_align bug
#
# Dependencies: 
# numarray - 
#  http://sourceforge.net/project/showfiles.php?group_id=1369&release_id=223264
# 
#
# This program supports the paper _Predicting Functionally Important Residues
# by Sequence Conservation_ by Capra and Singh 2007.
#
# It contains code for each method of scoring conservation that is
# evaluated: sum of pairs, weighted sum of pairs, Shannon entropy, Shannon
# entropy with property groupings (Valdar and Thornton 01), von
# Neumann entropy (Caffrey et al 04), relative entropy (Samudrala and Wang 06),
# and Jensen-Shannon divergence. 
#
# The code distributed with Mayrose et al 04 is used for Rate4Site. As of today
# it can be obtained from:
# http://www.tau.ac.il/~itaymay/cp/rate4site.html
# 
# 
# All scoring functions follow the same prototype:
#
# def score(col, sim_matrix, bg_disr, seq_weights, gap_penalty=1):
#
# - col: the column to be scored.
# 
# - sim_matrix: the similarity (scoring) matrix to be used. Not all 
# methods will use this parameter. 
# 
# - bg_distr: a list containing an amino acid probability distribution. Not
# all methods use this parameter. The default is the blosum62 background, but
# other distributions can be given. 
#
# - seq_weights: an array of floats that is used to weight the contribution
# of each seqeuence. If the len(seq_weights) != len(col), then every sequence 
# gets a weight of one.
#
# - gap_penalty: a binary variable: 0 for no gap penalty and 1
# for gap penalty. The default is to use a penalty. The gap penalty used is
# the score times the fraction of non-gap positions in the column.
#
#
# For a window score of any of above methods use the window_score method to 
# transform the individual column scores. 
#
################################################################################

import math, sys
import cgi, cStringIO
import cgitb; cgitb.enable()

##sys.path.append('/u/tonyc/lib/python/')
##from numarray import *
##import numarray.linear_algebra as la


PSEUDOCOUNT = .0000001

amino_acids = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V', '-']
iupac_alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "Y", "Z", "X", "*", "-"] 

# dictionary to map from amino acid to its row/column in a similarity matrix
aa_to_index = {}
for i, aa in enumerate(amino_acids):
    aa_to_index[aa] = i



################################################################################
# Frequency Count and Gap Penalty
################################################################################

def weighted_freq_count_pseudocount(col, seq_weights, pc_amount):
    """ Return the weighted frequency count for a column--with pseudocount."""

    # if the weights do not match, use equal weight
    if len(seq_weights) != len(col):
	 seq_weights = [1.] * len(col)

    aa_num = 0
    freq_counts = len(amino_acids)*[pc_amount] # in order defined by amino_acids

    for aa in amino_acids:
	 for j in range(len(col)):
	     if col[j] == aa:
		 freq_counts[aa_num] += 1 * seq_weights[j]

	 aa_num += 1

    for j in range(len(freq_counts)):
	 freq_counts[j] = freq_counts[j] / (sum(seq_weights) + len(amino_acids) * pc_amount)

    return freq_counts


def weighted_gap_penalty(col, seq_weights):
    """ Calculate the simple gap penalty multiplier for the column. If the 
    sequences are weighted, the gaps, when penalized, are weighted 
    accordingly. """

    # if the weights do not match, use equal weight
    if len(seq_weights) != len(col):
	 seq_weights = [1.] * len(col)
    
    gap_sum = 0.
    for i in range(len(col)):
	 if col[i] == '-':
	     gap_sum += seq_weights[i]

    return 1 - (gap_sum / sum(seq_weights))



################################################################################
# Shannon Entropy
################################################################################

def shannon_entropy(col, sim_matrix, bg_distr, seq_weights, gap_penalty=1):
    """Calculates the Shannon entropy of the column col. sim_matrix  and 
    bg_distr are ignored. If gap_penalty == 1, then gaps are penalized. The 
    entropy will be between zero and one because of its base. See p.13 of 
    Valdar 02 for details. The information score 1 - h is returned for the sake 
    of consistency with other scores."""

    fc = weighted_freq_count_pseudocount(col, seq_weights, PSEUDOCOUNT)

    h = 0. 
    for i in range(len(fc)):
	 if fc[i] != 0:
	     h += fc[i] * math.log(fc[i])

#    h /= math.log(len(fc))
    h /= math.log(min(len(fc), len(col)))

    inf_score = 1 - (-1 * h)

    if gap_penalty == 1: 
	 return inf_score * weighted_gap_penalty(col, seq_weights)
    else: 
	 return inf_score


################################################################################
# Property Entropy
################################################################################

def property_entropy(col, sim_matrix, bg_distr, seq_weights, gap_penalty=1):
    """Calculate the entropy of a column col relative to a partition of the 
    amino acids. Similar to Mirny '99. sim_matrix and bg_distr are ignored, but 
    could be used to define the sets. """

    # Mirny and Shakn. '99
    property_partition = [['A','V','L','I','M','C'], ['F','W','Y','H'], ['S','T','N','Q'], ['K','R'], ['D', 'E'], ['G', 'P'], ['-']]

    # Williamson '95
    # property_partition = [['V','L', 'I','M'], ['F','W','Y'], ['S','T'], ['N','Q'], ['H','K','R'], ['D','E'], ['A','G'], ['P'], ['C'], ['-']]

    fc = weighted_freq_count_pseudocount(col, seq_weights, PSEUDOCOUNT)

    # sum the aa frequencies to get the property frequencies
    prop_fc = [0.] * len(property_partition)
    for p in range(len(property_partition)):
	 for aa in property_partition[p]:
	     prop_fc[p] += fc[aa_to_index[aa]]

    h = 0. 
    for i in range(len(prop_fc)):
	 if prop_fc[i] != 0:
	     h += prop_fc[i] * math.log(prop_fc[i])

    h /= math.log(min(len(property_partition), len(col)))

    inf_score = 1 - (-1 * h)

    if gap_penalty == 1: 
	 return inf_score * weighted_gap_penalty(col, seq_weights)
    else: 
	 return inf_score


################################################################################
# von Neumann Entropy
################################################################################

def vn_entropy(col, sim_matrix, bg_distr, seq_weights, gap_penalty=1):
    """ Calculate the von Neuman Entropy as described in Caffrey et al. 04.
    This code was adapted from the implementation found in the PFAAT project 
    available on SourceForge. bg_distr is ignored."""

    aa_counts = [0.] * 20
    for aa in col:
	 if aa != '-': aa_counts[aa_to_index[aa]] += 1

    dm_size = 0
    dm_aas = []
    for i in range(len(aa_counts)):
	 if aa_counts[i] != 0:
	     dm_aas.append(i)
	     dm_size += 1

    if dm_size == 0: return 0.0

    row_i = 0
    col_i = 0
    dm = zeros((dm_size, dm_size), Float32)
    for i in range(dm_size):
	 row_i = dm_aas[i]
	 for j in range(dm_size):
	     col_i = dm_aas[j]
	     dm[i][j] = aa_counts[row_i] * sim_matrix[row_i][col_i]

#    ev = la.eigenvalues(dm).real
    ev = []

    temp = 0.
    for e in ev:
	 temp += e

    if temp != 0:
	 for i in range(len(ev)):
	     ev[i] = ev[i] / temp

    vne = 0.0
    for e in ev:
	 if e > (10**-10):
	     vne -= e * math.log(e) / math.log(20)

    if gap_penalty == 1: 
	 return (1-vne) * weighted_gap_penalty(col, seq_weights)
    else: 
	 return 1 - vne


################################################################################
# Relative Entropy 
################################################################################

def relative_entropy(col, sim_matix, bg_distr, seq_weights, gap_penalty=1):
    """Calculate the relative entropy of the column distribution with a 
    background distribution specified in bg_distr. This is similar to the 
    approach proposed in Wang and Samudrala 06. sim_matrix is ignored."""

    distr = bg_distr[:]

    fc = weighted_freq_count_pseudocount(col, seq_weights, PSEUDOCOUNT)

    # remove gap count
    if len(distr) == 20: 
	 new_fc = fc[:-1]
	 s = sum(new_fc)
	 for i in range(len(new_fc)):
	     new_fc[i] = new_fc[i] / s
	 fc = new_fc

    if len(fc) != len(distr): return -1

    d = 0.
    for i in range(len(fc)):
	 if distr[i] != 0.0:
	     d += fc[i] * math.log(fc[i]/distr[i])

    d /= math.log(len(fc))

    if gap_penalty == 1: 
	 return d * weighted_gap_penalty(col, seq_weights)
    else: 
	 return d



################################################################################
# Jensen-Shannon Divergence
################################################################################

def js_divergence(col, sim_matrix, bg_distr, seq_weights, gap_penalty=1):
    """ Return the Jensen-Shannon Divergence for the column with the background
    distribution bg_distr. sim_matrix is ignored. JSD is the default method."""

    distr = bg_distr[:]

    fc = weighted_freq_count_pseudocount(col, seq_weights, PSEUDOCOUNT)

    # if background distrubtion lacks a gap count, remove fc gap count
    if len(distr) == 20: 
	 new_fc = fc[:-1]
	 s = sum(new_fc)
	 for i in range(len(new_fc)):
	     new_fc[i] = new_fc[i] / s
	 fc = new_fc

    if len(fc) != len(distr): return -1

    # make r distriubtion
    r = []
    for i in range(len(fc)):
	 r.append(.5 * fc[i] + .5 * distr[i])

    d = 0.
    for i in range(len(fc)):
	 if r[i] != 0.0:
	     if fc[i] == 0.0:
		 d += distr[i] * math.log(distr[i]/r[i], 2)
	     elif distr[i] == 0.0:
		 d += fc[i] * math.log(fc[i]/r[i], 2) 
	     else:
		 d += fc[i] * math.log(fc[i]/r[i], 2) + distr[i] * math.log(distr[i]/r[i], 2)

    # d /= 2 * math.log(len(fc))
    d /= 2

    if gap_penalty == 1: 
	 return d * weighted_gap_penalty(col, seq_weights)
    else: 
	 return d


################################################################################
# Mutation Weighted Pairwise Match
################################################################################

def sum_of_pairs(col, sim_matrix, bg_distr, seq_weights, gap_penalty=1):
    """ Sum the similarity matrix values for all pairs in the column. 
    This method is similar to those proposed in Valdar 02. bg_distr is ignored."""

    sum = 0.
    max_sum = 0.

    for i in range(len(col)):
	 for j in range(i):
	     if col[i] != '-' and col[j] != '-':
		 max_sum += seq_weights[i] * seq_weights[j]
		 sum += seq_weights[i] * seq_weights[j] * sim_matrix[aa_to_index[col[i]]][aa_to_index[col[j]]]

    if max_sum != 0: 
	 sum /= max_sum
    else:
	 sum = 0.

    if gap_penalty == 1: 
	 return sum * weighted_gap_penalty(col, seq_weights)
    else:
	 return sum



################################################################################
# Window Score
################################################################################

def window_score(scores, window_len):
    """ This function takes a list of scores and a length and transforms them 
    so that each position is a weighted average of the surrounding positions. 
    Positions with scores less than zero are not changed and are ignored in the 
    calculation. Here window_len is interpreted to mean window_len residues on 
    either side of the current residue. """

    w_scores = scores[:]

    lam = .5

    for i in range(window_len, len(scores) - window_len):
	 if scores[i] < 0: 
	     continue

	 sum = 0.
	 num_terms = 0.
	 for j in range(i - window_len, i + window_len + 1):
	     if i != j and scores[j] >= 0:
		 num_terms += 1
		 sum += scores[j]

	 if num_terms > 0:
	     w_scores[i] = (1 - lam) * (sum / num_terms) + lam * scores[i]

    return w_scores



################################################################################
################################################################################
################################################################################
#  END CONSERVATION SCORES
################################################################################
################################################################################
################################################################################

def calculate_sequence_weights(msa):
	 """ Calculate the sequence weights using the Henikoff '94 method
	 for the given msa. """

	 seq_weights = [0.] * len(msa)
	 for i in range(len(msa[0])):
		 freq_counts = [0] * len(amino_acids)
	 
		 col = []
		 for j in range(len(msa)): 
		     if msa[j][i] != '-': # ignore gaps
			 freq_counts[aa_to_index[msa[j][i]]] += 1
	 
		 num_observed_types = 0 
		 for j in range(len(freq_counts)):
		     if freq_counts[j] > 0: num_observed_types +=1

		 for j in range(len(msa)):
		     d = freq_counts[aa_to_index[msa[j][i]]] * num_observed_types
		     if d > 0: 
			 seq_weights[j] += 1. / d

	 for w in range(len(seq_weights)):
		 seq_weights[w] /= len(msa[0])

	 return seq_weights


def read_scoring_matrix(sm_file):
    """ Read in a scoring matrix from a file, e.g., blosum80.bla, and return it
    as an array. Return identity matrix if can't find/read sm_file."""
    aa_index = 0
    first_line = 1
    row = []
    list_sm = [] # hold the matrix in list form

    try:
	 matrix_file = open(sm_file, 'r')

	 for line in matrix_file:

	     if line[0] != '#' and first_line:
		 first_line = 0
		 if len(amino_acids) == 0:
		     for c in line.split():
			 aa_to_index[string.lower(c)] = aa_index
			 amino_acids.append(string.lower(c))
			 aa_index += 1

	     elif line[0] != '#' and first_line == 0:
		 if len(line) > 1:
		     row = line.split()
		     list_sm.append(row)

    except IOError, e:
#	print "Could not load similarity matrix: %s. Please email us to let us know of the problem. <p>Using identity matrix..." % sm_file
#	return identity(20)
	 return None	

    # if matrix is stored in lower tri form, copy to upper
    if len(list_sm[0]) < 20:
	 for i in range(0,19):
	     for j in range(i+1, 20):
		 list_sm[i].append(list_sm[j][i])

    for i in range(len(list_sm)):
	 for j in range(len(list_sm[i])):
	     list_sm[i][j] = float(list_sm[i][j])

    return list_sm
#    sim_matrix = array(list_sm, type=Float32)
#    return sim_matrix



def get_column(col_num, alignment):
    """Return the col_num column of alignment as a list."""
    col = []
    for seq in alignment:
	 if col_num < len(seq): col.append(seq[col_num])

    return col

def get_distribution_from_file(fname):
    """ Read an amino acid distribution from a file. The probabilities should
    be on a single line separated by whitespace in alphabetical order as in 
    amino_acids above. # is the comment character."""

    distribution = []
    try:
	 f = open(fname)
	 for line in f:
	     if line[0] == '#': continue
	     line = line[:-1]
	     distribution = line.split()
	     distribution = map(float, distribution)

	     
    except IOError, e:
	 print e, "Using default (BLOSUM62) background."
	 return []

    # use a range to be flexible about round off
    if .997 > sum(distribution) or sum(distribution) > 1.003:
	 print "Distribution does not sum to 1. Using default (BLOSUM62) background."
	 print sum(distribution)
	 return []

    return distribution


def read_fasta_alignment_string(align_string):
    """ Read in the alignment stored in the FASTA string, align_string. Return two
    lists: the identifiers and sequences. """

    f = cStringIO.StringIO(align_string.replace('\r', ''))

    names = []
    alignment = []
    cur_seq = ''

    for line in f:
	 line = line[:-1]
	 if len(line) == 0: continue

	 if line[0] == ';': continue
	 if line[0] == '>':
	     names.append(line)

	     if cur_seq != '':
		 alignment.append(cur_seq.replace('B', 'D').replace('Z', 'Q').replace('X', '-'))
		 cur_seq = ''
	 elif line[0] in iupac_alphabet:
	     cur_seq += line

    # add the last sequence
    alignment.append(cur_seq.replace('B', 'D').replace('Z', 'Q').replace('X', '-'))

    return names, alignment
	 
def read_clustal_alignment_string(align_string):
    """ Read in the alignment stored in the CLUSTAL string, align_string. Return
    two lists: the names and sequences. """

    names = []
    alignment = []

    f = cStringIO.StringIO(align_string.replace('\r', ''))

    for line in f:
	 line = line[:-1]
	 if len(line) == 0: continue
	 if '*' in line: continue

	 if 'CLUSTAL' in line: continue

	 t = line.split()

	 if len(t) == 2 and t[1][0] in iupac_alphabet:
	     if t[0] not in names:
		 names.append(t[0])
		 alignment.append(t[1].upper().replace('B', 'D').replace('Z', 'Q').replace('X', '-'))
	     else:
		 alignment[names.index(t[0])] += t[1].upper().replace('B', 'D').replace('Z', 'Q').replace('X', '-')
		    
    return names, alignment


ef make_results_page(error_string, results_string):
	 """ Make a results html page. """

	 print "Content-type: text/html\n"
	 print "<html>\n<head>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\">\n<title>Conservation Results</title>\n</head>\n"
	 print "<a href=\"score.html\">Score another</a><p>\n"

	 if error_string != '':
		 print "<hr>\nError log:<br>\n"
		 print error_string
		 print "<hr>\n<p>\n"


	 print results_string


	 print "</body>\n</html>"

################################################################################
# Begin execution
################################################################################

# BLOSUM62 background distribution
blosum_background_distr = [0.078, 0.051, 0.041, 0.052, 0.024, 0.034, 0.059, 0.083, 0.025, 0.062, 0.092, 0.056, 0.024, 0.044, 0.043, 0.059, 0.055, 0.014, 0.034, 0.072]
# SwissProt background distribution
swissprot_background_distr = [.0788, .054, .0414, .0535, .0151, .0395, .0668, .0695, .0229, .0590, .0963, .0594, .0237, .0397, .0482, .0682, .0540, .0113, .0304, .0673]

error_string = '' # hold error messages generated

form = cgi.FieldStorage()
align_string = ''

# set defaults
scoring_function = None
s_matrix_file = ''
window_size = 0
bg_distribution = []
use_seq_weights = False
filename = 'user_input'

## get settings from form
#try:
#	  try:
#		  window_size = int(form['window_size'].value) # 0 = no window
#	  except ValueError:
#		  window_size = -1
#
#	  if window_size < 0:
#		  error_string += "<p>Couldn't parse window size. Please enter an integer <= 0.<p>Using window size of 0...<p>"
#		  window_size = 0
#
#	  if form['background_select'].value == 'swissprot':
#		  bg_distribution = swissprot_background_distr[:]
#	  else:
#		  bg_distribution = blosum_background_distr[:]
#
#	  if form['method_select'].value == 'shannon_entropy': scoring_function = shannon_entropy
#	  elif form['method_select'].value == 'property_entropy': scoring_function = property_entropy
#	  elif form['method_select'].value == 'vn_entropy': scoring_function = vn_entropy
#	  elif form['method_select'].value == 'relative_entropy': scoring_function = relative_entropy
#	  elif form['method_select'].value == 'js_divergence': scoring_function = js_divergence
#	  elif form['method_select'].value == 'sum_of_pairs': scoring_function = sum_of_pairs
#	  else: scoring_function = js_divergence
#
#	  if scoring_function == 'vn_entropy':
#		  s_matrix_file = "matrix/%s.qij" % form['matrix_select'].value
#	  else:
#		  s_matrix_file = "matrix/%s.bla" % form['matrix_select'].value
#
#	  if form.has_key('seq_weight'): use_seq_weights = True
#
#	  align_string = form['alignment'].value
#	  if align_string == '':
#		  align_string = form['align_file'].value
#		  if form['align_file'].filename != '': filename = form['align_file'].filename
#
#
#except KeyError:
#	  pass
#
#

make_results_page('hello', 'hello')
sys.exit()


#s_matrix = read_scoring_matrix(s_matrix_file)
#if s_matrix == None:
#	 error_string +=  "<p>Could not load similarity matrix: %s. Please email us to let us know of the problem. <p>Using identity matrix...<p>" % s_matrix_file
#	 s_matrix = identity(20)
#
#
#names = []
#alignment = []
#if '\n>' in align_string:
#	 names, alignment = read_fasta_alignment_string(align_string)
#else:
#	 names, alignment = read_clustal_alignment_string(align_string)
#
#if len(alignment) != len(names) or alignment == []: 
#	 error_string += "<p>Unable to parse alignment. Did you enter an alignment in FASTA or CLUSTAL format?<p>If you did, please send us a summary of the problem and the alignment.<p>"
#	 make_results_page(error_string, '')
#	 sys.exit()
#
#seq_len = len(alignment[0])
#for i, seq in enumerate(alignment):
#	 if len(seq) != seq_len:
#	 error_string += "<p>ERROR: Sequences of different lengths: %s (%d) != %s (%d).\n" % (names[0], seq_len, names[i], len(seq))
#	 make_results_page(error_string, '')
#	 #sys.exit()
#
#
#seq_weights = []
#if use_seq_weights: seq_weights = calculate_sequence_weights(alignment)
#
#if len(seq_weights) != len(alignment): seq_weights = [1.] * len(alignment)
#
## calculate scores
#scores = []
#for i in range(len(alignment[0])):
#    col = get_column(i, alignment)
#
#    if len(col) == len(alignment):
#	 scores.append(scoring_function(col, s_matrix, bg_distribution, seq_weights))
#
#if window_size > 0:
#    scores = window_score(scores, window_size)
#
#
#results_string = '<pre>\n'
## print results
#results_string +=  "# %s -- %s - window_size: %d - background: %s - seq. weighting: %s\n# column number - score - column\n" % (filename, scoring_function.__name__, window_size, form['background_select'].value, use_seq_weights)
#
#for i, score in enumerate(scores):
#	 results_string +=  "%d\t%.5f\t%s\n" % (i, score, "".join(get_column(i, alignment)))
#
#results_string +=  "</pre>\n"
#
#make_results_page(error_string, results_string)
