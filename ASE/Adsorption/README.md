---
layout: page
mathjax: true
permalink: /ASE/Adsorption/
---

# ASE Tutorials
1. [Introduction to ASE](../)
2. [Getting Started](../Getting_Started/)
3. [Adsorption](../Adsorption/)
4. [Transition States](../Transition_States/)
5. [Error Estimation and Density of States](../BEEF_DOS/)

____

## Adsorption on Surfaces ##

In the second exercise, you will be calculating the dissociative adsorption of N<sub>2</sub> onto the your cluster and (111) surface. This will set you up for calculating the transition state in the third exercise. We will also calculate all the intermediates in the ammonia synthesis pathway (N\*, NH\*, NH<sub>2</sub>\*, NH<sub>3</sub>\*, H\*)

## Contents
1. [Gaseous Molecules](#gaseous-molecules)
2. [Adsorption Sites](#adsorption-sites)
3. [Remaining Reaction Intermediates](#reaction-intermediates)

### Required Files ###

Obtain the required files by running:

on Sherlock:

```bash
cd $SCRATCH
wget http://chemeng444.github.io/ASE/Getting_Started/exercise_2_sherlock.tar
tar -xvf exercise_2_sherlock.tar
```

or on CEES:

```bash
cd ~/$USER
wget http://chemeng444.github.io/ASE/Getting_Started/exercise_2_cees.tar
tar -xvf exercise_2_cees.tar
```

This will create a folder called `Exercise_2_Adsorption`.

<a name='gaseous-molecules'></a>

### Gaseous Molecules ###

In this exercise you will be calculating the dissociative adsorption of N<sub>2</sub> on your extended surface and your M<sub>13</sub> surface from the [previous exercise](../Getting_Started/). The dissociative adsorption energy is defined as:
<div>

$$
\Delta E_\mathrm{ads} = E_\mathrm{surface + 2N*}  - E_\mathrm{surface} - E_\mathrm{N_2}
$$

</div>

where N\* refers to adsorbed N. We have *E*<sub>surface</sub> from the previous exercise, so we will need to calculate both *E*<sub>surface + 2N\*</sub> and *E*<sub>N<sub>2</sub></sub> in this exercise.

In the `N2_gas` subfolder, find the [`run_N2.py`](run_N2.py) script. This is a typical script for calculating gas phase species: the optimized geometry is determined, then the electronic energy, as well as the vibrational modes are computed and used to determine the free energy. Run the script and check that the vibrational modes are reasonable. Ideally, one large vibrational frequency corresponding to the N-N stretching should be observed.



<a name='adsorption-sites'></a>

### Adsorption Sites ###

Take a look [here](http://chemeng444.github.io/ASE/#ase-gui) if you need a reminder on how to add atoms using `ase-gui`. We will describe how to add atoms within the ASE script below.

Enter the `Adsorption` subfolder.

There are four possible adsorption sites on fcc (111) surfaces that an adsorbate can bind to: the fcc, hcp, ontop, and bridge sites. For a bcc (110), there are three sites: hollow, ontop, and bridge. For the M<sub>13</sub> clusters, there are four sites: 1-fold, 2-fold, 3-fold, and 4-fold coordinated sites. These are illustrated below:
<style>
table {
    width:100%;
}
table, th, td {
    border-collapse: collapse;
}
th, td {
    padding: 5px;
    text-align: center;
}
th {
    border-top: 1px solid #ddd;
    border-bottom: 1px solid #ddd;
}
tr.last
{
    border-bottom: 1px solid #ddd;
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
<center>
<table>
<tr>
    <th></th><th colspan="4"><center>Coordination</center></th>
</tr>
<tr>
    <th><center>Structure</center></th>
    <th><center>one-fold</center></th>
    <th><center>two-fold</center></th>
    <th><center>three-fold</center></th>
    <th><center>four-fold</center></th>
</tr>
<tr>
    <td>M<sub>13</sub></td>
    <td><img src="Images/cluster_ontop.png" style="width: 100px;"/><br>on-top</td>
    <td><img src="Images/cluster_twofold.png" style="width: 100px;"/><br>two-fold</td>
    <td><center><img src="Images/cluster_threefold.png" style="width: 100px;"/><br>three-fold</center></td>
    <td><img src="Images/cluster_fourfold.png" style="width: 100px;"/><br>four-fold</td>
</tr>
<tr>
    <td>fcc (111)</td>
    <td><img src="Images/111_ontop.png" style="width: 100px;"/><br>on-top</td>
    <td><img src="Images/111_bridge.png" style="width: 100px;"/><br>bridge</td>
    <td><center><img src="Images/111_fcc.png" style="width: 100px;"/>
    <img src="Images/111_hcp.png" style="width: 100px;"/><br>fcc, hcp</center></td>
    <td></td>
</tr>
<tr class="last">
    <td>bcc (110)</td>
    <td><img src="Images/110_ontop.png" style="width: 100px;"/><br>on-top</td>
    <td><img src="Images/110_bridge.png" style="width: 100px;"/><br>bridge</td>
    <td><img src="Images/110_hollow.png" style="width: 100px;"/><br>hollow</td>
    <td></td>
</tr>
</table>
</center>

If you are working with an alloy system, it is possible that the structure has distorted significantly. In that case, just identify the unique adsorption sites for your system.

In the [`setup_ads.py`](setup_ads.py) script, an optimized structure is read, and then the adsorbate atoms are added manually. This script can be executed in the login node using `python setup_ads.py`. The `add_adsorbate()` function is used to add adsorbates:

```python
add_adsorbate(slab, 'N', 1.5, (3, 1.7))
add_adsorbate(slab, 'N', 1.5, (1.5, 0.86))
```

Here `add_adsorbate(slab, element, z, (x,y)` is used, where slab is the loaded trajectory file, `z` is the vertical height above the surface, and `(x,y)` are the x and y coordinates.

Edit the script to add the adsorbates in the sites you need.

Alternatively, for extended surfaces, one can first use the `fcc111` (`bcc110` if you are calculating Mo) function from the `ase.lattice.surface` module to set up the surface. Then, special keywords in the `add_adsorbate()` function can be directly used to add adsorbates to the special sites, *e.g.*

```python
atoms = fcc111(Pt, a = 3.989, size = (2,2,4), vacuum = 7.0)
add_adsorbate(atoms, 'N', 1.5, 'fcc')
```

This can only be done if the surface has just been created, not if it is being read from a saved `.traj` file. More information can be found [here](https://wiki.fysik.dtu.dk/ase/ase/surface.html).

One could also use the ASE graphical user interface `ase-gui` to add an adsorbate or molecule as well. Use `ase-gui <file>.traj` to open the trajectory file. Then simply click the atom above where the adsorbate will sit, and click `Ctrl + A`, then specify the adsorbate and the vertical distance above the site. You can also hold `Ctrl` to select multiple atoms and add an adsorbate, which will be at the center of all the selected atoms.


<a name='dissociative-adsorption'></a>

### Dissociative adsorption ###

We will focus on the dissociative adsorption mechanism for the first bond-breaking step of N<sub>2</sub>, where the N<sub>2</sub> molecule separates as two N* adsorbed onto the surface. In this case you need to check all unique neighboring sites for the two N\* atoms.

You will be making comparisons between the M<sub>13</sub> cluster and the surface for the 2N\* state and the dissociation barrier. 

For the rest of the ammonia synthesis pathway, you are only required to perform calculations on the M<sub>13</sub> cluster. If time allows, you are welcome to do more calculations.

Organize your directories in the following way:

```bash
../Adsorption/2N_surface/
../Adsorption/2N_cluster/
../Adsorption/N/
../Adsorption/N/ontop
../Adsorption/N/bridge
...
../Adsorption/NH3/
```

Once you have all your structures set up, it is time to run the structural optimization. The `opt.py` script should be submitted within each subdirectory **for each** adsorption site. This way the output files will be written to their respective subdirectories. 

**Note:** You will need to explore all possible adsorption sites to find the ones with the lowest energy, as those will be the most stable configurations. For the 2N\* calculation, you will need to focus on neighboring sites. However, what constitutes a "neighboring" site might depend on your system. You might find that when the two N\* atoms are close to each other, that they combine to form an adsorbed N<sub>2</sub>\* during the optimization. This just means that your surface may be so reactive that it can stabilize the N<sub>2</sub> molecule without relying on the N-N bond being broken. In that case you will have to look for sites slightly further apart.

**<font color="red">Requirement:</font>** 
Complete structural optimizations for the following adsorbates:

* Calculate 2N\* adsorption on all possible sites on the M<sub>13</sub> cluster **and** the extended surface.
* Calculate the reaction intermediates (from N\* through NH3\*) on all possible adsorption sites **only** for the M<sub>13</sub> cluster.
* There may be a lot of possible configurations, so we recommend that you set up *all* possible ones and submit them at the same time.

**Next**: move on to [Transition States](../Transition_States/) to learn about how to determine transition states and barriers.
