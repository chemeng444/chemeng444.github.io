from ase import *
from ase.constraints import *
from ase.dft.bee import BEEF_Ensemble
from ase.io import read
from ase.optimize import QuasiNewton
from espresso import espresso
import cPickle as pickle

# read in trajectory file
# it can be the clean surface or
# with atoms adsorbed
atoms = read('surface.traj')

# for slabs, specify height below where atoms are fixed (bottom two layers)
# for clusters, comment out everything from this line until `atoms.set_constraint(fixatoms)`
z_height = 10.0 

# set constraints. these should already be in place
# if you set this previously in exercise 1
mask = [atom.z<z_height for atom in atoms]
fixatoms = FixAtoms(mask=mask)
atoms.set_constraint(fixatoms)

#set up espresso calculator with 20 extra bands
#and 4x4x1 k-point sampling
calc = espresso(pw=500,             #plane-wave cutoff
                dw=5000,            #density cutoff
                xc='BEEF-vdW',      #exchange-correlation functional
                kpts=(4,4,1),       #k-point sampling;
                nbands=-20,         #20 extra bands besides the bands needed to hold
                                    #the valence electrons
                sigma=0.1,
                psppath='/home/vossj/suncat/psp/gbrv1.5pbe',    #pseudopotential path
                convergence= {'energy':1e-5, #convergence parameters
                              'mixing':0.1,
                              'nmix':10,
                              'mix':4,
                              'maxsteps':500,
                              'diag':'david'
                              },
                dipole={'status':True}, #dipole correction to account for periodicity in z
                beefensemble = True,
                printensemble =True,
                outdir='calcdir')    #output directory for Quantum Espresso files

# attach the espresso calculator to the surface
atoms.set_calculator(calc)

# optimize the structure until the maximum force is
# at most 0.05 eV/AA
# output will be written to "qn.traj" with optimization log
# written to "qn.log"
qn = QuasiNewton(atoms, trajectory='qn.traj', logfile='qn.log')
qn.run(fmax=0.05)

#relevant commands for saving the BEEF error ensemble
#useful if you choose to perform error analysis
ens = BEEF_Ensemble(calc)
ens_e = ens.get_ensemble_energies()
ens.write('ensemble.bee')
pickle.dump(ens_e,open('ensemble.pkl','w'))
