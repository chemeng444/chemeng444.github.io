---
layout: page
mathjax: true
permalink: /ASE/
---

## ASE Tutorials
1. [Getting Started](Getting_Started/)
2. [Adsorption](Adsorption/)
3. [Transition States](Transition_States/)

## Introduction

### Atomic Simulation Environment (ASE)
Currently, most of us at SUNCAT use the Quantum ESPRESSO calculator as implemented in the Atomic Simulation Envrionment (ASE), which is written in Python. ASE provides Python modules for manipulating atoms, performing calculations, and analyzing and visualizing the results. ASE scripts are simply regular Python scripts that incorporate the ASE modules. 

Here is an example of a few commonly used modules for a calculation and how you would use them in your Python scripts:

```python
from ase import Atoms
from ase.constraints import FixAtoms
from ase import optimize
from espresso import espresso
import numpy as np
```

The modules provide functions that can be used for setting up the system and performing calculations. The `ase.optimize` module is needed for performing geometry optimizations, the `espresso` module is needed to use the Quantum ESPRESSO calculator, and the `numpy` module is needed for using certain mathematical functions.

Typically, the script will first read a trajectory file (`.traj`) that contains the structure, then set up the Quantum ESPRESSO calculator, and then perform the optimization. You can use the ASE graphical user interface `ag` to view trajectory files or to setup or modify structures. To visualize a trajectory file, simply type:

```bash
ag <trajectory_file>.traj
```

ASE supports a variety of file formats. More information about ASE can be found in the [official documentation](https://wiki.fysik.dtu.dk/ase/ase/ase.html).


The following tutorials will take you through the water dissociation reaction on the Pt(111) surface.
