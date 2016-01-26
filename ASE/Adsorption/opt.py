#!/home/vossj/suncat/bin/python
#above line selects special python interpreter needed to run espresso
#SBATCH -p slac
#################
#set a job name
#you can also use --job-name=$PWD when submitting
#SBATCH --job-name=myjob
#################
#a file for job output, you can check job progress
#SBATCH --output=myjob.out
#################
# a file for errors from the job
#SBATCH --error=myjob.err
#################
#time you think you need; default is 20 hours
#SBATCH --time=20:00:00
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

from ase.constraints import *
from ase import *
from ase.io import read
from ase.optimize import QuasiNewton
from espresso import espresso
from ase.dft.bee import BEEF_Ensemble
import cPickle as pickle

# read in trajectory file
# it can be the clean surface or
# with atoms adsorbed
atoms = read('surface.traj')

#set up espresso calculator with 20 extra bands
#and 4x4x1 k-point sampling
calc = espresso(pw=500,	            #plane-wave cutoff
                dw=5000,	    #density cutoff
                xc='BEEF-vdW',	    #exchange-correlation functional
                kpts=(4,4,1),       #k-point sampling;
                nbands=-20,	    #20 extra bands besides the bands needed to hold
                		    #the valence electrons
                sigma=0.1,
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
                outdir='calcdir')	#output directory for Quantum Espresso files

# set constraints. these should already be in place
# if you used the generic scripts for 
# setting up the surfaces, double check to make sure
# the bottom two layers are fixed
mask = [atom.z<10.0 for atom in atoms]
fixatoms = FixAtoms(mask=mask)
atoms.set_constraint(fixatoms)

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
