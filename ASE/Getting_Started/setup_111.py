from ase import *
from espresso import espresso
from ase.lattice.surface import *
from ase.optimize import *
from ase.constraints import *
from ase import io

#create a (111) surface slab of 2x2x3
#(2x2 surface area; 3 layers along surface normal)
#7 angstrom vacuum layer added on each side

a = 3.989 #lattice parameter for fcc Pd. Use your optimized value
      #from the previous calculations

slab = fcc111('Pt', a=a, size=(2,2,3), vacuum=7.0)    #function for setting up a fcc(111) surface

# mask for atoms with z-axis less than 10 A
# set constraint to Fix Atoms
mask = [atom.z<10.0 for atom in slab]
slab.set_constraint(FixAtoms(mask=mask))

fixatoms = FixAtoms(mask=mask)
slab.set_constraint(fixatoms) #fix everything but the top layer atoms
slab.rattle()                 #define random displacements to

slab.write('slab.traj')
