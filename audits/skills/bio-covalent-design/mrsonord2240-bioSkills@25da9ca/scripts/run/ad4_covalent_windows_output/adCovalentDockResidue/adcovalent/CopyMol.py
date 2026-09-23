#!/usr/bin/env/python

import pybel
ob = pybel.ob
import os


class OBMolCopy(ob.OBMol):
    """ Duplicate OBMolecule with extra properties
           
        The new molecule will have the following extra attributes
        as lookup tables (dictionaries):

             self._numbering: 
                used to provide consistent indexing to GetAtom()
                even when not the entire molecule is copied
                allowing to ask for atom 991 in a molecule with 6 atoms

            self._numberingReverse:
                allows to perform inverse mapping to find which atom
                in the copy corresponds to the original molecule 
                (i.e. atom 6 -> 991) 
    
            self.bondToAtoms:

            self.atomsToBond: 

                provide an index to identify them
                by their begin/end atoms instead of bond index
                (useful when tracking bonds after deleting one
                or more [i.e., bond indexing altered] )


    """

    def __init__(self, **args):
        """ duplicate molecule with extra properties"""
        ob.OBMol.__init__(self, **args)

        self._numbering = {}
        self._numberingReverse = {}
        """
        """        
        self.bondToAtoms = {}
        self.atomsToBond = {}

    def GetAtom(self, idx, translate=False, reverse=False):
        """ overload the original OB function
            to conserve indexing and allow to
            return atom 1322 in a molecule with 6 atoms
            # XXX TODO this should be simplified using the
            # 'original' kw?
            TODO DOCUMENT THIS!!!
        """
        if translate:
            try:
                if reverse: 
                    internalIdx = self._numberingReverse[idx]
                else:       
                    internalIdx = self._numbering[idx]
            except: # mimic the original OBMol.GetAtom() behavior
                return None
        else:
            internalIdx = idx
        return ob.OBMol.GetAtom(self, internalIdx)


class MoleculeDuplicator:

