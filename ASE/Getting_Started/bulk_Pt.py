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
#SBATCH --time=20:00
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


import numpy as np    #vectors, matrices, lin. alg., etc.
from math import sqrt
import matplotlib
matplotlib.use('Agg') #turn off screen output so we can plot from the cluster
from ase.utils.eos import *  # Equation of state: fit equilibrium latt. const
from ase.units import kJ
from ase import *
from espresso import espresso

a=3.97     #initial guess for lattice constant
b=a/2.
strains = np.linspace(0.97, 1.03, 7) #range for scaling of latt. consts.
                                     #[0.97..1.03] in 7 steps
volumes = []  #we'll store unit cell volumes and total energies in these lists
energies = []
#setup up Quantum Espresso calculator
calc = espresso(pw=500, #plane-wave cutoff
            dw=5000,    #density cutoff
            xc='BEEF-vdW',    #exchange-correlation functional
            kpts=(11,11,11), #sampling grid of the Brillouin zone
                        #(is internally folded back to the
                             #irreducible Brillouin zone)
            nbands=-10, #10 extra bands besides the bands needed to hold
                        #the valence electrons
            sigma=0.1,
            convergence= {'energy':1e-5,    #convergence parameters
                          'mixing':0.1,
                          'nmix':10,
                          'mix':4,
                          'maxsteps':500,
                          'diag':'david'
                          },  
            outdir='calcdir') #output directory for Quantum Espresso files

for i in strains: #loop over scaling factors
    #build Pt unit cell
    atoms=Atoms(symbols='Pt',positions=[(0.0,0.0,0.0)],
                cell=[[0., b*i, b*i], #primitive cell for face-centered cubic structure
                      [b*i, 0., b*i],
                      [b*i, b*i, 0.]])

    atoms.set_pbc([1,1,1])       #periodic boundary conditions about x,y & z
    atoms.set_calculator(calc)   #connect espresso to Pt unit cell
    volumes.append(atoms.get_volume())  #append the current unit cell volume
                                        #to list of volumes
    energy=atoms.get_potential_energy() #append total energy to list of
    energies.append(energy)             #energies

eos = EquationOfState(volumes, energies) #Fit calculated energies at different
v0, e0, B = eos.fit()                    #lattice constants to an
                                         #equation of state
#output of lattice constant = cubic root of volume of conventional unit cell
#fcc primitive cell volume = 1/4 * conventional cell volume 
print 'Lattice constant:', (4.*v0)**(1./3.), 'AA'
print 'Bulk modulus:', B / kJ * 1e24, 'GPa'
print '(Fitted) total energy at equilibrium latt. const.:', e0, 'eV'
eos.plot(atoms.get_name()+'-eos.png')    #create a png plot of eos fit
