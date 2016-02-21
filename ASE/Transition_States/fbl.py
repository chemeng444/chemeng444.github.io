import sys
import cPickle as pickle

from ase import *
from ase import io
from ase.constraints import FixAtoms, FixBondLength
from ase.dft.bee import BEEF_Ensemble
from ase.optimize import QuasiNewton
from espresso import espresso

#########################################################################################################
#####                                     YOUR SETTINGS HERE                                        #####
#########################################################################################################

# read in trajectory. this should be the dissociated OH and H
atoms = io.read('surface.traj')

# specify the two atoms whose distance is to be fixed
# during the geometry optimization
# One should be the O atom, and the other is the dissociated H
# MAKE SURE YOU HAVE CHOSEN THE RIGHT ATOMS BEFORE SUBMITTING
# don't wait until it has finished running to find out you fixed
# the wrong atoms

atom1=12
atom2=13

metals = ['Pt','Rh'] # first specify a list of metals or just the single metal, e.g. ['Pt']

# SET TO True if fix cluster, otherwise False
fix_cluster = True

threshold = 0.9    # threshold bond-length for terminating the FBL calculation

## KPTS SET AUTOMATICALLY

#########################################################################################################
#####                                     END                                                       #####
#########################################################################################################


# apply all constraints
constraints = [FixBondLength(atom1,atom2)]

num_atoms = len([atom.index for atom in atoms if atom.symbol not in ['N','H']])


#### FOR SLABS ONLY ####
# specify height below where atoms are fixed (bottom two layers)
# for clusters, comment out everything from this line until `atoms.set_constraint(fixatoms)`
if num_atoms == 16:
    print "slab calculation..."
    kpts = (4, 4, 1)
    mask = [atom.z < 10 for atom in atoms]      # atoms in the structure to be fixed
    constraints.append(FixAtoms(mask=mask))     # this is NOT needed for the M13 cluster!!


#### FOR FIXED CLUSTERS ONLY ####
# ONLY use this if you have a system that reconstructed significantly during reconstruction
# i.e. if it flattened out with distortions.
# If your cluster optimized normally without distortions then this is not needed!
elif  num_atoms == 13:
    print "cluster calculation..."
    kpts = 'gamma'
    if fix_cluster:
        fixatoms = FixAtoms(indices=[atom.index for atom in atoms if atom.symbol in metals])
        constraints.append(fixatoms)


#### FOR CLUSTERS THAT DISTORT WITH AN ADSORBATE ####
# relaxed_idx = [1, 2, 3]  # index of atoms allowed to relax
# fixatoms = FixAtoms(indices=[atom.index for atom in atoms if atom.index not in relaxed_idx])
else:
    print "Wrong number of metal atoms! Check your input trajectory!"
    exit()


# apply constraints - always use this unless NO atoms are fixed
atoms.set_constraint(constraints)


# Find the distance between the two atoms to fix
a = Atoms()
a.append(atoms[atom1])
a.append(atoms[atom2])
d = a.get_distance(0,1)
        
# calculator setup, using the same settings as before
calc = espresso(pw = 500,
                dw = 5000,
                kpts = kpts,     # (4,4,1) FOR SURFACES and 'gamma' FOR CLUSTERS
                nbands = -10,
                xc = 'BEEF-vdW', 
                psppath='/home/vossj/suncat/psp/gbrv1.5pbe',
                convergence = {'energy':1e-5,
                               'mixing':0.1,
                               'nmix':10,
                               'maxsteps':500,
                               'diag':'david'
                                },
                beefensemble=True,
                spinpol = False,
                outdir = 'calcdir',
                )   

# attach the calculator
atoms.set_calculator(calc)

# Print the results to a file called "PES.dat"
# this will write out the total energy at each fixed bond length
f = open('PES.dat', 'w')
print >> f,'newlength energy'

# number of steps
numsteps = 40

# for loop that changes the distance between the atoms, fixes it, and performs
# a structural optimization. results writen out as i*.traj files
for step, delta in enumerate(xrange(0,30,1)):
    if atoms.get_distance(atom1, atom2) < threshold:
        break

    if step < numsteps:
        atoms.set_distance(atom1, atom2, d, fix=0.5)

        qn = QuasiNewton(atoms, trajectory='i'+str(delta)+'.traj')
        qn.run(fmax=0.05)
        
        e = atoms.get_potential_energy()

        print d, e
        print >> f, d, e
        f.flush()
        
    d -= 0.1

f.close()

# ensemble
ens = BEEF_Ensemble(calc)
ens.get_ensemble_energies()
ens.write('fbl.bee')
del sys, calc, ens
