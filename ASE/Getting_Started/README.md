---
layout: page
mathjax: false 
permalink: /ASE/Getting_Started/
---

# ASE Tutorials #
1. [Getting Started](../Getting_Started/)
2. [Adsorption](../Adsorption/)
3. [Transition States](../Transition_States/)

## Getting Started ##

To begin with, we will be looking at bulk metals and how to determine lattice constants, then we will be setting up metal surfaces. We will be using Pt throughout.

## Contents ##

1. [A Typical ASE Script](#a-typical-ase-script)
2. [Bulk metal](#bulk)
  1. [Lattice Constant Determination](#lattice-constant-determination)
  2. [Convergence with k-Points](#convergence-with-k-points)
3. [Setting up Surfaces](#surfaces)
4. [Setting up Clusters](#clusters)
5. [Next Steps](#next)

### Required Files ###

Obtain the required files by running

```bash
wget http://chemeng444.github.io/ASE/Getting_Started/download_files_1.sh
chmod +x download_files_1.sh
./download_files_1.sh
```

This should create a folder called `Exercise_1_Getting_Started/` containing subfolders with all the starter scripts you will need.

<a name='a-typical-ase-script'></a>

### A Typical ASE Script ###

ASE scripts can be run directly in the terminal (in the login node) or submitting to external nodes. Generally, you will be submitting jobs to external nodes and only small scripts will be run on the login node. By default, all output from any submitted script will be written *from the directory where the submission command was executed*, so make sure you are inside the calculation folder before running the submission command.

Let's look at how a typical ASE script is written. Open the [`run_surf.py`](run_surf.py) script.

```bash
vi run_surf.py
```

The first line,

```python
#!/usr/bin/env /home/vossj/suncat/bin/python
```
will ensure that the version of Python that is being used is the one that has all the software from SUNCAT installed.

Next, notice the comments in the beginning. These lines will be ignored by Python, but will be read by the job submission system. These include information such as how much time to allocate, the number of nodes required, what the names of the output and error files are, what the name of the job should be, and what your email is. Most of the settings will be the same regardless of the job you submit. You will mostly just be changing the amount of allocated time and the number of nodes, for jobs that require parallelization.

```python
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
```

Next, we import all the relevant ASE modules in for this calculation

```python
from ase import *
from ase.lattice.surface import *
from ase.optimize import *
from ase.constraints import *
from espresso import espresso
```

The asterisks `*` indicates that all methods and classes should be imported. You can also specify the ones you need. `from ase import *` imports all the basic functionality in ase, `from ase.lattice.surface import *` import methods and classes related to solid surfaces, `from ase.optimize import *` imports the optimization methods, `from ase.constraints import *` imports the constraint methods, and most importantly `from espresso import espresso` import the Quantum ESPRESSO calculator for the ASE interface.

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
<a name='bulk'></a>

### Bulk Metal ###

Head into the `Exercise_1_Getting_Started/Bulk/` folder.

As a first example, we will be setting up a bulk fcc metal. You will typically do this when working with an entirely new system. 

<a name='lattice-constant-determination'></a>

### Lattice Constant Determination
Find the [`bulk_metal.py`](bulk_metal.py) script in the `lattice` folder. This script determines the optimum lattice parameter for bulk fcc Pt using the equation of state model. **Change Pt into the metal you have been assigned for the project** and also look up a reasonable initial guess for the lattice parameter, then replace `a = `.  Submit the script by running

```bash
$ sbatch --job-name=$PWD bulk_metal.py
```
Here, `--job-name=$PWD` sets the current working directory as the job name. This plots the energy as a function of lattice parameter and determine the lattice parameter corresponding to the minimum energy.

**Requirement:** Submit the plot for the equation of state that is generated by running the script.

You should see a plot looking like this:

<center><img src="Images/Cu3Re-eos.png" alt="Cu3Re" style="width: 450px;"/>
<br>Equation of state plot for a Cu<sub>3</sub>Re bulk fcc alloy</center>

with the following output in a `myjob.out` file:

```
Lattice constant: 3.72570317144 AA
Bulk modulus: 204.462225193 GPa
(Fitted) total energy at equilibrium latt. const.: -19142.1406997 eV
```

**Check to make sure your lattice parameters match the ones below:**

<style>
table {
    width:35%;
}
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 5px;
    text-align: left;
}
table#t01 tr:nth-child(even) {
    background-color: #eee;
}
table#t01 tr:nth-child(odd) {
   background-color:#fff;
}
table#t01 th    {
    background-color: black;
    color: white;
}
</style>
<center>Lattice Parameters for Pure Metals (fcc unless otherwise stated)</center>
<center>
<table>
<tr><th>Metal</th>
<th>Lattice Constant (Å)</th></tr>
<tr><td>Ag</td>
<td>4.214</td></tr>
<tr><td>Au</td>
<td>4.225</td></tr>
<tr><td>Cu</td>
<td>3.685</td></tr>
<tr><td>Pt</td>
<td>4.015</td></tr>
<tr><td>Pd</td>
<td>3.987</td></tr>
<tr><td>Ir</td>
<td>3.892</td></tr>
<tr><td>Ru</td>
<td>3.863</td></tr>
<tr><td>Re</td>
<td>3.889</td></tr>
<tr><td>Rh</td>
<td>3.863</td></tr>
<tr><td>Mo (bcc)</td>
<td>3.174</td></tr>
</table>
</center>


<style>
table {
    width:50%;
}
</style>
<center>Lattice Parameters for Alloys Metals (all fcc)
</center>
<center>
<table>
<tr><th>Alloy</th>
<th>Lattice Constant (Å)</th>
<th>Alloy</th>
<th>Lattice Constant (Å)</th>
</tr>
<tr>
<td>AgPd</td>
<td>4.137</td>
<td>AgPt</td>
<td>4.125</td>
</tr>
<tr>
<td>AgIr</td>
<td>4.096</td>
<td>AgRu</td>
<td>4.106</td>
</tr>
<tr>
<td>AgRe</td>
<td>4.107</td>
<td>AgRh</td>
<td>4.109</td>
</tr>
<tr>
<td>AgMo</td>
<td>4.165</td>
<td>AuPd</td>
<td>4.124</td>
</tr>
<tr>
<td>AuPt</td>
<td>4.122</td>
<td>AuIr</td>
<td>4.095</td>
</tr>
<tr>
<td>AuRu</td>
<td>4.094</td>
<td>AuRe</td>
<td>4.104</td>
</tr>
<tr>
<td>AuRh</td>
<td>4.097</td>
<td>AuMo</td>
<td>4.146</td>
</tr>
<tr>
<td>CuPd</td>
<td>3.748</td>
<td>CuPt</td>
<td>3.747</td>
</tr>
<tr>
<td>CuIr</td>
<td>3.719</td>
<td>CuRu</td>
<td>3.713</td>
</tr>
<tr>
<td>CuRe</td>
<td>3.726</td>
<td>CuRh</td>
<td>3.719</td>
</tr>
<tr>
<td>CuMo</td>
<td>3.772</td>
<td>PdPt</td>
<td>3.974</td>
</tr>
<tr>
<td>PdIr</td>
<td>3.944</td>
<td>PdRu</td>
<td>3.935</td>
</tr>
<tr>
<td>PdRe</td>
<td>3.937</td>
<td>PdRh</td>
<td>3.949</td>
</tr>
<tr>
<td>PdMo</td>
<td>3.963</td>
<td>PtIr</td>
<td>3.950</td>
</tr>
<tr>
<td>PtRu</td>
<td>3.937</td>
<td>PtRe</td>
<td>3.947</td>
</tr>
<tr>
<td>PtRh</td>
<td>3.946</td>
<td>PtMo</td>
<td>3.968</td>
</tr>
</table>
</center>

<a name='convergence-with-k-points'></a>

### Convergence with k-Points ###
Next, we will determine how well-converged the energy is with respect to the number of k-points in each direction. Submit the [`run_sp.py`](run_sp.py) script in the kpts folder using the lattice parameter obtained from the previous section.

```bash
$ sbatch --job-name=$PWD run_sp.py
```

**Requirement**: Try using k = 6, 10, 14, and 18 in all three directions (i.e., k×k×k). Plot the energy as a function of k-points. Pick one and try to justify why it would be a reasonable choice. Use the optimal k-point sampling to re-run the lattice optimization script again and check if the results are consistent. The relevant k-points will usually be known, since we have consistent settings that we use throughout the group. In principle, one should always check for convergence when working with a new system.

<a name='surfaces'></a>

### Metal Surfaces ###

Head into the `Exercise_1_Getting_Started/Surface/` folder.

Next we will set up various common surface terminations of a metal using the `ase.lattice.surface` module and optimize the geometry. We will focus on the 111 surface for fcc metals (110 for bcc). The [`setup_surf.py`](setup_surf.py) file sets up the (111) surface for Pt, with specification of the size and lattice parameter. **Edit the file and replace Pt with your metal and the lattice constant with your optimized result from running **`bulk_metal.py`. You can execute this directly from the terminal and view the results, e.g.:

```bash
$ python setup_surf.py
$ ase-gui slab.traj
```

This will generate slab.traj and the second command opens the file with the ASE gui visualizer.

[`run_surf.py`](run_surf.py) is a script that sets up the Quantum ESPRESSO calculator and performs the geometry optimization with respect to energy. This must be submitted to an external queue and should not be run directly in the login node. Make sure that you have run `setup_surf.py` to generate your `slab.traj` file, then submit the optimization script using:

```bash
$ sbatch --job-id=$PWD run_surf.py
```

where again `--job-id=$PWD` will use the present working directory for the the SLURM (the job submission system) job name.

Try changing the number of k-points in the x and y-direction (i.e., k×k×1) using k = 4, 6, and 8. There are 7 Å of vacuum in the z-direction so 1 k-point is sufficient.

**Requirement:** Plot the change in the total slab energy as a function of the different k-points. How many k-points are sufficient?

<a name='clusters'></a>

### Metal Clusters ###

Head into the `Exercise_1_Getting_Started/Cluster/` folder.

Next we will use the `ase.cluster.icosahedron` module to set up metal clusters. The [`setup_cluster.py`](setup_cluster.py) script demonstrates how to set up a 13 atom metallic cluster. **Change Pt into the metal or alloy you have been assigned**. This can be run within the login node using

```bash
$ python setup_cluster.py
$ ase-gui cluster.traj
```

Next the [`run_cluster.py`](run_cluster.py) script will perform the optimization. Read through the script and when you have made the required modifications, submit the job using

```bash
$ sbatch --job-id=$PWD run_cluster.py
```

**Requirement:** Plot the change in the total slab energy as a function of different k-points. By default the 'gamma' keyword can be used when only 1 k-point is needed in all directions. Otherwise, specify all three k-points in the script.

<a name='next'></a>

### Next Steps ###

**Requirement:** Before we begin calculating adsorption energies, it is important to adopt a consistent set of calculation settings for the whole class, so that adsorption energies calculated by different students can be properly compared. 

After you have finished the exercises above, make sure you have calculated your (111) or (110) surface at these settings:

* (2×2×4) unit cell
* 4 layers, top 2 layers relaxed, bottom 2 layers fixed
* 4×4×1 Monkhorst-Pack k-point set
* 7 Å vacuum in the z-direction (both directions)

And for your M<sub>13</sub>  cluster:

* All atoms relaxed
* `'gamma'` point for k-point sampling
* 10 Å vacuum in all directions