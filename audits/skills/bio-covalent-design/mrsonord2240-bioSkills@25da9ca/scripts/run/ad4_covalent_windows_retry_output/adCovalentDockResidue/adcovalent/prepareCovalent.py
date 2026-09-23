#!/usr/bin/env python
#
# Covalent Docking preparation for AutoDock 
#
# v.1.0c  Stefano Forli
#
# Copyright 2014, Molecular Graphics Lab
#     The Scripps Research Institute
#        _  
#       (,)  T  h e
#      _/
#     (.)    S  c r i p p s
#      '\_
#       (,)  R  e s e a r c h
#      ./'
#     ( )    I  n s t i t u t e
#      "
#
#################################################################################
#
#     This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#

import sys, os, math
import pybel
ob = pybel.ob
import argparse
import numpy as np
from math import sqrt, sin, cos, acos, degrees
import ResidueProfiler
from CopyMol import MoleculeDuplicator


# TODO improve the method to build the bond directly, calculating
#      bond lenght and its placement

#### Debug functions
def makePdb(coord, keyw = "ATOM  ", at_index = 1, res_index = 1, atype = 'X', elem = None,
            res = "CNT", chain  ="Z", bfactor = 10,pcharge = 0.0):
    if not elem: elem = atype
    # padding bfactor
    bfactor = "%2.2f" % bfactor
    if len(bfactor.split(".")[0]) == 1:
        bfactor = " "+bfactor
    if len(atype) == 1:
        atype = atype + " "
    #atom = "%s%5d  %2s  %3s %1s%4d    %8.3f%8.3f%8.3f  1.00 %02.2f  %8.3f %1s" % (keyw,
    # SOURCE: http://cupnet.net/pdb-format/
    "%-6s%5d %4s%1s%3s %1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s%2s"
    atom = "%s%5d %2s   %3s %1s%4d    %8.3f%8.3f%8.3f  1.00 %s  %8.3f %1s" % (keyw,
            at_index, elem, res, chain, res_index, 
            coord[0], coord[1], coord[2], bfactor, pcharge, atype)
    return atom

def writeList(filename, inlist, mode = 'w', addNewLine = False):
    if addNewLine: nl = "\n"
    else: nl = ""
    fp = open(filename, mode)
    for i in inlist:
        fp.write(str(i)+nl)
    fp.close()


def vector(p1 , p2 = None, norm = 0): # TODO use Numpy?
    if not p2 == None:
        vec = np.array([p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]],'f')
    else:
        vec = np.array([p1[0], p1[1], p1[2] ], 'f' )

    if norm:
        return normalize(vec)
    else:
        return vec

def dot(vector1, vector2):  # TODO remove and use Numpy
    dot_product = 0.
    for i in range(0, len(vector1)):
        dot_product += (vector1[i] * vector2[i])
    return dot_product

def vecAngle(v1, v2, rad=1): # TODO remove and use Numpy?
    angle = dot(normalize(v1), normalize(v2))
    try:
        if rad:
            return acos(angle)
        else:
            return degrees(acos(angle))
    except:
        print "#vecAngle> CHECK TrottNormalization"
        return 0

def norm(A): # TODO use Numpy
        "Return vector norm"
        return math.sqrt(sum(A*A))

def normalize(A): # TODO use Numpy
        "Normalize the Vector"
        return A/norm(A)



def calcPlane(p1, p2, p3):
    # returns the plane containing the 3 input points
    v12 = vector(p1,p2)
    v13 = vector(p3,p2)
    return normalize(np.cross(v12, v13))



def rotatePoint(pt,m,ax):
    """
    Rotate a point applied in m around a pivot ax ?


    pt = point that is rotated
    ax = vector around wich rotation is performed
    """
    # point 
    x=pt[0]
    y=pt[1]
    z=pt[2]
    # rotation pivot
    u=ax[0]
    v=ax[1]
    w=ax[2]
    ux=u*x
    uy=u*y
    uz=u*z
    vx=v*x
    vy=v*y
    vz=v*z
    wx=w*x
    wy=w*y
    wz=w*z
    sa=sin(ax[3])
    ca=cos(ax[3])
    p0 =(u*(ux+vy+wz)+(x*(v*v+w*w)-u*(vy+wz))*ca+(-wy+vz)*sa)+ m[0]
    p1=(v*(ux+vy+wz)+(y*(u*u+w*w)-v*(ux+wz))*ca+(wx-uz)*sa)+ m[1]
    p2=(w*(ux+vy+wz)+(z*(u*u+v*v)-w*(ux+vy))*ca+(-vx+uy)*sa)+ m[2]
    return np.array([ p0, p1, p2])




