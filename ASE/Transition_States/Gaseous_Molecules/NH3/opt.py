#!/usr/bin/env python

#LSF -q suncat-short
#LSF -n 8 
#LSF -o opt.log
#LSF -e err.log
#LSF -sp 100


import numpy as np
from ase import io, units
from ase import Atom, Atoms
from ase.io import read, write
from espresso import espresso
from ase import optimize
from ase.data.molecules import molecule
from ase.io.trajectory import PickleTrajectory
from ase.vibrations import Vibrations
from ase.thermochemistry import HarmonicThermo, IdealGasThermo


Rydberg= 13.6058

xc = 'BEEF'


atoms = io.read('init.traj')

atoms.write('input.traj')

calc = espresso(pw=500,
		 dw=5000,
		 nbands=-10,
		 sigma=0.1,
		 dipole={'status':True},
		 convergence = {'mixing':0.2,'maxsteps':200},
		 output = {'avoidio':True,'removewf':True,'wf_collect':False},
		 xc=xc,
		 outdir='calcdir')


 
atoms.set_calculator(calc)


dyn = optimize.QuasiNewton(atoms, trajectory='trajfile.traj', logfile='logfile.log',restart='qn.pckl')
dyn.run(fmax=0.01)	# fmax?

energy = atoms.get_potential_energy()

vib = Vibrations(atoms)
vib.run()
vibenergies = vib.get_energies()
vib.summary(log='vib.txt')

gibbs = IdealGasThermo(vib_energies = vibenergies,
                        electronicenergy = energy,
                        atoms = atoms,
                        geometry='nonlinear',
                        symmetrynumber =3,
                        spin=0.0)

freeenergy = gibbs.get_free_energy(300,101325)  #At 300K and 101325 Pa

f=open('out.energy','w')
f.write(str(energy)+'\n'+str(freeenergy))
f.close
