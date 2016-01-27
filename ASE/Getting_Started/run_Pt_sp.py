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
#SBATCH  --mail-user=SUNETID@stanford.edu
#################
#task to run per node; each node has 16 cores
#SBATCH --ntasks-per-node=16
#################

"""Bulk Pt(fcc) test"""

from ase import *
from espresso import espresso

name = 'Pt-fcc'
a = 3.989  # optimized lattice constant
b = a/2

#construct primitive Pt fcc cell
bulk = Atoms(symbols='Pt',positions=[(0.0, 0.0, 0.0)],
             cell=[[0., b, b],
                   [b, 0., b],
                   [b, b, 0.]])

k = 8
calc = espresso(pw=500, #plane-wave cutoff
          dw=5000,    #density cutoff
          xc='BEEF-vdW',    #exchange-correlation functional
          kpts=(k,k,k), #sampling grid of the Brillouin zone
                      #(is internally folded back to the
                           #irreducible Brillouin zone)
          nbands=-10, #10 extra bands besides the bands needed to hold
                    #the valence electrons
          sigma=0.1,
          convergence= {'energy':1e-5,
                     'mixing':0.1,
                     'nmix':10,
                     'mix':4,
                     'maxsteps':500,
                     'diag':'david'
                      },  #convergence parameters
          outdir='calcdir') 

bulk.set_pbc([1,1,1])      #periodic boundary conditions in all directions
bulk.set_calculator(calc)  #connect espresso to Pt structure

energy = bulk.get_potential_energy()  #this triggers a DFT calculation

print 'Total energy:', energy, 'eV'

