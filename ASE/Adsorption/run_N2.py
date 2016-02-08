#!/usr/bin/env /home/vossj/suncat/bin/python
#above line selects special python interpreter needed to run espresso
#SBATCH -p iric 
#################
#set a job 
#SBATCH --job-=myjob
#################
#a file for job output, you can check job progress
#SBATCH --output=myjob.out
#################
# a file for errors from the job
#SBATCH --error=myjob.err
#################
#time you think you need; default is one hour
#in minutes in this case
#SBATCH --time=5:00:00
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
#SBATCH  --mail-user=ctsai89@stanford.edu
#################
#task to run per node; each node has 16 cores
#SBATCH --ntasks-per-node=16
#################

from ase import *
from ase import io
from ase.structure import molecule
from ase.vibrations import Vibrations
from ase.optimize import QuasiNewton
from espresso import espresso
from espresso.vibespresso import vibespresso
from ase.dft.bee import BEEF_Ensemble
import cPickle as pickle
from ase.thermochemistry import IdealGasThermo

name = 'N2'
atoms = molecule('N2')

calc = espresso(pw=500,	        #plane-wave cutoff
                dw=5000,		#density cutoff
                xc='BEEF-vdW',  #exchange-correlation functional
                kpts=(1,1,1),   #k-point sampling
                nbands=-10,	    #10 extra bands besides the bands needed to hold
                				#the valence electrons
                sigma=0.1,
                psppath='/home/vossj/suncat/psp/gbrv1.5pbe',    #pseudopotential
                convergence= {'energy':1e-5,
					               'mixing':0.1,
					               'nmix':10,
					               'mix':4,
					               'maxsteps':500,
					               'diag':'david'
					                },	#convergence parameters
                beefensemble = True,
                printensemble = True,
                outdir='calcdir')	#output directory for Quantum Espresso files

atoms.set_calculator(calc)

vibrateatoms = [atom.index for atom in atoms]

dyn = QuasiNewton(atoms, logfile= 'H2O.log', trajectory='H2O.traj')
dyn.run(fmax=0.05)

energy = atoms.get_potential_energy()

calc.stop()

# Calculate vibrations
calcvib = vibespresso(pw=500,	#plane-wave cutoff
                dw=5000,		#density cutoff
                xc='BEEF-vdW',		#exchange-correlation functional
                kpts=(1,1,1), #k-point sampling
                nbands=-10,	#10 extra bands besides the bands needed to hold
                					#the valence electrons
                sigma=0.1,
                psppath='/home/vossj/suncat/psp/gbrv1.5pbe',    #pseudopotential
                convergence= {'energy':1e-5,
					               'mixing':0.1,
					               'nmix':10,
					               'mix':4,
					               'maxsteps':500,
					               'diag':'david'
					                },	#convergence parameters
                outdirprefix='calcdirv')	#output directory for Quantum Espresso files

atoms.set_calculator(calcvib)


vib = Vibrations(atoms,indices=vibrateatoms,delta=0.03)
vib.run()
vib.summary(method='standard')

# Make trajectory files to visualize the modes.
for mode in range(len(vibrateatoms)*3):
    vib.write_mode(mode)

# Calculate free energy
vib_energies=vib.get_energies()
thermo = IdealGasThermo(vib_energies=vib_energies,
                        electronicenergy=energy,
                        atoms=atoms,
                        geometry='nonlinear',
                        symmetrynumber=2, spin=0)

# At 300K and 101325 Pa
# change for your operating conditions
freeenergy = thermo.get_gibbs_energy(temperature=300,pressure=101325)

f=open('H2O.energy','w')
f.write('Potential energy: '+str(energy)+'\n'+'Free energy: '+str(freeenergy)+'\n')
f.close

ens = BEEF_Ensemble(calc)
ens_e = ens.get_ensemble_energies()
ens.write('ensemble.bee')
pickle.dump(ens_e,open('ensemble.pkl','w'))