class CovalentDockingMaker:
    """ This class generate the input for covalent dockings.
        Required input are :

            - ligand structure (any OB-supported 3D format)
            - receptor structure (any OB-supported 3D format)
        
        Ligand and receptor structures should share at least 2 atoms
        to be overlapped, e.g.:

                Cys-Ca-Cb-S     Cb-S-Lig

        Alignment can be performed using one of the following criteria:

            - indices: two indices pairs for ligand and receptor

            - SMARTS: a pattern and two atom indices must be defied for the ligand; 
                      if nothing is defined for the receptor (default), the residue
                      type will be used to pick its strongst nucleophyle atom, 
                      i.e. Cys-SG, Ser/Thr-OG, Lys-NZ.

            - bond: a bond for each structure is provided and indices 
                    calculated from them; bonds must be terminal bonds 
                    (not counting H's)
                    (not working yet)
    """
    def __init__(self, 
            lig,    # ligand openbabel molecule
            rec,    # receptor openbabel molecule
            resName,# residue id to be modifled (i.e. A:THR276)

            smartsLig=None, smartsRec=None,   # use SMARTS patterns
                                              # patterns should be aligned
            smartsIdxLig=(), smartsIdxRec=(), # align using atomIdx from SMARTS patterns

            bondIdxLig=None, bondIdxRec=None, # use bonds

            indicesLig=None, indicesRec=None, # use atom indices in both

            genFullRec = False,               # add the covalent ligand to the receptor
                                              # as modified residue; this is *NOT* 
                                              # recommended, because it can lead to
                                              # spurious bonds between the mod res
                                              # and the rest of the receptor
            genLigand = False,                  


            auto=True,                        # start automatically
            debug = False,
            verbose=False):

        self.verbose = verbose
        self.debug = debug
        # LIGAND 
        dup = MoleculeDuplicator(lig)
        self.lig = dup.getCopy()
        # parameters(REQUIRED)
        self.smartsLig = smartsLig       # smarts 
        self.smartsIdxLig = smartsIdxLig # smarts indices
        self.bondIdxLig = bondIdxLig     # bonds
        self.indicesLig = indicesLig     # indices (direct)

        # RECEPTOR
        self.fullRec = rec
        self.resName = resName.upper()
        # parameters (OPTIONAL)
        self.smartsRec = smartsRec        # smarts           
        self.smartsIdxRec = smartsIdxRec  # smarts indices
        self.bondIdxRec = bondIdxRec      # bonds
        self.indicesRec = indicesRec      # indices (direct)
        # collect receptor information
        self.genFullRec = genFullRec
        self.setMode()
        self.initResidue() 
        if auto:
            self.process()


    def vprint(self, msg):
        """ """
        if not self.verbose:
            return
        print("VERBOSE " + msg)
    

    def setMode(self):  
        """ """
        # ligand mode
        if self.indicesLig:
            self._ligmode = 'idx'
        elif self.smartsLig:
            self._ligmode = 'smarts'
        elif self.bondIdxLig:
            self._ligmode = 'bond'
        self.vprint("[setMode] ligand alignment mode: %s" % self._ligmode)
        # receptor mode
        if self.indicesRec:
            self._recmode = 'idx'
        elif self.smartsRec:
            self._recmode = 'smarts'
        elif self.bondIdxRec:
            self._recmode = 'bond'
        else:
            self._recmode = 'smarts'
            self.vprint("[setMode] no mode specified-> switching to default")
        self.vprint("[setMode] receptor alignment mode: %s" % self._recmode)
    
    def initResidue(self):
        """ initialize residue information"""
        string = self.resName
        chain, res = string.split(":")
        self.resInfo = { 'chain' : chain,
                         'name'  : res[0:3],
                         'num': int(res[3:]),
                       }
        if self.debug: print "PROCESSING RESIDUE", self.resName
        self.residueProfile()

    def process(self):
        """ do the stuff"""
        if self.verbose: print "Aligning ligand on residue...", self.resName
        self.align()
        self.cleanup()

    def residueProfile(self):
        """ tries to recognize the receptor residue
            and rename atoms to facilitate Calpha-Cbeta identification
        """
        self.receptorProfiler = ResidueProfiler.AminoAcidProfiler(self.fullRec,
                resId=self.resName, setLabels=True, 
                auto=True, debug=self.debug)
        self.resType = self.receptorProfiler.residues[self.resName]['type']
        if self.verbose: 
            print "Selected residue recognized as:", self.resType.upper()
        dup = MoleculeDuplicator(self.fullRec, resList=[self.resName]) 
        self.modifiedRes = dup.getCopy()
        if self._recmode == 'idx':
            org = self.indicesRec[:]
            self.indicesRec = [ self.modifiedRes._numbering[x] for x in self.indicesRec]
            self.vprint( ('converting full receptor indices [%s] to '
                 'residue copy indices [%s]' % (org, self.indicesRec)))
        self.setResidueParms()

    def setResidueParms(self):
        """ populate automatically SMARTS and indices for
            the residue if nothing was specified already
        """
        if not self._recmode == 'smarts':
            msg = "[setResidueParm] receptor alignment mode is (%s), skipping" 
            self.vprint (msg % self._recmode)
            return
        if self.smartsRec:
            msg = ("[setResidueParms] receptor SMARTS already defined [%s], skipping")
            self.vprint(msg % self.smartsRec)
            return
        self._residueParms = {'cys' : { 'patternIdx' : [3,2],     # when using SMARTS patterns from ResProfiler
                                 'atNames': ['SG', 'CB'],   # when looking for [setMode] atom names in the structure
                                },
                        'ser' : { 'patternIdx' : [3,2],
                                 'atNames' : ['OG', 'CB'],
                                },
                        'thr' : { 'patternIdx' : [4,2],
                                 'atNames' :  ['OG', 'CB'],
                                },
                        'lys' : { 'patternIdx': [6,5],
                                 'atNames': ['NZ','CE'],
                                },
                        }
        resInfo = self._residueParms[self.resType]
        self.smartsRec = self.receptorProfiler.getResPattern(self.resType)
        self.smartsIdxRec = resInfo['patternIdx']
        if self.verbose:
            print "Auto-parameters for residue (%s)" % (self.resType)
            print "    SMARTS pattern : %s" % self.smartsRec
            print "    atom indices   : %s" % self.smartsIdxRec
            print "    atom names     : %s" % resInfo['atNames']

    def align(self):
        """ where the magic happens... perform the alignment"""
        self.populateIndices()
        if not self.ready:
            print "Molecule not ready... Aborting."
            return
        aligner = VectorMolAligner(lig=self.lig, rec=self.modifiedRes, 
            ligIndices=self.indicesLig, recIndices=self.indicesRec, 
            verbose=self.verbose, debug=self.debug)

    def populateIndices(self):
        """ populate indices pairs accordingly to the modes"""
        # XXX add a check for missing matches
        # ligand indices:
        self.ready = True
        if self._ligmode == 'smarts':
            smarter = IndicesFromSMARTS(mol = self.lig,
                pattern = self.smartsLig, indices = self.smartsIdxLig,
                firstOnly = False, debug = self.debug)
            if not smarter.matches:
                print "*** WARNING *** Pattern not found in the ligand"
                self.ready = False
                return
            self.indicesLig = smarter.matches[0]
        elif self._ligmode == 'bond':
            pass
        else:
            self.vprint("[align] Using provided indices for ligand")
        # receptor indices
        if self._recmode == 'smarts':
            smarter = IndicesFromSMARTS(mol = self.modifiedRes,
                pattern = self.smartsRec, indices = self.smartsIdxRec,
                debug = self.debug)
            if not smarter.matches:
                print "*** WARNING *** Pattern not found in the receptor"
                self.ready = False
                return
            self.indicesRec = smarter.matches[0]
        elif self._recmode == 'bond':
            pass
        else:
            self.vprint("[align] Using provided indices for receptor")
        
    def cleanup(self):
        """ Lig: remove from A on...
            Rec: remove from I on...
            merge from CA on to the residue
        """
        if not self.ready:
            return
        self.cleanLigand()
        self.cleanReceptor()
        self.cleanModRes()
        if self.genFullRec:
            self.generateFullRec()

    def cleanLigand(self):
        """ remove atoms A and B from the ligand"""
        # delete ligand atoms used to overlap
        for a in [ self.lig.GetAtom(i) for i in self.indicesLig ]:
            self.lig.DeleteAtom(a)
        # delete hydrogens
        self.lig.DeleteHydrogens()
        # create new molecule (XXX maybe it should be moved at the beginning?
        # before deleting atoms
        dup = MoleculeDuplicator(self.lig, name='Covalent docking of...')
        self.covalentLigand = dup.getCopy()
        # XXX BUG this triggers the creation of a residue "LIG" for ligands
        # with no residues
        self.covalentLigand.GetAtom(1).GetResidue()
        covalentRes = self.covalentLigand.GetResidue(0)
        #if covalentRes:
        covalentRes.SetName(self.resType.upper())
        # renaming ligand atoms 'C -> CX' to avoid issues later (ADT...)
        for atom in ob.OBResidueAtomIter(covalentRes):
            oldIdFull = covalentRes.GetAtomID(atom)
            # keep the element letter, throw the rest...
            oldId = oldIdFull[0] 
            covalentRes.SetAtomID(atom, oldId+'X')

        if self.debug: 
            pybel.Molecule(self.lig).write('pdb', 'DEBUG_cleanLig.pdb', overwrite=1)

    def cleanReceptor(self):
        """ use PDB atom labels to decide atoms to be kept
        """
        # XXX CORRECT XXX
        #accepted = ['CA', 'N'] + self.receptorProfiler.getResLabels(self.resType,
        # backbone=False)
        accepted = ['CA'] + self.receptorProfiler.getResLabels(self.resType,
            backbone=True)
        if self.debug:
            print "Accepted residue atom names:" , accepted
        covalentRes = self.covalentLigand.GetResidue(0)
        for atom in ob.OBMolAtomIter(self.modifiedRes):
            aName = self.getAtomName(atom, True)
            if self.debug: print "Scanning atom [%s]" % aName
            if aName in accepted:
                if self.debug: print "[ accepted ]"
                newName = ' {0:3}'.format(aName)
                newAtom = self.covalentLigand.NewAtom()
                newAtom.Duplicate(atom)
                covalentRes.AddAtom(newAtom)
                # residue atoms will be ATOM
                covalentRes.SetAtomID(newAtom, newName)
        if self.debug:
            mol = pybel.Molecule(self.covalentLigand)
            mol.write('pdb', 'final.pdb', overwrite=1)
    
    def cleanModRes(self, setHet=True, connect=True, addH=True):
        """ perform last clean-up operations:
                conect : autodetect bonds 
                addH   : add hydrogens
                setHet : set all atom records as HETATM
        """
        # autodetect bonds
        if connect:
            self.covalentLigand.ConnectTheDots()
        # add hydrogens
        if addH:
            self.addHydrogens()
        # set all atoms to be HETATM records
        covalentRes = [ x for x in ob.OBResidueIter(self.covalentLigand)][0]
        if setHet:
            for a in ob.OBMolAtomIter(self.covalentLigand):
                covalentRes.SetHetAtom(a, True)

        covalentRes.SetName(self.resType.upper())
        chain, res = self.resName.split(':',1)
        print "CHAIN", chain
        rnum = res[3:]
        covalentRes.SetNum(int(rnum))
        covalentRes.SetChain(chain)

    def generateFullRec(self):
        """ replace the original residue with the 
            modified one
        """
        rName = self.resInfo['name']
        rChain = self.resInfo['chain']
        rNum = self.resInfo['num']
        for res in ob.OBResidueIter(self.rec):
            if (res.GetChain() == rChain):
                if (res.GetNum() == rNum):
                        self.rec.DeleteResidue(res)
                        if self.verbose:
                            print "deleted residue [%s:%s%s]" % (rChain, rName, rNum)
                        break
        # add modified residue
        #covalentRes = [ x for x in ob.OBResidueIter(self.covalentLigand)][0]
        #self.rec.AddResidue(covalentRes)


    def addHydrogens(self):
        """ manages all the gymnastics for adding hydrogens at pH 7.4 (DEFAULT)"""
        #self._temporaryPHFix()
        self.covalentLigand.DeleteHydrogens()
        self.covalentLigand.UnsetFlag(ob.OB_PH_CORRECTED_MOL)
        for a in ob.OBMolAtomIter(self.covalentLigand):
            a.SetFormalCharge(0)
        self.covalentLigand.SetAutomaticFormalCharge(True)
        #self.covalentLigand.PerceiveBondOrders()
        self.covalentLigand.AddHydrogens(False, True )#, pH)

        #self.covalentLigand.AddHydrogens(False,True)

    def _temporaryPHFix(self):
        """ this is a nasty workaround for an even nastier bug in OB:
            http://sourceforge.net/p/openbabel/bugs/710/
        """
        t = 'mol2'
        n = '.tmpmol'
        m = pybel.Molecule(self.covalentLigand)
        m.write(t, n, overwrite=1)
        self.covalentLigand = pybel.readfile(t, n).next().OBMol
        os.remove(n)
        
    def getAtomName(self, atom, strip=False):
        """ return the PDB atom name """
        res = atom.GetResidue()
        if strip:
            return res.GetAtomID(atom).strip()
        return res.GetAtomID(atom)


    def writeCovalent(self, outFname, _format='pdb'):
        """ _format could be any OB format
        
            NOTE: test mol2 to avoid spurious bonds?
        """
        if self.genFullRec:
            mol = self.rec
        else:
            mol = self.covalentLigand

        if _format == 'pdbqt':
            self._writePdbqt(outFname+'.pdbqt')
        else:
            #fname = "%s.%s" % ( outFname, _format.lower() )
            fname = outFname
            conv = ob.OBConversion()
            conv.SetOutFormat(_format)
            conv.WriteFile(mol, fname)
            if self.verbose: print "Written: %s" % (fname)
            
    def _writePdbqt(self, outFname):
        """ not necessary, for now, we will use prepare_flexres code later"""
        if self.genFullRec:
            mol = self.rec
        else:
            mol = self.covalentLigand


