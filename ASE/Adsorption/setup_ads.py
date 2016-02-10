from ase import io
from ase.lattice.surface import add_adsorbate, fcc111

# name of output trajectory file

# lattice constant for fcc Pt
metal = 'Pt'
a = 3.989

# read in clean surface trajectory
slab = fcc111(metal, a = 3.989, size = (2,2,4), vacuum = 7.0)

# add adsorbate using add_adsorbate(surface,symbol,z,(x,y))
# where "surface" is the object containing the surface, "slab" in this case
# and z is the position above the surface (from the center of the top most atom)
# and x and y are the absolute coordinates

# add two neighboring N atoms
add_adsorbate(slab, 'N', 1.5, (3, 1.7))
add_adsorbate(slab, 'N', 1.5, (1.5, 0.86))
# use ag to view the slab and find the right x,y position

# save the trajectory file
slab.write(metal+'N+N.traj')