#class DuplicateMolecule(ob.OBMol):
    """ 
        create a copy of the input OBMol trying to preserve
        properties from the original.

        The following properties are preserved in the copy:

          RESIDUE : name, seq. number, idx, chain, chain#
          ATOM    : element, idx, coordinates, bonds, bondIdx

        When copying bonds, populate two indexed lookup tables,
        bondToAtoms and atomsToBond, that allow to keep track
        of bonds even upon atoms/bonds deletion (OB indices 
        in these case change!)
    """
    def __init__(self, mol, name = None, resList = [], debug=False):
        """ mol     : original OBMol

            name    : new molecule name [OPT]

            resList : copy only residues in the list [OPT]
                      residues are specified with the following
                      format: chain:resRESNUM
                      NOTE: When reslist is used, bond index is not
                      preserved!
        """
        self.debug = debug
        if self.debug:
            print "\n\n=============================\nINIT\n=-=====================",resList
        self.original = mol
        self.name = name
        if self.name == None:
            self.name = "%s [COPY]" % self.original.GetTitle()

        self.initMolecule()
        self.initResList(resList)
        self.copyStructHerarchy()
        self.copyBonds()
        self.copyData()
        if self.debug:
            self.debugStruct()
        

    def debugStruct(self):
        """ """
        pass


    def initMolecule(self):
        """ initialize OBMol object used later

        """
        self.mol = OBMolCopy()
        self.mol.SetTitle(self.name)

    def initResList(self, resList):
        """ create the list of residues to be copied"""
        if resList == []:
            self.resToCopy = [ x for x in ob.OBResidueIter(self.original) ]
            return
        self.resList = dict([ (x.upper(), None) for x in resList ])
        self.resToCopy = []
        for res in ob.OBResidueIter(self.original):
            chain = res.GetChain()
            name = res.GetName()
            num = res.GetNum()
            item = "%s:%s%s" % (chain, name, num)
            if item in self.resList:
                self.resToCopy.append(res)
        if len(self.resToCopy) == 0:
            print "WARNING: no residues copied"
        

    def _getallres(self):
        """ generator for getting all residues"""
        yield None
        

    def _getselres(self, resList):
        """ generator for getting some residues"""
        yield None



    def copyStructHerarchy(self):
        """ copy the structure herarchy of the original
            molecule in the new one.
            iterate residues and atoms.
        """
        # XXX add chain copy
        #for res in ob.OBResidueIter(self.original):
        if len(self.resToCopy):
            if self.debug: 
                print "COPYING FROM RESIDUES"
            self.copyAtomsFromResidues()
        else:
            if self.debug: 
                print "COPYING FROM ATOMS"
            self.copyAtomsFromMol()


    def copyAtomsFromMol(self):
        """ copy atoms from molecules with no residue specification"""
        tot = range(self.original.NumAtoms())
        allAtoms = [ self.original.GetAtom(i+1) for i in tot ]
        for a in allAtoms:
            new = self.copyAtom(a)
            #self.mol

    def copyAtomsFromResidues(self):
        """ copy residue structure"""
        for res in self.resToCopy:
            newRes = self.copyResidue(res)
            for a in ob.OBResidueAtomIter(res):
                # create a copy of the new atom
                newAtom = self.copyAtom(a)
                # include the atom in the newly created atom 
                newRes.AddAtom(newAtom)
                newAtom.SetResidue(newRes)
                # copy PDB atom id from the old atom in the old residue
                newRes.SetAtomID( newAtom, res.GetAtomID(a) )
            self.mol.AddResidue(newRes)
            self.last = newRes

    def copyResidue(self, res):
        """ create copy of residue in the new molecule"""
        new = self.mol.NewResidue() 
        new.SetName( res.GetName() )
        new.SetIdx(  res.GetIdx() )
        new.SetNum(  res.GetNum() )
        new.SetChain( res.GetChain() )
        new.SetChainNum( res.GetChainNum() )
        return new

    def copyAtom(self, atom):
        """ create copy of atom in the new molecule """
        new = self.mol.NewAtom()
        new.SetAtomicNum( atom.GetAtomicNum() )
        new.SetIdx( atom.GetIdx() ) # this is useless...
        self.mol._numbering[atom.GetIdx()] = len(self.mol._numbering.keys())+1
        self.mol._numberingReverse[len(self.mol._numbering.keys())] = atom.GetIdx()
        new.SetVector( atom.GetVector() )
        return new

    def copyBonds(self):
        """ copy bonds"""

        if len(self.resToCopy):
            self.copyBondsFromResidue()
        else:
            self.copyBondsFromMolecule()


    def copyBondsFromResidue(self):
        """ copy bonds iterating through residues"""
        missedBonds = []
        for res in self.resToCopy:
            #print "COPYING", res.GetName()
            acount = 0
            bcount = 0
            for atom in ob.OBResidueAtomIter(res):
                acount +=1
                bpa = 0
                for bond in ob.OBAtomBondIter(atom):
                    bcount += 1
                    bpa+=1
                    idx = bond.GetIdx()
                    #print "BOIDX", idx
                    begin = bond.GetBeginAtomIdx()
                    end = bond.GetEndAtomIdx()
                    newBegin = self.mol.GetAtom(begin, translate=1)
                    # This triggers a SEGFAULT!
                    #if newBegin == None:
                    #    continue
                    newEnd = self.mol.GetAtom(end, translate=1)
                    try:
                        newBegin = newBegin.GetIdx()
                        newEnd = newEnd.GetIdx()
                    except:
                        # broken bond
                        if self.debug: print "MISSING BOND", newBegin, newEnd
                        missedBonds.append(bond)
                        continue
                    order = bond.GetBondOrder()
                    new = self.mol.AddBond(newBegin, newEnd, order)
                    self.mol.bondToAtoms[idx] = [ begin, end ]
                    # key indexing
                    key1 = "%d_%d" % (begin, end)
                    key2 = "%d_%d" % (end, begin)
                    self.mol.atomsToBond[key1] = self.mol.GetBond(self.mol.NumBonds()-1)
                    self.mol.atomsToBond[key2] = self.mol.GetBond(self.mol.NumBonds()-1)
                #print "BPATOM", bpa, res.GetAtomID(atom)
            #print "WACOUNT", acount, bcount
        if self.debug: 
            print "Residue [%s]:"" %d missed bonds" % (res.GetName(), len(missedBonds)),
            if len(missedBonds) > 2 :
                print "WARNING!",
            print " "
        return

    def copyBondsFromMolecule(self):
        """ copy bonds iterating through residues"""
        missedBonds = []
        #print "COPYING", res.GetName()
        tot = range(self.original.NumAtoms())
        allAtoms = [ self.original.GetAtom(i+1) for i in tot ]
        acount = 0
        bcount = 0
        for atom in allAtoms:
            acount +=1
            bpa = 0
            for bond in ob.OBAtomBondIter(atom):
                bcount += 1
                bpa+=1
                idx = bond.GetIdx()
                #print "BOIDX", idx
                begin = bond.GetBeginAtomIdx()
                end = bond.GetEndAtomIdx()
                newBegin = self.mol.GetAtom(begin, translate=1)
                # This triggers a SEGFAULT!
                #if newBegin == None:
                #    continue
                newEnd = self.mol.GetAtom(end, translate=1)
                try:
                    newBegin = newBegin.GetIdx()
                    newEnd = newEnd.GetIdx()
                except:
                    # broken bond
                    if self.debug: print "MISSING BOND", newBegin, newEnd
                    missedBonds.append(bond)
                    continue
                order = bond.GetBondOrder()
                new = self.mol.AddBond(newBegin, newEnd, order)
                self.mol.bondToAtoms[idx] = [ begin, end ]
                # key indexing
                key1 = "%d_%d" % (begin, end)
                key2 = "%d_%d" % (end, begin)
                self.mol.atomsToBond[key1] = self.mol.GetBond(self.mol.NumBonds()-1)
                self.mol.atomsToBond[key2] = self.mol.GetBond(self.mol.NumBonds()-1)
            #print "BPATOM", bpa, res.GetAtomID(atom)
        #print "WACOUNT", acount, bcount
        return




    def copyData(self):
        """ """
        # XXX not implemented yet
        return

    def getCopy(self):
        """ return the copy (OBMolCopy) of the original molecule """
        return self.mol

if __name__ == "__main__":
    from sys import argv
    import pybel
    ob = pybel.ob
    import os
    name, ext = os.path.splitext(argv[1])
    ext = ext[1:]
    #try:
    if True:
        resList = argv[2].split(",")
        print "SPLITTING RESIDUES", resList
    #except:
    #    resList = []

    org = pybel.readfile(ext, argv[1]).next()
    duplicator = MoleculeDuplicator(org.OBMol,resList = resList)
    new_mol = duplicator.getCopy()
    #newp = pybel.Molecule(new_mol)
    for res in ob.OBResidueIter(new_mol):
        print res.GetName()
        for a in ob.OBResidueAtomIter(res):
            print "ATOM", a.GetAtomicNum()
            break
        break