class IndicesFromSMARTS:
    """ Given a SMARTS pattern, return the atom indices matching
        the specified atoms in the pattern
    """
    def __init__(self, mol, pattern, indices=(), firstOnly = True, debug=False): 
        """ mol : OBMol()
            pattern = SMARTS string
            [ indices: indices of the SMARTS atoms that need to be identified ]
            [ firstOnly: by default only first match is returned; multiple are possible]
        """
        self.debug = debug
        self.mol = mol
        if self.debug:
            print "IndicesFromSMARTS> MOLECULE NAME", self.mol.GetTitle()
            print "IndicesFromSMARTS> MOLECULE ", self.mol
            print "PATTERN", pattern
        self.pattern = pattern
        self.indices = indices
        if self.indices == ():
            self.indices = (0,1)
            print "pointMatch> WARNING! missing indices, using default (0,1)"
        self.matches = []
        self.pointMatch()

    def pointMatch(self):
        """ correct the indexing from the SMARTS pattern indexing to 
            the 0-based used to retrieve atoms
        """
        result = self.findSmarts()
        if not len(result):
            print "IndexFromSMARTS: NO MATCH FOUND! troubles ahead..."
            return 
        if self.debug:
            print "[IndicesFromSMARTS] >>> raw out", result 
        if len(result) > 1:
            print "TMP: MULTIPLE MATCHES FOUND!", len(result)
        i,j = self.indices
        if self.debug:
            print "[IndicesFromSMARTS]> extracting indices [%d,%d] from smarts[%s]" % (i,j,result)
        self.matches = [ (r[i],r[j]) for r in result ]

        if self.debug:
            print "FOUND!", self.matches
            for a in ob.OBMolAtomIter(self.mol):
                if a.GetIdx() in self.matches[0]:
                    res = a.GetResidue()
                    print "RESNAME", res.GetName()
        return self.matches

    def findSmarts(self):
        """ OB SMARTS matcher """
        obpat = ob.OBSmartsPattern()
        obpat.Init(self.pattern)
        obpat.Match(self.mol)
        if self.debug:
            print "PROCESSING MOLECULE", self.getSmi()
        return [ x for x in obpat.GetUMapList() ]
    
    def getSmi(self):
        """ """
        m = pybel.Molecule(self.mol)
        return m.__str__()
        


