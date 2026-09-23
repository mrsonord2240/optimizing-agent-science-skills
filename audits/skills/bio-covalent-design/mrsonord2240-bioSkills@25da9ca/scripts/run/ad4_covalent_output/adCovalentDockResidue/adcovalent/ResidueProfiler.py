#!/usr/bin/env python

import sys, os, math

import pybel
ob = pybel.ob

import numpy as np
from CopyMol import MoleculeDuplicator 
#import AutoDockTools.HelperFunctionsN3P as hf


class AminoAcidProfiler:

    def __init__(self, mol, resId=None, setLabels=True, auto=True, debug=False):
        """ mol         : pybel molecule
            resId       : residue specification (chain:res:num)
                          if not set, all residues in mol will be
                          processed
            setLabels   : assign default PDB atom names for residues
            auto        : process molecule after initializing this class
            debug:      : enable debug messages
        """
        self.debug = debug
        self.resId = resId
        self.setLabels=setLabels
        self.auto=auto
        self.mol = mol
        self.initPatterns()
        self.initResidues()

        if self.auto:
            self.process()


    def process(self):
        """ does the whole process"""
        self.scanResidues()
        #if self.setLabels:
        #    self.labelAtoms()
        if self.debug:
            pybel.Molecule(self.mol).write('pdb', 'DEBUG_renamed.pdb', overwrite=1)

    def initResidues(self):
        """ set the residues to process"""
        self.residues = {}
        #for res in ob.OBResidueIter(self.mol.OBMol):
        for res in ob.OBResidueIter(self.mol):
            chain = res.GetChain()
            name = res.GetName()
            num = res.GetNum()
            item = "%s:%s%s" % (chain, name, num)
            if (self.resId == None) or (item == self.resId):
                self.residues[item] = { 'obj' : res }

    def initPatterns(self): 
        """ initialize this class variables"""
        self.aaId = None        

        self.aminoacid = { 
            # Adaptation from original from DayLight:
            #     http://www.daylight.com/dayhtml_tutorials/languages/smarts/smarts_examples.html
            # extra O/N at the end have been removed, because troublesome.
            #'pro' : '[$([NX3H,NX4H2+]),$([NX3](C)(C)(C))]1[CX4H]([CH2][CH2][CH2]1)[CX3](=[OX1])[OX2H,OX1-,N]',
            #'generic' : '[$([NX3H2,NX4H3+]),$([NX3H](C)(C))][CX4H]([*])[CX3](=[OX1])',
            #'gly' : '[$([$([NX3H2,NX4H3+]),$([NX3H](C)(C))][CX4H2][CX3](=[OX1])[OX2H,OX1-,N])]',
            #
            # Also, Lys and Arg patterns have been modified to have an extra generic N, otherwise
            # OpenBabel is not able to match them.
            'generic' : '[$([NX3H2,NX4H3+]),$([NX3H](C)(C))][CX4H]([*])[CX3](=[OX1])',
            # do not match Pro and Gly
            'pro' : '[$([NX3H,NX4H2+]),$([NX3](C)(C)(C))]1[CX4H]([CH2][CH2][CH2]1)[CX3](=[OX1])',
            'gly' : '[$([$([NX3H2,NX4H3+]),$([NX3H](C)(C))][CX4H2][CX3](=[OX1]))]',
                }
        self.backbone = { 'labels' : [ ['N','CA'], ['C', 'O'] ]}
        self.prolyne = [ 'N', 'CA', 'CB', 'CG', 'CD', 'C', 'O' ]

        self.sideChains = {  
            'ala': { 'pattern' : '[CH3X4]',
                    'labels' : ['CB'], },

            
            'arg': { 'pattern' : '[CH2X4][CH2X4][CH2X4][NHX3][CH0X3](=[NH2X3+,NHX2+0,N])[NH2X3]', 
                    # Hits acid and conjugate base. MODIFIED from original implementation
                    # adding an extra generic 'N' type for the head, otherwise OB will
                    # miss it
                     'labels' : [ 'CB', 'CG', 'CD', 'NE', 'CZ', 'NH1', 'NH2' ],
                     },

            'asn': { 'pattern' : '[CH2X4][CX3](=[OX1])[NX3H2]', # 
                    # Also hits Gln side chain when used alone
                     'labels' : [ 'CB', 'CG', 'OD1','ND2' ],
                    },

            'gln': { 'pattern' : '[CH2X4][CH2X4][CX3](=[OX1])[NX3H2]', # 
                    # Also hits Gln side chain when used alone
                     'labels' : [ 'CB', 'CG', 'CD', 'OE1','NE2' ],
                    },
                
            'asp': { 'pattern' : '[CH2X4][CX3](=[OX1])[OH0-,OH]',
                    # Aspartate (or Aspartic acid) side chain. Hits acid and conjugate base.
                    # Also hits Glu side chain when used alone.
                     'labels' : [ 'CB', 'CG', 'OD1','OD2' ],
                     },

            'cys' : { 'pattern': '[CH2X4][SX2H,SX1H0-]', # Cysteine side chain. Hits acid and conjugate base
                     'labels' : [ 'CB', 'SG' ],
                     },

            'glu' : { 'pattern' : '[CH2X4][CH2X4][CX3](=[OX1])[OH0-,OH]', # Hits acid and conjugate base
                      'labels' : [ 'CB', 'CG', 'CD', 'OE1', 'OE2'] ,
                      },

            'his' : { 'pattern' : ('[CH2X4][#6X3]1:[$([#7X3H+,#7X2H0+0]:[#6X3H]:[#7X3H]),$([#7X3H])]:'
                                   '[#6X3H]:[$([#7X3H+,#7X2H0+0]:[#6X3H]:[#7X3H]),$([#7X3H])]:[#6X3H]1'),
                    #Hits acid & conjugate base for either Nitrogen. Note that the Ns can be either
                    # ([(Cationic 3-connected with one H) or (Neutral 2-connected without any Hs)] 
                    # where there is a second-neighbor who is [3-connected with one H]) or (3-connected with one H).
                    'labels': ['CB', 'CG', 'ND1', 'CD2', 'CE1', 'NE2'],
                    },

            'ile' : { 'pattern' : '[CHX4]([CH3X4])[CH2X4][CH3X4]',
                    'labels' : ['CB', 'CG1', 'CG2', 'CD1'] ,
                    },

            
            'leu' : { 'pattern' : '[CH2X4][CHX4]([CH3X4])[CH3X4]',
                     'labels' : ['CB', 'CG', 'CD1', 'CD2' ] 
                     },

            'lys' : { 'pattern' : '[CH2X4][CH2X4][CH2X4][CH2X4][NX4+,NX3+0,N]',
                    # MODIFIED from original implementation
                    # adding an extra generic 'N' type for the head, otherwise OB will
                    # miss it
                     'labels' : [ 'CB', 'CG', 'CD', 'CE', 'NZ' ],
                     },

            'met' : { 'pattern': '[CH2X4][CH2X4][SX2][CH3X4]',
                     'labels' : [ 'CB', 'CG', 'SD', 'CE' ],
                     },


            'phe' :  { 'pattern' : '[CH2X4][cX3](1[cX3H][cX3H][cX3H][cX3H][cX3H]1)',
                      'labels' : [ 'CB', 'CG', 'CD1', 'CD2', 'CZ', 'CE1', 'CE2' ] ,
                      },

            'ser' :  {'pattern': '[CH2X4][OX2H]',
                        'labels' : [ 'CB', 'OG' ],
                        },

            'thr' : {'pattern' : '[CHX4]([CH3X4])[OX2H]',
                     'labels' : [ 'CB', 'CG2', 'OG1' ],
                     },

            'trp' : { 'pattern' : '[CH2X4][cX3]1[cX3H][nX3H][cX3]2[cX3H][cX3H][cX3H][cX3H][cX3]12',
                     'labels' : [ 'CB', 'CG', 'CD1', 'CD2', 'NE1', 'CE2', 'CE3', 'CZ2', 'CZ3', 'CH2' ],
                     },

            'tyr' : {'pattern': '[CH2X4][cX3]1[cX3H][cX3H][cX3]([OHX2,OH0X1-])[cX3H][cX3H]1', # Acid and conjugate base
                    'labels' : [ 'CB', 'CG', 'CD1', 'CD2', 'CZ', 'OH', 'CE1', 'CE2'],
                    },

            'val' : { 'pattern' : '[CHX4]([CH3X4])[CH3X4]',
                    'labels' : [ 'CB', 'CG1', 'CG2'] ,
                    },
                }

    def findSmartsRes(self, resObj, resId, pattern):
        """ perform SMARTS pattern matching only on a residue 
            from a molecule by duplicating the residue as 
            new molecule
        """
        #duplicator = MoleculeDuplicator(self.mol, resList=[resId], debug=self.debug)
        #resMol = duplicator.getCopy()
        if self.debug:
            pybel.Molecule(resObj).write('pdb', 'DEBUG_%s.pdb' % resId, overwrite=1)
        return self.findSmarts(resObj, pattern)

    def findSmarts(self, mol, pattern):
        """ OB SMARTS matcher """
        obpat = ob.OBSmartsPattern()
        obpat.Init(pattern)
        obpat.Match(mol)
        return [ x for x in obpat.GetUMapList() ]

    def getResPattern(self, resName):
        """ return the proper SMARTS pattern for residue"""
        generic = self.aminoacid['generic'].replace('[*]', '%s', 1)
        fullPattern = generic % self.sideChains[resName]['pattern']
        return fullPattern

    def scanResidues(self):
        """ check if the molecule is (contains?) an aminoacid
            or if it is proline or glycine
        """
        for resId, data in self.residues.items():
            resObj = data['obj']
            dup = MoleculeDuplicator(self.mol, resList=[resId], debug=self.debug)
            resCopy = dup.getCopy()
            if self.debug: print "PROCESSING RESIDUE", resObj.GetName(), resId, data
            guess = self.guessResType(resId)
            for name, pattern in self.getAminoAcidPatterns(sort=guess):
                found = self.findSmartsRes(resCopy, resId, pattern)
                if len(found):
                    self.residues[resId]['type'] = name
                    self.residues[resId]['pattern'] = found[0]
                    if self.debug: print "RESIDUE TYPE FOUND", name
                    if self.setLabels:
                        self.labelAtoms(resId)
                    break
            if not 'pattern' in self.residues[resId]:
                #dup = MoleculeDuplicator(self.mol, resList=[resId], debug=self.debug)
                #new = dup.getCopy()
                #).__str__().split()[0]
                print "WARNING! Residue [%s] was not recognized" % resId,
                smi = pybel.Molecule(resCopy)
                print "SMILES[ %s ]" % smi
                name, pattern = self.getAminoAcidPatterns(sort=guess)[0]
                print "Guess was [%s], Pattern |%s|" %  (name, pattern)
        return 

    def guessResType(self, resId):
        """ save time"""
        data = self.sideChains.items()
        name = resId.split(':', 1)[1]
        name = name[0:3].strip().lower()
        if self.debug: print "\tGUESSING RES TYPE", name
        return name
    

    def getAminoAcidPatterns(self, sort=None):
        """ return full SMARTS pattern of all AA
            if optional sort 3-letter name is provided,
            the specified aa will be the first
        """
        # gly, pro
        pattern = [ ( 'gly', self.aminoacid['gly']), 
                    ( 'pro', self.aminoacid['pro']) ]
        # all other aa's
        for resName in self.sideChains.keys():
            fullPattern = self.getResPattern(resName)
            pattern.append( (resName, fullPattern) )
        # sorting
        if not sort == None:
            for x in range(len(pattern)):
                if pattern[x][0] == sort:
                    break
            pattern = [ pattern.pop(x) ] + pattern
        return pattern
            

    def getSortedSideChains(self, rType): # XXX OBSOLETE
        """ return list of sidechain SMARTS patterns
            sorted by the requested rType guess
        """
        if rType in self.sideChains.keys():
            out = [ ( rType, self.sideChains[rType] ) ]
            for i, j in data:
                if not i == name:
                    out.append(( i,j))
            return out
        return data


    def getResLabels(self, resType, backbone=True):
        """ return standard labels of atoms in resType"""
        
        if resType == 'pro':
            return self.prolyne
        
        bbLabels = self.backbone['labels']
        if (resType == 'gly'):
            sideChainLabels = []
        else:
            sideChainLabels = self.sideChains[resType]['labels']
        if backbone:
            return bbLabels[0] + sideChainLabels + bbLabels[1]
        return sideChainLabels
        
    def labelAtoms(self, resId):
        """ assign standard PDB atom labels for residues"""
        #bbLabels = self.backbone['labels']
        rType = self.residues[resId]['type']
        rObj = self.residues[resId]['obj']
        match = self.residues[resId]['pattern']
        labels = self.getResLabels(rType)
        indices = [ x.GetIdx() for x in ob.OBResidueAtomIter(rObj) ]
        indices.sort()
        offset = indices[0]-1
        for atom in ob.OBResidueAtomIter(rObj):
            oldName = rObj.GetAtomID(atom)
            num = atom.GetIdx() - offset
            if num in match:
                idx = match.index(num)
                newName = ' {0:3}'.format(labels[idx])
                if self.debug:
                    print "OLD[%s] => NEW[%s] [%d]" % (oldName, newName, match.index(num))
                rObj.SetAtomID(atom, newName)
            else:
                if self.debug: print "MISSING", num, match
        return



if __name__ == '__main__':
    ftype = sys.argv[1].rsplit('.',1)[1].lower()
    mol = pybel.readfile(ftype, sys.argv[1]).next()

    aa = AminoAcidProfiler( mol.OBMol, debug=1)
