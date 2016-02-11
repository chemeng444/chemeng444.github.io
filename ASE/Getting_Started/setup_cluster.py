from ase.cluster.icosahedron import Icosahedron

# script for setting up M13 cluster

# replace with your assigned element and your optimized lattice parameter
# if your assigned system is a binary alloy, specify element2 (e.g. 'Cu')
element1 = 'Mo'
element2 = 'Cu'
a = None
vacuum = 10.0

# create the cluster and add vacuum around the cluster
atoms = Icosahedron(element1, noshells=2)
atoms.center(vacuum=vacuum)

# if there is a second element, swap out 6 of the atoms for the other metal
if element2:
    for i in range(1,len(atoms),2):
        atoms[i].symbol = element2

# write out the cluster
atoms.write('cluster.traj')