# XXX INACCURATE! PROBABLY TO BE DROPPED?
class IndicesFromBond:
    """ identify atom indices involved in a bond"""
    def __init__(self, mol, bond):
        """ The requirement
        XXX the requirement is that there must be a unique atom type that's
        
        common?  -X-S  S-Y-

        Some smartness could be used to guess what is the 'terminal'
        direction to infer the proper orientation of the molecules

        """
        pass


class VectorMolAligner:
    """ """
    def __init__(self, lig, rec, ligIndices=(), recIndices=(), auto=True, 
        verbose=False, debug=False):
        """ 
        Given two OB Molecules and two pairs of atom indices
        (A,B) and (I,J) perform the covalent alignment

        0. Initial configuration

                    B
                   /
           [L]----A      I---J--[R]
                        /
                       X


        1. Translate [L] to overlap A->I


                    B
                   /
           [L]----A  ->  I---J--[R]
                        /
                       X

                          B
                         /
                 [L]----AI---J--[R]
                        /
                       X


        2. Rotate [L] around the normal of plane (B,A,J) to overlap B->J
              
                [L]
                  \
                   AI--BJ--[R]
                   / 
                  X 


        Indexing provided must be as following:
                ligIndices = (B, A)
                recIndices = (I, J)

        """
        self.debug = debug
        self.verbose = verbose
        self.lig = lig
        self.rec = rec
        self.ligIndices = ligIndices
        self.recIndices = recIndices
        if auto:
            self.align()

    def align(self):
        """ perform the alignment based on vectors
        """
        self.getVectors()
        self.translate()
        self.rotate()


    def getVectors(self):
        """ convert all lig and rec indices to vectors

        """
        # XXX ADAPT THIS TO WORK WITH MULTIPLE MATCHES
        if self.debug: print "GETTING LIGAND VECTORS..."
        self._ligB = self._idxToVec(self.lig, self.ligIndices[0])
        self._ligA = self._idxToVec(self.lig, self.ligIndices[1])


        if self.debug: print "GETTING RECEPTOR VECTORS..."
        self._recI = self._idxToVec(self.rec, self.recIndices[0], translate=0) #  , reverse=)
        self._recJ = self._idxToVec(self.rec, self.recIndices[1], translate=0) # , reverse=True)
        #self._recI = self._idxToVec(self.rec, self.recIndices[0], translate=True, reverse=True)
        #self._recJ = self._idxToVec(self.rec, self.recIndices[1], translate=True, reverse=True)


        #self._recI = self._idxToVec(self.rec, self.recIndices[0], translate=True) #  , reverse=)
        #self._recJ = self._idxToVec(self.rec, self.recIndices[1], translate=True) # , reverse=True)

        if self.debug:
            c = 1
            buff = ['MODEL']
            buff.append( makePdb(coord=self._ligB, at_index=c, atype='P'))
            c+=1
            buff.append( makePdb(coord=self._ligA, at_index=c, atype='P'))
            c+=1
            buff.append( makePdb(coord=self._recI, at_index=c, atype='S'))
            c+=1
            buff.append( makePdb(coord=self._recJ, at_index=c, atype='S'))
            buff.append('ENDMDL')
            writeList('DEBUG_getVectors.pdb', buff, addNewLine=1, mode='a')

    def _idxToVec(self, mol, atIdx, convert=True,translate=False):
        """ return the vector of the atom at index atIdx
            if convert requested, return Numpy array instead of OB.Vector3
        """
        #print "CALLED BY", mol, atIdx, convert, translate
        atIdx = int(atIdx)
        if translate:
            # DuplicateMolecule obj
            atom = mol.GetAtom(atIdx, translate=True)
        else:
            # OBMol object
            atom = mol.GetAtom(atIdx)
        try:
            vec = atom.GetVector()
        except:
            print "*** ERROR:", sys.exc_info()[1]
            print "*** REQUESTED", atIdx
            print "*** FOUND", 
            for a in ob.OBMolAtomIter(mol):
                print a.GetIdx(),
            print " "
            return
        if not convert:
            return vec
        return self.obVecToNumpy( vec )


    def translate(self):
        """ perform the 1. translation step """
        if self.verbose: print "Translation...",
        translation = vector( self._ligA, self._recI)
        self._translateMol(self.lig, translation)
        # update vector coords after translation
        self.getVectors()
        if self.debug:
            pybel.Molecule(self.lig).write('pdb', 
                'DEBUG_translated.pdb', overwrite=True)
        if self.verbose: print "[ DONE ]"

    def rotate(self):
        """ perform the 2. rotation step"""
        import math
        if self.verbose: print "Rotation...",
        ## rotation
        p1 = self._ligB
        p2 = self._ligA
        p3 = self._recJ
        p4 = self._recI
        v1 = vector(p1,p2)
        v2 = vector(p3,p2)
        angle = vecAngle(v1, v2) # rad
        center = vector(p2)
        normVec = calcPlane( p1, p2, p3)
        if angle < 0.09:
            if self.verbose: 
                print ( '[ skipping rotation, angle near-zero (%1.3f ), '
                        'ligand possibly already in place' % (angle) )
            #return
            pass
        if self.debug:
            print "Rotation angle:", math.degrees(angle)
            pdb1 = makePdb(coord=p1, at_index = 1, atype ='S')
            pdb2 = makePdb(coord=p2, at_index = 2, atype ='S')
            pdb3 = makePdb(coord=p3, at_index = 3, atype ='S')
            pdb4 = makePdb(coord=normVec+p2, at_index = 4, atype ='N')
            self._testrot(p1, p2, normVec) # writes rotor.pdb
            writeList('DEBUG_plane.pdb', [pdb1, pdb2, pdb3, pdb4], addNewLine=1)
        rotor = ( normVec[0], normVec[1], normVec[2], angle )
        self._rotateMol( self.lig, p2, rotor)
        if self.debug:
            pybel.Molecule(self.lig).write('pdb', 'DEBUG_rotated.pdb', overwrite=True)
        if self.verbose: print "[ DONE ]"
        return


    def _translateMol(self, mol, v):
        """ translate the molecule using vector3"""
        for i in range(mol.NumAtoms()):
            atom = mol.GetAtom(i+1)
            pre = (atom.GetX(), atom.GetY(), atom.GetZ())
            post = (pre[0]+v[0], pre[1]+v[1], pre[2]+v[2])
            obvec = ob.vector3()
            obvec.Set(post[0], post[1], post[2])
            atom.SetVector(obvec)
        return

    def _rotateMol(self, mol, center, rotor):
        """ rotate molecule atoms applying vector around center"""
        for a in ob.OBMolAtomIter(mol):
            coord = self.obVecToNumpy( a.GetVector() )
            vec = vector(center, coord)
            newCoord = rotatePoint( vec, center, rotor)
            x,y,z = self.vecToDouble(newCoord)
            vec = ob.vector3()
            vec.Set(x,y,z)
            a.SetVector(vec)

    def _testrot(self, point, center, norm):
        """ debug function to depict the rotor applied in the mol rotation"""
        buff = []
        buff = [  makePdb((0.,0.,0.), at_index =1, atype='S') ]
        buff.append(  makePdb((1.8,0.,0.), at_index =2, atype='S') )
        buff.append(  makePdb((0.,1.8,0.), at_index =3, atype='S') )
        buff.append(  makePdb((0.,0.,1.8), at_index =4, atype='S') )
        buff.append(  makePdb(point, at_index =5, atype='S') )
        c = 6
        for a in range(0, 360, 30):
            a = math.radians(a)
            rotor = ( norm[0], norm[1], norm[2], a)
            coord = vector(point,center)
            new = rotatePoint( coord, center, rotor)
            atom = makePdb(new, at_index =c)
            buff.append(atom)
        writeList('DEBUG_rotor.pdb', buff, addNewLine=1)
        
        
    def obVecToNumpy(self, ObVec):
        """ """
        return np.array( ( ObVec.GetX(), ObVec.GetY(), ObVec.GetZ() ), 'f')

    def vecToDouble(self, vector):
        """ """
        return float(vector[0]), float(vector[1]), float(vector[2])
        
