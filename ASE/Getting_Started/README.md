---
layout: page
mathjax: false 
permalink: /ASE/Getting_Started/
---

## Getting Started
To begin with, we will be looking at bulk metals and how to determine lattice constants, then we will be setting up metal surfaces. We will be using Pt throughout.
## Contents
1. [A typical ASE script](#a-typical-ase-script)
1. [Bulk Pt](#bulk-pt)
  1. [Lattice constant determination](#lattice-constant-determination)
  2. [Convergence with k-points](#convergence-with-k-points)
2. [Pt surfaces](#pt-surfaces)

<a name='a-typical-ase-script'></a>
## A typical ASE script

Let's look at how a typical ASE script is written. Open the [`run_Pt111.py`](run_Pt111.py) script.
```bash
vi run_Pt111.py
```

The first line,
```python
#!/home/vossj/suncat/bin/python
```
will ensure that the version of Python that is being used is the one that has all the software from SUNCAT installed.

Next, notice the comments in the beginning. These lines will be ignored by Python, but will be read by the job submission system. These include information such as how much time to allocate, the number of nodes required, what the names of the output and error files are, what the name of the job should be, and what your email is. Most of the settings will be the same regardless of the job you submit. You will mostly just be changing the amount of allocated time and the number of nodes, for jobs that require parallelization.
```python
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
```

Next, we import all the relevant ASE modules in for this calculation
```python
from ase import *
from ase.lattice.surface import *
from ase.optimize import *
from ase.constraints import *
from espresso import espresso
```

The astericks `*` indicates that all methods and classes should be imported. You can also specify the ones you need. `from ase import *` imports all the basic functionality in ase, `from ase.lattice.surface import *` import methods and classes related to solid surfaces, `from ase.optimize import *` imports the optimization methods, `from ase.constraints import *` imports the constraint methods, and most importantly `from espresso import espresso` import the Quantum ESPRESSO calculator for the ASE interface.

We define a string

```python
name = 'Pt111'
```
which we can easily modify and use for naming output files.

The `fcc111` method sets up a FCC 111 surface and returns an [Atoms](https://wiki.fysik.dtu.dk/ase/ase/atoms.html) object containing the surface. 

```python
slab = fcc111('Pt', a=a, size=(2,2,3), vacuum=7.0)    #function for setting up a fcc(111) surface
```


Then, the Quantum ESPRESSO calculator is set up. All parameters related to the electronic structure calculation are included here. The following example shows typical parameters that we use in the group for metal calculations. Typically, the number of k-points is determined using 24 Å per lattice vector for transition metals.

```python
#espresso calculator setup
calc = espresso(pw=500,           #plane-wave cutoff
                dw=5000,          #density cutoff
                xc='BEEF-vdW',    #exchange-correlation functional
                kpts=(4,4,1),     #k-point sampling, no dispersion to be sampled along z
                nbands=-10,       #10 extra bands besides the bands needed to hold the valence electrons
                sigma=0.1,
                convergence= {'energy':1e-5,  #convergence parameters
                              'mixing':0.1,
                              'nmix':10,
                              'mix':4,
                              'maxsteps':500,
                              'diag':'david'
                             },
                outdir='calcdir') #output directory for Quantum Espresso files
```

Then, atomic constraints are set. Since there are only a finite number of layers in the slab, the lowest layers are fixed to emulate the bulk. 

```python
mask = [atom.z < 10 for atom in atoms]  #atoms in the structure to be fixed
fixatoms = FixAtoms(mask=mask)
slab.set_constraint(fixatoms)           #fix everything but the top layer atoms
slab.rattle()                           #define random displacements to the atomic positions before optimization
```

Finally, the Quantum ESPRESSO calculator is attached to the `slab` Atoms object, and the optimizer is defined. `QuasiNewton()` is an object for the [structural optimization](https://wiki.fysik.dtu.dk/ase/ase/optimize.html), which takes an Atoms object as an input. A convergence criteria is set and `qn.run()` initiates the optimization.

```python
slab.set_calculator(calc)                       #connect espresso to slab
qn = QuasiNewton(slab, trajectory=name+'.traj') #relax slab
qn.run(fmax=0.05)                               #until max force<=0.05 eV/AA
```
<a name='bulk-pt'></a>
## Bulk Pt
As a first example, we will be setting up bulk fcc Pt. You will typically do this when working with an entirely new system. 
<a name='lattice-constant-determination'></a>
### Lattice constant determination
Find the [`bulk_Pt.py`](bulk_Pt.py) script in the `lattice` folder. This script determines the optimum lattice parameter for bulk fcc Pt using the equation of state model. Submit the script by running
```bash
$ sbatch --job-name=$PWD bulk_Pt.py
```
Here, `--job-name=$PWD` sets the current working directory as the job name. This plots the energy as a function of lattice parameter and determine the lattice parameter corresponding to the minimum energy.

<a name='convergence-with-k-points'></a>
### Convergence with k-points
Next, we will determine how well-converged the energy is with respect to the number of k-points in each direction. Submit the [`run_Pt_sp.py`](run_Pt_sp.py) script in the kpts folder using the lattice parameter obtained from the previous section.

```bash
$ sbatch --job-name=$PWD run_Pt_sp.py
```
Try using k = 6, 10, 14, and 18 in all three directions (i.e., k×k×k). Plot the energy as a function of k-points. Pick one and try to justify why it would be a reasonable choice. Use the optimal k-point sampling to re-run the lattice optimization script again and check if the results are consistent. The relevant k-points will usually be known, since we have consistent settings that we use throughout the group. In principle, one should always check for convergence when working with a new system.

<a name='pt-surfaces'></a>
## Pt surfaces
Next we will set up various common surface terminations of Pt using the `ase.lattice.surface` module and optimize the geometry. We will focus on the 111 surface. The [`setup_111.py`](setup_111.py) file sets up the (111) surface, with specification of the size and lattice parameter. You can execute this directly from the terminal and view the results, e.g.:
```bash
$ python setup_111.py
$ ag slab.traj
```

This will generate slab.traj and the second command opens the file with the ASE gui visualizer.
`run_opt.py` is the script that sets up the Quantum ESPRESSO calculator and performs the geometry optimization with respect to energy. This must be submitted to an external queue and should not be run directly in the login node. It is possible to set up the surface and run the optimization within the same script. An example is contained in [`run_Pt111.py`](run_Pt111.py) . Try submitting this using:

```bash
$ sbatch --job-id=$PWD run_Pt111.py
```

where again `--job-id=$PWD` will use the present working directory for the the SLURM (the job submission system) job name.

Try changing the number of k-points in the x and y-direction (i.e., k×k×1) using k = 4, 6, and 8. There are 7 Å of vacuum in the z-direction so 1 k-point is sufficient.
