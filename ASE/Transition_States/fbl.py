#!/home/vossj/suncat/bin/python
#above line selects special python interpreter needed to run espresso
#SBATCH -p slac
#################
#set a job name
#SBATCH --job-name=myjob
#################
#a file for job output, you can check job progress
#SBATCH --output=myjob.out
#################
# a file for errors from the job
#SBATCH --error=myjob.err
#################
#time you think you need; default is one hour
#in minutes in this case
#SBATCH --time=2880:00
#################
#number of nodes you are requesting
#SBATCH --nodes=1
#################
#SBATCH --mem-per-cpu=4000
#################
#get emailed about job BEGIN, END, and FAIL
#SBATCH --mail-type=ALL
#################
#who to send email to; please change to your email
#SBATCH  --mail-user=SUNETID@stanford.edu
#################
#task to run per node; each node has 16 cores
#SBATCH --ntasks-per-node=16
#################

import sys
import cPickle as pickle

from ase import *
from ase import io
from ase.constraints import FixBondLength
from ase.constraints import FixAtoms
from ase.dft.bee import BEEF_Ensemble
from ase.optimize import QuasiNewton
from espresso import espresso

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

# apply all constraints
# if you used mask from above to fix layers, uncomment the second one
constraints = [FixBondLength(atom1,atom2)]
mask = [atom.z < 10 for atom in atoms]      # atoms in the structure to be fixed
constraints.append(FixAtoms(mask=mask))
atoms.set_constraint(constraints)


# Find the distance between the two atoms to fix
a = Atoms()
a.append(atoms[atom1])
a.append(atoms[atom2])
d = a.get_distance(0,1)
        
# calculator setup, using the same settings as before
calc = espresso(pw=500,
                dw = 5000,
                kpts = (4, 4, 1), 
                nbands = -10,
                xc = 'BEEF-vdW', 
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
    if step < numsteps:
        atoms.set_distance(atom1, atom2, d, fix=0.5)

        #traj = PickleTrajectory('i'+str(delta)+'.traj','w',atoms)

        qn = QuasiNewton(atoms, trajectory='i'+str(delta)+'.traj')
        qn.run(fmax=0.05)
        
        e = atoms.get_potential_energy()

        print d, e
        print >> f, d, e
        f.flush()
        
    d -= 0.1
    if d <= 1:
      delta=30

f.close()

# ensemble
ens = BEEF_Ensemble(calc)
ens.get_ensemble_energies()
ens.write('fbl.bee')

del sys, calc, ens
