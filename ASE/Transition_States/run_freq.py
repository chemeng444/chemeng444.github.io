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
#SBATCH --time=30:00:00
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

from ase.io import read
from ase.constraints import FixAtoms
from ase.vibrations import Vibrations
from espresso import espresso
from espresso.vibespresso import vibespresso
from ase.thermochemistry import HarmonicThermo


#############
## more information here: https://wiki.fysik.dtu.dk/ase/ase/thermochemistry/thermochemistry.html
#############

# rename to the name of your trajectory file
# containing the surface with adsorbates

atoms = read('ads_surface.traj')

calc = espresso(pw = 500,
                dw = 5000,
                kpts = (4, 4, 1), 
                nbands = -20,
                xc = 'BEEF-vdW', 
                convergence = {'energy':1e-5,
                               'mixing':0.1,
                               'nmix':10,
                               'maxsteps':500,
                               'diag':'david'
                                },
                spinpol = False,
                outdir = 'calcdir',
                ) 

# special calculator for the vibration calculations
calcvib = vibespresso(pw = 500,
                dw = 5000,
                kpts = (4, 4, 1), 
                nbands = -20,
                xc = 'BEEF-vdW', 
                convergence = {'energy':1e-5,
                               'mixing':0.1,
                               'nmix':10,
                               'maxsteps':500,
                               'diag':'david'
                                },
                spinpol = False,
                outdirprefix = 'vibdir',
                )  	      	      	      	   # log file                                         

atoms.set_calculator(calc)    	      	      	      	   # attach calculator to the atoms                   

energy = atoms.get_potential_energy()                      # caclulate the energy, to be used to determine G

# CHANGE TO THE ATOMS YOU NEED TO VIBRATE
# metal atoms can be assumed to be fixed
vibrateatoms=[12,13,14]	      	      	      	      	   # calculate the vibration modes of atoms #12 and #13
                                                           # change it to the atoms on your surface
atoms.set_calculator(calcvib)    	      	      	         # attach vibrations calculator to the atoms                   

# Calculate vibrations                                                                                        
vib = Vibrations(atoms,indices=vibrateatoms,delta=0.03)    # define a vibration calculation                   
vib.run()     	      	      	      	      	      	   # run the vibration calculation                    
vib.summary(method='standard')	      	      	      	   # summarize the calculated results                 

for mode in range(len(vibrateatoms)*3):                    # Make trajectory files to visualize the modes.    
    vib.write_mode(mode)

# Calculate free energy
vibenergies=vib.get_energies()
vibenergies[:]=[vib for vib in vibenergies if not isinstance(vib,complex)]  # only take the real modes
gibbs = HarmonicThermo(vib_energies = vibenergies, electronicenergy = energy)

# At 300K and 101325 Pa
# change for your operating conditions 
freeenergy = gibbs.get_gibbs_energy(300,101325)

f=open('out.energy','w')
f.write('Potential energy: '+str(energy)+'\n'+'Free energy: '+str(freeenergy)+'\n')
f.close
