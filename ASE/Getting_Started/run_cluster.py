#!/usr/bin/env /home/vossj/suncat/bin/python
#above line selects special python interpreter needed to run espresso
#SBATCH -p iric 
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
#SBATCH  --mail-user=<<<<<<<insert your sunetid>>>>>>>>>>@stanford.edu
#################
#task to run per node; each node has 16 cores
#SBATCH --ntasks-per-node=16
#################

from ase import *
from ase import io
from ase.cluster.icosahedron import Icosahedron
from ase.optimize import *
from espresso import espresso

# read in the cluster
name = 'PtCu13'
atoms = io.read('cluster.traj')

#espresso calculator setup
calc = espresso(pw=500,           #plane-wave cutoff
                dw=5000,          #density cutoff
                xc='BEEF-vdW',    #exchange-correlation functional
                kpts='gamma',     #k-point sampling. 'gamma' for (1,1,1)
                nbands=-10,       #10 extra bands besides the bands needed to hold
                                  #the valence electrons
                sigma=0.1,
                psppath='/home/vossj/suncat/psp/gbrv1.5pbe',    #pseudopotential path
                convergence= {'energy':1e-5,
                              'mixing':0.1,
                              'nmix':10,
                              'mix':4,
                              'maxsteps':500,
                              'diag':'david'
                             },  #convergence parameters
                outdir='calcdir') #output directory for Quantum Espresso files

atoms.set_calculator(calc)                       #connect espresso to cluster
qn = QuasiNewton(atoms, trajectory=name+'.traj') #relax atoms
qn.run(fmax=0.05)                               #until max force<=0.05 eV/AA