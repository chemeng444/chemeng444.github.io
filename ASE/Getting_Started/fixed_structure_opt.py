#!/usr/bin/env /home/vossj/suncat/bin/python
#SBATCH -p iric 
#SBATCH --job-name=myjob
#SBATCH --output=myjob.out
#SBATCH --error=myjob.err
#SBATCH --time=1200:00
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=4000
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ctsai89@stanford.edu
#SBATCH --ntasks-per-node=16


import numpy as np
import os
from numpy import *
from espresso import espresso
from scipy.optimize import fmin


lc = 3.9

f = open('alloys.txt').readlines()

for line in f:
    element1 = line.split()[0]

    # if you have a metal alloy, specify the second metal as well
    if line.split()[1] != 'None':
        element2 = line.split()[1]
    else:
        element2 = None

    name = element1 + element2

    if not os.path.exists(name):
        os.makedirs(name)

    def get_energy(x):
        global iteration
        iteration +=1
        
        atoms = Octahedron(element1, length=3, cutoff=1, latticeconstant=x)
        atoms.center(vacuum=7.0)

        # if there is a second element, swap out 6 of the atoms for the other metal
        if element2:
            for i in range(1,len(atoms),2):
                atoms[i].symbol = element2

        calc = espresso(pw=500,
                    dw=5000,
                    xc='BEEF-vdW',
                    kpts='gamma',
                    nbands=-20,
                    sigma=0.1,
                    convergence = {'energy':0.0005,
                                   'mixing':0.1,
                                   'nmix':10,
                                   'maxsteps':500,
                                   'diag':'david',
                                   },
                    outdir=name+'/calcdir_'+str(iteration),
                    )

        atoms.set_calculator(calc)
        energy = atoms.get_potential_energy()
        
        print('%20.8f%20.8f' % (x,energy))
        
        f = open(name+'/out%04i.energy' % iteration, 'w')
        f.write(repr(x) + ' ' + str(energy))
        f.close()
        calc.stop()
        
        del calc
        return energy

    print name
    print('%20s%20s' % ('a','energy'))
    iteration = 0.

    x = fmin(get_energy, x0=lc, xtol=0.001, ftol=0.00001)
    print('Best lc')
    print x