from ase.cluster.icosahedron import Icosahedron

# script for setting up M13 cluster

# replace with your assigned element and your optimized lattice parameter
element1 = 'Pt'
element2 = 'Cu'
a = None

vacuum = 7.0

atoms = Icosahedron(element1, noshells=2)
atoms.center(vacuum=vacuum)

name = element1
if element2:
    for i in range(1,len(atoms),2):
        atoms[i].symbol = element2
    name += element2

atoms.write(name+'13.traj')