class CovalentReaction:
    def __init__(self):
        """ simmeglio """
        """ IT SHOULD be used to attach the next group to the reaction 
        to be used for the alignment """
        pass

            


# ########################


class CovalentDockingMaster:
    """ manage settings for the CovalentDocking object""" 

    def __init__(self, debug=False, verbose=False):
        """ """
        self.debug = debug
        self.verbose = verbose
        self.initOpts()
        self.parseOpts()
        self.start()

    def getFnameExt(self,string):
        """ """
        name, ext = os.path.splitext(string)
        ext = ext[1:]
        return name, ext

    def initOpts(self):
        """ """
        self.initDefaults()
        self.initDocs()
        self.opts = {

        '--ligand' : {'help': 'ligand file (OPTIONAL)',
            'action':'store', #'required':True,
            'type':str},

        '--receptor' : {'help':'receptor file (REQUIRED)',
            'action':'store', 'required':True, 'type':str},

        '--residue' : {'help': ('residue to modify; the format is "chain:resNUM (es. "B:THR276")'
                               '; multiple residues can be specified by repeating --residue (note: '
                                'case insensitive)'), 'action':'append', 'default':[], 'type':str},

###        '--residuelist' : {'help' : 'modify residues read from file (one per line)',
###                            'action':'store', 'metavar': 'FILE', 'default':None},
###
###        '--covresidue' : {'help':'prepare modified residue for the covalent residue mode (default)',
###            'default': True, 'action': 'store_true'},
###
###        '--covmap' : {'help': 'calculate coordinates for Z-map covalent method',
###            'default': False, 'action': 'store_true'},
###
###
        '--ligsmarts' : {'help':('ligand SMARTS pattern; by default, the first two atoms of '
                         'the pattern are used; use --ligindices to specify different atoms'),
            'action':'store', 'type':str, 'metavar':'SMARTS', 'default':None},

        '--ligindices' : {'help':('indices of ligand atoms to use for alignment (i.e X-Y-lig)'
            'starting from 1; by default, indices refer to atoms in the ligand file; if --ligsmarts '
            'is used, indices specify atoms in the SMARTS pattern'),
            'action':'store', 'type':str, 'metavar':'X,Y'},

        '--recsmarts' : {'help':('receptor SMARTS pattern; by default, the first two atoms of '
                         'the pattern are used; use --recindices to specify different atoms'),
            'action':'store', 'type':str, 'metavar':'SMARTS', 'default':None},

        '--recindices' : {'help':('indices of receptor atoms to use for alignment (i.e. I-J-rec) '
            'starting from 1; by default, indices refer to atoms in the ligand file; if --recsmarts '
            'is used, indices specify atoms in the SMARTS pattern'),
            'action':'store', 'type':str, 'metavar':'I,J'},

        '--genfullrec' :  {'help':('generate combined receptor-ligand structure; '
                       'by default, only the modified residue (including the ligand) is written '
                        '(default : %s)' % self.default_genfullrec ) ,
                'action':'store_true' },

        '--outputfile' :  {'help':('save the output in the file specified'
                       '(default : use input file'),
            'action':'store', 'type':str, 'metavar':'FILENAME'},

###        '--generatelig' : {'help' : ('generate structure of flexible covalent ligand for AutoDock'),
###                       'action':'store_true', 'default':self.default_flex},
###
        '--generaterec' : {'help' : ('generate structure')},

        '--verbose':{'help': ('enable verbose mode'), 'action':'store_true',
                    'default':False},

        '--log' : {'help' : ('write log file'), 'action':'store', 'metavar' : 'LOGFILE'},

        '--help_advanced':{'help': ('show advanced help and documentation'), 
            'action': 'store_true', 'default':False} 
            }

        self.groups_order = ['INPUT STRUCTURES', 'RESIDUE SPECIFICATION',# 'MODE', 
            'LIGAND ALIGNMENT DATA', 'RECEPTOR ALIGNMENT DATA (OPTIONAL)', 'OUTPUT', 'LOGGING/HELP']

        self.groups = { 'INPUT STRUCTURES' : ['--receptor', '--ligand'],
            
                        'RESIDUE SPECIFICATION' : ['--residue'  ],

                        #'MODE' : ['--covresidue', '--covmap'],

                        'LIGAND ALIGNMENT DATA': ['--ligindices', '--ligsmarts'],


                        'RECEPTOR ALIGNMENT DATA (OPTIONAL)': ['--recindices', '--recsmarts'],

                        'OUTPUT' : [ '--generaterec', '--genfullrec', '--outputfile'],
                        'LOGGING/HELP':['--log', '--verbose', '--help_advanced'],
                        }
        self.usage = '%s --ligand xxxx.xxx --receptor xxxx.xxx [ alignment mode ]' 
        self.usage = None
        
    def initDocs(self):
        """ """
        self.description = (
        """Raccoon PrepareCovalent: typical usages

 Create input ligand/receptor structures for covalent docking:
    %(name)s --receptor receptor.pdb --ligand ligand.pdb --residue A:CYS113 --ligsmarts CSCC --
        
 Create input ligand/receptor structures for covalent docking:
    %(name)s --receptor receptor.pdb --ligand ligand.pdb --residue A:CYS113 --ligsmarts CSCC
        """% { 'name': sys.argv[0] } )
        self.epilog = "(C) 2014 Stefano Forli, MGL, TSRI\n Please cite..."

    def initDefaults(self):
        """ """
        self.default_ligPatternIdx = (0,1)
        self.default_recPatternIdx = None #(0,1)
        self.default_genfullrec = False
        self.default_ligpatternidx = (0,1)
        self.default_recpatternidx = None #(0,1)
        self.default_outputfile = None
        self.default_flex = False

    def showAdvancedHelp(self):
        """ """
        advHelp = ('[ADVANCED HELP GOES HERE')
        print advHelp
        sys.exit(0)

    def parseForeignOpts(self):
        """ remove foreign options from the command line"""
        foreign = {'prepare': []}
        # debug
        if '--debug' in sys.argv[1:]:
            print "\n**** Debug mode activated ***\n\n"
            self.debug = True
            sys.argv.remove('--debug')
        # prepare
        for k in foreign.keys():
            remove = []
            for opt in sys.argv[1:]:
                if opt[2:].startswith(k):
                    foreign[k] = opt
                    remove.append(opt)
            for opt in remove:
                sys.argv.remove(opt)

    def parseOpts(self):
        """ parse command-line options"""
        self.parseForeignOpts()

        self.parser = argparse.ArgumentParser(description = self.description,
            usage=self.usage, epilog=self.epilog, 
            formatter_class = argparse.RawDescriptionHelpFormatter)
        for g in self.groups_order:
            group = self.parser.add_argument_group(g)
            for i in self.groups[g]:
                    opts = self.opts[i]
                    group.add_argument(i, **opts)
        self.args = self.parser.parse_args()
        if self.args.help_advanced:
            self.showAdvancedHelp()
        self.alignerArgs = {}
        self.verbose =  self.alignerArgs['verbose'] = self.args.verbose
        self.validateOpts()
        if hasattr(self.args, 'outputfile'):
            self._output = self.args.outputfile
        else:
            self._output = None

    def validateOpts(self):
        """ validate all options and set the modes for the actual calculation"""
        self.validateMode()
        self.setLigandMode()
        self.setReceptorMode()

    def setLigandMode(self):
        """ guess the ligand mode basing on the spefication of indices or SMARTS
            --ligindices 
            --ligsmarts [ --ligindices ]
        """
        args = self.alignerArgs #= {}
        self._ligmode = 'idx'
        idxError = ('Ligand indices (--ligindices) must be specified as "number,number" (starting from 1)')
        # ligand mode
        if self.args.ligsmarts:
            self._ligmode = 'smarts'
            args['smartsLig'] = self.args.ligsmarts
            if self.args.ligindices: 
                try:
                    # smarts indices are 0-based internally
                    args['smartsIdxLig'] = [int(x)-1 for x in  self.args.ligindices.split(',')]
                except:
                    self.showError(idxError)
            else:
                args['smartsIdxLig'] = self.default_ligPatternIdx
        else:
            if not self.args.ligindices:
                msg = ('Ligand indices (--ligindices) are required, or use SMARTS (--ligsmarts)')
                self.showError(msg)
            else:
                try:
                    args['indicesLig'] = [int(x) for x in  self.args.ligindices.split(',')]
                except:
                    self.showError(idxError)
        self.vprint("LIGAND MODE:"+self._ligmode)

    def setReceptorMode(self):
        """ set receptor alignment mode (OPTIONAL)"""
        args = self.alignerArgs #= {}
        self._recmode = None
        idxError = ('Receptor indices (--recindices) must be specified as "number,number" (starting from 1)')
        # receptor mode
        if self.args.recsmarts:
            self._recmode = 'smarts'
            args['smartsRec'] = self.args.recsmarts
            if self.args.recindices:
                try:
                    # smarts indices are 0-based internally
                    args['smartsIdxRec'] = [int(x)-1 for x in  self.args.recindices.split(',')]
                except:
                    self.showError(idxError)
            else:
                args['smartsIdxRec'] = self.default_recPatternIdx
        else:
            if self.args.recindices:
                self._recmode = 'idx'
                try:
                    args['indicesRec'] = [int(x) for x in  self.args.recindices.split(',')]
                except:
                    self.showError(idxError)
        # check that specified residue is managed, then no SMARTS/indices is required
        if (self._recmode == None):
            unsupported = self.checkManagedResidue()
            if len(unsupported):
                msg = ('The specified residue types are not supported automatically: %s. Use either '
                        '--recsmarts or --recindices.' % (','.join(unsupported)))
                self.showError(msg)
        args['genFullRec'] = self.args.genfullrec
         
    def validateMode(self):
        """ set session mode to be:
                - normal (lig + receptor + residue|residuetype)
        """
        self.mode = 'normal'
        if not self.args.residue:
            msg = ('No residue specification. Use at least --residue to specify which residue to modify')
            self.showError(msg)
        if self.args.residue and not self.args.ligand:
            msg = ('option --residue requires --ligand to be specified')
            self.showError(msg)
    
    def checkManagedResidue(self):
        """ check that requested residue type is 
            among managed residues: CYS, SER, THR, LYS
        """
        supported = ['cys', 'ser', 'thr', 'lys']
        unsupported = []
        for r in self.args.residue:
            if ':' in r:
                r = r.split(":")[1][:3].lower()
                if not r in supported:
                    unsupported.append(r)
        return set([ x.upper() for x in unsupported])

        



    def parseLigAlignmentOpts(self):
        """ validate parameters for ligand alignment """ 
        self._ligmode = None
        # SMART INDICES
        self.ligsmarts = self.args.ligsmarts
        if self.ligsmarts:
            self._ligmode = 'smarts'
        self.ligsmartsidx = self.args.ligsmartsidx
        try:
            if not self.ligsmartsidx == None:
                self.ligsmartsidx = [ int(x) for x in self.ligsmartsidx.split(',') ]
        except:
            print "ERROR (--ligsmartsidx): indices must be specified with number pairs, e.g. 1,3"
            sys.exit(1)
        self._ligmode = 'smarts'

        # ATOM INDICES
        self.ligatomidx = self.args.ligatomidx
        if self.ligatomidx and self._ligmode == 'smarts':
            msg = ('Multiple alignment modes selected: use either SMARTS (\'--ligsmarts\')'
                    'or atom indices(\'--ligatomidx\')')
            self.showError(msg)
        # INDICES
        try:    
            if not self.ligatomidx == None:
                self.ligatomidx = [ int(x) for x in self.ligatomidx.split(',') ]
        except:
            print "ERROR (--ligatomidx): indices must be specified with number pairs, e.g. 1,3"
            sys.exit(1)


    def parseRecAlignmentOpts(self):
        """ """
        # validate receptor SMARTS indices
        try:
            self.recsmartsidx = self.args.recsmartsidx
            if not  self.recsmartsidx == None:
                self.recsmartsidx = [ int(x) for x in self.recsmartsidx.split(',') ]
        except:
            print "ERROR (--recsmartsidx): indices must be specified with number pairs, e.g. 1,3"
            sys.exit(1)
        # validate receptor atom indices  
        try:
            self.recatomidx = self.args.recatomidx
            if not self.recatomidx == None:
                self.recatomidx = [ int(x) for x in self.recatomidx.split(',') ]
        except:
            print "ERROR (--recatomidx): indices must be specified with number pairs, e.g. 1,3"
            sys.exit(1)

    def showError(self, msg, showhelp=True):
        """ error reporting facility (modify to STDERR)"""
        tag = '[ ERROR ] '
        msg = msg.replace('\n', ('\n%s' % (" " * len(tag) )  ) )
        print("%s%s" % (tag, msg))
        if showhelp:
            print ""
            self.parser.print_help()
        sys.exit(1)

    def vprint(self, msg):
        """ verbose printer"""
        if not self.verbose:
            return
        print("VERBOSE: "+msg)

    def getMolecule(self, fname, perceiveChains=False):
        """ molecule parser"""
        name, ext = self.getFnameExt(fname)
        self.molParser.SetInFormat(ext)
        mol = ob.OBMol()
        result = False
        try:
            result = self.molParser.ReadFile(mol, fname) 
        except:
            msg = ('Fail to read molecule "%s" : %s' % (fname, sys.exc_info()[1]))
            self.showError(msg, showhelp=False)
        if not result:
            msg = ('Fail to read molecule "%s"' % (fname))
            self.showError(msg, showhelp=False)
        if perceiveChains:
            self.chainParser.PerceiveChains(mol)
        return mol, name

    def loadMolecules(self):
        """ import ligand and receptor structures"""
        args = self.alignerArgs
        args['rec'], self.recName = self.getMolecule(self.args.receptor)
        args['lig'], self.ligName = self.getMolecule(self.args.ligand, True)


    def getResidues(self, log=None):
        """ find which residue(s) will be modified:
            - specific residues
            - residue types (surface-accessible residues)
        """
        residue = self.args.residue
        if not residue:
            msg = ('No residues specified. Use either to process!')
            self.showError(msg)
        self.residuePool = residue
        chain = None
        if len(self.residuePool) == 0:
            msg = ('No residues to process!')
            self.showError(msg)
        self.residuePool.sort()
        if log:
            fp = open(log, 'w')
            for r in self.residuePool:
                #fp.write( '%s:%s\n' % (self.recName,r))
                fp.write( '%s\n' % (r))
            fp.close()
        #print "========================================================"
        #print "Total number of residues to process [%d]" % len(self.residuePool)
                
    def initParsers(self):
        """ initialize molecule parser and chain perception"""
        self.molParser = ob.OBConversion()
        self.chainParser = ob.OBChainsParser()

    def start(self):
        """ """
        #  XXX validate here that the indices are within the lenght of matches?
        self.initParsers()
        self.loadMolecules()
        self.getResidues('residues.log')
        self.processResidues()

    def processResidues(self):
        """ perform full covalent protocol"""
        outType = 'pdb'
        outType = 'mol2'

        for count, residue in enumerate(self.residuePool):
            #print "Processing residue %s\t (%d/%d)" % (residue, 
            #    count+1, len(self.residuePool)),
            print "Processing residue %s" % residue
            if not self._output == None:
                outname = self._output
                outType = os.path.splitext(self._output)[1][1:]
            else:
                outname = '%s_%s_cov_%s' % (os.path.basename(self.ligName), 
                    os.path.basename(self.recName),
                        residue.replace(':','').upper())
                outname = outname + "." + outType 
            self.vprint("[start] output filename is: "+ outname)
            print ("[start] output filename is: "+ outname)

            self.alignerArgs['resName'] = residue
            if self.verbose:
                print "==============="
                print "[start] Calling CovalentDockingMaker with settings:"
                for k,v in self.alignerArgs.items():
                    if isinstance(v, ob.OBMol):
                        print "KW[%s]: %d atoms" % (k, v.NumAtoms())
                    else:
                        print "KW[%s]:" % k, v

                print "==============="
            #print "\n==============\n", self.alignerArgs
            if self.debug:
                self.alignerArgs['debug'] = True
            aligner = self.x = CovalentDockingMaker(**self.alignerArgs)
            if not aligner.ready:
                print "\t\t\tSKIPPING?"
                continue

            #print "\t=>", outname + '.pdb'
            # XXX LOCAL FILE HERE
            fname = os.path.basename(outname) # + '.pdb'
            #aligner.writeCovalent(outname, 'pdb')
            aligner.writeCovalent(fname, outType)
            print "Writing output filename: %s" % fname

            #aligner.writeCovalent(outname, 'pdbqt')
            # WORKING PATTERNS
            #           LIG     REC
            #    -------------------------------
            #           CSCC    '[SH]C'
            #                   '[$(SH1);$(SC)]'
            #           SCC     '[$([SH1]);$(SC)]'
    
if __name__ == '__main__':
    x = CovalentDockingMaster()


