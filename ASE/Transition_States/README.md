---
layout: page
mathjax: false
permalink: /ASE/Transition_States/
---

# ASE Tutorials
1. [Introduction to ASE](../)
2. [Getting Started](../Getting_Started/)
3. [Adsorption](../Adsorption/)
4. [Transition States](../Transition_States/)

____

## <font color="red">UNDER CONSTRUCTION</font> ##

## Transition State Calculations

In this final tutorial, you will be calculating the transition state energy using the nudged elastic band (NEB) and the fixed bond length (FBL) method.


## Contents
2. [Fixed bond length calculation](#fixed-bond-length-calculation)
3. [Vibrational frequencies](#vibrational-frequencies)
4. [Reaction rate](#reaction-rate)
5. [Nudged elastic band calculation](#nudged-elastic-band-calculation)


## Required Files

Obtain the required files by running:

on Sherlock:

```bash
cd $SCRATCH
wget http://chemeng444.github.io/ASE/Getting_Started/exercise_3_sherlock.tar
tar -xvf exercise_3_sherlock.tar
```

or on CEES:

```bash
cd ~/$USER
wget http://chemeng444.github.io/ASE/Getting_Started/exercise_3_cees.tar
tar -xvf exercise_3_cees.tar
```

<a name='fixed-bond-length-calculation'></a>
## Fixed bond length calculation

The fixed bond length (FBL) method is a much faster but cruder way to approximate the minimum energy path and determine the transition state energy. It doesn’t require parallelization over different nodes but may not give you the exact transition state. Generally, one could perform a fixed bond length calculation first and determine if a transition state was found (by checking the vibrational modes). If the transition state is poorly described, then a NEB calculation can be performed based on the fixed bond length results as the inputs.

In a FBL calculation, you provide an initial state of the dissociated products (the *final* state in our H<sub>2</sub>O dissociation reaction), then fix the bond length between two atoms that are required to come together and form a bond (OH* + H* --> H<sub>2</sub>). Then, you iteratively decrease the distance between the two atoms and optimize the geometry of the entire structure while keeping the bond length fixed. Follow the [`fbl.py`](fbl.py) script to determine the transition state for the dissociative adsorption of H<sub>2</sub>O on Pt(111). The script requires an initial state and a specification of the two atoms whose distance is to be fixed (O in the OH* atom and the H* atom).

```python
atom1=12
atom2=13
```

Make sure that the two atoms whose bond distance is to be fixed is correct. Since `FixBondLength()` is a constraint, all constraints on the unit cell must be re-specified when setting the constraints.

```python
constraints = [FixBondLength(atom1,atom2)]
mask = [atom.z < 10 for atom in atoms]      # atoms in the structure to be fixed
constraints.append(FixAtoms(mask=mask))
atoms.set_constraint(constraints)
```

Then for each fixed H-O distance, a structural relaxation is performed.

The fixed bond length calculation can continue beyond the final state and start to give you structures with unrealistically high energies. These would not be relevant for the reaction path and you should select only the trajectory images you want to view. To do this, you can combine the `.traj` files from each step first,

```bash
ag i?.traj i??.traj -n -1 -o combined.traj
```

where `ag` will read all files of the form `i?.traj` followed by `i??.traj`, combine their final steps (using `-n -1`), and then write out a combined file called `combined.traj`.

Then, to select the range of images within `combined.traj`, you can use the @ symbol followed by a range, such as:

```bash
ag combined.traj@:22
```

which will display images 1 through 22 within the combined trajectory file. The image range follows Python syntax. Choose the range where you get a clear view of the initial state, transition state, and final state.

<a name='vibrational-frequencies'></a>
## Vibrational frequencies
Calculate the vibrational frequencies for transition state and the final state using the [`run_freq.py`](run_freq.py) script. Use `ag` to view the vibrational modes, which are written out as `vib*.traj` files. There should be 3N vibrational modes for all adsorbed states, and 3N - 1 vibrational modes for the transition state.

<a name='nudged-elastic-band-calculation'></a>
## Nudged elastic band

To perform a nudged elastic band (NEB) calculation, one needs to provide an initial and final state trajectory. A series of "images" between the initial and final states will then be used to determine the minimum energy path. This band of images will be relaxed. For a NEB calculation, you only need to provide the initial and final state and the number of images in between. Go through the [`neb.py`](neb.py) script. Typically 5~7 images between the initial and final states will be sufficient. Intermediate images will be generated using a linear interpretation of the initial and final trajectory. An odd number of images should be chosen so that the one image will be at the transition state. NEB calculations can take a long time, and the [`neb_restart.py`](neb_restart.py) should be used to read in the previous images. You can also start at with k-points to speed up the calculation, and then restart the calculation with higher k-points.

In the `neb.py` file make sure the line specifying the number of nodes.

```python
#SBATCH --nodes=5
```
corresponds to the number of _intermediate_ images. Check that `intermediate_images = 5` matches. 

Both `neb.py` and `neb_restart.py` scripts require the initial and final states of the reaction path to be provided. This is specified in the lines:

```python
initial = io.read('neb0.traj')
final = io.read('neb6.traj')
```

make sure that the trajectory files are in the directory and are named in the same manner. For the `neb_restart.py` script, the initial and final trajectories must be named in the `neb*.traj` format, where `*` is a number. The script will read in all intermediate images based on the number in the initial and final trajectory.

To view all the trajectory files, run the following command

```bash
ag neb*.traj –n -1
```

where all files of the form `neb*.traj` (with * referring to any number of characters) will be opened in ag. The `-n` flag specifies the image within each trajectory file. Since you are optimizing the entire reaction path, each step in the NEB will be stored in each image file. Specifying `-n -1` tells ag to only read the last image of each file (i.e. the most current step).