from ase.constraints import FixAtoms
from ase.io import read
from ase.thermochemistry import HarmonicThermo
from ase.vibrations import Vibrations
from espresso import espresso
from espresso.vibespresso import vibespresso

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
                      )

atoms.set_calculator(calc)                            # attach calculator to the atoms                   

energy = atoms.get_potential_energy()                 # caclulate the energy, to be used to determine G

# CHANGE TO THE ATOMS YOU NEED TO VIBRATE
# metal atoms can be assumed to be fixed
vibrateatoms=[atom.index for atom in atoms if atom.symbol in ['H','N']]   # calculate the vibrational modes for all N and H atoms
atoms.set_calculator(calcvib)                                             # attach vibrations calculator to the atoms                   

# Calculate vibrations                                                                                        
vib = Vibrations(atoms,indices=vibrateatoms,delta=0.03)    # define a vibration calculation                   
vib.run()                                                  # run the vibration calculation                    
vib.summary(method='standard')                             # summarize the calculated results                 

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
